#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : serializer
# author : ly_13
# date : 2022/9/13
import datetime
import logging

from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

logger = logging.getLogger(__file__)
from api import models


class TokenObtainSerializer(TokenObtainPairSerializer):

    def get_token(self, user):
        token = super().get_token(user)
        token['name'] = user.username
        return token


class AliyunDriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AliyunDrive
        exclude = ["owner_id", "access_token", "refresh_token"]
        read_only_fields = list(
            set([x.name for x in models.AliyunDrive._meta.fields]) - {"enable", "private", "description"})


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'email', 'last_login']


class FileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileInfo
        exclude = ["owner_id", "aliyun_drive_id"]
        read_only_fields = list(
            set([x.name for x in models.FileInfo._meta.fields]) - {"description"})


class ShareCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShareCode
        exclude = ["owner_id", "file_id"]
        read_only_fields = list(
            set([x.name for x in models.ShareCode._meta.fields]) - {"description", "password", "expired_time"})

    file_info_list = serializers.SerializerMethodField()

    def get_file_info_list(self, obj):
        return FileInfoSerializer(obj.file_id.all(), many=True).data

    is_expired = serializers.SerializerMethodField()

    def get_is_expired(self, obj):
        default_timezone = timezone.get_default_timezone()
        value = timezone.make_aware(datetime.datetime.now(), default_timezone)
        return obj.expired_time < value

    size = serializers.SerializerMethodField()

    def get_size(self, obj):
        return obj.file_id.all().aggregate(size=Sum('size')).get('size', 0)

    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        return obj.file_id.count()
    # expired_time = serializers.DateTimeField()
    #
    # def validate_expired_time(self, attrs):
    #     logger.error(attrs)
    #     return attrs
    #
    # def validate(self, data):
    #     """
    #     Check that start is before finish.
    #     """
    #     logger.error(data)
    #     return data


class ShortSerializer(ShareCodeSerializer):
    class Meta:
        model = models.ShareCode
        exclude = ["owner_id", "file_id", "id", "short", "password"]
        read_only_fields = [x.name for x in models.ShareCode._meta.fields]

    def get_file_info_list(self, obj):
        if obj.password and not obj.password == self.context.get('password'):
            return []
        return FileInfoSerializer(obj.file_id.all(), many=True).data

    need_password = serializers.SerializerMethodField()

    def get_need_password(self, obj):
        return bool(obj.password)
