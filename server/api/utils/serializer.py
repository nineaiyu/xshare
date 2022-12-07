#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : serializer
# author : ly_13
# date : 2022/9/13
import datetime
import logging

from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers

from api import models
from common.utils.token import make_token

logger = logging.getLogger(__file__)


class AliyunDriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AliyunDrive
        exclude = ["owner_id", "access_token", "refresh_token"]
        read_only_fields = list(
            set([x.name for x in models.AliyunDrive._meta.fields]) - {"enable", "private", "description"})


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'email', 'last_login', 'expired_time']
        read_only_fields = list(
            set([x.name for x in models.User._meta.fields]) - {"first_name"})

    first_name = serializers.SerializerMethodField()

    def get_first_name(self, obj):
        return obj.first_name if obj.first_name else obj.username

    expired_time = serializers.SerializerMethodField()

    def get_expired_time(self, obj):
        if obj.last_name == "0":
            default_timezone = timezone.get_default_timezone()
            return timezone.make_naive(obj.last_login + settings.TEMP_USER_CLEAN_TIME, default_timezone)
        else:
            return "1"


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name', 'old_password', 'new_password']
        extra_kwargs = {
            "old_password": {"write_only": True},
            "new_password": {"write_only": True},
        }

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        old_password = validated_data.get("old_password")
        new_password = validated_data.get("new_password")
        if old_password and new_password and instance.last_name != "0":
            if not instance.check_password(validated_data.get("old_password")):
                raise Exception('旧密码校验失败')
            instance.set_password(validated_data.get("new_password"))
            instance.save()
            return instance
        return super(UserInfoUpdateSerializer, self).update(instance, validated_data)


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


class FileShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileInfo
        exclude = ["owner_id", "aliyun_drive_id", "id", "content_type", "crc64_hash"]

    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        return make_token(key=obj.file_id, time_limit=600, force_new=True)


class ShortSerializer(ShareCodeSerializer):
    class Meta:
        model = models.ShareCode
        exclude = ["owner_id", "file_id", "id", "short", "password"]
        read_only_fields = [x.name for x in models.ShareCode._meta.fields]

    def get_file_info_list(self, obj):
        if obj.password and not obj.password == self.context.get('password'):
            return []
        return FileShortSerializer(obj.file_id.all(), many=True).data

    need_password = serializers.SerializerMethodField()

    def get_need_password(self, obj):
        return bool(obj.password)


class LobbyShareSerializer(ShareCodeSerializer):
    class Meta:
        model = models.ShareCode
        fields = ['short', 'created_time', 'description', 'size', 'count']


class LobbyFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileInfo
        fields = ['name', 'created_at', 'size', 'downloads', 'description', 'file_id', 'token', 'category']

    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        context = self.context
        time_limit = context.get('time_limit', 600)
        prefix = context.get('prefix', 'lobby')
        return make_token(key=obj.file_id, time_limit=time_limit, force_new=True, prefix=prefix)
