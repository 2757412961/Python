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
# SAVE_DIR = 'F:/Ocean'
SAVE_DIR = '/home/zjh/Ocean'


def get_web_url_png(classification, parameter, year, month, day):
    # https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/CHL/L3/2002/0716/AQUA_MODIS.20020716.L3m.DAY.CHL.chlor_a.4km.nc.png
    return f'https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/{classification}/L3/{year}/{month}{day}' \
           f'/AQUA_MODIS.{year}{month}{day}.L3m.DAY.{classification}.{parameter}.4km.nc.png'


def get_file_path_png(classification, parameter, year, month, day):
    # https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/CHL/L3/2002/0716/AQUA_MODIS.20020716.L3m.DAY.CHL.chlor_a.4km.nc.png
    return f'{SAVE_DIR}/MODIS_AQUA_{classification}_{parameter}' \
           f'/AQUA_MODIS.{year}{month}{day}.L3m.DAY.{classification}.{parameter}.4km.nc.png'


def get_web_url(classification, parameter, year, month, day):
    # https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/AQUA_MODIS.20020719.L3m.DAY.CHL.chlor_a.4km.nc
    return f'https://oceandata.sci.gsfc.nasa.gov/cgi/getfile' \
           f'/AQUA_MODIS.{year}{month}{day}.L3m.DAY.{classification}.{parameter}.4km.nc'


def get_file_path(classification, parameter, year, month, day):
    # https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/AQUA_MODIS.20020719.L3m.DAY.CHL.chlor_a.4km.nc
    return f'{SAVE_DIR}/MODIS_AQUA_{classification}_{parameter}' \
           f'/AQUA_MODIS.{year}{month}{day}.L3m.DAY.{classification}.{parameter}.4km.nc'


# refer to web url
# https://oceancolor.gsfc.nasa.gov/l3/
# key=种类 value=影像值要素
PARAMETERS = {
    'CHL': ['chlor_a'],
    'FLH': ['ipar'],
    'KD': ['Kd_490'],
    'PAR': ['par'],
    'POC': ['poc'],
    'PIC': ['pic'],
    'SST': ['sst'],
    'SST4': ['sst4'],
    'IOP': [
        'bbp_443',
        'a_412',
        'a_443',
        'a_469',
        'a_488',
        'a_531',
        'a_547',
        'a_555',
        'a_667',
        'a_678'],
    'RRS': [
        'aot_869',
        'Rrs_412',
        'Rrs_443',
        'Rrs_469',
        'Rrs_488',
        'Rrs_531',
        'Rrs_547',
        'Rrs_555',
        'Rrs_667',
        'Rrs_678']
}

if __name__ == '__main__':
    begin = datetime.date(2003, 1, 1)
    end = datetime.date(2022, 1, 1)

    for k, vs in PARAMETERS.items():
        for v in vs:
            logger.info(f"classification:{k} in parameter:{v} start to download")
            urls = []
            files = []
            for i in range((end - begin).days + 1):
                time = begin + datetime.timedelta(days=i)
                year = time.strftime("%Y")
                month = time.strftime("%m")
                day = time.strftime("%d")
                url = get_web_url_png(k, v, year, month, day)
                file = get_file_path_png(k, v, year, month, day)
                FileUtil.check_generate_files(file)
                if not FileUtil.exist(file):
                    urls.append(url)
                    files.append(file)

            # #### 用线程池下载 ####
            mtpd = MulThreadPoolDownload()
            mtpd.download(urls, files)

    exit(0)
