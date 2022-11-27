# -*- coding: utf-8 -*-
# @File  : modisl3Download.py
# @Author: Zjh
# @Date  : 2022/11/27
# @Update: 2022/11/27
# @Desc  :

import datetime
from utils import LogUtil
from utils import FileUtil
from utils.MultiDownload import MulThreadDownload, MulThreadConcurrentDownload, MulThreadPoolDownload

# 日志
LOG_URL = FileUtil.generate_logfile_url("logs/modis.l3.log")
logger = LogUtil.Logger(LOG_URL)
# 常量
SAVE_DIR = 'F:\Ocean'

# refer to web url
# https://oceancolor.gsfc.nasa.gov/l3/
# key=种类 value=影像值要素
PARAMETERS = {
    'CHL': ['chlor_a'],
    'RRS': ['aot_869']
}


def get_web_url(classification, parameter, year, month, day):
    # https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/CHL/L3/2002/0716/AQUA_MODIS.20020716.L3m.DAY.CHL.chlor_a.4km.nc.png
    return 'https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/' + classification + '/L3/' + year + '/' + month + day \
           + '/AQUA_MODIS.' + year + month + day + '.L3m.DAY.' + classification + '.' + parameter + '.4km.nc.png'


def get_file_path(classification, parameter, year, month, day):
    return f"{SAVE_DIR}\MODIS_AQUA_{classification}_{parameter}\AQUA_MODIS.{year}{month}{day}.L3m.DAY.{classification}.{parameter}.4km.nc.png"


if __name__ == '__main__':
    begin = datetime.date(2013, 1, 1)
    end = datetime.date(2022, 1, 1)

    for k, vs in PARAMETERS.items():
        for v in vs:
            logger.info(f"classification:{k} in parameter:{v} start to download")
            urls = []
            files = []
            for i in range((end - begin).days + 1):
                time = begin + datetime.timedelta(days=i)
                url = get_web_url(k, v, str(time.year), str(time.month), str(time.day))
                file = get_file_path(k, v, str(time.year), str(time.month), str(time.day))
                FileUtil.check_generate_files(file)
                if not FileUtil.exist(file):
                    urls.append(url)
                    files.append(file)

            # #### 用线程池下载 ####
            mtpd = MulThreadPoolDownload()
            mtpd.download(urls, files)

    # urls = getDownloadUrls()
    #
    # #### 用线程池下载 ####
    # mtpd = MulThreadPoolDownload()
    # lst_url = []
    # lst_file = []
    # urls.reverse()
    # for _, url in enumerate(urls):
    #     sub_path = url.replace(BASE_URL, '')
    #     sub_path = sub_path[10:]
    #     file_path = SAVE_DIR + sub_path
    #     FileUtil.check_generate_files(file_path)
    #     if not FileUtil.exist(file_path):
    #         lst_url.append(url)
    #         lst_file.append(file_path)

    exit(0)
