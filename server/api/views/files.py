#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : files
# author : ly_13
# date : 2022/9/18
import logging

from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView

from api.models import FileInfo, ShareCode
from api.utils.model import get_aliyun_drive, batch_get_download_url, batch_delete_file
from api.utils.serializer import FileInfoSerializer
from common.cache.storage import DownloadUrlCache
from common.core.filter import OwnerUserFilter
from common.core.modelset import BaseModelSet
from common.core.response import PageNumber, ApiResponse

logger = logging.getLogger(__file__)


class FileInfoFilter(filters.FilterSet):
    min_size = filters.NumberFilter(field_name="size", lookup_expr='gte')
    max_size = filters.NumberFilter(field_name="size", lookup_expr='lte')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = FileInfo
        fields = ['name']


class FileInfoView(BaseModelSet):
    queryset = FileInfo.objects.all()
    serializer_class = FileInfoSerializer
    pagination_class = PageNumber

    filter_backends = [OwnerUserFilter, filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['size', 'created_at', 'downloads']
    filterset_class = FileInfoFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ali_obj = get_aliyun_drive(instance.aliyun_drive_id)
        result = ali_obj.move_file_to_trash(instance.file_id)
        DownloadUrlCache(instance.drive_id, instance.file_id).del_storage_cache()
        logger.debug(f'{instance.aliyun_drive_id} move {instance} to trash.result:{result}')
        self.perform_destroy(instance)
        return ApiResponse()

    def create(self, request, *args, **kwargs):
        return ApiResponse(code=1001, msg='添加失败')


class ManyView(APIView):

    def get(self, request, name):
        if name == 'share':
            short = request.query_params.get('short')
            if short:
                share_obj = ShareCode.objects.filter(owner_id=request.user, short=short).first()
                serializer = FileInfoSerializer(share_obj.file_id.all(), many=True)
                return ApiResponse(data=serializer.data)
        return ApiResponse(code=1001, msg='操作失败')

    def post(self, request, name):
        if name == 'file':
            action = request.data.get('action', '')
            file_id_list = request.data.get('file_id_list', [])
            if action in ['delete', 'download'] and file_id_list:
                file_obj_list = FileInfo.objects.filter(owner_id=request.user, file_id__in=file_id_list).all()
                if file_obj_list:
                    if action == 'download':
                        return ApiResponse(data=batch_get_download_url(file_obj_list))
                    elif action == 'delete':
                        batch_delete_file(file_obj_list)
                        FileInfo.objects.filter(owner_id=request.user, file_id__in=file_id_list).delete()
                        return ApiResponse()
        elif name == 'share':
            action = request.data.get('action', '')
            share_id_list = request.data.get('share_id_list', [])
            if action in ['delete'] and share_id_list:
                ShareCode.objects.filter(owner_id=request.user, short__in=share_id_list).delete()
                return ApiResponse()
            elif action in ['clean']:
                deleted, _ = ShareCode.objects.filter(owner_id=request.user, file_id__isnull=True).delete()
                return ApiResponse(data={'count': deleted})

        return ApiResponse(code=1001, msg='操作失败')
