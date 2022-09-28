#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : flower
# author : ly_13
# date : 2022/9/28
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import gettext as _
from proxy.views import proxy_view
from rest_framework.views import APIView

flower_url = f'{settings.CELERY_FLOWER_HOST}:{settings.CELERY_FLOWER_PORT}'


class CeleryFlowerView(APIView):
    def get(self, request, path):
        if not request.user.is_superuser:
            return HttpResponse("Forbidden")
        remote_url = 'http://{}/flower/{}'.format(flower_url, path)
        try:
            response = proxy_view(request, remote_url)
        except Exception as e:
            msg = _("<h1>Flower service unavailable, check it</h1>") + \
                  '<br><br> <div>{}</div>'.format(e)
            response = HttpResponse(msg)
        return response

    def post(self, request, path):
        return self.get(request, path)
