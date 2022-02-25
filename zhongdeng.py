#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from aip import AipOcr

driver = webdriver.Chrome()
code_image = './logs/zhongdeng/code_img.png'


def code_detect(count:int):
    APP_ID = '25623390'
    API_KEY = '0YhViGc9p3fhGa6ZZBOzoxf0'
    SECRET_KEY = 'jtXgDnGCDWhYmMlHOec5G7bMG0pMvbj0'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    image = open(code_image, 'rb').read()

    # 定义参数变量
    options = {}
    # 定义图像方向
    options['detect_direction'] = 'true'

    # 调用通用文字识别接口
    # res=client.basicGeneral(image, options) #普通
    res = client.basicAccurate(image, options)  # 高精度

    # 将所有的文字都合并到一起
    strx = ""
    for tex in res["words_result"]:  # 遍历结果
        strx += tex["words"]  # 每一行

    data = "".join(list(filter(str.isdigit, strx)))
    if len(data) == 4:
        return data
    else:
        if count > 0:
            code_detect(count-1)
        else:
            return ""

def ocr_code() -> str:
    check_img = driver.find_element(By.ID, "checkImg")

    times = 0
    while True:
        check_img.screenshot(code_image)
        time.sleep(0.2)

        data = code_detect(20)
        print('ocr_code = ' + data)

        # 中登网验证码是4位
        if len(data) == 4:
            return data
        else:
            check_img.click()
            time.sleep(1)
            times += 1
            print("验证码识别失败，重试第{}次".format(times))
            if times == 20:
                return ""

def is_element_present(how, what):
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True

def login_ocr_submit(count: int):
    code = ocr_code()

    usercode = driver.find_element(By.ID, "usercode")
    usercode.clear()
    usercode.send_keys('winterwd')

    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys('Qazxsw1!')

    verifyCode = driver.find_element(By.ID, "verifyCode")
    verifyCode.clear()
    verifyCode.send_keys(code)

    loginButton = driver.find_element(By.ID, "btn_login")
    loginButton.click()
    time.sleep(1)

    if is_element_present(By.ID, "sendCode"):
        sendCode = driver.find_element(By.ID, "sendCode")
        sendCode.click()

        dynamicCode = driver.find_element(By.ID, "dynamicCode")
        mbNumber = driver.find_element(By.ID, "mbNumberAlert").value
        dynamic_code = input("请输入" + mbNumber + "验证码")
        if len(dynamic_code) > 0:
            dynamicCode.click()
    else:
        if count > 0:
            login_ocr_submit(count - 1)
        else:
            print("验证码识别校验失败!")
            driver.quit()


def zhongdeng_login():
    driver.get("https://www.zhongdengwang.org.cn/")
    time.sleep(1)
    login_ocr_submit(10)


if __name__ == '__main__':
    # zhongdeng_login()
    # 微信小程序可以查询10次


