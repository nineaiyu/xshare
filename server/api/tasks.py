#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : tasks.py
# author : ly_13
# date : 2022/9/23

import logging
from datetime import datetime, timedelta

from common.cache.state import SyncDriveSizeState
from xshare.celery import app
from api.models import AliyunDrive
from api.utils.model import get_aliyun_drive
from celery import shared_task

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


def delay_sync_drive_size(drive_obj):
    with SyncDriveSizeState(f'delay_sync_drive_size_{drive_obj.user_id}', timeout=60 * 10) as state:
        if state:
            c_task = sync_drive_size.apply_async(args=([drive_obj],), eta=eta_second(60 * 10))
            result = c_task.get(propagate=False)
            logger.info(f'{drive_obj} delay exec success {result}')
        else:
            logger.info(f'{drive_obj} delay exist and return')
            return


@app.task
def batch_sync_drive_size(batch=100):
    """
    :param batch:
    :return:
    主要用户阿里网盘token刷新，并获取磁盘次年小，每天凌晨2点执行
    """
    drive_queryset = AliyunDrive.objects.filter(active=True, enable=True).all()
    for index in range(int(len(drive_queryset) / batch) + 1):
        batch_queryset = drive_queryset[index * batch:(index + 1) * batch]
        if batch_queryset:
            sync_drive_size.apply_async(args=(batch_queryset,))
