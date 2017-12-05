#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"

import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8')
curser = conn.cursor()


def insert_url(page):
    with open("E:\statics\作物科学\作物野生资源及其生境数据库\data\{}.csv".format(str(page)), 'r', ) as f:
        try:
            data = f.readlines()
            for i in data[2:]:
                result = i.split(',')
                if "," in result[3]:
                    result[3] = str(result[3]) + ',' + str(result[4])
                    del result[4]
                for j in range(0, len(result)-1):
                    if not result[j]:
                        result[j] = 'Null'
                if result[-1] == '\n':
                    result[-1] = 'Null'

                result = result[1:]
                sql = """
                    INSERT INTO `myprojects`.`作物野生资源及其生境数据库`(`作物名称`, `原位点号`, `考察号`, `普查日期`,
                     `省`, `市县`, `地形`, `生态环境`, `坡面`, `坡度`, `土壤类型`, `土壤肥力`, `平均温度`, `最高温度`,
                      `最低温度`, `降雨量`, `学名`, `生长习性`, `生育周期`, `形态`, `分布面积`, `种群数量`, `危害因素`, 
                      `危害状况`, `多样性评价`, `备注`) VALUES ('{0}', "{1}", '{2}','{3}', '{4}','{5}', '{6}', '{7}', '{8}',
                      '{9}', '{10}','{11}','{12}','{13}', '{14}','{15}','{16}','{17}', '{18}', '{19}', '{20}','{21}',
                      '{22}','{23}', '{24}', '{25}')""".format(*result)
                try:
                    curser.execute(sql)
                    conn.commit()
                    # print(page)
                except:
                    # print(sql)
                    pass
                print(i)
        except Exception as e:
            print(e)


for ii in range(1, 3):
    insert_url(ii)
