#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "xin nix"
import requests
import json
import pymysql

# category_code = {
#     "13079": "畜产品",
#     "13080": "水产品",
#     "13073": "粮油",
#     "13076": "果品",
#     "13075": "蔬菜",
# }

url = "http://api.map.baidu.com/cloudgc/v1"
conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()
curser.execute("SELECT * FROM `行政区划清单`")
addrees = curser.fetchall()
for i in addrees:

    if not i['location']:
        querystring = {"address": i['城市'] + i['区县'],
                       "ak": "XbKB5htKalcYGbal6DbWlEY8pKzeXG8F"}
        headers = {
            'cache-control': "no-cache",
            'postman-token': "cd3f8abf-6a35-936a-5a34-65b66eb3c2e1"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = json.loads(response.text)
        print(response)
        if response['result']:
            data = response['result'][0]
            result = {
                'bound': data['bound'],
                'formatted_address': data['formatted_address'],
                'city': data['address_components']["city"],
                'district': data['address_components']['district'],
                'province': data['address_components']['province'],
                'location': str(data['location']['lng']) + "," + str(data['location']['lat']),
                'name': querystring['address'],
                "ci": i['城市'],
                "di": i['区县'],
            }
            # sql = """UPDATE `myprojects`.`行政区划清单` SET `location` = '{location}', `bound` = '{bound}', `formatted_address` = '{formatted_address}', `province` = '{province}', `city` = '{city}', `district` = '{district}' WHERE `名称` = '{name}'""".format(**result)

            sql = """UPDATE `myprojects`.`行政区划清单` SET `location` = '{location}',
                    `bound` = '{bound}', `formatted_address` = '{formatted_address}', `province` = '{province}', `city` = '{city}', 
                    `district` = '{district}' WHERE `城市` = '{ci}' and `区县` = '{di}'""".format(**result)
            results = curser.execute(sql)
            conn.commit()
            print(results, result)