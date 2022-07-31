#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 2022-02-21
:desc: 阿里ocr https://ocr.console.aliyun.com/overview?accounttraceid=6d6ab52558af48e5a1232c6545140de8tlvd
"""

import time
from typing import Optional
from alibabacloud_ocr_api20210707.client import Client as ocr_api20210707Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_darabonba_stream.client import Client as StreamClient
from alibabacloud_ocr_api20210707 import models as ocr_api_20210707_models

access_key_id = 'xxx'
access_key_secret = 'xxx'


class AliOCR:

    def __init__(self, ocr_file_path=None):
        self.__count = 0
        self.__client = AliOCR.create_client()
        self.__file_path = ocr_file_path

    def set_file_path(self, file=None):
        self.__file_path = file

    def detect(self, count: int = 1):
        self.__count = count
        return self.__request_ocr()

    def __code_detect(self):
        return self.__request_ocr()

    def __request_ocr(self):
        if not self.__file_path:
            return None

        body_stream = StreamClient.read_from_file_path(self.__file_path)
        recognize_advanced_request = ocr_api_20210707_models.RecognizeAdvancedRequest(
            body=body_stream
        )

        result = self.__client.recognize_advanced(recognize_advanced_request)
        res = result.body.data
        res_dict = eval(res)
        print(f'ali_ocr result: {res_dict}')

        if not res_dict:
            self.__count -= 1
            if self.__count > 0:
                time.sleep(0.5)
                return self.__request_ocr()
            else:
                return None
        return res_dict.get('content', '').split(' ')

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
