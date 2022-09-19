#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : storage
# author : ly_13
# date : 2022/9/17

import base64
import json
import logging

from django.core.cache import cache

from xshare.settings import CACHE_KEY_TEMPLATE

logger = logging.getLogger(__file__)


class RedisCacheBase(object):
    def __init__(self, cache_key):
        self.cache_key = cache_key

    def __getattribute__(self, item):
        if isinstance(item, str) and item != 'cache_key':
            if hasattr(self, "cache_key"):
                logger.debug(f'act:{item} cache_key:{super().__getattribute__("cache_key")}')
        return super().__getattribute__(item)

    def get_storage_cache(self):
        return cache.get(self.cache_key)

    def get_storage_key_and_cache(self):
        return self.cache_key, cache.get(self.cache_key)

    def set_storage_cache(self, value, timeout=600):
        return cache.set(self.cache_key, value, timeout)

    def del_storage_cache(self):
        return cache.delete(self.cache_key)

    def incr(self, amount=1):
        return cache.incr(self.cache_key, amount)

    def expire(self, timeout):
        return cache.expire(self.cache_key, timeout=timeout)

    def iter_keys(self):
        if not self.cache_key.endswith('*'):
            self.cache_key = f"{self.cache_key}*"
        return cache.iter_keys(self.cache_key)

    def get_many(self):
        return cache.get_many(self.cache_key)

    def del_many(self):
        for delete_key in cache.iter_keys(self.cache_key):
            cache.delete(delete_key)
        return True


class CloudStorageCache(RedisCacheBase):
    def __init__(self, auth, uid):
        if auth == '*':
            bid = auth
        else:
            bid = base64.b64encode(json.dumps(auth).encode("utf-8")).decode("utf-8")[0:64]
        self.cache_key = f"xxxxxxxxxxx_{uid}_{bid}"

        super().__init__(self.cache_key)


class TokenManagerCache(RedisCacheBase):
    def __init__(self, key, release_id):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('make_token_key')}_{key.lower()}_{release_id}"
        super().__init__(self.cache_key)


class PendingStateCache(RedisCacheBase):
    def __init__(self, locker_key):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('pending_state_key')}_{locker_key}"
        super().__init__(self.cache_key)


class UploadPartInfoCache(RedisCacheBase):
    def __init__(self, locker_key):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('upload_part_info_key')}_{locker_key}"
        super().__init__(self.cache_key)


class DriveQrCache(RedisCacheBase):
    def __init__(self, locker_key):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('drive_qrcode_key')}_{locker_key}"
        super().__init__(self.cache_key)
