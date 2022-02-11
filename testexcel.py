#!/usr/bin/python3
# -*-: coding: utf-8 -*-
"""
:author: winter
:date: 02/10/2022
"""

from util import excel
from db.models import Company

if __name__ == '__main__':

    companies = []

    for i in range(3):
        item = Company()
        item.keyword = 'keyword'
        item.short_name = '企业简称' + str(i)
        item.name = '企业名称' + str(i)
        item.province = '所属区域' + str(i)
        item.city = '所属区域' + str(i)
        item.district = '所属区域' + str(i)
        item.company_address = '联系地址' + str(i)
        item.contact = '联系方式' + str(i)
        item.representative = '企业法人' + str(i)
        item.biz_status = '经营状态' + str(i)
        item.found_time = '成立时间' + str(i)
        item.tags = ['标签列表' + str(i),'标签列表' + str(i)]
        item.industry = '行业分类' + str(i)

        companies.append(item)

    excel.write("./logs/tianyancha.xlsx", companies)