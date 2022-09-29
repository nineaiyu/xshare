#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : alidrive
# author : ly_13
# date : 2022/9/13
import logging

from django.conf import settings
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView

from api.models import AliyunDrive, FileInfo, ShareCode
from api.utils.model import get_aliyun_drive
from api.utils.serializer import AliyunDriveSerializer
from common.base.magic import MagicCacheData
from common.base.utils import AesBaseCrypt
from common.cache.storage import DriveQrCache, DownloadUrlCache
from common.core.filter import OwnerUserFilter
from common.core.modelset import BaseModelSet
from common.core.response import PageNumber, ApiResponse
from common.libs.alidrive import Aligo
from common.libs.alidrive.core.Auth import Auth
from common.utils.pending import get_pending_result

logger = logging.getLogger(__file__)


class AliyunDriveFilter(filters.FilterSet):
    min_used_size = filters.NumberFilter(field_name="used_size", lookup_expr='gte')
    max_used_size = filters.NumberFilter(field_name="used_size", lookup_expr='lte')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = AliyunDrive
        fields = ['user_id', 'user_name']


def clean_drive_file(instance):
    ali_obj = get_aliyun_drive(instance)
    result = ali_obj.get_folder_by_path(settings.XSHARE)
    if result:
        result_list = ali_obj.move_file_to_trash(result.file_id)
        DownloadUrlCache(instance.default_drive_id, '*').del_many()
        logger.debug(f'{instance} move {result} to trash.result:{result_list}')


class AliyunDriveView(BaseModelSet):
    queryset = AliyunDrive.objects.all()
    serializer_class = AliyunDriveSerializer
    pagination_class = PageNumber

    filter_backends = [OwnerUserFilter, filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['updated_time', 'used_size', 'created_time', 'total_size']
    filterset_class = AliyunDriveFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        clean_drive_file(instance)
        self.perform_destroy(instance)
        return ApiResponse()

    def create(self, request, *args, **kwargs):
        self.kwargs = request.data
        instance = self.get_object()
        if self.kwargs.get('action') == 'clean' and instance.enable and instance.active:
            clean_drive_file(instance)
            FileInfo.objects.filter(aliyun_drive_id=instance).delete()
            ShareCode.objects.filter(owner_id=request.user, file_id__isnull=True).delete()
            return ApiResponse()
        return ApiResponse(code=1001, msg='操作失败')

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = super().update(request, *args, **kwargs).data
        MagicCacheData.invalid_cache(f'get_aliyun_drive_{instance.user_id}')
        return ApiResponse(data=data)


def expect_func(result, *args, **kwargs):
    if result and result.get('code', -1) in [0, 1, 2]:
        return True


class AliyunDriveQRView(APIView):

    def get(self, request):
        drive_obj = AliyunDrive(owner_id=request.user)
        ali_auth = Auth(drive_obj)
        login_qr_data = ali_auth.get_login_qr()
        qr_link = login_qr_data['codeContent']
        sid = AesBaseCrypt().set_encrypt_uid(qr_link)
        DriveQrCache(sid).set_storage_cache(login_qr_data, 300)
        return ApiResponse(data={'qr_link': qr_link, 'sid': sid})

    def post(self, request):
        sid = request.data['sid']
        user_id = request.data.get('user_id')
        if user_id:
            auto_obj = AliyunDrive.objects.filter(owner_id=request.user, user_id=user_id).first()
            if auto_obj.refresh_token and auto_obj.default_drive_id:
                try:
                    ali_obj = Aligo(auto_obj, refresh_token=auto_obj.refresh_token)
                    result = ali_obj.get_default_drive()
                    if result.drive_id == auto_obj.default_drive_id:
                        auto_obj.total_size = result.total_size
                        auto_obj.used_size = result.used_size
                        auto_obj.active = True
                        auto_obj.save(update_fields=['total_size', 'used_size', 'active', 'updated_time'])
                        return ApiResponse(data={'pending_status': True, 'data': {}})
                except Exception as e:
                    logger.warning(f'auth check failed {e}')

        drive_obj = AliyunDrive(owner_id=request.user)
        ali_auth = Auth(drive_obj)
        data = DriveQrCache(sid).get_storage_cache()
        if data:
            status, result = get_pending_result(ali_auth.check_scan_qr, expect_func, data=data, run_func_count=1,
                                                locker_key=sid, unique_key=sid)
            if status and result.get('data', {}).get('code') == 0:
                ali_drive_obj = AliyunDrive.objects.filter(owner_id=request.user,
                                                           user_id=ali_auth.token.user_id).first()
                MagicCacheData.invalid_cache(f'get_aliyun_drive_{ali_drive_obj.user_id}')
                ali_obj = get_aliyun_drive(ali_drive_obj)
                default_drive_obj = ali_obj.get_default_drive()
                ali_drive_obj.total_size = default_drive_obj.total_size
                ali_drive_obj.used_size = default_drive_obj.used_size
                ali_drive_obj.active = True
                ali_drive_obj.save(update_fields=['total_size', 'used_size', 'active'])
            return ApiResponse(data={'pending_status': status, 'data': result})
        return ApiResponse(code=1001, msg='异常请求，请重试')
