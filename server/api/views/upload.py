#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : upload
# author : ly_13
# date : 2022/9/18
import json
import logging
import time

from django.conf import settings
from django.db.models import F
from rest_framework.views import APIView

from api.models import FileInfo, AliyunDrive
from api.tasks import delay_sync_drive_size
from api.utils.model import get_aliyun_drive
from common.base.utils import AesBaseCrypt
from common.cache.storage import UploadPartInfoCache
from common.core.response import ApiResponse
from common.core.throttle import UploadThrottle
from common.utils.token import generate_alphanumeric_token_of_length

logger = logging.getLogger(__file__)


def check_sid(request, sid):
    try:
        res = AesBaseCrypt().get_decrypt_uid(sid)
        data = json.loads(res)
        n_time = time.time()
        if data['username'] == request.user.username and data['expire'] > n_time:
            return True
    except Exception as e:
        logger.warning(f'check sid failed. load data exception {e}')
    return False


def save_file_info(complete, request, drive_obj):
    fields = ['name', 'file_id', 'drive_id', 'created_at', 'size', 'content_type', 'content_hash',
              'crc64_hash', 'category']

    defaults = {}
    for f in fields:
        defaults[f] = getattr(complete, f)
    FileInfo.objects.create(
        owner_id=request.user,
        aliyun_drive_id=drive_obj,
        **defaults
    )
    delay_sync_drive_size(drive_obj)


class AliyunDriveUploadView(APIView):
    throttle_classes = [UploadThrottle]

    def get(self, request):
        n_time = time.time()
        sid = AesBaseCrypt().set_encrypt_uid(json.dumps({'username': request.user.username, 'expire': n_time + 1800}))
        return ApiResponse(data={'sid': sid})

    def post(self, request):
        action = request.data.get('action', '')

        file_info = request.data.get('file_info')
        if file_info and check_sid(request, file_info.get('sid', '')) and action in ['pre_hash', 'content_hash',
                                                                                     'upload_complete']:

            file_name = file_info.get("file_name", generate_alphanumeric_token_of_length(32))
            owner_dir = "member" if request.user.last_name == "1" else "visitor"
            file_info['file_name'] = f'{settings.XSHARE}/{owner_dir}/{request.user.username}/{file_name}'
            drive_queryset = AliyunDrive.objects.filter(active=True, enable=True,
                                                        total_size__gte=F('used_size') + file_info.get('file_size', 0),
                                                        access_token__isnull=False)

            drive_obj = drive_queryset.filter(owner_id=request.user).order_by('created_time').first()
            if not drive_obj:
                drive_obj = drive_queryset.filter(private=False).order_by('created_time').first()
                if not drive_obj:
                    return ApiResponse(code=1002, msg='暂无可用存储')
            ali_obj = get_aliyun_drive(drive_obj)
            if action == 'pre_hash':
                part_info, check_status = ali_obj.pre_hash_check(file_info)
                logger.debug(f'{file_info.get("file_name")} pre_hash check {part_info}')
                data = {
                    'check_status': check_status,
                    'md5_token': ali_obj.get_md5_token(),
                    'upload_extra': ali_obj.get_upload_extra(),
                }
                if not check_status:
                    data['part_info_list'] = ali_obj.reget_upload_part_url(part_info)
                return ApiResponse(data=data)
            elif action == 'content_hash':
                part_info, check_status = ali_obj.content_hash_check(file_info)
                logger.debug(f'{file_info.get("file_name")} pre_hash check {part_info}')
                data = {'check_status': check_status, 'upload_extra': ali_obj.get_upload_extra()}
                if not check_status:
                    data['part_info_list'] = ali_obj.reget_upload_part_url(part_info)
                else:
                    complete = ali_obj.get_file(part_info.file_id, part_info.drive_id)
                    save_file_info(complete, request, drive_obj)
                    UploadPartInfoCache(file_info.get('sid')).del_storage_cache()
                    data['file_id'] = complete.file_id
                return ApiResponse(data=data)

            elif action == 'upload_complete':
                complete, check_status = ali_obj.upload_complete(file_info)
                logger.debug(f'{file_info.get("file_name")} pre_hash check {complete}')
                if complete and check_status:
                    save_file_info(complete, request, drive_obj)
                    UploadPartInfoCache(file_info.get('sid')).del_storage_cache()
                return ApiResponse(data={'check_status': check_status, 'file_id': complete.file_id})
        return ApiResponse(code=1001, msg='错误请求')
