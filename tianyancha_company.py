#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 03/13/2023
"""

from tianyancha import company_info
from functools import reduce
from util import log
import numpy as np
import urllib3
import time
urllib3.disable_warnings()

log.set_file("./logs/tianyancha_c.log")

if __name__ == '__main__':
    names = []
    with open('./logs/company.txt', 'r') as file:
        items = file.read().split()
        func = lambda x, y: x if y in x else x + [y]
        keys = reduce(func, [[], ] + items)

        names = np.array_split(keys, 10)

    for name in names:
        company_info.start(name)
        time.sleep(600)
