#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 2022-02-21
:desc:
"""

from tencent_ocr import TencentOCR
from baidu_ocr import BaiduOCR
from ali_ocr import AliOCR


class ZDClient:

    @staticmethod
    def ocr_detect():
        res = TencentOCR().detect()
        if res is None:
            print('TencentOCR fail')
        else:
            print('TencentOCR = ' + res)

        res = BaiduOCR().detect()
        if res is None:
            print('BaiduOCR fail')
        else:
            print('BaiduOCR = ' + res)

        res = AliOCR().detect()
        if res is None:
            print('AliOCR fail')
        else:
            print('AliOCR = ' + res)


if __name__ == '__main__':
    ZDClient.ocr_detect()