import csv
import sys
import os
import django
import pandas
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_to_mysql.settings")

django.setup()
from items.models import WheatFamilyData
for i in range(1, 3567):
    path = 'E:\statics\作物科学\小麦系谱数据库\小麦系谱数据库\\{}.csv'.format(str(i))
    data = pandas.read_csv(path).fillna('')
    try:
        insert_data = {
            "id": int(data['1'][0]),
            "unit_id": int(['3'][0]),
            "name": data['5'][0],
            "family": data['7'][0].strip(),
            "original_name": data['1'][1],
            "source": data['3'][1],
            "original_addr": data['5'][1],
            "unit": data['7'][1],
            "height": int(data['1'][2]) if data['1'][2] else None,
            "qian_weight": data['3'][2] if data['1'][2] else None,
            "year": str(data['5'][2]).strip('.0'),
            "comment": data['7'][2],
        }
        exited = WheatFamilyData.objects.filter(id=int(data['1'][0])).exists()
        if not exited:
                WheatFamilyData.objects.create(**insert_data).save()
                print(i)
    except Exception as e:
        print(e, i)

