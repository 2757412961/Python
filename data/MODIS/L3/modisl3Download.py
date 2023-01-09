# -*- coding: utf-8 -*-
# @File  : modisl3Download.py
# @Author: Zjh
# @Date  : 2022/11/27
# @Update: 2022/11/27
# @Desc  :

import os
import datetime
import pandas as pd
import config
from utils import LogUtil
from utils import FileUtil
from utils.MultiDownload import MulThreadDownload, MulThreadConcurrentDownload, MulThreadPoolDownload

# 日志
LOG_URL = FileUtil.generate_logfile_url("logs/modis.l3.download.log")
logger = LogUtil.Logger(LOG_URL)
# 常量
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


# Modis L3 png 每日数据Url和文件Path
def get_web_url_daily_png(classification, parameter, year, month, day):
    # https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/CHL/L3/2002/0716/AQUA_MODIS.20020716.L3m.DAY.CHL.chlor_a.4km.nc.png
    return f'https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/{classification}/L3/{year}/{month}{day}' \
           f'/AQUA_MODIS.{year}{month}{day}.L3m.DAY.{classification}.{parameter}.4km.nc.png'


def get_file_path_daily_png(classification, parameter, year, month, day):
    # {SAVE_DIR}/MODIS_AQUA_CHL_chlor_a/IMAGES/AQUA_MODIS.20020716.L3m.DAY.CHL.chlor_a.4km.nc.png
    return f'{config.DATA_ROOT}/MODIS_AQUA_{classification}_{parameter}' \
           f'/AQUA_MODIS.{year}{month}{day}.L3m.DAY.{classification}.{parameter}.4km.nc.png'


# Modis L3 png 每月数据Url和文件Path
def get_web_url_monthly_png(classification, parameter, year, month, day, start_date, end_date):
    # https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/POC/L3/2003/0701/AQUA_MODIS.20030701_20030731.L3m.MO.POC.poc.4km.nc.png
    return f'https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/{classification}/L3/{year}/{month}{day}' \
           f'/AQUA_MODIS.{start_date}_{end_date}.L3m.MO.{classification}.{parameter}.4km.nc.png'


def get_file_path_monthly_png(classification, parameter, year, month, day, start_date, end_date):
    # {SAVE_DIR}/MODIS_AQUA_POC_poc/IMAGES/AQUA_MODIS.200307.L3m.MO.POC.poc.4km.nc.png
    return f'{config.DATA_ROOT}/MODIS_AQUA_{classification}_{parameter}' \
           f'/AQUA_MODIS.{year}{month}.L3m.MO.{classification}.{parameter}.4km.nc.png'


# Modis L3 nc 每日数据Url和文件Path
def get_web_url_daily_nc(classification, parameter, year, month, day):
    # https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/AQUA_MODIS.20020719.L3m.DAY.CHL.chlor_a.4km.nc
    return f'https://oceandata.sci.gsfc.nasa.gov/cgi/getfile' \
           f'/AQUA_MODIS.{year}{month}{day}.L3m.DAY.{classification}.{parameter}.4km.nc'


def get_file_path_daily_nc(classification, parameter, year, month, day):
    # https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/AQUA_MODIS.20020719.L3m.DAY.CHL.chlor_a.4km.nc
    return f'{config.DATA_ROOT}/MODIS_AQUA_{classification}_{parameter}' \
           f'/AQUA_MODIS.{year}{month}{day}.L3m.DAY.{classification}.{parameter}.4km.nc'


def download_daily(begin=datetime.date(1, 1, 1), end=datetime.date(1, 1, 1), params={}):
    '''
    下载 Modis L3 级别的每日数据
    :param begin: 起始日期
    :param end: 终止日期
    :param params: 下载参数
    :return:
    '''
    for k, vs in params.items():
        for v in vs:
            logger.info(f"classification:{k} in parameter:{v} start to download")
            urls = []
            files = []
            for i in range((end - begin).days + 1):
                time = begin + datetime.timedelta(days=i)
                year = time.strftime("%Y")
                month = time.strftime("%m")
                day = time.strftime("%d")
                url = get_web_url_daily_nc(k, v, year, month, day)
                file = get_file_path_daily_nc(k, v, year, month, day)
                FileUtil.check_generate_files(file)
                # if FileUtil.exist(file):
                #     os.remove(file)
                if not FileUtil.exist(file):
                    urls.append(url)
                    files.append(file)

            # #### 用线程池下载 ####
            mtpd = MulThreadPoolDownload()
            mtpd.download(urls, files)


def download_monthly(begin=datetime.date(1, 1, 1), end=datetime.date(1, 1, 1), params={}):
    '''
    下载 Modis L3 级别的每月数据
    :param begin: 起始日期
    :param end: 终止日期
    :param params: 下载参数
    :return:
    '''
    periods = (end.year - begin.year) * 12 + (end.month - begin.month)
    time_series = pd.period_range(begin, periods=periods, freq='M')
    for k, vs in params.items():
        for v in vs:
            logger.info(f"classification:{k} in parameter:{v} start to download")
            urls = []
            files = []
            for t in time_series:  # 2003-08
                start_time = t.start_time  # 2003-08-01
                end_time = t.end_time  # 2003-08-31
                ############################################
                year = start_time.strftime("%Y")  # 2003
                month = start_time.strftime("%m")  # 01
                day = start_time.strftime("%d")  # 01
                start_date = start_time.strftime("%Y%m%d")
                end_date = end_time.strftime("%Y%m%d")
                ############################################
                url = get_web_url_monthly_png(k, v, year, month, day, start_date, end_date)
                file = get_file_path_monthly_png(k, v, year, month, day, start_date, end_date)
                FileUtil.check_generate_files(file)
                if not FileUtil.exist(file):
                    urls.append(url)
                    files.append(file)

            # #### 用线程池下载 ####
            mtpd = MulThreadPoolDownload()
            mtpd.download(urls, files)


if __name__ == '__main__':
    begin_date = datetime.date(2003, 1, 1)
    end_date = datetime.date(2022, 1, 1)

    ###################
    # 下载每日Modis数据 #
    ###################
    download_daily(begin_date, end_date, PARAMETERS)

    ###################
    # 下载每月Modis数据 #
    ###################
    # download_monthly(begin_date, end_date, PARAMETERS)

    exit(0)
