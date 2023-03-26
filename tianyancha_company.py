#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 03/13/2023
"""

import math
import time

import numpy as np
import urllib3

from tianyancha import company_info
from util import log

urllib3.disable_warnings()
log.set_file("./logs/tianyancha_c.log")
WAIT_SECOND = 600


def batch_process_names(names=None):
    if names is None:
        names = []

    index = 0
    for name in names:
        if len(name) > 0:
            path = f'./logs/tianyancha_company_{index}.xls'
            company_info.start(name, path)
            time.sleep(WAIT_SECOND)
            index += 1


if __name__ == '__main__':
    with open('./logs/company.txt', 'r') as file:
        items = file.read().split()
        keys = [x for i, x in enumerate(items) if x not in items[:i]]

        MAX_PAGE = 10
        MAX_PAGE_COUNT = 400
        count = min(MAX_PAGE, math.ceil(len(keys) / MAX_PAGE_COUNT))
        array = np.array_split(keys, count)

        batch_process_names(array)
