#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"
import os
import pandas
path = "E:\statics\中国行政区划数据\行政区划清单 V3.0 9.03.xlsx"
import pymysql


conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()
sql = """INSERT INTO `myprojects`.`行政区划清单`(`id`, `province`, `city`, `county`, `provincecode`, `citycode`, `countycode`, `alias`) VALUES ({0}, '{1}', '{2}', '{3}', {4},  {5},  {6}, '{7}')"""
data = pandas.read_excel(path)
for j in range(1, len(data) + 1):
    insert_data = []
    for i in data:
        try:
            insert_data.append(int(data[i][j-1]))
        except:
            if isinstance(data[i][j-1], float):
                insert_data.append(0)
            else:
                insert_data.append(data[i][j - 1])
    sqls = sql.format(*insert_data) + "ON DUPLICATE KEY UPDATE  `id`=VALUES( `id`)"
    print(sqls)

    curser.execute(sqls)
    conn.commit()
    print(insert_data)
