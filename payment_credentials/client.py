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
from util import log
import os
import logging

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
                L.append(os.path.join(dir_path, file))

        self.files = L

    def ocr_detect(self):
        logging.info('ocr start...')

        index = min(self.index, len(self.files) - 1)
        file_paths = self.files[index:]

        ocr_result = []
        for i in range(len(file_paths)):
            path = file_paths[i]
            logging.info(f'ocr file: {path}, index:{i}')
            ocr_res: [] = self.fetch_ocr_result(path)

            if len(ocr_res) > 0:
                logging.info(f'ocr success, index:{i}')
                ocr_result += ocr_res
            else:
                logging.error(f'ocr fail, index:{i}')

        self.ocr_res = ocr_result
        logging.info('ocr completed...')

    def fetch_ocr_result(self, path):
        # self.ali_ocr.set_file_path(path)
        # ocr_res = self.ali_ocr.detect()

        self.baidu_ocr.set_file_path(path)
        items = self.baidu_ocr.detect()
        logging.info(f'ocr result: {items}')
        if items:
            return self.get_payment(items, path)
        return []

    def get_payment(self, items: [str], path):
        payments: [Payment] = []

        time = None
        payer = None
        receiver = None
        amount = None
        desc = None

        pre_name = ''
        for text in items:
            temp = text

            is_time = temp.replace('-', '').replace(':', '').replace('：', '')
            is_time = is_time != text and is_time.isdigit()

            is_amount = False
            if self.baidu_ocr:
                # baidu: '小写：30,000.00'
                is_amount = temp.replace(',', '').replace('.', '').replace('小写：', '')
            elif self.ali_ocr:
                # ali '：30，000.00'
                is_amount = temp.replace('，', '').replace('.', '').replace('：', '')
            is_amount = is_amount != text and is_amount.isdigit()

            company_name = (pre_name + text)
            if '全' in text:
                # 记录公司名标识
                pre_name = text

            if '全称：' in company_name:
                has_name = len(company_name.split('：')) > 1
                if not has_name:
                    # pre_name: '全', text: '称：'
                    break

                pre_name = ''
                # '全称：深圳市星锐实业发展有限公'
                name: str = temp
                if '：' in name:
                    name = name.split('：')[1]
                elif ':' in name:
                    name = name.split(':')[1]

                if not payer:
                    payer = name
                elif not receiver:
                    receiver = name

            elif is_time:
                # 2020-11-2613：13：12
                temp = temp.split('-').pop()
                if '：' in temp:
                    temp = temp.split('：')[0]
                elif ':' in temp:
                    temp = temp.split(':')[0]
                new_temp = self.str_insert(temp, 2, ' ')
                # 2020-11-26 13:13:12
                time = text.replace('：', ':').replace(temp, new_temp)
            elif is_amount:
                # ali '：30，000.00'
                # baidu: '小写：30,000.00'
                amount = text.replace(',', '').replace('，', '').split('：')[1]
            elif '途：' in temp:
                # '用', '途：客房饰品定金'
                desc = temp.split('：')[1]

            # 一组数据识别完成
            if time and payer and receiver and amount and desc:
                payments.append(Payment(time, receiver, payer, amount, desc, file=path))
                time = None
                payer = None
                receiver = None
                amount = None
                desc = None

        return payments

    def export_to_excel(self):
        logging.info('excel start...')

        objs: [Payment] = self.ocr_res
        if len(objs) > 0:
            excel.write(PC_OCR_EXCEL_PATH, objs)
            logging.info('excel end...')
        else:
            logging.info('excel no value...')

    @staticmethod
    def str_insert(origin, pos, str_add):
        """
        指定位置插入 str_add
        """
        str_list = list(origin)  # 字符串转list
        str_list.insert(pos, str_add)  # 在指定位置插入字符串
        str_out = ''.join(str_list)  # 空字符连接
        return str_out


if __name__ == '__main__':
    logging.info('start...')
    PaymentOCR().start()
    logging.info("completed")
