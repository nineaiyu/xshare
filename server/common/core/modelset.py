#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : modelset
# author : ly_13
# date : 2022/9/13
from rest_framework.viewsets import ModelViewSet

from common.core.response import ApiResponse


class BaseModelSet(ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        return ApiResponse(data=data)

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        return ApiResponse(data=data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse()

    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs).data
        return ApiResponse(data=data)
