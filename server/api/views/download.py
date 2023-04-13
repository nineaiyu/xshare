#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : download
# author : ly_13
# date : 2022/9/19

import logging
from io import BytesIO
from wsgiref.util import FileWrapper

from django.http import FileResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views import View
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import FileInfo
from api.utils.model import get_download_url, get_video_m3u8
from api.utils.serializer import FileInfoSerializer
from common.core.filter import OwnerUserFilter
from common.core.response import ApiResponse
from common.utils.token import verify_token

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
        return ApiResponse(code=1001, msg='文件违规')

    def list(self, request, *args, **kwargs):
        return ApiResponse(code=1001, msg='获取失败')


class M3U8View(View):
    def get(self, request, file_id):
        token = request.GET.get('token')
        if token and file_id and verify_token(token, file_id, success_once=False):
            instance = FileInfo.objects.filter(file_id=file_id, category='video').first()
            if instance:
                m3u8_data = get_video_m3u8(instance)
                buffer = BytesIO(m3u8_data.encode('utf-8'))
                m3u8_file = FileWrapper(buffer)
                response = FileResponse(m3u8_file)
                response['Content-Type'] = "audio/mpegurl"
                return response
        return ApiResponse(msg='error')


class DirectlyDownloadView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, file_pk, file_id, file_name):
        instance = FileInfo.objects.filter(pk=file_pk, file_id=file_id).first()
        if instance:
            download_url_dict = get_download_url(instance)
            logger.warning(download_url_dict)
            if download_url_dict and download_url_dict.get('download_url'):
                instance.downloads += 1
                instance.save(update_fields=['downloads'])
                return HttpResponseRedirect(redirect_to=download_url_dict.get('download_url'))
        return HttpResponseNotFound(content="文件不存在")
