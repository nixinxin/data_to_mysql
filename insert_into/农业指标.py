#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"
import pandas
import MySQLdb
import os

conn = MySQLdb.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8')
curser = conn.cursor()

locations = ['中国', '北京市', '天津市', '河北省', '山西省', '内蒙古', '辽宁省', '吉林省', '黑龙江', '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '广西', '海南省', '重庆市', '四川省', '贵州省', '云南省', '西藏', '陕西省', '甘肃省', '青海省', '宁夏', '新疆']

sql = """INSERT INTO `myprojects`.`农业指标`(`index`, `values`, `location`, `year`) VALUES ('{0}', '{1}', '{2}', {3})""" + " ON DUPLICATE KEY UPDATE  `index`=VALUES(`index`)"

base_dir = "E:\statics\农业指标"

"""马年底头数指数((解放前最高年=100))"""

def insert_index(path):
    # index = path.split("\\")[-1][:-4]
    data = pandas.read_excel(path, skiprows=[1, ])
    index = pandas.read_excel(path, skiprows=[0, ], nrows=1)
    index = index.keys()[1]
    for j in range(1, len(data) + 1):
        weizhi_num = -1
        for i in data:
            weizhi_num += 1
            location = locations[weizhi_num]
            insert_data = [index, data[i][j - 1], location, 2017 - j]
            sqls = sql.format(*insert_data)
            result = curser.execute(sqls)
            conn.commit()
            print(result, insert_data)


# index_one = os.listdir(base_dir)
# for i in index_one:
#     one_path = os.path.join(base_dir, i)
#     for j in os.listdir(one_path):
#         two_path = os.path.join(one_path, j)
#         if ".xls" in two_path:
#             insert_index(two_path)
#         else:
#             for k in os.listdir(two_path):
#                 three_path = os.path.join(two_path, k)
#                 if ".xls" in three_path:
#                     try:
#                         insert_index(three_path)
#                     except Exception as e:
#                         print(e)

wenti_path = "E:\statics\农业指标\农业生产及其产量\牲畜年末数\问题"
for k in os.listdir(wenti_path):
    three_path = os.path.join(wenti_path, k)
    if ".xls" in three_path:
        print(three_path)
        try:
            # sql = """delete from `myprojects`.`农业指标` where `index`='{}'"""
            # index = pandas.read_excel(three_path, skiprows=[0, ], nrows=1)
            # index = index.keys()[1]
            # sql = sql.format(index)
            # ss = curser.execute(sql)
            # conn.commit()
            # print(ss)
            insert_index(three_path)
        except Exception as e:
            print(e)

