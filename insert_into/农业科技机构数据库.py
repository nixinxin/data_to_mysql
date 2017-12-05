#!/usr/bin/python
# -*- coding:utf-8 -*-
import queue

import pymysql

__author__ = "xin nix"
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from pyquery import PyQuery as pq
import json
import re

import threading
import contextlib
import time

StopEvent = object()
conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()

qingqiucanshu = {
        '__VIEWSTATE': '''/ wEPDwUKLTMyODk2Nzk2Nw9kFgICAQ9kFggCAQ9kFgQCBQ8PFgIeBFRleHQFBueZu + W9lWRkAgcPFgIfAAXcBTx1bD48bGk + PGEgaHJlZj0iLi4vRGVmYXVsdC5hc3B4P01lbnVJZD0zNCIgdGFyZ2V0PSJfc2VsZiIgdGl0bGU9IummlumhtSIgY2xhc3M9IlNlbGVjdGVkIj7pppbpobU8L2E + PC9saT48bGk + PGEgaHJlZj0iLi4vRGF0YU1ldGEvU2VhcmNoTGlzdC5hc3B4P01lbnVJZD0zNiIgdGFyZ2V0PSJfc2VsZiIgdGl0bGU9IuWFg + aVsOaNriI + 5YWD5pWw5o2uPC9hPjwvbGk + PGxpPjxhIGhyZWY9Ii4uL0RhdGFUYWJsZS9TZWFyY2hMaXN0LmFzcHg / TWVudUlkPTM3IiB0YXJnZXQ9Il9zZWxmIiB0aXRsZT0i5pWw5o2uIj7mlbDmja48L2E + PC9saT48bGk + PGEgaHJlZj0i…gYeG1BhZ2VTcGxpdEJvdHRvbV90b3RhbFJlY29yZAK / Ax4YUGFnZVNwbGl0Qm90dG9tX2N1cnJQYWdlAgEeGFBhZ2VTcGxpdEJvdHRvbV9QYWdlU2l6ZQIKZBYCAgYPEGRkFgBkAg0PEGRkFgFmZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBgUgUGFnZVNwbGl0Qm90dG9tJEltYWdlQnV0dG9uRmlyc3QFHlBhZ2VTcGxpdEJvdHRvbSRJbWFnZUJ1dHRvblByZQUfUGFnZVNwbGl0Qm90dG9tJEltYWdlQnV0dG9uTmV4dAUfUGFnZVNwbGl0Qm90dG9tJEltYWdlQnV0dG9uTGFzdAUfUGFnZVNwbGl0Qm90dG9tJEltYWdlQnV0dG9uR290bwUkUGFnZVNwbGl0Qm90dG9tJEltYWdlQnV0dG9uR290b0NvdW50Zy6rm2KfWCoGzV2KIeAxhM / WnjLBQrvah0b3lDdSz88 =''',
        '__VIEWSTATEGENERATOR': '7B37A01C',
        '__EVENTVALIDATION': '/ wEdABCICeCvPq5dojeUznC6NAYjdd / LZ + E8u4j0WjnM8OIt9ylPoWxsDo8AHyruJ6 / EO3jNZs5DOkylD / xsi5Wzri / +dOaS6 + L64K2I / RjypYe1LAF7r1QOqZVl5ra7Evso46Dp72ZTX0uduvKZf3Rh6HzVPPXB + 9 V6mtWKAHDIgICY + Uw4svsZlq2PFdW7HAQNkExQADPJb9qk3dm65SRf1v / BU5 / YCCqOy6ltlKT6dPJ4Gjh4fKA2Ltrb2EAXDs / YPSDkZdCzDguI5q0eJt7oKyBil0a6EDy9Bq9cy6Il5gVgLDuUpDNy2SiL4sSws50u4KexM / Y5NC6d07Sbkq1EubGFeHHmV5pKMhb1heedN5rQKHJ0tWKsjfPIcZX2dDpFUQw =',
        'PageSplitBottom$textBoxPageSize': '1',
        'DropDownListRowCount': '50',
    }
