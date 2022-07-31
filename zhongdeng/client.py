#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 2022-02-21
:desc:
"""

import time
from util.ocr.tencent_ocr import TencentOCR
from util.ocr.baidu_ocr import BaiduOCR
from util.ocr.ali_ocr import AliOCR
from zhongdeng import CODE_IMAGE_PATH


class ZDClient:

    def __init__(self):
        self.__count = 1
        self.ali_ocr = AliOCR(CODE_IMAGE_PATH)
        self.tencent_ocr = TencentOCR(CODE_IMAGE_PATH)
        self.baidu_ocr = BaiduOCR(CODE_IMAGE_PATH)

    def ali_ocr_detect(self):
        res_dict: dict = self.ali_ocr.detect()
        content = res_dict.get('content')

        data = "".join(list(filter(str.isdigit, content)))
        if len(data) == 4:
            return data
        else:
            self.__count -= 1
            if self.__count > 0:
                time.sleep(0.5)
                return self.ali_ocr_detect()
            else:
                return None

    def tencent_ocr_detect(self):
        res = self.tencent_ocr.detect()
        if res is None:
            print('TencentOCR fail')
        else:
            print('TencentOCR = ' + res)

        # if len(resp.TextDetections) > 0:
        #     detectedText: TextDetection = resp.TextDetections[0]
        #     strx = detectedText.DetectedText
        #     data = "".join(list(filter(str.isdigit, strx)))
        #
        #     if len(data) == 4:
        #         return data
        #     else:
        #         return None

    def baidu_ocr_detect(self):
        res = self.baidu_ocr.detect()
        if res is None:
            print('BaiduOCR fail')
        else:
            print('BaiduOCR = ' + res)

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
