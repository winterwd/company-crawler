#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 2022-02-21
:desc: 百度ocr https://console.bce.baidu.com/ai/?fromai=1#/ai/ocr/app/list
"""

from typing import Optional
from aip import AipOcr

APP_ID = 'xxx'
API_KEY = 'xxx'
SECRET_KEY = 'xxx'


class BaiduOCR:

    def __init__(self, ocr_file_path=None):
        self.__count = 0
        self.__file_path = ocr_file_path
        self.__client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    def set_file_path(self, file=None):
        self.__file_path = file

    def detect(self, count: int = 1):
        self.__count = count
        return self.__code_detect()

    def __code_detect(self):
        if not self.__file_path:
            return None

        image = open(self.__file_path, 'rb').read()
        return self.__request_ocr(image)

    def __request_ocr(self, image):
        # 定义图像方向
        options = {'detect_direction': 'true'}
        res = self.__client.basicAccurate(image, options)  # 高精度
        print(f'baidu_ocr result: {res}')

        # 将所有的文字都合并到一起
        str_x = []
        for tex in res.get("words_result", []):  # 遍历结果
            words = tex.get('words')
            if words:
                str_x.append(words)

        return str_x
