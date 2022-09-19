#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : download
# author : ly_13
# date : 2022/9/19

# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : files
# author : ly_13
# date : 2022/9/18
import logging

from common.libs.alidrive import Aligo
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import FileInfo, AliyunDrive
from api.utils.serializer import FileInfoSerializer
from common.core.filter import OwnerUserFilter
from common.core.response import ApiResponse

logger = logging.getLogger(__file__)


class DownloadView(ReadOnlyModelViewSet):
    queryset = FileInfo.objects.all()
    serializer_class = FileInfoSerializer
    filter_backends = [OwnerUserFilter]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        drive_obj = AliyunDrive.objects.filter(active=True, enable=True, access_token__isnull=False,
                                               pk=instance.aliyun_drive_id.pk).first()
        action = request.query_params.get('action', 'file')
        if drive_obj:
            ali_obj = Aligo(drive_obj)
            if action == 'download':
                result = ali_obj.get_download_url(file_id=instance.file_id, drive_id=instance.drive_id)
                download_url = result.cdn_url if result.cdn_url else result.url
            else:
                result = ali_obj.get_file(file_id=instance.file_id, drive_id=instance.drive_id)
                download_url = result.download_url if result.download_url else result.url
            logger.debug(f'{instance.aliyun_drive_id} move {instance} to trash.result:{result}')
            instance.downloads += 1
            instance.save(update_fields=['downloads'])
            return ApiResponse(data={'download_url': download_url})
        return ApiResponse(code=1001, msg='云盘不可用')

    def list(self, request, *args, **kwargs):
        return ApiResponse(code=1001, msg='获取失败')