headers = {
    'Host':	'stb.agridata.cn',
    'Proxy-Connection': 'keep-alive',
    'Content-Length': '82',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://stb.agridata.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://stb.agridata.cn/Site/DataTable/List.aspx?DataCategoryGId=3d8af79e-d8ab-40ff-8f55-a1f11afad890',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'ASP.NET_SessionId=stcujiyxlxprvdpz0pc2fh3j',
}
url = "http://stb.agridata.cn/Site/DataTable/List.aspx?DataCategoryGId=3d8af79e-d8ab-40ff-8f55-a1f11afad890"
# driver = webdriver.Firefox()
# driver.get(url)
sql = """INSERT INTO `myprojects`.`农业科技机构数据库`(`机构编号`, `规范名称`, `英文名称`, `其他名称`, `成立年份`,
 `机构类型`, `所在地区`, `上级单位`, `机构简介`, `英文简介`, `研究领域`, `学科分类`, `人才队伍`, `机构设置`, `科技平台`,
 `主要成果`, `主办期刊`, `通讯地址`, `邮政编码`, `联系电话`, `电子邮箱`, `传真`, `网址`)
  VALUES ("{0}", "{1}", "{2}", "{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}","{14}","{15}","{16}","{17}","{18}","{19}","{20}","{21}","{22}") on duplicate KEY UPDATE `机构编号`=VALUES (`机构编号`)"""
a = 0
# sql = """INSERT INTO `myprojects`.`农业科技机构数据库`(`{0}`, `{1}`, `{2}`, `{3}`, `{4}`,
#  `{5}`, `{6}`, `{7}`, `{8}`, `{9}`, `{10}`, `{11}`, `{12}`, `{13}`, `{14}`,
#  `{15}`, `{16}`, `{17}`, `{18}`, `{19}`, `{20}`, `{21}`, `{22}`)
#   VALUES ("{23}", "{24}", "{25}", "{26}","{27}","{28}","{29}","{30}","{31}","{32}","{33}","{34}","{35}","{36}","{37}","{38}","{39}","{40}","{41}","{42}","{43}","{44}","{45}") on duplicate KEY UPDATE `机构编号`=VALUES (`机构编号`)"""
aaa = []

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
driver.get(url)
htmls = pq(driver.page_source).find(".ListContent1.EllipsisTable  a").items()
errors = []
# driver.find_element_by_css_selector("#DropDownListRowCount > option:nth-child(3)").click()
for j in range(1, 46):
    if j >= 1:
        num = 1
        for i in htmls:
            num += 1
            driver.find_element_by_css_selector(".ListContent1 > tbody:nth-child(1) > tr:nth-child({}) > td:nth-child(2) > a".format(num)).click()
            key = driver.find_element_by_css_selector(".ListContent1 > tbody:nth-child(1) > tr:nth-child({}) > td:nth-child(3)".format(num)).text
            now_handle = driver.current_window_handle
            all_handles = driver.window_handles
            driver.switch_to.window(all_handles[-1])
            data = driver.page_source
            data = pq(data).find("#form1 > div.Box10.ClearFloat > div.Box77.FloatLeft.MarginLeft10 > div > table > tbody > tr")
            # print(data)
            content = data.items()
            insert_data = []
            for k in content:
                values = k.find('td').text().replace("\xa0", "").replace("\xa01", "").replace("\xa04", "").replace("\xa02", "").replace("\ua004", "").replace("\xa03", "").replace("\xa025", "")
                values = values.replace("\ue0043", "").replace("\ue0042", "").replace("\ue0044", "").replace("\ue0045", "").replace("\ue0046", "")
                insert_data.append(values)
            try:
                # print(insert_data)
                result = curser.execute(sql.format(*insert_data))
                conn.commit()
                print(result, insert_data)
            except Exception as e:
                print(e)
                errors.append(key)
                assert input()
            driver.close()
            driver.switch_to.window(now_handle)
    if j <= 44:
            driver.find_element_by_css_selector("#PageSplitBottom_ImageButtonNext").click()
            # driver.find_element_by_css_selector("#DropDownListRowCount > option:nth-child(3)").click()
            htmls = pq(driver.page_source).find(".ListContent1.EllipsisTable  a").items()