#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" A simple disk cache implemention

@Author: Liu Shaofeng(liushaofeng01@baidu.com)
@Date: 2023/03/18 21:45
"""

import os
import sys
import time
import json
import shelve

def disk_cache(cache_path, expire_time=864000): # 默认10天过期
    cache = DiskCache(cache_path, expire_time)
    def decrator(func):
        def wrapper(key, *args, **kwargs):
            ckey = key
            if args or kwargs:
                ckey = str((key, args, kwargs))
            #print(f"disk_cache() ckey = {ckey}")
            val = cache.get(ckey)
            if val:
                return val
            val = func(key, *args, **kwargs)
            if val is not None:
                cache.set(ckey, val)
            return val
        return wrapper
    return decrator

class DiskCache:
    def __init__(self, cache_path, expire_time):
        path = '/'
        for part in os.path.abspath(cache_path).split('/')[1:-1]:
            if not part:
                continue
            path = os.path.join(path, part)
            if not os.path.exists(path):
                os.mkdir(path)

        self._cache_path = cache_path
        self._expire_time = expire_time
        self._db = shelve.open(cache_path)

    def get(self, key):
        key = str(key)
        #print(f"[DiskCache:{self._cache_path}] get({key})", file=sys.stderr)
        if key is None or key not in self._db:
            return None

        ts = time.time()
        cc = self._db[key]
        if ts - cc['create_time'] < self._expire_time:
            return cc['value']
        return None

    def set(self, key, value):
        key = str(key)
        #print(f"[DiskCache:{self._cache_path}] set({key}, {value})", file=sys.stderr)
        if value is not None:
            self._db[key] = {
                'value':value,
                'create_time':int(time.time()),
            }

    def __exit__(self):
        if self._db is not None:
            self._db.close()
            self._db = None

    def __del__(self):
        if self._db is not None:
            self._db.close()
            self._db = None

if __name__ == '__main__':
    @disk_cache(cache_path="/tmp/tmp_disk_cache.shelve", expire_time=2)
    def search(key:str) -> str:
        print(f"[search] key={key}")
        return f"This is the result for {key}"

    search(sys.argv[1])

