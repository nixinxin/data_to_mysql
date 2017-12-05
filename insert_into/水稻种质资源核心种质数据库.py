
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8')
curser = conn.cursor()


def insert_url(page):
    with open("E:\statics\作物科学\作物核心种质数据库\水稻种质资源核心种质数据库\\{}.csv".format(page), 'r', encoding='utf-8') as f:
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
            result[-1] = result[-1].strip('\n')
            result = tuple(result[1:])
            sql = """
                INSERT INTO `myprojects`.`水稻种质资源核心种质数据库`(`统一编号`, `品种名称`, `高程`, `东经`, `北纬`, `原产地`,
                 `保存单位`, `单位编号`, `籼粳`, `早中晚`, `水陆`, `粘糯`, `米色`, `米香`, `芒长`, `粒形状`, `粒长度`, `长宽比`,
                  `颖尖色`, `颖壳色`, `颖毛有无`, `护颖长短`, `颖尖弯直`, `株高`, `出穗期`, `糙米率`, `精米率`, `垩白率`, `蛋白质`,
                   `赖氨酸`, `总淀粉`, `直链淀粉`, `支链淀粉`, `糊化温度`, `胶稠度`, `苗瘟`, `白叶枯`, `纹枯病`, `褐稻虱`, 
                   `白背飞虱`, `芽期耐寒`, `苗期耐旱`, `耐盐`, `省`, `稻区`) VALUES 
                   ('{0}', '{1}', {2},{3}, {4},'{5}', '{6}', '{7}', '{8}','{9}', '{10}','{11}', '{12}','{13}', '{14}',
                   '{15}','{16}','{17}', '{18}', '{19}', '{20}','{21}','{22}',{23}, {24}, {25}, {26},'{27}', {28},
                    {29}, {30}, {31}, {32},{33}, {34},{35}, {36},'{37}', {38},{39}, {40},{41},
                     {42}, '{43}', '{44}')
                """.format(*result)
            curser.execute(sql)
            conn.commit()


for ii in range(1, 107):
    insert_url(ii)
    print(ii)