#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xshare
# filename : utils
# author : ly_13
# date : 2022/9/13


import base64
import hashlib
import logging

from Cryptodome import Random
from Cryptodome.Cipher import AES

logger = logging.getLogger(__file__)


class AESCipher(object):

    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pack_data(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpack_data(cipher.decrypt(enc[AES.block_size:]))

    @staticmethod
    def _pack_data(s):
        return s + ((AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)).encode(
            'utf-8')

    @staticmethod
    def _unpack_data(s):
        data = s[:-ord(s[len(s) - 1:])]
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        return data


class AesBaseCrypt(object):

    def __init__(self):
        self.cipher = AESCipher(self.__class__.__name__)

    def set_encrypt_uid(self, key):
        return self.cipher.encrypt(key.encode('utf-8')).decode('utf-8')

    def get_decrypt_uid(self, enc):
        try:
            return self.cipher.decrypt(enc)
        except Exception as e:
            logger.warning(f'decrypt {enc} failed. exception:{e}')
