#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : lobby
# author : ly_13
# date : 2022/9/26
import datetime
import logging

from django.db.models import Q
from django.utils import timezone
from rest_framework.views import APIView

from api.models import ShareCode, FileInfo
from api.utils.serializer import LobbyShareSerializer, LobbyFileSerializer
from common.core.response import ApiResponse

logger = logging.getLogger(__file__)


class FileLobbyView(APIView):
    permission_classes = []
    authentication_classes = []

    # @cache_response(timeout=600)
    def get(self, request):
        query_params = request.query_params
        default_timezone = timezone.get_default_timezone()
        value = timezone.make_aware(datetime.datetime.now(), default_timezone)
        share_queryset = ShareCode.objects.filter(expired_time__gt=value).filter(
            Q(password__isnull=True) | Q(password='')).order_by('-created_time')[:20]

        file_queryset = FileInfo.objects.filter(sharecode__expired_time__gt=value).filter(
            Q(sharecode__password__isnull=True) | Q(sharecode__password='')).order_by('-downloads').distinct()[:20]

        return ApiResponse(data={
            'share_data': LobbyShareSerializer(share_queryset, many=True).data,
            'file_data': LobbyFileSerializer(file_queryset, many=True).data
        })
