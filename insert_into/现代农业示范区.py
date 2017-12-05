#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"
import json

num = 0

import pymysql


conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()
sql = """INSERT INTO `myprojects`.`现代农业示范区`(`id`, `title`, `href`) VALUES ({0}, '{1}', '{2}')""" + "ON DUPLICATE KEY UPDATE  `id`=VALUES( `id`)"
with open("现代农业示范区.json", 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
    for i in data:
        num += 1
        sqls = sql.format(num, i['title'], i['href'])
        curser.execute(sqls)
        conn.commit()
        print(sqls)