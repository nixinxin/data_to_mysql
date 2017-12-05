#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"

import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8')
curser = conn.cursor()


def insert_url(page):
    with open("E:\statics\作物科学\作物核心种质数据库\玉米种质资源核心种质数据库\\{}.csv".format(page), 'r', encoding='utf-8') as f:
        data = f.readlines()
        new = list()
        for i in data[2:]:
            result = i.split(',')

            for j in range(0, len(result)-1):
                if "." in result[j]:
                    try:
                        result[j] = float(result[j])
                    except:
                        result[j] = str(result[j])
                else:
                    try:
                        if isinstance(int(result[j]), int):
                            result[j] = int(result[j]) if result[j] else None

                    except:
                        pass
                if not result[j]:
                    result[j] = 'Null'
            if result[-1] == '\n':
                result[-1] = 'Null'
            result = result[1:]
            sql = """
                INSERT INTO `myprojects`.`玉米种质资源核心种质数据库`(`统一编号`, `品种名称`, `原产地`, `亲本来源`, 
                `保存单位`, `保存编号`, `播种期`, `株高`, `穗位高`, `主茎叶片数`, `雄穗分枝数`, `抽丝日数`, `生育日数`,
                 `双穗率`, `穗形`, `粒型`, `粒色`, `轴色`, `穗长`, `穗粗`, `穗行数`, `千粒重`, `地点`, `播种日期`,
                  `株型`, `单株粒重`, `出籽率`, `大斑病`, `小斑病`, `黑穗病`, `花叶病`, `粗蛋白`, `粗脂肪`, `总淀粉`,
                   `赖氨酸`) VALUES ('{0}', "{1}", '{2}','{3}', '{4}','{5}', '{6}', '{7}', '{8}','{9}', '{10}','{11}','{12}','{13}', 
                   '{14}','{15}','{16}','{17}', '{18}', '{19}', '{20}','{21}','{22}','{23}', '{24}', '{25}', '{26}','{27}', '{28}',
                    '{29}', '{30}', '{31}', '{32}','{33}', '{34}')""".format(*result)
            # print(sql)
            try:
                curser.execute(sql)
                conn.commit()
                print(page)
            except:
                print(sql)


for ii in range(1, 29):
    insert_url(ii)
