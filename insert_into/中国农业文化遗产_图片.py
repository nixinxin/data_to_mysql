#!/usr/bin/python
# -*- coding:utf-8 -*-
import os

__author__ = "xin nix"

BASE_DIR = "E:\statics\中国重要农业文化遗产"


import pymysql
from collections import defaultdict

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()
aa = 0
insert_data = []

result = os.listdir(BASE_DIR)
index_one = ["第一批中国重要农业文化遗产", "第二批中国重要农业文化遗产", "第三批中国重要农业文化遗产", "第四批中国重要农业文化遗产"]
for j in index_one:
    index_twos = []
    results = os.listdir(os.path.join(BASE_DIR, j))
    for k in results:

        rabs = ["中国重要农业文化遗产", j, k]
        print(rabs)

        # abs_path = "/".join(rabs)
        abs_path = "agridata/images/culture/" + rabs[-1]
        aa += 1
        image_num = 1
        if "1" in k:
            image_num += 1
        sql = """INSERT INTO `chartsite`.`中国重要农业文化遗产_图片`(`id`, `标题`, `图片号`,  `批次`, `路径`)  VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(aa, k.replace("(1)", '').replace(".jpg", ""), image_num, j, abs_path) + "ON DUPLICATE KEY UPDATE  `路径`=VALUES( `路径`)"
        res = curser.execute(sql)
        conn.commit()
        print(aa, res, sql)




