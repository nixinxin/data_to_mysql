
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='myprojects', charset='utf8')
curser = conn.cursor()



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
pool = ThreadPool(10)


def insert_url(page):
    with open("E:\statics\作物科学\作物核心种质数据库\小麦种质资源核心种质数据库\\{}.csv".format(str(page)), 'r', encoding='utf-8') as f:
        data = f.readlines()
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
                try:
                    if '\n' in result[j]:
                        result[j].strip('\n')
                except:
                    pass
            result = tuple(result[1:])
            print(result)
            sql = """
                INSERT INTO `myprojects`.`小麦种质资源核心种质数据库`(`统一编号`, `保存单位`, `品种名称`, `系谱`, `原产地`, `芒`,
                 `壳色`, `粒色`, `冬春性`, `成熟期`, `穗粒数`, `穗长`, `株高`, `千粒重`, `粗蛋白`, `省`) VALUES 
                   ('{0}', '{1}', '{2}','{3}', '{4}','{5}', '{6}', '{7}', '{8}','{9}', {10},{11}, {12},{13}, {14},
                   '{15}')
                """.format(*result)
            curser.execute(sql)
            conn.commit()



for ii in range(1, 97):
    insert_url(ii)