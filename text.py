#!/usr/bin/python
# -*- coding:utf-8 -*-
import pymysql

__author__ = "xin nix"
import requests
from pyquery import PyQuery as pq

# conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
# curser = conn.cursor()
# sql = """INSERT INTO `myprojects`.`农业科技机构数据库`({0})
#   VALUES ({1}) on duplicate KEY UPDATE `机构编号`=VALUES (`机构编号`)"""
# while True:
#     data = input()
#     content = pq(data.strip()).find("tr").items()
#     insert_data = []
#     insert_key = []
#     for k in content:
#         key = k.find('th').text()
#         insert_key.append(key)
#         values = k.find('td').text().replace('"', "")
#         insert_data.append(values)
#     # print(len(insert_data))
#     keys = "`" + "`, `".join(insert_key) + "`"
#     # print(keys)
#     nums = ''
#     for num in range(0, len(insert_data)):
#         nums += '"{' + str(num) + '}", '
#     nums = nums[:-2]
#     # print('1', insert_data)
#     try:
#         sql = """INSERT INTO `myprojects`.`农业科技机构数据库`(""" + keys + ") VALUES (" + nums + ") on duplicate KEY UPDATE `机构编号`=VALUES (`机构编号`)"""
#         sql = sql.format(*insert_data)
#         resaulst = curser.execute(sql)
#         conn.commit()
#         print(resaulst, sql)
#     except Exception as e:
#         # print(e, len(insert_data))
#         # print(insert_data)
#         pass

que = ['中国农村杂志社', '房山区农业机械研究所', '浙江海洋水产养殖研究所', '北京市农业机械研究所',
       '中国水产科学研究院黄海水产研究所', '中国农业大学食品学院食品技术服务中心', '湖南师范大学',
       '中国肉类食品综合研究中心', '四川农业大学动物营养研究所', '四川省农业科学院质量标准与检测技术研究所',
       '北京市大兴区农业技术推广站', '北京市海淀区农业科学研究所', '宁波市海洋与渔业研究院', '北京农学院计算机与信息工程学院',
       '中国种子协会', '青海省渔业环境监测站', '云南省水产研究所', '河南师范大学水产学院', '顺义区农机维修服务站',
       '农业部规划设计研究院设施农业研究所', '北京农药学会', '中国农业大学理学院', '农业部规划设计研究院农业发展与投资研究所',
       '北京市农业机械试验鉴定推广站', '中国肉类协会', '北京水产学会', '中国农业科学院', '四川农业大学小麦研究所',
       '延庆县农村合作经济经营管理站', '长安大学', '中国绿色食品发展中心', '青海湖裸鲤救护中心', '四川省草原工作总站',
       '中国农业科学院甜菜研究所', '中国食用菌协会', '华南农业大学', '中国科协农村专业技术服务中心',
       '北京市大兴区植保植检站', '北京绿能经济植物研究所', '四川农业大学动物科技学院', '国家玉米改良中心',
       '中国水产科学研究院长江水产研究所']

test = " '品种来源:\xa0\xa0\xa0\xa0吉林省农业科学院旱地农业研究中心,1995年以白绿522为母本，以自选系T62为父本进行人工杂交选育而成。原品系代号洮9947。 产量表现:\xa0\xa0\xa0\xa02004-2005年区域试验平均公顷产量1330.18公斤，比对照品种白绿6号增产13.33%。2005-2006年生产试验平均公顷产量1232.32公斤，比对照品种白绿6号增产12.16%。'"
print(test)
test = test.replace("\xa0", "")
print(test)