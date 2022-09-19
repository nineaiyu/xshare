#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : response
# author : ly_13
# date : 2022/9/13

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumber(PageNumberPagination):
    page_size = 20  # 每页显示多少条
    page_size_query_param = 'size'  # URL中每页显示条数的参数
    page_query_param = 'page'  # URL中页码的参数
    max_page_size = 100  # 最大页码数限制


class ApiResponse(Response):
    def __init__(self, code=1000, msg='success', data=None, status=None, headers=None, content_type=None, **kwargs):
        dic = {
            'code': code,
            'msg': msg
        }
        if data is not None:
            dic['data'] = data
        dic.update(kwargs)
        self._data = data
        # 对象来调用对象的绑定方法，会自动传值
        super().__init__(data=dic, status=status, headers=headers, content_type=content_type)

        # 类来调用对象的绑定方法，这个方法就是一个普通函数，有几个参数就要传几个参数
        # Response.__init__(data=dic,status=status,headers=headers,content_type=content_type)
