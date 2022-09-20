#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : share
# author : ly_13
# date : 2022/9/19
import datetime
import logging
import random

from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from api.models import ShareCode, FileInfo
from api.utils.serializer import ShareCodeSerializer
from common.core.filter import OwnerUserFilter
from common.core.modelset import BaseModelSet
from common.core.response import PageNumber, ApiResponse

logger = logging.getLogger(__file__)


class ShareCodeFilter(filters.FilterSet):
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    expired = filters.BooleanFilter(field_name='expired_time', method='filter_expired')

    def filter_expired(self, queryset, name, value):
        default_timezone = timezone.get_default_timezone()
        now_time = timezone.make_aware(datetime.datetime.now(), default_timezone)
        if value:
            key = 'lt'
        else:
            key = 'gt'
        lookup = '__'.join([name, key])
        print({lookup: now_time})
        return queryset.filter(**{lookup: now_time})

    class Meta:
        model = ShareCode
        fields = ['short', 'expired', 'description']


def get_random_short(number=6):
    short = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
         'e', 'd', 'c', 'b', 'a'], number))
    share_obj = ShareCode.objects.filter(short=short).count()
    if share_obj:
        number += 2
        return get_random_short(number)
    else:
        return short


class ShareCodeView(BaseModelSet):
    queryset = ShareCode.objects.all()
    serializer_class = ShareCodeSerializer
    pagination_class = PageNumber

    filter_backends = [OwnerUserFilter, filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_time', 'expired_time']
    filterset_class = ShareCodeFilter

    def create(self, request, *args, **kwargs):
        file_id_list = request.data.get('file_id_list', [])
        share_info = request.data.get('share_info', {})
        if file_id_list and share_info:
            file_id_list_obj = FileInfo.objects.filter(owner_id=request.user, file_id__in=file_id_list)
            if file_id_list_obj:
                short = share_info.get('short')
                if short and len(short) > 5:
                    if ShareCode.objects.filter(short=short).count():
                        short = get_random_short(number=6)
                share_info['owner_id'] = request.user
                share_info['short'] = short if short else get_random_short(number=6)
                expired_time = share_info.get('expired_time')
                if expired_time:
                    try:
                        expired_time = datetime.datetime.fromtimestamp(int(share_info.get('expired_time')) / 1000)
                    except Exception as e:
                        logger.warning(f'format expired_time {expired_time} failed.{e}')
                        expired_time = None
                share_info['expired_time'] = expired_time
                share_code_obj = ShareCode.objects.create(**share_info)
                share_code_obj.file_id.add(*file_id_list_obj)
                return ApiResponse(data={'short': share_code_obj.short, 'password': share_code_obj.password})
        return ApiResponse(code=1001, msg='添加失败')
