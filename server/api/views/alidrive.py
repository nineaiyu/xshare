#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : alidrive
# author : ly_13
# date : 2022/9/13
import logging

from common.libs.alidrive import Aligo
from common.libs.alidrive.core.Auth import Auth
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView

from api.models import AliyunDrive, FileInfo
from api.utils.serializer import AliyunDriveSerializer
from common.base.utils import AesBaseCrypt
from common.cache.storage import DriveQrCache
from common.core.filter import OwnerUserFilter
from common.core.modelset import BaseModelSet
from common.core.response import PageNumber, ApiResponse
from common.utils.pending import get_pending_result

logger = logging.getLogger(__file__)


class AliyunDriveFilter(filters.FilterSet):
    min_used_size = filters.NumberFilter(field_name="used_size", lookup_expr='gte')
    max_used_size = filters.NumberFilter(field_name="used_size", lookup_expr='lte')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = AliyunDrive
        fields = ['user_id', 'user_name']


class AliyunDriveView(BaseModelSet):
    # permission_classes = []
    queryset = AliyunDrive.objects.all()
    serializer_class = AliyunDriveSerializer
    pagination_class = PageNumber

    filter_backends = [OwnerUserFilter, filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['updated_time', 'used_size', 'created_time', 'total_size']
    filterset_class = AliyunDriveFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ali_obj = Aligo(instance)
        file_id_list = [file.get('file_id') for file in
                        FileInfo.objects.filter(aliyun_drive_id=instance).values('file_id').all()]
        result_list = ali_obj.batch_move_to_trash(file_id_list)
        logger.debug(f'{instance} move {file_id_list} to trash.result:{result_list}')
        self.perform_destroy(instance)
        return ApiResponse()

    def create(self, request, *args, **kwargs):
        return ApiResponse(code=1001, msg='添加失败')


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
        drive_obj = AliyunDrive(owner_id=request.user)
        ali_auth = Auth(drive_obj)
        sid = request.data['sid']
        data = DriveQrCache(sid).get_storage_cache()
        if data:
            status, result = get_pending_result(ali_auth.check_scan_qr, expect_func, data=data, run_func_count=1,
                                                locker_key=sid, unique_key=sid)
            if status and result.get('data', {}).get('code') == 0:
                ali_drive_obj = AliyunDrive.objects.filter(owner_id=request.user,
                                                           user_id=ali_auth.token.user_id).first()
                ali_obj = Aligo(ali_drive_obj)
                default_drive_obj = ali_obj.get_default_drive()
                ali_drive_obj.total_size = default_drive_obj.total_size
                ali_drive_obj.used_size = default_drive_obj.used_size
                ali_drive_obj.active = True
                ali_drive_obj.save(update_fields=['total_size', 'used_size', 'active'])
            return ApiResponse(data={'pending_status': status, 'data': result})
        return ApiResponse(code=1001, msg='异常请求，请重试')
