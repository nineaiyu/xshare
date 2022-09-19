#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : userinfo
# author : ly_13
# date : 2022/9/13
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.utils.serializer import TokenObtainSerializer, UserInfoSerializer
from common.core.response import ApiResponse


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer

    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs).data
        return ApiResponse(data=data)


class UserInfoView(APIView):

    def get(self, request):
        data = UserInfoSerializer(request.user).data
        return ApiResponse(data=data)
