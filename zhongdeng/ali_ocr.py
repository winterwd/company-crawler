#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 2022-02-21
:desc: 阿里ocr
"""

import time
from typing import Optional
from zhongdeng import *
from alibabacloud_ocr_api20210707.client import Client as ocr_api20210707Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_darabonba_stream.client import Client as StreamClient
from alibabacloud_ocr_api20210707 import models as ocr_api_20210707_models

access_key_id = 'LTAI5tLRyog8Sd5CMscJn3FJ'
access_key_secret = 'jvXgy4HiaITL3WeomWXvHlmX8yshYd'


class AliOCR:

    def __init__(self):
        self.__count = 0
        self.__client = AliOCR.create_client()

    def detect(self, count: int = 1) -> Optional[str]:
        self.__count = count
        return self.__request_ocr()

    def __code_detect(self) -> Optional[str]:
        return self.__request_ocr()

    def __request_ocr(self) -> Optional[str]:

        body_stream = StreamClient.read_from_file_path(CODE_IMAGE_PATH)
        recognize_advanced_request = ocr_api_20210707_models.RecognizeAdvancedRequest(
            body=body_stream
        )

        result = self.__client.recognize_advanced(recognize_advanced_request)
        res = result.body.data
        res_dict = eval(res)
        print(res_dict)

        strx = res_dict['content']

        data = "".join(list(filter(str.isdigit, strx)))
        if len(data) == 4:
            return data
        else:
            self.__count -= 1
            if self.__count > 0:
                time.sleep(0.5)
                return self.__request_ocr()
            else:
                return None

    @staticmethod
    def create_client() -> ocr_api20210707Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'ocr-api.cn-hangzhou.aliyuncs.com'
        return ocr_api20210707Client(config)
