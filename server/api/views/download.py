#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : download
# author : ly_13
# date : 2022/9/19

import logging

from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import FileInfo
from api.utils.model import get_download_url
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
        download_url = get_download_url(instance)
        logger.warning(download_url)
        if download_url:
            instance.downloads += 1
            instance.save(update_fields=['downloads'])
            return ApiResponse(data=download_url)
        return ApiResponse(code=1001, msg='云盘不可用')

    def list(self, request, *args, **kwargs):
        return ApiResponse(code=1001, msg='获取失败')
