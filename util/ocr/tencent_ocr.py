#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 2022-02-21
:desc: 腾讯ocr https://console.cloud.tencent.com/ocr/overview
"""

import json
import base64
import time
from typing import Optional
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models
from tencentcloud.ocr.v20181119.models import TextDetection
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

SecretId = 'xxx'
SecretKey = 'xxx'


class TencentOCR:

    def __init__(self, ocr_file_path=None):
        self.__count = 0
        self.__file_path = ocr_file_path

        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        self.__client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)

    def set_file_path(self, file=None):
        self.__file_path = file

    def detect(self, count: int = 1) -> Optional[dict]:
        self.__count = count
        return self.__code_detect()

    def __code_detect(self) -> Optional[dict]:
        if not self.__file_path:
            return None

        image = open(self.__file_path, 'rb').read()
        image_base64 = base64.b64encode(image).decode()
        return self.__request_ocr(image_base64)

    def __request_ocr(self, image) -> Optional[dict]:

        req = models.GeneralAccurateOCRRequest()
        params = {
            "ImageBase64": image
        }
        req.from_json_string(json.dumps(params))

        try:
            resp = self.__client.GeneralAccurateOCR(req)
            res_str = resp.to_json_string()
            print(f'tencent_ocr result: {resp}')

            if not res_str:
                self.__count -= 1
                if self.__count > 0:
                    time.sleep(0.5)
                    return self.__request_ocr(image)
                else:
                    return None
            return res_str
        except TencentCloudSDKException as e:
            return None

