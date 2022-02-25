#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 2022-02-21
:desc: 阿里ocr
"""
from zhongdeng import *
from typing import List
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

    def detect(self, count: int) -> str:
        self.__count = count
        return self.__code_detect()

    def __code_detect(self) -> str:

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

    def __request(self, args: List[str]) -> str:
        body_stream = StreamClient.read_from_file_path(CODE_IMAGE_PATH)
        recognize_advanced_request = ocr_api_20210707_models.RecognizeAdvancedRequest(
            body=body_stream
        )

        result = self.__client.recognize_advanced(recognize_advanced_request)

    async def __request_async(self, args: List[str]) -> None:
        body_stream = StreamClient.read_from_file_path(CODE_IMAGE_PATH)
        recognize_advanced_request = ocr_api_20210707_models.RecognizeAdvancedRequest(
            body=body_stream
        )

        result = await self.__client.recognize_advanced_async(recognize_advanced_request)
