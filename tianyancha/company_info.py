#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 03/13/2023
"""

import logging

from db.models import Company
from tianyancha.client import TycClient
from util import excel
import os
import time


def start(keys: list = None, path: str = './logs/company_info.xlsx'):
    if keys is None:
        keys = []

    def __printall(items):
        for elem in items:
            logging.info(elem.__str__())

    datas = []
    for key in keys:
        logging.info(f'正在采集[{key}]...')
        companies = TycClient().search(key, pageSize=1, page=1).companies
        __printall(companies)
        if len(companies) > 0:
            datas.extend(companies)
            time.sleep(2)
        else:
            # 可能接口异常，没有获取到数据，添加默认数据
            logging.warning(f'采集[{key}]...出错')
            target = Company()
            target.keyword = key
            target.short_name = key
            target.name = key
            items = [target]
            datas.extend(items)

    xls_path = os.path.abspath(os.path.join(os.getcwd(), path))
    excel.write(xls_path, datas)
    logging.info("completed")
