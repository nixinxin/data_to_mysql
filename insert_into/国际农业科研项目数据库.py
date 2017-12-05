#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"

import json
import pymysql
import requests
import time
from selenium import webdriver
from pyquery import PyQuery as pq

from selenium.common.exceptions import  TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#  on duplicate key update `疾病名称`= VALUES (`疾病名称`)
conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()
a = 0
url = "http://stb.agridata.cn/Site/DataTable/List.aspx?DataCategoryGId=0f00d72a-74f8-49f5-8e74-5ef43fc20724"
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
driver.get(url)
htmls = pq(driver.page_source).find(".ListContent1.EllipsisTable  a").items()
errors = []

# driver.find_element_by_css_selector("#DropDownListRowCount > option:nth-child(3)").click()

for j in range(1, 453):
    try:
        if j >= 1:
            num = 1
            for i in htmls:
                num += 1
                try:

                    driver.find_element_by_css_selector(".ListContent1 > tbody:nth-child(1) > tr:nth-child({}) a".format(num)).click()
                    key = driver.find_element_by_css_selector(".ListContent1 > tbody:nth-child(1) > tr:nth-child({}) > td:nth-child(3)".format(num)).text
                    now_handle = driver.current_window_handle
                    all_handles = driver.window_handles
                    driver.switch_to.window(all_handles[-1])

                    data = driver.page_source
                    data = pq(data).find("#form1 > div.Box10.ClearFloat > div.Box77.FloatLeft.MarginLeft10 > div > table > tbody > tr")
                    content = data.items()
                    insert_data = []
                    for k in content:
                        values = k.find('td').text().replace("\xa0", "").replace("\xa01", "").replace("\xa04", "").replace("\xa02", "").replace("\ua004", "").replace("\xa03", "").replace("\xa025", "")
                        values = values.replace("\ue0043", "").replace("\ue0042", "").replace("\ue0044", "").replace("\ue0045", "").replace("\ue0046", "").replace('"', "'")
                        insert_data.append(values)

                    try:
                        sql = """INSERT INTO `myprojects`.`国际农业科研项目数据库`(`项目名称`, `项目简介`, `承担机构`, `关键词`, `研究进展`, `项目来源`, `资助机构`, `项目成员`, `起止时间`, `专业分类`) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}') ON DUPLICATE KEY UPDATE  `项目名称`=VALUES( `项目名称`)"""
                        sql = sql.format(*insert_data)
                        result = curser.execute(sql.format(*insert_data))
                        conn.commit()
                        # print(j, num, result, insert_data[:4])
                    except Exception as e:
                        print(j, num, key, e)
                        aaa = [j, num]
                        errors.append(aaa)
                    if len(all_handles) >= 2:
                        driver.close()
                    driver.switch_to.window(now_handle)
                except:
                    pass
        driver.find_element_by_css_selector("#PageSplitBottom_ImageButtonNext").click()
        htmls = pq(driver.page_source).find(".ListContent1.EllipsisTable  a").items()
    except:
        pass
with open("国际农业.json", 'w', encoding='utf-8') as f:
    f.write(json.dumps(errors))