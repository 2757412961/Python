# -*- coding: utf-8 -*-
# @File  : MultiDownload.py
# @Author: Zjh
# @Date  : 2022/11/24
# @Update: 2022/11/24
# @Desc  :
import logging
import threading
from concurrent import futures
from tqdm import tqdm, trange
from progressbar import *
import requests
import os
import random


class BulkDownload(threading.Thread):
    '''
    单个文件进行分割，每个线程下载一部分
    '''

    def __init__(self, url, startpos, endpos, file_dup):
        super(BulkDownload, self).__init__()
        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = file_dup

    def parse(self):
        headers = {
            "Range": "bytes=%s-%s" % (self.startpos, self.endpos)
        }
        # resp.content是bytes类型，而resp.text是str类型
        response = requests.get(self.url, headers=headers)
        self.fd.seek(self.startpos)
        self.fd.write(response.content)

    def run(self):
        self.parse()


class MulThreadConcurrentDownload():
    '''
    单个文件进行分割，每个线程下载一部分
    '''

    def __init__(self, thread_num=4):
        self.thread_num = thread_num
        threading.BoundedSemaphore(self.thread_num)

    def download(self, url, tar_path):
        file_size = int(requests.head(url).headers['Content-Length'])
        step = file_size // self.thread_num
        thread_list = []
        start = 0
        end = -1
        with open(tar_path, 'wb+') as f:
            fileno = f.fileno()
            while end < file_size - 1:
                start = end + 1
                end = start + step - 1
                if end > file_size:
                    end = file_size
                dup = os.dup(fileno)
                file_dup = os.fdopen(dup, 'rb+', -1)
                # print(fd)
                thread = BulkDownload(url, start, end, file_dup)
                thread.start()
                thread_list.append(thread)
            for thread in thread_list:
                thread.join()
        return thread_list


class SingleDownload(threading.Thread):
    '''
    一个线程下载一个文件，同时开启多个线程下载多个文件
    '''

    def __init__(self, url, file_path):
        super(SingleDownload, self).__init__()
        self.url = url
        self.file_path = file_path
        self.ua = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2995.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.0 Safari/537.36'
        ]

    def parse(self):
        headers = {
            "User-Agent": random.choice(self.ua)
        }
        # 获取文件的大小
        response = requests.get(self.url, headers=headers)
        f = open(self.file_path, "wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        print(f"finish: {self.url}")

    def run(self):
        self.parse()


class MulThreadDownload():
    '''
    一个线程下载一个文件，同时开启多个线程下载多个文件
    '''

    def __init__(self, thread_num=16):
        self.thread_num = thread_num
        threading.BoundedSemaphore(thread_num)

    def download(self, url_list, tar_path_list):
        if type(url_list) is list and type(tar_path_list) is list:
            None
        elif type(url_list) is str and type(tar_path_list) is str:
            url_list = [url_list]
            tar_path_list = [tar_path_list]
        else:
            raise Exception("Parameter not match!")

        thread_list = []
        for _, (url, tar_path) in enumerate(zip(url_list, tar_path_list)):
            # 请空并生成文件
            thread = SingleDownload(url, tar_path)
            thread.start()
            thread_list.append(thread)
        for thread in thread_list:
            thread.join()
        return thread_list


class MulThreadPoolDownload():

    def __init__(self, workers=32):
        self.workers = workers
        self.ua = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2995.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.0 Safari/537.36'
        ]

    def parse(self, url, file_path):
        headers = {
            "User-Agent": random.choice(self.ua),
            # 'cookie': '_ga=GA1.5.448334129.1672556555; app-obdaac=42e785ef43e9079d84f216221b735e9e81149345; _ga_T0WYSFJPBT=GS1.1.1673290475.1.0.1673290475.0.0.0; _ga=GA1.1.448334129.1672556555; app-obdaac=42e785ef43e9079d84f216221b735e9e81149345'
        }
        # 获取文件的大小
        response = requests.get(url, headers=headers)
        # response = requests.get(url, headers=headers, cookies={'app-obdaac': '42e785ef43e9079d84f216221b735e9e81149345; Path=/; Secure;'})
        f = open(file_path, "wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(f"{currentTime}|finish: {url}")

    def download(self, url_list, tar_path_list):
        if type(url_list) is list and type(tar_path_list) is list:
            None
        elif type(url_list) is str and type(tar_path_list) is str:
            url_list = [url_list]
            tar_path_list = [tar_path_list]
        else:
            raise Exception("Parameter not match!")

        with futures.ThreadPoolExecutor(self.workers) as executor:
            to_do = []
            for _, (url, tar_path) in enumerate(zip(url_list, tar_path_list)):
                to_do.append(executor.submit(self.parse, url, tar_path))
            # 获取Future的结果，futures.as_completed(to_do)的参数是Future列表，返回迭代器。只有当有Future运行结束后，才产出future
            for future in tqdm(to_do, desc='Processing'):
                # future变量表示已完成的Future对象，所以后续future.result()绝不会阻塞
                try:
                    result = future.result()
                    print(f'Task result:{result}')
                except Exception as e:
                    print(e)
            # widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
            # bar = ProgressBar(widgets=widgets)
            # for future in bar(to_do):  # future变量表示已完成的Future对象，所以后续future.result()绝不会阻塞
            #     try:
            #         result = future.result()
            #         print(result)
            #     except Exception as e:
            #         print(e)


if __name__ == "__main__":
    # 多线程下载一个文件
    mtcd = MulThreadConcurrentDownload(4)
    mtcd.download('https://picx.zhimg.com/v2-eaf6db06d882762435c54a9bb17be3c0_1440w.jpg', 'test')

    # 单线程下载一个文件
    sd = SingleDownload('https://picx.zhimg.com/v2-eaf6db06d882762435c54a9bb17be3c0_1440w.jpg', 'test')
    # sd.run()

    # 多线程下载多个文件
    mtd = MulThreadDownload()
    # mtd.download('https://picx.zhimg.com/v2-eaf6db06d882762435c54a9bb17be3c0_1440w.jpg', 'test')

    # 线程池下载多个文件
    mtpd = MulThreadPoolDownload()
    # mtpd.download('https://picx.zhimg.com/v2-eaf6db06d882762435c54a9bb17be3c0_1440w.jpg', 'test')
