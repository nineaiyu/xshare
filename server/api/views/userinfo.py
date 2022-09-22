#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : userinfo
# author : ly_13
# date : 2022/9/13
from django.conf import settings
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.utils.serializer import UserInfoSerializer
from common.core.response import ApiResponse
from common.utils.token import make_token, verify_token


def get_token_lifetime():
    access_token_lifetime = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
    refresh_token_lifetime = settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME')
    return {
        'access_token_lifetime': int(access_token_lifetime.total_seconds()),
        'refresh_token_lifetime': int(refresh_token_lifetime.total_seconds()),
    }


class LoginView(TokenObtainPairView):

    def get(self, request):
        token = make_token(request.query_params.get('client_id'))
        data = {'token': token}
        data.update(get_token_lifetime())
        return ApiResponse(data=data)

    def post(self, request, *args, **kwargs):
        client_id = request.data.get('client_id')
        token = request.data.get('token')
        if verify_token(token, client_id, success_once=True):
            data = super().post(request, *args, **kwargs).data
            data.update(get_token_lifetime())
            return ApiResponse(data=data)
        return ApiResponse(code=9999, msg='token校验失败,请刷新页面重试')


class RefreshTokenView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs).data
        data.update(get_token_lifetime())
        return ApiResponse(data=data)


class UserInfoView(APIView):

    def get(self, request):
        data = UserInfoSerializer(request.user).data
        return ApiResponse(data=data)

    def post(self, request):
        auth.logout(request)


class LogoutView(APIView):

    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return ApiResponse()
