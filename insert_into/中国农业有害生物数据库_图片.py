#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"
import os

import pymysql
from collections import defaultdict

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()

base_dir = "E:\statics\中国农业有害生物数据库\中国农业有害生物数据库"
index_one = os.listdir(base_dir)
aa = 0
for i in index_one:
    # print(i)
    path = os.path.join(base_dir, i, "图片")
    index_two = os.listdir(path)
    for j in index_two:
        name = j[:-4]
        species = i
        link = "agridata/images/" + "/".join(["中国农业有害生物数据库", str(species), j])
        aa += 1
        sql = "INSERT INTO `myprojects`.`中国农业有害生物数据库_图片`(`id`, `名称`, `种类`, `链接`) VALUES ({0}, '{1}', '{2}', '{3}') on duplicate key UPDATE `链接`= VALUES (`链接`)".format(aa, name, species, link)
        result = curser.execute(sql)
        conn.commit()
        print(name, species, link, result)
