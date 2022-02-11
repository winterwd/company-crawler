#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 02/10/2022
:desc: excel生成工具类
"""

import os
import xlwings as xw
from db.models import Company

class CellItem(object):
    def __init__(self, src:Company=None):
        if not src:
            self.keyword = '关键词'
            self.short_name = '企业简称'
            self.name = '企业名称'
            self.company_area = '所属区域'
            self.company_address = '联系地址'
            self.contact = '联系方式'
            self.representative = '企业法人'
            self.biz_status = '经营状态'
            self.found_time = '成立时间'
            self.tags = '标签列表'
            self.industry = '行业分类'
        else:
            self.keyword = src.keyword
            self.short_name = src.short_name
            self.name = src.name
            self.company_area = src.province + src.city + src.district
            self.company_address = src.company_address
            self.contact = src.contact
            self.representative = src.representative
            self.biz_status = src.biz_status
            self.found_time = src.found_time
            self.tags = ','.join(src.tags)
            self.industry = src.industry

    def values(self):
        return [
            self.keyword,
            self.short_name,
            self.name,
            self.company_area,
            self.company_address,
            self.contact,
            self.representative,
            self.biz_status,
            self.found_time,
            self.tags,
            self.industry,
        ]

def write(file_path: str, value: list[Company]):
    if not file_path:
        return

    if not value:
        return

    header = CellItem()
    cell_list = [header.values()]

    for company in value:
        item = CellItem(company)
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