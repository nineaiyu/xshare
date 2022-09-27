#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : model
# author : ly_13
# date : 2022/9/21
import datetime
import logging
import time
from urllib.parse import parse_qs

from common.libs.alidrive import Aligo
from django.utils import timezone

from api.models import AliyunDrive, FileInfo
from common.base.magic import run_function_by_locker
from common.cache.storage import DownloadUrlCache, AliDriveCache

logger = logging.getLogger(__file__)


def get_locker(*args, **kwargs):
    return {
        'locker_key': f'get_aliyun_drive_{args[0].user_id}'
    }


@run_function_by_locker(lock_func=get_locker)
def get_aliyun_drive(drive_obj: AliyunDrive) -> Aligo:
    drive_cache = AliDriveCache(drive_obj.user_id)
    cache_data = drive_cache.get_storage_cache()
    if not cache_data:
        cache_data = Aligo(drive_obj, refresh_token=drive_obj.refresh_token)
        default_timezone = timezone.get_default_timezone()
        value = timezone.make_aware(datetime.datetime.now(), default_timezone)
        drive_cache.set_storage_cache(cache_data, timeout=(drive_obj.expire_time - value).seconds)
    return cache_data


def get_download_url(file_obj: FileInfo, download=False) -> dict:
    if not file_obj:
        return {}
    download_cache = DownloadUrlCache(file_obj.drive_id, file_obj.file_id)
    cache_url = download_cache.get_storage_cache()
    if cache_url:
        return {'file_id': file_obj.file_id, 'download_url': cache_url}
    else:
        drive_obj = AliyunDrive.objects.filter(active=True, enable=True, access_token__isnull=False,
                                               pk=file_obj.aliyun_drive_id.pk).first()
        if drive_obj:
            ali_obj = get_aliyun_drive(drive_obj)
            if download:
                result = ali_obj.get_download_url(file_id=file_obj.file_id, drive_id=file_obj.drive_id)
                expired = datetime.datetime.strptime(result.expiration, '%Y-%m-%dT%H:%M:%S.%fZ')
                expired_second = (expired - datetime.datetime.utcnow()).seconds
                download_url = result.url
            else:
                result = ali_obj.get_file(file_id=file_obj.file_id, drive_id=file_obj.drive_id)
                download_url = result.download_url
                parse_data = parse_qs(download_url)
                expired = parse_data.get('x-oss-expires')
                if expired and len(expired) == 1:
                    expired_second = int(expired[0]) - time.time()
                else:
                    return {}
            download_cache.set_storage_cache(download_url, timeout=expired_second - 300)
            return {'file_id': file_obj.file_id, 'download_url': download_url}
    return {}


def batch_get_download_url(file_obj_list: [FileInfo]) -> list:
    cache_result = []
    drive_obj_dict = {}

    for file_obj in file_obj_list:
        download_cache = DownloadUrlCache(file_obj.drive_id, file_obj.file_id)
        cache_url = download_cache.get_storage_cache()
        if cache_url:
            cache_result.append({'file_id': file_obj.file_id, 'download_url': cache_url})
        else:
            drive_user_id = file_obj.aliyun_drive_id.user_id
            drive_obj = drive_obj_dict.get(drive_user_id)
            if not drive_obj:
                drive_obj_dict[drive_user_id] = [file_obj.file_id]
            else:
                drive_obj_dict[drive_user_id].append(file_obj.file_id)

    for drive_user_id, file_info_list in drive_obj_dict.items():
        drive_obj = AliyunDrive.objects.filter(user_id=drive_user_id, active=True, enable=True,
                                               access_token__isnull=False).first()
        if drive_obj:
            ali_obj = get_aliyun_drive(drive_obj)
            result_list = ali_obj.batch_get_files(file_info_list)
            for result in result_list:
                download_url = result.download_url
                parse_data = parse_qs(download_url)
                expired = parse_data.get('x-oss-expires')
                if expired and len(expired) == 1:
                    expired_second = int(expired[0]) - time.time()
                    download_cache = DownloadUrlCache(result.drive_id, result.file_id)
                    download_cache.set_storage_cache(download_url, timeout=expired_second - 300)
                    cache_result.append({'file_id': result.file_id, 'download_url': download_url})

    return cache_result


def batch_delete_file(file_obj_list: [FileInfo]) -> bool:
    drive_obj_dict = {}
    for file_obj in file_obj_list:
        drive_user_id = file_obj.aliyun_drive_id.user_id
        drive_obj = drive_obj_dict.get(drive_user_id)
        if not drive_obj:
            drive_obj_dict[drive_user_id] = [file_obj.file_id]
        else:
            drive_obj_dict[drive_user_id].append(file_obj.file_id)

    for drive_user_id, file_info_list in drive_obj_dict.items():
        drive_obj = AliyunDrive.objects.filter(user_id=drive_user_id, active=True, enable=True,
                                               access_token__isnull=False).first()
        if drive_obj:
            ali_obj = get_aliyun_drive(drive_obj)
            ali_obj.batch_move_to_trash(file_info_list)
    return True
