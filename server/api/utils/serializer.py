#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : serializer
# author : ly_13
# date : 2022/9/13
import logging

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
            set([x.name for x in models.AliyunDrive._meta.fields]) - {"description"})
