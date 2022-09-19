#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : aligotest
# author : ly_13
# date : 2022/9/13
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xshare.settings')
django.setup()
from api.models import AliyunDrive
from api.models import FileInfo

a = FileInfo.objects.filter().first()
drive_obj = AliyunDrive.objects.first()
# print(ali.get_file_list(),ali.get_default_drive())
# print(ali.get_file(file_id='63202f0905f29e7936374699ae9dd73ccda13aa9').__dict__)
# print(ali.get_share_token(share_id='LkUS6BrconT'))
# # exit(1)
# x = ali.get_share_link_download_url(file_id="62409af18e55ddd38969485b902d6d2a7dfe1c4b", share_id='LkUS6BrconT',
#                                     share_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21Kc29uIjoie1wiZG9tYWluX2lkXCI6XCJiajI5XCIsXCJzaGFyZV9pZFwiOlwiTGtVUzZCcmNvblRcIixcImNyZWF0b3JcIjpcIjE4NjViOWIwNmU2ZTQzYWJhZjhhZTkwYzI2MzQyNTkxXCIsXCJ1c2VyX2lkXCI6XCJhbm9ueW1vdXNcIn0iLCJjdXN0b21UeXBlIjoic2hhcmVfbGluayIsImV4cCI6MTY2MzA2MjI1NiwiaWF0IjoxNjYzMDU0OTk2fQ.W_ZsQ5IOa_jZb7C5jaJ3ydhatQl5yuEh2pG3qvdWrnG3ysCb_lhBEcrJJ9Bo_zIxQlZjobHb-t88yuXSsCYYHCwXxptUfuz3EJ_BwgCYiS0iNlgqT41u96g-p_kTvEHOS4uJeAe0q6plIdDY2p3FN_3nVCMyOfGFuY9WpNApIMw')
# print(x)
# print(ali.upload_file())
# res = ali.('w:\\dvcloud.xin_20220810_165027.zip')
# print(res)
# a =open('w:\\dvcloud.xin_20220810_165027.zip','rb').read(1024)
#
from common.libs.alidrive import Aligo

ali = Aligo(drive_obj)
# print(ali.get_default_drive())
print(ali.get_file(a.file_id, a.drive_id).__dict__)
# print(a.hex())
# print(hashlib.sha1(a).hexdigest())
# print(hashlib.sha256(a).hexdigest())
