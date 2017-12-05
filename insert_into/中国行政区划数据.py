#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"
import json
import re

import pymysql

sql = """INSERT INTO `myprojects`.`中国行政区划数据库`(`citycode`, `adcode`, `name`, `center`, `level`) VALUES ({0}, {1}, '{2}', '{3}', '{4}')"""
conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()

with open("E:\statics\中国行政区划数据\中国行政区划数据.json", 'r', encoding='utf-8') as f:

    pattern = '"citycode":"(.*?)","adcode":"(.*?)","name":"(.*?)","center":"(.*?)","level":"(.*?)"'
    result = re.findall(pattern ,f.read())
    for i in result:
        sqls = sql.format(*i)
        curser.execute(sqls)
        conn.commit()
        print(sqls)

