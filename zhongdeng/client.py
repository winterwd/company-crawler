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
        # res = TencentOCR().detect(3)
        # print('TencentOCR = ' + res)

        res = BaiduOCR().detect(3)
        print('BaiduOCR = ' + res)
        #
        # res = AliOCR().detect(3)
        # print('AliOCR = ' + res)


if __name__ == '__main__':
    ZDClient.ocr_detect()