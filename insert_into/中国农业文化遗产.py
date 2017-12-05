import json
import re

import pymysql
from pyquery import PyQuery as pq
id = 0


conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8', cursorclass=pymysql.cursors.DictCursor,)
curser = conn.cursor()
pattern = '.*.jpg"/></p>\\n<p align=\"center\">(.*?)</p>\\n<p>.*'
with open("E:\statics\中国重要农业文化遗产\中国重要农业文化遗产.json", 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
    for i in data:
       for j in i.items():
           for k in j[1]:
                id += 1
                if "第二批中国重要农业文化遗产" in k['标题']:
                    k['标题'] = k['标题'][15:]
                if "来源" in k['来源']:
                    k['来源'] = k['来源'][3:]
                if "日期" in k['日期']:
                    k['日期'] = k['日期'][3:]
                k['批次'] = j[0][:3]
                datas = [id, k['标题'], k['批次'], str(k['内容']), k['链接'], k['来源'],  k['点击次数'], k['日期']]
                sql = "INSERT INTO `myprojects`.`中国重要农业文化遗产`(`id`, `标题`, `批次`, `内容`, `链接`, `来源`, `点击次数`, `日期`) VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}','{7}')".format(*datas) + "ON DUPLICATE KEY UPDATE  `id`=VALUES( `id`)"
                result = curser.execute(sql)
                conn.commit()
                print(id , result, sql)