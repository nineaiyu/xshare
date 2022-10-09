#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : tasks.py
# author : ly_13
# date : 2022/9/23

import logging
from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from api.models import AliyunDrive, ShareCode, FileInfo
from api.utils.model import get_aliyun_drive
from common.base.magic import MagicCacheData, cache_response
from xshare.celery import app

logger = logging.getLogger(__file__)


def eta_second(second):
    ctime = datetime.now()
    utc_ctime = datetime.utcfromtimestamp(ctime.timestamp())
    time_delay = timedelta(seconds=second)
    return utc_ctime + time_delay


@shared_task
def sync_drive_size(batch_queryset):
    for drive_obj in batch_queryset:
        try:
            ali_obj = get_aliyun_drive(drive_obj)
            default_drive_obj = ali_obj.get_default_drive()
            drive_obj.total_size = default_drive_obj.total_size
            drive_obj.used_size = default_drive_obj.used_size
            drive_obj.active = True
            drive_obj.save(update_fields=['total_size', 'used_size', 'active', 'updated_time'])
            logger.info(f'{drive_obj} update size success')
        except Exception as e:
            logger.warning(f'{drive_obj} update drive size failed:{e}')


@MagicCacheData.make_cache(timeout=60 * 10, key_func=lambda *args: args[0].user_id)
def delay_sync_drive_size(drive_obj):
    c_task = sync_drive_size.apply_async(args=([drive_obj],), eta=eta_second(60 * 10))
    logger.info(f'{drive_obj} delay exec {c_task}')


@app.task
def batch_sync_drive_size(batch=100):
    """
    :param batch:
    :return:
    主要用户阿里网盘token刷新，并获取磁盘空间大小，每天凌晨2点执行
    """
    drive_queryset = AliyunDrive.objects.filter(active=True, enable=True).all()
    for index in range(int(len(drive_queryset) / batch) + 1):
        batch_queryset = drive_queryset[index * batch:(index + 1) * batch]
        if batch_queryset:
            sync_drive_size.apply_async(args=(batch_queryset,))


@app.task
def auth_clean_invalid_share():
    default_timezone = timezone.get_default_timezone()
    value = timezone.make_aware(datetime.now(), default_timezone)
    deleted, _ = ShareCode.objects.filter(file_id__isnull=True, expired_time__lt=value).delete()


@shared_task
def refresh_lobby_cache():
    cache_response.invalid_cache('FileLobbyView_get')


@MagicCacheData.make_cache(timeout=60)
def delay_refresh_lobby_cache():
    c_task = refresh_lobby_cache.apply_async(eta=eta_second(60))
    logger.info(f'delay_refresh_lobby_cache exec {c_task}')


@app.task
def clean_visitor_user():
    default_timezone = timezone.get_default_timezone()
    value = timezone.make_aware(datetime.now() - settings.TEMP_USER_CLEAN_TIME, default_timezone)
    user_queryset = User.objects.filter(is_active=True, is_superuser=False, is_staff=False, last_name='0',
                                        last_login__lte=value)
    file_user_queryset = user_queryset.filter(fileinfo__isnull=False)

    items = FileInfo.objects.filter(owner_id__in=file_user_queryset).values('owner_id__username',
                                                                            'aliyun_drive_id').distinct()

    drive_info_dict = {}
    logger.info(f'items:{items}')
    for item in items:
        aliyun_drive_id = item.get('aliyun_drive_id')
        username = item.get('owner_id__username')
        owner_ids = drive_info_dict.get(aliyun_drive_id)
        if not owner_ids:
            drive_info_dict[aliyun_drive_id] = [username]
        else:
            drive_info_dict[aliyun_drive_id].append(username)
    logger.info(f"drive_info_dict:{drive_info_dict}")
    for drive_id, username_list in drive_info_dict.items():
        drive_obj = AliyunDrive.objects.filter(pk=drive_id, active=True).first()
        try:
            ali_obj = get_aliyun_drive(drive_obj)
            res = ali_obj.get_folder_by_path(f"{settings.XSHARE}/visitor")
            file_list = ali_obj.get_file_list(parent_file_id=res.file_id)
            file_id_list = []
            for file in file_list:
                if file.type == 'folder' and file.name in username_list:
                    file_id_list.append(file.file_id)
            ali_obj.batch_move_to_trash(file_id_list)
            logger.info(f'{drive_obj} clean visitor user data {username_list} success')
        except Exception as e:
            logger.error(f'{drive_obj} clean visitor user data failed {e}')
    logger.info(f'delete {user_queryset}')
    user_queryset.delete()
