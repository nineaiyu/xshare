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

from api.models import ShareCode, FileInfo
from api.utils.model import get_download_url, batch_get_download_url
from api.utils.serializer import ShortSerializer
from common.base.magic import cache_response
from common.core.response import ApiResponse
from common.utils.token import verify_token

logger = logging.getLogger(__file__)


class ShortView(APIView):
    permission_classes = []
    authentication_classes = []

    def get_cache_key(self, *args, **kwargs):
        request = kwargs.get('request')
        query_params = request.query_params
        return f"{query_params.get('short')}_{query_params.get('password')}"

    @cache_response(timeout=59 * 10, key_func='get_cache_key')
    def get(self, request):
        query_params = request.query_params
        short = query_params.get('short')
        password = query_params.get('password')
        if short:
            default_timezone = timezone.get_default_timezone()
            value = timezone.make_aware(datetime.datetime.now(), default_timezone)
            share_obj = ShareCode.objects.filter(short=short, expired_time__gt=value).first()
            if share_obj:
                user_obj = share_obj.owner_id
                first_name = user_obj.first_name if user_obj.first_name else user_obj.username
                return ApiResponse(data={
                    'first_name': first_name,
                    'share_info': ShortSerializer(share_obj, context={'password': password}).data
                })
        return ApiResponse(code=1001, msg='链接失效')

    def post(self, request):
        auth_infos = request.data.get('auth_infos')
        if auth_infos and isinstance(auth_infos, list):
            if len(auth_infos) == 1:
                download_token = auth_infos[0].get('token')
                file_id = auth_infos[0].get('file_id')

                if download_token and file_id and verify_token(download_token, file_id, success_once=False):
                    file_obj = FileInfo.objects.filter(file_id=file_id).first()
                    download_url = get_download_url(file_obj)
                    if download_url:
                        file_obj.downloads += 1
                        file_obj.save(update_fields=['downloads'])
                        return ApiResponse(data=[download_url])
            else:
                verify_file_id_list = []
                for auth_info in auth_infos:
                    download_token = auth_info.get('token')
                    file_id = auth_info.get('file_id')
                    if download_token and file_id and verify_token(download_token, file_id, success_once=False):
                        verify_file_id_list.append(file_id)
                if verify_file_id_list:
                    file_obj_list = FileInfo.objects.filter(file_id__in=verify_file_id_list).all()
                    if file_obj_list:
                        return ApiResponse(data=batch_get_download_url(file_obj_list))
        return ApiResponse(code=1001, msg="授权过期")
