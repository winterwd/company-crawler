#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: albert
:date: 02/28/2019
:desc: http请求工具类
"""
import logging
import requests

from config import GLOBAL_PROXY


class Request:
    def __init__(self, url, params=None, proxy=False, **kwargs):
        self.proxy = proxy
        self.url = url
        self.params = params
        self.data = None
        self.get(**kwargs)

    def get(self, **kwargs):
        p = proxy() if GLOBAL_PROXY and self.proxy else None
        try:
            resp = requests.get(self.url, params=self.params, verify=False, proxies=p, **kwargs)
            if resp and resp.status_code == 200:
                self.data = resp.text
            else:
                logging.warning(resp)
        except IOError:
            logging.error('Error')


def proxy():
    import json
    from config.settings import PROXY_POOL_URL

    p = Request(f"{PROXY_POOL_URL}/get").data
    if p:
        p = json.loads(p)
        return {"http": "http://%s" % p.get("proxy")}
