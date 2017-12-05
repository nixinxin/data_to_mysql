#!/usr/bin/python
# -*- coding:utf-8 -*-
from twisted.enterprise import adbapi

__author__ = "xin nix"
import json
import re

import pymysql
from collections import defaultdict

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls):
        dbparms = dict(
            host='127.0.0.1',
            user='root',
            password='123456',
            db='myprojects',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item) #处理异常

    def handle_error(self, failure):
        #处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, insert_sql, params):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        cursor.execute(insert_sql, params)


with open("E:\statics\作物科学\作物优异资源种质数据库\作物优异资源种质数据库.json", 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
    for k, v in data.items():
        # print(k)
        for i in v:
            for item in i.items():
                # print(item)
                for j in item[1]:
                    for kk, vv in j.items():

                        insert_data = dict()

                        pattern = ".*种质类型：(.*)种质来源：(.*)优异性状：(.*)利用价值：(.*)评定等级：(.*)联系单位：(.*)"
                        result = re.findall(pattern, vv)
                        if result:
                            result = re.findall(pattern, vv)[0]
                            insert_data = {
                                "种质类型": result[0],
                                "种质来源": result[1],
                                "优异性状": result[2],
                                "利用价值": result[3],
                                "评定等级": result[4],
                                "联系单位": result[5],
                            }
                        if not result:
                            pattern = "(.*)优异性状：(.*)利用价值：(.*)评定等级：(.*)联系单位：(.*).*种质类型：(.*)种质来源："
                            result = re.findall(pattern, vv)
                            if result:
                                result = re.findall(pattern, vv)[0]
                                insert_data = {
                                    "种质类型": result[4],
                                    "种质来源": result[5],
                                    "优异性状": result[0],
                                    "利用价值": result[1],
                                    "评定等级": result[2],
                                    "联系单位": result[3],
                                }
                        if not result:
                            pattern = ".*种质类型：(.*)种质来源：(.*)优异性状：(.*)利用价值：(.*)联系单位：(.*)"
                            result = re.findall(pattern, vv)
                            if result:
                                result = re.findall(pattern, vv)[0]
                                insert_data = {
                                    "种质类型": result[0],
                                    "种质来源": result[1],
                                    "优异性状": result[2],
                                    "利用价值": result[3],
                                    "评定等级": '',
                                    "联系单位": result[4],
                                }
                        if not result:
                            pattern = ".*种质类型：(.*)种质来源：(.*)优异种质：(.*)利用价值：(.*)联系单位：(.*)"
                            result = re.findall(pattern, vv)
                            if result:
                                result = re.findall(pattern, vv)[0]
                                insert_data = {
                                    "种质类型": result[0],
                                    "种质来源": result[1],
                                    "优异性状": result[2],
                                    "利用价值": result[3],
                                    "评定等级": '',
                                    "联系单位": result[4],
                                }
                        if not result:
                            pattern = ".*种质类型：(.*)种质来源：(.*)优异性状：(.*)利用价值：(.*)评定等级：(.*)"
                            result = re.findall(pattern, vv)
                            if result:
                                result = re.findall(pattern, vv)[0]
                                insert_data = {
                                    "种质类型": result[0],
                                    "种质来源": result[1],
                                    "优异性状": result[2],
                                    "利用价值": result[3],
                                    "评定等级": result[4],
                                    "联系单位": result[4],
                                }
                        if "铁谷9号（91-117)" in vv:
                            pattern = ".*优异性状：(.*)利用价值：(.*)评定等级：(.*)联系单位：(.*)种质类型：(.*)种质来源(.*)"
                            result = re.findall(pattern, vv)
                            if result:
                                result = re.findall(pattern, vv)[0]
                                insert_data = {
                                    "种质类型": result[4],
                                    "种质来源": result[5],
                                    "优异性状": result[0],
                                    "利用价值": result[1],
                                    "评定等级": result[2],
                                    "联系单位": result[3],
                                }
                        if result:
                            insert_data['种质名称'] = kk
                            insert_data['种质大类'] = k
                            insert_data['种质小类'] = item[0]
                            insert_sql = """
                                INSERT INTO `myprojects`.`作物优异资源种质数据库`(`种质名称`, `种质小类`, `种质大类`,
                                `种质类型`, `种质来源`, `优异性状`, `利用价值`, `评定等级`, `联系单位`)
                                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')on duplicate KEY
                                UPDATE 种质来源=VALUES(种质来源)"""
                            insert_datas = (
                                insert_data["种质名称"],
                                insert_data["种质小类"],
                                insert_data["种质大类"],
                                insert_data["种质类型"],
                                insert_data["种质来源"],
                                insert_data["优异性状"],
                                insert_data["利用价值"],
                                insert_data["评定等级"],
                                insert_data["联系单位"], )
                            curser.execute(insert_sql.format(*insert_datas))
                            conn.commit()
                            print(insert_data)




