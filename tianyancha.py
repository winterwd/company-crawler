#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: lubosin
:date: 03/28/2019
"""
from tianyancha import crawler
from util import log
import urllib3
urllib3.disable_warnings()


log.set_file("./logs/tianyancha.log")


if __name__ == '__main__':
    keys = ['广东 环保 公路 交通 环境 整治 治理 污水']
    crawler.load_keys(keys)
    crawler.start()




