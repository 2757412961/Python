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

# 日志
LOG_URL = FileUtil.generate_logfile_url("logs/test.log")
logger = LogUtil.Logger(LOG_URL)
# 常量
BASE_URL = 'https://data.remss.com'
URLS_FILE = 'urls.npy'
SAVE_DIR = 'F:\Ocean\CCMP_V3'


def saveList(urls, filename):
    '''
    保存
    filename = open(‘urls.txt’, ‘w’)
    for value in a:
    filename.write(str(value))
    filename.close()

    读取
    f= open(“a.txt”,“r”)
    a = f.read()
    f.close()
    以上这种方法虽然占用空间小，但是原来的list格式会被破坏。为此也可以用以下发方法，此方法可以保留list原格式。

    保存
    import numpy as np
    a=np.array(a)
    np.save(‘a.npy’,a)   # 保存为.npy格式

    读取
    a=np.load(‘a.npy’)
    a=a.tolist()
    ps:
    如果读取的.txt文件是中文名，需要加以下内容：

    readme = pd.read_csv(‘读我.txt’,sep=’:’,encoding=“utf-8”, engine=‘python’,header=None)
    readme = np.array(readme)
    :return:
    '''
    import numpy as np
    urls = np.array(urls)
    np.save(filename, urls)


def loadList(filename):
    import numpy as np
    np.load.__defaults__ = (None, True, True, 'ASCII')
    urls = np.load(filename)
    np.load.__defaults__ = (None, False, True, 'ASCII')
    urls = urls.tolist()
    return urls


def getDownloadUrl(url):
    """
    获取网页源码
    :param url: 网页url
    :return:
    """
    header = HeaderUtil.gen_headers()
    resp = requests.get(url=url, headers=header)
    html = resp.text
    logger.info(str(resp.status_code) + ' ' + resp.url)

    soup = BeautifulSoup(html, 'html.parser')
    # logger.debug(soup.prettify())

    lst = []
    for _, link in enumerate(soup.find_all('a')):
        if _ == 0:  # skip first line of the file
            # 返回上一级目录链接
            continue

        sub_url = link.get('href')
        if not sub_url or sub_url.endswith('.nc'):
            lst.append(BASE_URL + sub_url)
        else:
            lst += getDownloadUrl(BASE_URL + sub_url)

    return lst


def getDownloadUrls():
    '''
       https://data.remss.com/ccmp/
       <dir> read_routines
       293185 readme_ccmp.pdf
       <dir> v02.0
       <dir> v02.0.NRT
       <dir> v02.1.NRT
       <dir> v03.0
       '''
    if FileUtil.exist(URLS_FILE):
        # 从本地文件导入Url
        urls = loadList(URLS_FILE)
    else:
        # 从网站文件解析Url
        urls = getDownloadUrl('https://data.remss.com/ccmp/v03.0')
        saveList(urls, URLS_FILE)
    logger.warning(urls)
    return urls


if __name__ == '__main__':
    urls = getDownloadUrls()

    exit(0)
