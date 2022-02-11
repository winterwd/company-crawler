#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: albert
:date: 03/08/2019
"""
import sys
sys.path.append('..')

TycQueryApi = "https://api9.tianyancha.com/services/v3/search/sNorV3/{q}"
TycPortraitApi = "https://api9.tianyancha.com/services/v3/t/common/baseinfoV5/{eid}"

""" 请求验证头 """
AUTHORIZATION = '0###oo34J0XLKLJm7K1c70TKF4c9hN2k###1644462918014###a65bff35590f2c8b5d745538132d70b6'
""" 请求token """
X_AUTH_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzI2NTc1ODc2NiIsImlhdCI6MTY0NDQ2Mjk2OSwiZXhwIjoxNjQ3MDU0OTY5fQ.uCSaDG3QL3WWYH9ITQPXTNhLqqwk4o022t4RBw9P53vX8CFnhUCxDCzv7SmO2wPK8x2EhV3kQut8Dkm4VyNstg"
""" 天眼查头信息 """
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.18(0x1800122a) NetType/WIFI Language/zh_CN",
    "version": "TYC-XCX-WX",
    "Host": "api9.tianyancha.com",
    "Connection": "keep-alive",
    "content-type": "application/json",
    "Authorization": AUTHORIZATION,
    'x-auth-token': X_AUTH_TOKEN,
}