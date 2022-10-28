#!/usr/bin/python3
# -*-: coding: utf-8 -*-

from tianyancha.client import TycClient
from util import log, excel
import logging
import os

log.set_file("logs/tianyancha.2022-10-27.log")


def _find_keys(path) -> list:
    with open(path, "r") as f:
        datas = f.read().split('\n')
        datas = set(datas)
        return list(datas.intersection(datas))
    return []


def start(items: list = None):
    if items is None:
        logging.info("completed")
        return

    companies: list = []
    for key in items:
        logging.info('正在采集[%s]...' % key)
        company = TycClient().search(key, pageSize=1).companies[0]
        logging.info(company.__str__())
        companies.append(company)

    xls_path = os.path.abspath(os.path.join(os.getcwd(), './logs/ty_phone.xls'))
    excel.write(xls_path, companies)
    logging.info("completed")


if __name__ == '__main__':
    filepath = './names.txt'
    keys = _find_keys(filepath)
    start(keys)
