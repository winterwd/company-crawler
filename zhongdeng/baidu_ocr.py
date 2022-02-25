#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 2022-02-21
:desc: 百度ocr
"""

import time
from typing import Optional

from aip import AipOcr
from zhongdeng import *

APP_ID = '25623390'
API_KEY = '0YhViGc9p3fhGa6ZZBOzoxf0'
SECRET_KEY = 'jtXgDnGCDWhYmMlHOec5G7bMG0pMvbj0'


class BaiduOCR:

    def __init__(self):
        self.__count = 0
        self.__client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    def detect(self, count: int) -> str:
        self.__count = count
        return self.__code_detect()

    def __code_detect(self) -> Optional[str]:
        image = open(CODE_IMAGE_PATH, 'rb').read()
        return self.__requset(image)

    def __requset(self, image) -> Optional[str]:
        # 定义图像方向
        options = {'detect_direction': 'true'}
        res = self.__client.basicAccurate(image, options)  # 高精度

        # 将所有的文字都合并到一起
        strx = ""
        for tex in res["words_result"]:  # 遍历结果
            strx += tex["words"]  # 每一行

        data = "".join(list(filter(str.isdigit, strx)))
        if len(data) == 4:
            return data
        else:
            if self.__count > 0:
                time.sleep(0.5)
                self.__count -= 1
                self.__requset(image)
            else:
                return None
