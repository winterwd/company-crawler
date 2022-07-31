#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 02/10/2022
:desc: excel生成工具类
"""

import os
import xlwings as xw
from payment_credentials.model import Payment


class CellItem(object):
    def __init__(self, src: Payment = None):
        if not src:
            self.time = '付款时间'
            self.payer = '付款人'
            self.receiver = '收款人'
            self.amount = '金额'
            self.desc = '用途'
            self.file = '图片'
        else:
            self.time = src.time
            self.payer = src.payer
            self.receiver = src.receiver
            self.amount = src.amount
            self.desc = src.desc
            self.file = src.file

    def values(self):
        return [
            '',
            self.time,
            self.payer,
            self.receiver,
            self.amount,
            self.desc,
            self.file
        ]


def write(file_path: str, value: list[Payment]):
    if not file_path:
        return

    if not value:
        return

    header = CellItem()
    cell_list = [header.values()]

    for payment in value:
        item = CellItem(payment)
        cell_list.append(item.values())

    app = xw.App(visible=True, add_book=False)

    wb = None
    sht = None
    if os.path.exists(file_path):
        wb = app.books.open(file_path)
        # wb = xw.Book(file_path)

        # new sheet
        wb.sheets.add()
        sht = wb.sheets[0]
    else:
        wb = app.books.add()
        wb.save(file_path)
        sht = wb.sheets[0]

    if not wb or not sht:
        return

    sht.range('A1').expand('table').value = cell_list
    wb.save()
    wb.close()
    app.quit()
