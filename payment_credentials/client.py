#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 2022/7/31
:desc: 识别付款回单，保存excel
"""

from util.ocr.tencent_ocr import TencentOCR
from util.ocr.baidu_ocr import BaiduOCR
from util.ocr.ali_ocr import AliOCR
from payment_credentials import PC_IMAGE_PATH
from payment_credentials import PC_OCR_RESULT_PATH
from payment_credentials import PC_OCR_EXCEL_PATH
from payment_credentials import PC_OCR_LOG_PATH
from payment_credentials import excel
from payment_credentials.model import Payment
from shutil import copyfile
from util import log
import os
import logging
import time
import re

log.set_file(PC_OCR_LOG_PATH)


class PaymentOCR:
    def __init__(self):
        self.index = 0
        self.files = []
        self.ocr_res = []
        self.ali_ocr = None
        self.baidu_ocr = None
        self.tencent_ocr = None

        # self.ali_ocr = AliOCR()
        # self.tencent_ocr = TencentOCR()
        self.baidu_ocr = BaiduOCR()

    def start(self):
        self.get_file_paths()
        self.ocr_detect()
        self.export_to_excel()

    def get_file_paths(self):
        files_dir = PC_IMAGE_PATH
        L = []
        for dir_path, dir_names, filenames in os.walk(files_dir):
            for file in filenames:
                if 'png' in file or 'jpg' in file:
                    L.append(os.path.join(dir_path, file))

        self.files = L

    def ocr_detect(self):
        logging.info('ocr file start...')
        index = min(self.index, len(self.files) - 1)
        file_paths = self.files[index:]

        ocr_result = []
        for i in range(len(file_paths)):
            path = file_paths[i]
            logging.info(f'ocr file: {path}, index:{i}')
            ocr_res: [] = self.fetch_ocr_result(path)

            if len(ocr_res) > 0:
                logging.info(f'ocr file success, index:{i}')
                ocr_result += ocr_res
            else:
                logging.error(f'ocr file fail, index:{i}, file:{path}')
                try:
                    # 将失败的文件存储
                    copyfile(path, path.replace('./', './error-'))
                except IOError as e:
                    print(f'Unable to copy file. {e}')

        self.ocr_res = ocr_result
        logging.info('ocr file completed...')

    def fetch_ocr_result(self, path):
        # self.ali_ocr.set_file_path(path)
        # ocr_res = self.ali_ocr.detect()

        self.baidu_ocr.set_file_path(path)
        items = self.baidu_ocr.detect()
        logging.info(f'ocr result: {items}')
        # QPS限制 2
        time.sleep(1)
        if items:
            return self.get_payment(items, path)
        return []

    @staticmethod
    def recognize_name(text_item):
        """
        识别付款人，收款人
        """
        temp = text_item
        if '账号：' in temp and '全称：' in temp:
            try:
                names = temp.split('账号：')[0]
                names = names.split('全称：')
                return names[1], names[2]
            except BaseException as e:
                logging.error(f'解析付款人，收款人 error. {e}')
                return '', ''

    @staticmethod
    def recognize_date(text_item):
        """
        识别付款交易时间
        """

        def str_insert(origin, pos, str_add):
            """
            指定位置插入 str_add
            """
            str_list = list(origin)  # 字符串转list
            str_list.insert(pos, str_add)  # 在指定位置插入字符串
            str_out = ''.join(str_list)  # 空字符连接
            return str_out

        temp = text_item
        if '交易时间：' in temp and '用途' in temp:
            try:
                date = temp.split('交易时间：')[1]
                date = date.split('用途')[0]
                date = date.replace('：', ':')
                # 2020-11-2613:13:12 > 2020-11-26 13:13:12
                date_temp = date
                date_temp = date_temp.split('-').pop()
                date_temp = date_temp.split(':')[0]
                new_date = str_insert(date_temp, 2, ' ')
                return date.replace(date_temp, new_date)
            except BaseException as e:
                logging.error(f'解析交易时间 error. {e}')
                return ''

    @staticmethod
    def recognize_amount(text_item):
        """
        识别付款金额
        """
        temp = text_item
        # if self.baidu_ocr:
        #     # baidu: '小写：30,000.00'
        #     temp = temp.replace(',', '').replace('.', '').replace('小写：', '')
        # elif self.ali_ocr:
        #     # ali '：30，000.00'
        #     temp = temp.replace('，', '').replace('.', '').replace('：', '')

        if '小写：' in temp and '：人民币' in temp:
            try:
                amount = temp.split('小写：')[1]
                amount = amount.split('：人民币')[0]
                amount = re.sub('[\u4e00-\u9fa5]', '', amount)
                return amount
            except BaseException as e:
                logging.error(f'解析交易金额 error. {e}')
                return ''

    @staticmethod
    def recognize_desc(text_item):
        """
        识别用途
        """
        temp = text_item
        if '用途：' in temp and '摘要' in temp:
            try:
                desc = temp.split('用途：')[1]
                desc = desc.split('摘要')[0]
                return desc
            except BaseException as e:
                logging.error(f'解析用途 error. {e}')
                return ''

    def get_payment(self, items: [str], path):
        payments: [Payment] = []

        text_items = "".join(str(item) for item in items).split('兴业银行汇款回单')
        text_items = [val for val in text_items if len(val) > 30]
        for text_item in text_items:
            try:
                payer, receiver = self.recognize_name(text_item)
                amount = self.recognize_amount(text_item)
                date = self.recognize_date(text_item)
                desc = self.recognize_desc(text_item)

                obj = Payment(date, receiver, payer, amount, desc, file=path)
                logging.info(obj.__str__())
                payments.append(obj)
            except BaseException as e:
                logging.error(f'解析 error. {e}')
        return payments

    def export_to_excel(self):
        logging.info('excel start...')

        objs: [Payment] = self.ocr_res
        if len(objs) > 0:
            excel.write(PC_OCR_EXCEL_PATH, objs)
            logging.info('excel end...')
        else:
            logging.info('excel no value...')


if __name__ == '__main__':
    logging.info('start...')
    PaymentOCR().start()
    logging.info("completed")
