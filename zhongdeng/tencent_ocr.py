#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 2022-02-21
:desc: 腾讯ocr
"""
from zhongdeng import *
import json
import base64
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models

SecretId = 'AKIDmOlrhHbeQwCBtVrxlJbcMp2ye4IGwLTL'
SecretKey = 'cx1pLaYGhsnBJCpBH6evwgAOL3UeXAWb'


class TencentOCR:

    def __init__(self):
        self.__count = 0

        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        self.__client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)

    def detect(self, count: int) -> str:
        self.__count = count
        return self.__code_detct()

    def __code_detct(self) -> str:
        image = open(CODE_IMAGE_PATH, 'rb').read()
        image_base64 = base64.b64encode(image).decode()

        req = models.GeneralAccurateOCRRequest()
        params = {
            "ImageBase64": image_base64
        }
        req.from_json_string(json.dumps(params))
        return self.__request(req)

    def __request(self, request) -> str:
        resp = self.__client.GeneralAccurateOCR(request)
        result = resp.to_json_string()
        print(result)
