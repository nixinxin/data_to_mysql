#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"
import os

import pymysql
from collections import defaultdict
import json
conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()

base_dir = "E:\statics\中国农业有害生物数据库\中国农业有害生物数据库"
index_one = os.listdir(base_dir)

for i in index_one:
    aa = 0
    # print(i)
    # try:
    #     drop_sql = 'drop table `myprojects`.`{}`'.format(i)
    #     curser.execute(drop_sql)
    #     conn.commit()
    # except:
    #     pass
    try:
        path = os.path.join(base_dir, i, i + '.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            for j in data:
                # If Not Exists
                create_sql = """create table If Not Exists`{}` (""".format(i)

                key_sql = ''
                num = -1
                values_into = []
                for ii, vv in j.items():
                    if ii:
                        ii = ii[:-1]
                        create_key = "`" + ii + "` int (10) , "
                        if ii != '编号':
                            create_key = "`" + ii + "` longtext  null,"
                        # if ii == '形态特征':
                        #     create_key = "`" + ii + "` longtext  null,"
                        # if ii == '拉丁学名':
                        #     create_key = "`" + ii + "` VARCHAR (80)  null,"
                        # if ii == '地理分布':
                        #     create_key = "`" + ii + "` VARCHAR (80)  null,"
                        # if ii == '相关文献':
                        #     create_key = "`" + ii + "` longtext  null,"
                        # if ii == '生物学特性':
                        #     create_key = "`" + ii + "` longtext  null,"
                        # if ii == '寄主昆虫':
                        #     create_key = "`" + ii + "` VARCHAR (80)  null,"
                        key_sql += "`" + ii + "`, "
                        num += 1
                        create_sql += create_key
                        values_into.append(str(vv))
                        # print(ii, len(vv))
                create_sql = create_sql[:-1]
                create_sql = create_sql + ", primary key(`编号`) " + ")"
                # print(create_sql)
                result = curser.execute(create_sql)
                conn.commit()
                try:
                    aa += 1
                    key_sql = key_sql[:-2]
                    vasual = ''
                    for values in values_into:
                        if "'" in values:
                            vasual += '"' + values + '", '
                        else:
                            vasual += "'" + values + "', "
                        if "}" in values:
                            vasual += "'" + values.replace("}", ")") + "', "

                    vasual = vasual[:-2] + ")"
                    # print(key_sql)
                    # print(vasual)
                    insert_sql = """INSERT INTO `myprojects`.`{0}`({1}) VALUES ({2} """.format(i, key_sql, vasual) + " ON DUPLICATE KEY UPDATE `编号`=VALUES(`编号`)"
                    # print(insert_sql)
                    insert_sql.format(*values_into)
                    results = curser.execute(insert_sql)
                    print(i, aa, results, values_into)
                except Exception as e:
                    # drop_sql = 'drop table `myprojects`.`{}`'.format(i)
                    # print(drop_sql," paichu")
                    # result = curser.execute(drop_sql)
                    curser.execute(create_sql)
                    conn.commit()
                    # print(result)
                    longs = []
                    for jjj in values_into:
                        longs.append(len(jjj))
                    print(e,)
                    print(key_sql)
                    print(vasual)
                    print(longs)
    except:
        drop_sql = 'drop table `myprojects`.`{}`'.format(i)
        result = curser.execute(drop_sql)
        # print(drop_sql, " paichu", result)
        pass

