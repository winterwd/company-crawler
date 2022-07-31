#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:file: model.py
:date: 2022/7/31
:desc: 
"""


class Payment(object):
    def __init__(self, time='', receiver='', payer='', amount='', desc='', file=''):
        self.time = time
        self.receiver = receiver
        self.payer = payer
        self.amount = amount
        self.desc = desc
        self.file = file
