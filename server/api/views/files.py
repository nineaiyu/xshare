#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : files
# author : ly_13
# date : 2022/9/18
import logging

from common.libs.alidrive import Aligo
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView

from api.models import FileInfo, AliyunDrive
from api.utils.serializer import FileInfoSerializer
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
        ali_obj = Aligo(instance.aliyun_drive_id)
        result = ali_obj.move_file_to_trash(instance.file_id)
        logger.debug(f'{instance.aliyun_drive_id} move {instance} to trash.result:{result}')
        self.perform_destroy(instance)
        return ApiResponse()

    def create(self, request, *args, **kwargs):
        return ApiResponse(code=1001, msg='添加失败')


class FileManyView(APIView):

    def post(self, request):
        action = request.data.get('action', '')
        file_id_list = request.data.get('file_id_list', [])
        if action in ['delete', 'download'] and file_id_list:
            drive_obj_dict = {}
            for file_obj in FileInfo.objects.filter(owner_id=request.user, file_id__in=file_id_list).all():
                drive_user_id = file_obj.aliyun_drive_id.user_id
                drive_obj = drive_obj_dict.get(drive_user_id)
                if not drive_obj:
                    drive_obj_dict[drive_user_id] = [file_obj.file_id]
                else:
                    drive_obj_dict[drive_user_id].append(file_obj.file_id)

            for drive_user_id, file_info_list in drive_obj_dict.items():
                drive_obj = AliyunDrive.objects.filter(user_id=drive_user_id, active=True, enable=True).first()
                if drive_obj:
                    ali_obj = Aligo(drive_obj)
                    if action == 'delete':
                        ali_obj.batch_move_to_trash(file_info_list)
                        FileInfo.objects.filter(owner_id=request.user, file_id__in=file_id_list).delete()
                        return ApiResponse()
                    elif action == 'download':
                        result_list = ali_obj.batch_get_files(file_info_list)
                        download_url_list = [result.download_url if result.download_url else result.url for result in
                                             result_list]
                        return ApiResponse(data=download_url_list)

        return ApiResponse(code=1001, msg='操作失败')
