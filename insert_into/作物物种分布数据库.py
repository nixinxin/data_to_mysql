#!/usr/bin/python
# -*- coding:utf-8 -*-
import os

__author__ = "xin nix"

BASE_DIR = "E:\statics\作物科学\作物物种分布数据库"
RELATE_DIR = "作物物种分布数据库"
lists = ['作物分布图']
listss = ['作物特性分布图']

import pymysql
from collections import defaultdict

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()
aa = 0
insert_data = []
# "作物分布图",
for i in lists:
    result = os.listdir(os.path.join(BASE_DIR, i))
    index_one = []
    for j in result:
        index_one.append(j)
        index_two = []
        results = os.listdir(os.path.join(BASE_DIR, i, j))
        for k in results:
            abspath = [i, j, k]
            abs_path = "-".join(abspath)
            aa += 1
            sql = """INSERT INTO `myprojects`.`作物物种分布数据库`(`id`, `title`, `category`, `path`) VALUES ('{0}', '{1}', '{2}', '{3}')""".format(
                aa, k, i, abs_path)
            print(sql)
            res = curser.execute(sql)
            conn.commit()
            print(aa, res, sql)

for i in listss:
    result = os.listdir(os.path.join(BASE_DIR, i))
    index_one = []
    for j in result:
        index_one.append(j)
        index_twos = []
        results = os.listdir(os.path.join(BASE_DIR, i, j))
        for k in results:
            resultss = os.listdir(os.path.join(BASE_DIR, i, j, k))
            index_three = []
            for l in resultss:
                index_three.append(l)
                for m in index_three:
                    rabs = [i, j, k, l]
                    # print(rabs)
                    abs_path = "-".join(rabs)
                    aa += 1
                    sql = """INSERT INTO `myprojects`.`作物物种分布数据库`(`id`, `title`, `category`, `path`) VALUES ('{0}', '{1}', '{2}', '{3}')""".format(
                        aa, l, i, abs_path)
                    res = curser.execute(sql)
                    conn.commit()
                    print(aa, res, sql)




