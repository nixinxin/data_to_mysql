import csv
import sys
import os
import django
import pandas

import os
import re
import time
import urllib.request

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from pyquery import PyQuery as pq
import json
import re

import queue
import threading
import contextlib
import time

StopEvent = object()


class ThreadPool(object):
    def __init__(self, max_num, max_task_num=None):
        if max_task_num:
            self.q = queue.Queue(max_task_num)
        else:
            self.q = queue.Queue()
        self.max_num = max_num
        self.cancel = False
        self.terminal = False
        self.generate_list = []
        self.free_list = []

    def run(self, func, args, callback=None):
        """
        线程池执行一个任务
        :param func: 任务函数
        :param args: 任务函数所需参数
        :param callback: 任务执行失败或成功后执行的回调函数，回调函数有两个参数1、任务函数执行状态；2、任务函数返回值（默认为None，即：不执行回调函数）
        :return: 如果线程池已经终止，则返回True否则None
        """
        if self.cancel:
            return
        if len(self.free_list) == 0 and len(self.generate_list) < self.max_num:
            self.generate_thread()
        w = (func, args, callback,)
        self.q.put(w)

    def generate_thread(self):
        """
        创建一个线程
        """
        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        """
        循环去获取任务函数并执行任务函数
        """
        current_thread = threading.currentThread()
        self.generate_list.append(current_thread)

        event = self.q.get()
        while event != StopEvent:

            func, arguments, callback = event
            try:
                result = func(*arguments)
                success = True
            except Exception as e:
                success = False
                result = None

            if callback is not None:
                try:
                    callback(success, result)
                except Exception as e:
                    pass

            with self.worker_state(self.free_list, current_thread):
                if self.terminal:
                    event = StopEvent
                else:
                    event = self.q.get()
        else:

            self.generate_list.remove(current_thread)

    def close(self):
        """
        执行完所有的任务后，所有线程停止
        """
        self.cancel = True
        full_size = len(self.generate_list)
        while full_size:
            self.q.put(StopEvent)
            full_size -= 1

    def terminate(self):
        """
        无论是否还有任务，终止线程
        """
        self.terminal = True

        while self.generate_list:
            self.q.put(StopEvent)

        self.q.queue.clear()

    @contextlib.contextmanager
    def worker_state(self, state_list, worker_thread):
        """
        用于记录线程中正在等待的线程数
        """
        state_list.append(worker_thread)
        try:
            yield
        finally:
            state_list.remove(worker_thread)


# How to use
pool = ThreadPool(120)

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_to_mysql.settings")

django.setup()
from items.models import ResourcesFromaBroad


def insert_into(arg):
        path = 'E:\statics\作物科学\国外引进作物资源数据库\国外引进作物种质资源数据库\\{}.csv'.format(str(arg))
        data = pandas.read_csv(path).fillna('')
        try:
            insert_data = {
                "total_id": data['1'][0],
                "import_id": data['3'][0] if ".0" not in str(data['3'][0]) else str(data['3'][0]).strip('.0'),
                "copes_category": data['5'][0],
                "copes_type": data['7'][0],
                "name": data['1'][1],
                "category_name": data['3'][1],
                "translated_name": data['5'][1],
                "source": data['7'][1],
                "source_area": data['1'][2],
                "total_way": data['3'][2],
                "import_way": data['5'][2],
                "import_year": data['7'][2],
                "import_time": data['1'][3],
                "distribution_unit": data['3'][3],
                "feature": data['5'][3],
                "Save_unit": data['7'][3],
                "comment": data['1'][4],
            }
            exited = ResourcesFromaBroad.objects.filter(**insert_data).exists()
            if not exited:
                ResourcesFromaBroad.objects.create(**insert_data).save()
                print(arg, insert_data)
        except Exception as e:
            print(arg, e)


for i in range(31578, 0, -1):
    pool.run(insert_into, args=(i, ))
