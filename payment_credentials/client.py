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
                logging.error(f'ocr fail, index:{i}, file:{path}')
                try:
                    # 将失败的文件存储
                    copyfile(path, path.replace('./', './error-'))
                except IOError as e:
                    print(f'Unable to copy file. {e}')

        self.ocr_res = ocr_result
        logging.info('ocr completed...')

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
    def recognize_name(pre_name, text):
        """
        识别付款人，收款人
        """
        # '全称：深圳市星锐实业发展有限公司全'
        # '全称：深圳市星锐实业发展有限公司账'
        full_name = (pre_name + text)
        if '全称：' in full_name:
            names = full_name.split('全称：')
            if len(names) < 2:
                return False, None
            name = names[1]
            if len(name) > 0 and name not in text:
                # 此处text 不包含name
                if '全' in text:
                    # '全'：第一个name截止
                    name = name.split('全')[0]
                    return True, name
                elif '账' in text:
                    # '账'：第二个name截止
                    name = name.split('账')[0]
                    return True, name
        return False, None

    def recognize_time(self, text):
        """
        识别付款交易时间
        """
        # '交易时间：2021-01-2214：25：44'
        # '：2021-01-2214：25：44'
        if '交易时间：' in text:
            text = text.replace('交易时间：', '')

        temp = text
        temp = temp.replace('-', '').replace(':', '').replace('：', '')
        is_time = temp != text and temp.isdigit()
        if not is_time:
            return False, None

        temp = text
        # 2020-11-2613：13：12
        temp = temp.split('-').pop()
        if '：' in temp:
            temp = temp.split('：')[0]
        elif ':' in temp:
            temp = temp.split(':')[0]
        new_temp = self.str_insert(temp, 2, ' ')
        # 2020-11-26 13:13:12
        time = text.replace('：', ':').replace(temp, new_temp)
        return True, time

    def recognize_amount(self, text):
        """
        识别付款金额
        """
        temp = text
        if self.baidu_ocr:
            # baidu: '小写：30,000.00'
            temp = temp.replace(',', '').replace('.', '').replace('小写：', '')
        elif self.ali_ocr:
            # ali '：30，000.00'
            temp = temp.replace('，', '').replace('.', '').replace('：', '')
        is_amount = temp != text and temp.isdigit()
        if not is_amount:
            return False, None

        temp = text
        # ali '：30，000.00'
        # baidu: '小写：30,000.00'
        amount = temp.replace(',', '').replace('，', '').split('：')[1]
        return True, amount

    @staticmethod
    def recognize_desc(text):
        """
        识别用途
        """
        temp = text
        if '途：' in temp:
            # '用', '途：客房饰品定金'
            desc = temp.split('：')[1]
            if len(desc) > 0:
                return True, desc
        return False, None

    def get_payment(self, items: [str], path):
        payments: [Payment] = []

        time_ = None
        payer = None
        receiver = None
        amount = None
        desc = None

        pre_name = ''
        for text in items:
            temp = text
            is_name, name_text = self.recognize_name(pre_name, temp)
            is_amount, amount_text = self.recognize_amount(temp)
            is_time, time_text = self.recognize_time(temp)
            is_desc, desc_text = self.recognize_desc(pre_name+temp)

            if payer and receiver:
                if not desc_text:
                    pre_name = text
                pass
            else:
                # 记录上一次的内容
                pre_name += text

            if is_name:
                if not payer:
                    payer = name_text
                elif not receiver:
                    receiver = name_text
                # 识别到一个name，重置
                pre_name = text
            elif is_time:
                time_ = time_text
            elif is_amount:
                amount = amount_text
            elif is_desc:
                desc = desc_text

            # 一组数据识别完成
            if time_ and payer and receiver and amount and desc:
                payments.append(Payment(time_, receiver, payer, amount, desc, file=path))
                time_ = None
                payer = None
                receiver = None
                amount = None
                desc = None
                pre_name = ''

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
