#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 03/13/2023
"""

import logging
from tianyancha.client import TycClient
from util import excel
import os
import time


def start(keys: list = None):
    if keys is None:
        keys = []

    def __printall(items):
        for elem in items:
            logging.info(elem.__str__())

    datas = []
    for key in keys:
        logging.info('正在采集[%s]...' % key)
        companies = TycClient().search(key, pageSize=1, page=1).companies
        __printall(companies)
        if len(companies) > 0:
            datas.extend(companies)
            time.sleep(2)
        else:
            # 可能接口异常就退出
            logging.warning('采集[%s]..出错' % key)
            break

    xls_path = os.path.abspath(os.path.join(os.getcwd(), './logs/tianyancha_company.xls'))
    excel.write(xls_path, datas)
    logging.info("completed")
