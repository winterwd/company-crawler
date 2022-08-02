#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:file: model.py
:date: 2022/7/31
:desc: 
"""


class Payment(object):
    def __init__(self, date='', receiver='', payer='', amount='', desc='', file=''):
        self.date = date
        self.receiver = receiver
        self.payer = payer
        self.amount = amount
        self.desc = desc
        self.file = file

    def __str__(self):  # 定义打印对象时打印的字符串
        return "".join(str(item) for item in (
            '交易时间：',
            self.date,
            ' 付款人：',
            self.payer,
            ' 收款人：',
            self.receiver,
            ' 金额：',
            self.amount,
            ' 备注：',
            self.desc))
