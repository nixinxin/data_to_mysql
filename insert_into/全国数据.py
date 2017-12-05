#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"
import pandas
import MySQLdb
import os

conn = MySQLdb.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8')
curser = conn.cursor()

locations = ['中国', ]

sql = """INSERT INTO `myprojects`.`农业指标`(`指标`, `数值`, `省份`, `年份`) VALUES ('{0}', '{1}', '{2}', {3})""" + " ON DUPLICATE KEY UPDATE  `指标`=VALUES(`指标`)"

base_dir = "E:\statics\农业指标"

"""马年底头数指数((解放前最高年=100))"""

def insert_index(path):
    # index = path.split("\\")[-1][:-4]
    data = pandas.read_excel(path, skiprows=[0, 1])
    # print(data)
    index = list(data.keys())
    data = pandas.read_excel(path, skiprows=[0, 1, ])
    data = data.fillna("--")
    aa = 0
    bb = 0
    for j in range(1, len(data) + 1 - 2):
        inx = -1
        for i in index:
            inx += 1
            if inx > 0:
                insert_data = [i, str(data[i][inx - 1]), "中国", int(data["时间"][inx - 1].replace("年", ''))]
                sqls = sql.format(*insert_data)
                result = curser.execute(sqls)
                conn.commit()
                print(result, insert_data)
                print(insert_data)


wenti_path = "E:\statics\content\全国数据"

for k in os.listdir(wenti_path):
    three_path = os.path.join(wenti_path, "主要农业机械年末拥有量.xls")
    if ".xls" in three_path:
        try:
            insert_index(three_path)
        except Exception as e:
            print(e)
