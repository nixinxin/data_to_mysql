#!/usr/bin/python
# -*- coding:utf-8 -*-
import json

import pymysql
import requests
import time
from selenium import webdriver
from fake_useragent import UserAgent
__author__ = "xin nix"
# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pyquery import PyQuery as pq
html = """"""

qingqiucanshu = {
        '__VIEWSTATE': '''/ wEPDwUKLTMyODk2Nzk2Nw9kFgICAQ9kFggCAQ9kFgQCBQ8PFgIeBFRleHQFBueZu + W9lWRkAgcPFgIfAAXcBTx1bD48bGk + PGEgaHJlZj0iLi4vRGVmYXVsdC5hc3B4P01lbnVJZD0zNCIgdGFyZ2V0PSJfc2VsZiIgdGl0bGU9IummlumhtSIgY2xhc3M9IlNlbGVjdGVkIj7pppbpobU8L2E + PC9saT48bGk + PGEgaHJlZj0iLi4vRGF0YU1ldGEvU2VhcmNoTGlzdC5hc3B4P01lbnVJZD0zNiIgdGFyZ2V0PSJfc2VsZiIgdGl0bGU9IuWFg + aVsOaNriI + 5YWD5pWw5o2uPC9hPjwvbGk + PGxpPjxhIGhyZWY9Ii4uL0RhdGFUYWJsZS9TZWFyY2hMaXN0LmFzcHg / TWVudUlkPTM3IiB0YXJnZXQ9Il9zZWxmIiB0aXRsZT0i5pWw5o2uIj7mlbDmja48L2E + PC9saT48bGk + PGEgaHJlZj0i…gYeG1BhZ2VTcGxpdEJvdHRvbV90b3RhbFJlY29yZAK / Ax4YUGFnZVNwbGl0Qm90dG9tX2N1cnJQYWdlAgEeGFBhZ2VTcGxpdEJvdHRvbV9QYWdlU2l6ZQIKZBYCAgYPEGRkFgBkAg0PEGRkFgFmZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBgUgUGFnZVNwbGl0Qm90dG9tJEltYWdlQnV0dG9uRmlyc3QFHlBhZ2VTcGxpdEJvdHRvbSRJbWFnZUJ1dHRvblByZQUfUGFnZVNwbGl0Qm90dG9tJEltYWdlQnV0dG9uTmV4dAUfUGFnZVNwbGl0Qm90dG9tJEltYWdlQnV0dG9uTGFzdAUfUGFnZVNwbGl0Qm90dG9tJEltYWdlQnV0dG9uR290bwUkUGFnZVNwbGl0Qm90dG9tJEltYWdlQnV0dG9uR290b0NvdW50Zy6rm2KfWCoGzV2KIeAxhM / WnjLBQrvah0b3lDdSz88 =''',
        '__VIEWSTATEGENERATOR': '7B37A01C',
        '__EVENTVALIDATION': '/ wEdABCICeCvPq5dojeUznC6NAYjdd / LZ + E8u4j0WjnM8OIt9ylPoWxsDo8AHyruJ6 / EO3jNZs5DOkylD / xsi5Wzri / +dOaS6 + L64K2I / RjypYe1LAF7r1QOqZVl5ra7Evso46Dp72ZTX0uduvKZf3Rh6HzVPPXB + 9 V6mtWKAHDIgICY + Uw4svsZlq2PFdW7HAQNkExQADPJb9qk3dm65SRf1v / BU5 / YCCqOy6ltlKT6dPJ4Gjh4fKA2Ltrb2EAXDs / YPSDkZdCzDguI5q0eJt7oKyBil0a6EDy9Bq9cy6Il5gVgLDuUpDNy2SiL4sSws50u4KexM / Y5NC6d07Sbkq1EubGFeHHmV5pKMhb1heedN5rQKHJ0tWKsjfPIcZX2dDpFUQw =',
        'PageSplitBottom$textBoxPageSize': "{}",
        'DropDownListRowCount': '50',
    }
headers = {
    'Host':	'stb.agridata.cn',
    'Proxy-Connection': 'keep-alive',
    'Content-Length': '82',
    'Cache-Control': 'max-age=0',
    'User-Agent': getattr(UserAgent(), 'random'),
    'Upgrade-Insecure-Requests': "{}",
    'Origin': 'http://stb.agridata.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://stb.agridata.cn/Site/DataTable/List.aspx?DataCategoryGId=3d8af79e-d8ab-40ff-8f55-a1f11afad890',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'ASP.NET_SessionId=stcujiyxlxprvdpz0pc2fh3j',
}
# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = '农作物名、优、特新品种数据库'

    # 表的结构:
    # category = Column(String(128),  name="作物种类")
    # brands = Column(String(128), name="作物品种")
    # name = Column(String(128), name="品种名称", primary_key=True)
    # desc = Column(String(4), name="基本情况")
    # feature = Column(String(4), name="特征特性")
    # mader = Column(String(255), name="培育者")
    # location = Column(String(4), name="地区及技术")
    # brands_cate = Column(String(128), name="品种类别")
    # test = Column(String(255), name="审定情况")
    # caiji = Column(String(10), name="资源采集日")
    category = Column(String(128))
    brands = Column(String(128))
    name = Column(String(128), primary_key=True)
    desc = Column(String(4))
    feature = Column(String(4))
    mader = Column(String(255))
    location = Column(String(4))
    brands_cate = Column(String(128))
    test = Column(String(255))
    caiji = Column(String(10))

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()
# 初始化数据库连接:
# engine = create_engine('mysql+mysqldb://root:123456@localhost:3306/myprojects?charset=utf8')

# Base.metadata.create_all(engine)

# 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)
# 创建session对象:

# session = DBSession()
# 创建新User对象:
from selenium.common.exceptions import  TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


a = 0
url = "http://stb.agridata.cn/Site/DataTable/List.aspx?DataCategoryGId=0180539b-98ab-43af-a76c-83362df4c25d"
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
driver.get(url)
htmls = pq(driver.page_source).find(".ListContent1.EllipsisTable  a").items()
errors = []
driver.find_element_by_css_selector("#DropDownListRowCount > option:nth-child(3)").click()
for j in range(1, 62):
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
                sql = """INSERT INTO `myprojects`.`农作物名、优、特新品种数据库`(`作物种类`, `作物品种`, `品种名称`, `基本情况`, `特征特性`, `培育者`, `地区及技术`, `品种类别`, `审定情况`, `资源采集日`) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}") on duplicate key update `作物种类`= VALUES (`作物种类`)"""
                result = curser.execute(sql.format(*insert_data))
                conn.commit()
                print(result, insert_data)
            except Exception as e:
                print(e)
                errors.append(key)
            driver.close()
            driver.switch_to.window(now_handle)
    if j <= 60:
        driver.find_element_by_css_selector("#PageSplitBottom_ImageButtonNext").click()
        # driver.find_element_by_css_selector("#DropDownListRowCount > option:nth-child(3)").click()
        htmls = pq(driver.page_source).find(".ListContent1.EllipsisTable  a").items()
with open("errors.json", 'w', encoding='utf-8') as f:
    f.write(json.dumps(errors))