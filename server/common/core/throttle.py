#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : throttle
# author : ly_13
# date : 2022/9/13


import hashlib

from rest_framework.throttling import SimpleRateThrottle


class UploadThrottle(SimpleRateThrottle):
    """上传速率限制"""
    scope = "UploadFile"

    def get_cache_key(self, request, view):
        return 'upload_file_' + self.get_ident(request) + hashlib.md5(
            request.META.get('HTTP_USER_AGENT', '').encode("utf-8")).hexdigest()


class LoginUserThrottle(SimpleRateThrottle):
    """登录用户访问频率限制"""
    scope = "LoginUser"

    def get_cache_key(self, request, view):
        if hasattr(request.user, 'username'):
            return request.user.username
        else:
            self.get_ident(request)
