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
LOG_URL = FileUtil.generate_logfile_url("logs/jmaco2.log")
logger = LogUtil.Logger(LOG_URL)
# 常量
BASE_URL = 'https://www.data.jma.go.jp/gmd/kaiyou/data/english/co2_flux'
URLS_FILE = 'urls.txt'
SAVE_DIR = 'F:\Ocean\JMA_Ocean_CO2_Map'


def print_url_lst():
    for i in range(90, 100):
        print('https://www.data.jma.go.jp/gmd/kaiyou/data/english/co2_flux/grid/JMA_co2map_19' + str(i) + '.ZIP')
    for i in range(0, 10):
        print('https://www.data.jma.go.jp/gmd/kaiyou/data/english/co2_flux/grid/JMA_co2map_200' + str(i) + '.ZIP')
    for i in range(10, 21):
        print('https://www.data.jma.go.jp/gmd/kaiyou/data/english/co2_flux/grid/JMA_co2map_20' + str(i) + '.ZIP')


def write_url(lst):
    filename = open(URLS_FILE, 'w')
    for value in lst:
        filename.write(str(value) + '\n')


def read_url():
    with open(URLS_FILE, 'r') as f:
        lst = f.read().splitlines()
    return lst


def getDownloadUrls():
    urls = read_url()
    logger.info(urls)
    return urls


if __name__ == '__main__':
    urls = getDownloadUrls()

    #### 用线程池下载 ####
    mtpd = MulThreadPoolDownload()
    lst_url = []
    lst_file = []
    urls.reverse()
    for _, url in enumerate(urls):
        sub_path = url.replace(BASE_URL, '')
        sub_path = sub_path[5:]
        file_path = SAVE_DIR + sub_path
        FileUtil.check_generate_files(file_path)
        if not FileUtil.exist(file_path):
            lst_url.append(url)
            lst_file.append(file_path)
    mtpd.download(lst_url, lst_file)

    exit(0)
