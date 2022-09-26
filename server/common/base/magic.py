#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : magic
# author : ly_13
# date : 2022/9/24

import logging
import time
from functools import wraps
from importlib import import_module

from django.core.cache import cache

logger = logging.getLogger(__name__)


def run_function_by_locker(timeout=60 * 5, lock_func=None):
    """
    :param timeout:
    :param lock_func:  func -> {'locker_key':''}
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            if lock_func:
                locker = lock_func(*args, **kwargs)
            else:
                locker = kwargs.get('locker', {})
                if locker:
                    kwargs.pop('locker')
            t_locker = {'timeout': timeout, 'locker_key': func.__name__}
            t_locker.update(locker)
            new_locker_key = t_locker.pop('locker_key')
            new_timeout = t_locker.pop('timeout')
            if locker and new_timeout and new_locker_key:
                with cache.lock(new_locker_key, timeout=new_timeout, **t_locker):
                    logger.info(f"{new_locker_key} exec {func} start. now time:{time.time()}")
                    res = func(*args, **kwargs)
            else:
                res = func(*args, **kwargs)
            logger.info(f"{new_locker_key} exec {func} finished. used time:{time.time() - start_time} result:{res}")
            return res

        return wrapper

    return decorator


def call_function_try_attempts(try_attempts=3, sleep_time=2, failed_callback=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = False, {}
            start_time = time.time()
            for i in range(try_attempts):
                res = func(*args, **kwargs)
                status, result = res
                if status:
                    return res
                else:
                    logger.warning(f'exec {func} failed. {try_attempts} times in total. now {sleep_time} later try '
                                   f'again...{i}')
                time.sleep(sleep_time)
            if not res[0]:
                logger.error(f'exec {func} failed after the maximum number of attempts. Failed:{res[1]}')
                if failed_callback:
                    logger.error(f'exec {func} failed and exec failed callback {failed_callback.__name__}')
                    failed_callback(*args, **kwargs, result=res)
            logger.info(f"exec {func} finished. time:{time.time() - start_time} result:{res}")
            return res

        return wrapper

    return decorator


def magic_wrapper(func, *args, **kwargs):
    @wraps(func)
    def wrapper():
        return func(*args, **kwargs)

    return wrapper


def import_from_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError(f"{dotted_path} doesn't look like a module path") from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(f'Module "{module_path}" does not define a "{class_name}" attribute/class') from err


def magic_call_in_times(call_time=24 * 3600, call_limit=6, key=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f'magic_call_in_times_{func.__name__}'
            if key:
                cache_key = f'{cache_key}_{key(*args, **kwargs)}'
            cache_data = cache.get(cache_key)
            if cache_data:
                if cache_data > call_limit:
                    err_msg = f'{func} not yet started. cache_key:{cache_key} call over limit {call_limit} in {call_time}'
                    logger.warning(err_msg)
                    return False, err_msg
                else:
                    cache.incr(cache_key, 1)
            else:
                cache.set(cache_key, 1, call_time)
            start_time = time.time()
            try:
                res = func(*args, **kwargs)
                logger.info(
                    f"exec {func} finished. time:{time.time() - start_time}  cache_key:{cache_key} result:{res}")
                status = True
            except Exception as e:
                res = str(e)
                logger.info(f"exec {func} failed. time:{time.time() - start_time}  cache_key:{cache_key} Exception:{e}")
                status = False

            return status, res

        return wrapper

    return decorator


class MagicCacheData(object):
    @staticmethod
    def make_cache(cache_time=60 * 10, invalid_time=0, key=None):
        """
        :param cache_time:  数据缓存的时候，单位秒
        :param invalid_time: 数据缓存提前失效时间，单位秒。该cache有效时间为 cache_time-invalid_time
        :param key: cache唯一标识，默认为所装饰函数名称
        :return:
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f'magic_cache_data_{func.__name__}'
                if key:
                    cache_key = f'{cache_key}_{key(*args, **kwargs)}'

                n_time = time.time()
                res = cache.get(cache_key)
                if res and n_time - res.get('c_time', n_time) < cache_time - invalid_time:
                    logger.info(f"exec {func} finished. cache_key:{cache_key}  cache data exist result:{res}")
                    return res['data']
                else:
                    try:
                        data = func(*args, **kwargs)
                        res = {'c_time': n_time, 'data': data}
                        cache.set(cache_key, res, cache_time)
                        logger.info(
                            f"exec {func} finished. time:{time.time() - n_time}  cache_key:{cache_key} result:{res}")
                    except Exception as e:
                        logger.error(
                            f"exec {func} failed. time:{time.time() - n_time}  cache_key:{cache_key} Exception:{e}")

                    return res['data']

            return wrapper

        return decorator

    @staticmethod
    def invalid_cache(key):
        cache_key = f'magic_cache_data_{key}'
        res = cache.delete(cache_key)
        logger.warning(f"invalid_cache cache_key:{cache_key} result:{res}")
