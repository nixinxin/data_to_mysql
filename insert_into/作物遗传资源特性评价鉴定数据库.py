#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"
import pandas
import re

import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()


def zhuanhuan(arg):
    if arg == 'nan':
        arg = None
    return arg

def jiexi(file_path):
    try:
        data = pandas.read_csv(file_path)
        names = file_path.split("\\")
        name = names[-2]
        data = pandas.DataFrame(data)
        dicts = {}
        for i, j in data.items():
            for key in data.values:
                for k in range(len(key)):
                    if divmod(k, 2)[1] != 0:
                        try:
                            dicts[str(key[k])] = key[k + 1]
                        except:
                            dicts[str(key[k])] = None
        # If Not Exists
        create_sql = """create table If Not Exists `作物遗传资源特性评价鉴定数据库_{}` (id int not null,""".format(name)
        key_sql = 'id, '
        num = -1
        values_into = []
        for ii, vv in dicts.items():
            if ii != 'nan':
                create_key = "`" + ii + "` VARCHAR (30) null,"
                if ii == '统一编号':
                    create_key = "`" + ii + "` VARCHAR (10) ,"
                if ii == '学名':
                    create_key = "`" + ii + "` VARCHAR (40) ,"
                key_sql += "`" + ii + "`, "
                num += 1
                create_sql += create_key
                values_into.append(str(vv))
        values_intos = []
        for iii in values_into:
            if iii == 'nan':
                iii = "--"
            values_intos.append(iii.replace('"', "'"))
        create_sql = create_sql[:-1]
        create_sql = create_sql + ', primary key(id, `统一编号`) ' + ')'
        # print(create_sql)
        curser.execute(create_sql)

        key_sql = key_sql[:-2]
        # value_sql = "'" + "', '".join(values_intos) + "')"
        value_sql = '"' + '", "'.join(values_intos) + '")'
        insert_sql = """INSERT INTO `myprojects`.`作物遗传资源特性评价鉴定数据库_{0}`({1}) VALUES ({2}, """.format(name, key_sql, int(names[-1][:-4])) + value_sql + "ON DUPLICATE KEY UPDATE id=VALUES(id)"
        # print(insert_sql)
        insert_sql.format(*values_intos)
        result = 0
        try:
            result = curser.execute(insert_sql)
            # print(name, int(names[-1][:-4]), result)
        except Exception as e:
            print(e, name, int(names[-1][:-4]), result)
    except Exception as e:
        pass

root = "E:\statics\作物科学\作物遗传资源特性评价鉴定数据库"
import os

result = os.listdir(root)
index_one = []
for i in result:
    if "." not in i:
        index_one.append(i)
index_one.remove('__pycache__')
for index in index_one:
    paths = os.path.join(root, index)
    results = os.listdir(paths)
    for num in results:
        path = paths + "\\" + num
        jiexi(path)

