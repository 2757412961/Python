# -*- coding: utf-8 -*-
# @File  : ccmpDownload.py
# @Author: Zjh
# @Date  : 2022/11/23
# @Update: 2022/11/23
# @Desc  :

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from utils import HeaderUtil
from utils import LogUtil
from utils import FileUtil
from utils.MultiDownload import MulThreadDownload, MulThreadConcurrentDownload, MulThreadPoolDownload

# 日志
LOG_URL = FileUtil.generate_logfile_url("logs/chla.log")
logger = LogUtil.Logger(LOG_URL)
# 常量
BASE_URL = 'https://oceandata.sci.gsfc.nasa.gov/cgi/getfile'
URLS_FILE = 'urls.txt'
SAVE_DIR = 'F:\Ocean\MODIS_AQUA_Chla'


def write_url(lst):
    filename = open(URLS_FILE, 'w')
    for value in lst:
        filename.write(str(value) + '\n')


def read_url():
    with open(URLS_FILE, 'r') as f:
        lst = f.read().splitlines()
    return lst


def getDownloadUrls():
    return read_url()


if __name__ == '__main__':
    urls = getDownloadUrls()

    print(urls)

    #### 用线程池下载 ####
    mtpd = MulThreadPoolDownload()
    lst_url = []
    lst_file = []
    urls.reverse()
    for _, url in enumerate(urls):
        sub_path = url.replace(BASE_URL, '')
        file_path = SAVE_DIR + sub_path
        FileUtil.check_generate_files(file_path)
        if not FileUtil.exist(file_path):
            lst_url.append(url)
            lst_file.append(file_path)
    mtpd.download(lst_url, lst_file)

    exit(0)
