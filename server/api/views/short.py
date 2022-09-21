#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : short
# author : ly_13
# date : 2022/9/20

# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : download
# author : ly_13
# date : 2022/9/19
import datetime
import logging

from django.utils import timezone
from rest_framework.views import APIView

from api.models import ShareCode
from api.utils.serializer import ShortSerializer
from common.core.response import ApiResponse

logger = logging.getLogger(__file__)


class ShortView(APIView):
    permission_classes = []

    # @CacheResponse(timeout=60)
    def get(self, request):
        query_params = request.query_params
        short = query_params.get('short')
        password = query_params.get('password')
        if short:
            default_timezone = timezone.get_default_timezone()
            value = timezone.make_aware(datetime.datetime.now(), default_timezone)
            share_obj = ShareCode.objects.filter(short=short, expired_time__gt=value).first()
            if share_obj:
                return ApiResponse(data={
                    'user_info': {
                        'head_img': 'https://static.wenshushu.cn/pf/1cnk77fx8rs/img',
                        'first_name': '谁许时光逝年华'
                    },
                    'share_info': ShortSerializer(share_obj, context={'password': password}).data
                })
        return ApiResponse(code=1001, msg='链接失效')
