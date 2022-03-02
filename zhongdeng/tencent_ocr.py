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
import time
from typing import Optional
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models
from tencentcloud.ocr.v20181119.models import TextDetection
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

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

    def detect(self, count: int = 1) -> Optional[str]:
        self.__count = count
        return self.__code_detct()

    def __code_detct(self) -> Optional[str]:
        image = open(CODE_IMAGE_PATH, 'rb').read()
        image_base64 = base64.b64encode(image).decode()
        return self.__request_ocr(image_base64)

    def __request_ocr(self, image) -> Optional[str]:

        req = models.GeneralHandwritingOCRRequest()
        params = {
            "ImageBase64": image
        }
        req.from_json_string(json.dumps(params))

        try:
            resp = self.__client.GeneralAccurateOCR(req)
            print(resp.to_json_string())

            if len(resp.TextDetections) > 0:
                detectedText: TextDetection = resp.TextDetections[0]
                strx = detectedText.DetectedText
                data = "".join(list(filter(str.isdigit, strx)))

                if len(data) == 4:
                    return data
                else:
                    return None
        except TencentCloudSDKException as e:
            return None

