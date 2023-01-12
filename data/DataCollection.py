# -*- coding: utf-8 -*-
"""
@File  : DataCollection.py
@Author: zjh
@Date  : 2023/1/9
@Update: 2023/1/9
@Desc  :
"""

import numpy as np
import pandas as pd
import netCDF4 as nc
import matplotlib.pyplot as plt
import time as t
import datetime
import config
import data.MODIS.L3.modisl3Download


class EAR5(object):
    def __init__(self, start_time, end_time):
        # # 2003-08-01  # 2003-08-31
        # 一段时间变量集合
        self.data = []
        base_dir = config.DATA_ROOT + "/ERA5"
        for i in range((end_time - start_time).days + 1):
            time = start_time + datetime.timedelta(days=i)
            year = time.strftime("%Y")  # 2003
            month = time.strftime("%m")  # 01
            day = time.strftime("%d")  # 02

            nc_path = base_dir + f"/ERA5_hourly_{year}{month}{day}.nc"
            nf = nc.Dataset(nc_path, 'r')
            # 直接输出查看nf会比较杂，先直接看下有什么变量：
            self.data.append(nf)

    def get(self, day, lat, lon):
        '''
        获取某个时间点（天）下的经纬度网格数据
        lat:-90~90
        lon:-180~180
        u10:'10 metre U wind component'
        v10:'10 metre V wind component'
        msl:'Mean sea level pressure'
        sst:'Sea surface temperature'
        tp:'Total precipitation'
        '''
        nf = self.data[day]
        i = 720 - int((lat + 90) / 180 * 720)
        j = int((lon + 180) / 360 * 1440)
        return nf.variables['u10'][0][i][j], nf.variables['v10'][0][i][j], \
            nf.variables['msl'][0][i][j], nf.variables['sst'][0][i][j], nf.variables['tp'][0][i][j]


class GlobalOceanPhysicsReanalysis(object):
    def __init__(self, start_time, end_time):
        # # 2003-08
        year = start_time.strftime("%Y")  # 2003
        month = start_time.strftime("%m")  # 08
        base_dir = config.DATA_ROOT + "/CMEMS/Global Ocean Physics Reanalysis"
        nc_path = base_dir + f"/MULTIOBS_GLO_BIO_CARBON_SURFACE_REP_{year}_{month}.nc"
        nf = nc.Dataset(nc_path, 'r')
        # 直接输出查看nf会比较杂，先直接看下有什么变量：
        self.data = nf

    def get(self, day, lat, lon):
        '''
        获取某个时间点（天）下的经纬度网格数据
        lat:-90~90
        lon:-180~180
        mlotst:'Density ocean mixed layer thickness'
        sithick:'Sea ice thickness'
        zos:'Sea surface height'
        '''
        nf = self.data
        i = int((lat + 80) / 170 * 2040)
        j = int((lon + 180) / 360 * 4320)
        return nf.variables['mlotst'][day][i][j], nf.variables['sithick'][day][i][j], nf.variables['zos'][day][i][j]


class OceanColor(object):
    def __init__(self, start_time, end_time):
        # # 2003-08-01  # 2003-08-31
        # 一段时间变量集合
        print(t.strftime('%Y-%m-%d %H:%M:%S', t.localtime(t.time())))
        self.days = (end_time - start_time).days + 1
        self.data = {}
        for k, vs in data.MODIS.L3.modisl3Download.PARAMETERS.items():
            for v in vs:
                # logger.info(f"{year}-{month}-{day}:classification:{k} in parameter:{v} start to train")
                values = []
                for i in range((end_time - start_time).days + 1):
                    time = start_time + datetime.timedelta(days=i)
                    year = time.strftime("%Y")  # 2003
                    month = time.strftime("%m")  # 01
                    day = time.strftime("%d")  # 02

                    file_path = data.MODIS.L3.modisl3Download.get_file_path_daily_png(k, v, year, month, day)
                    im = plt.imread(file_path)
                    im_gray = 0.299 * im[:, :, 0] + 0.587 * im[:, :, 1] + 0.114 * im[:, :, 2]  # 灰度化
                    values.append(im_gray)
                    print(f"{year}-{month}-{day}:classification:{k} in parameter:{v}")
                self.data[v] = np.array(values, dtype="float16")
        print(t.strftime('%Y-%m-%d %H:%M:%S', t.localtime(t.time())))
        print()

    def get(self, day, lat, lon):
        '''
        获取某个时间点（天）下的经纬度网格数据
        lat:-90~90
        lon:-180~180
        '''
        data = self.data
        i = 4320 - int((lat + 90) / 180 * 4320)
        j = int((lon + 180) / 360 * 8640)
        # return data['chlor_a'][day][i][j], data['Kd_490'][day][i][j], data['poc'][day][i][j], \
        #     data['pic'][day][i][j], data['sst'][day][i][j], data['bbp_443'][day][i][j], \
        #     data['Rrs_412'][day][i][j], data['Rrs_443'][day][i][j], data['Rrs_469'][day][i][j], \
        #     data['Rrs_488'][day][i][j], data['Rrs_531'][day][i][j], data['Rrs_547'][day][i][j], \
        #     data['Rrs_555'][day][i][j], data['Rrs_667'][day][i][j], data['Rrs_678'][day][i][j]
        return self.find('chlor_a', day, i, j), self.find('Kd_490', day, i, j), self.find('poc', day, i, j), \
            self.find('pic', day, i, j), self.find('sst', day, i, j), self.find('bbp_443', day, i, j), \
            self.find('Rrs_412', day, i, j), self.find('Rrs_443', day, i, j), self.find('Rrs_469', day, i, j), \
            self.find('Rrs_488', day, i, j), self.find('Rrs_531', day, i, j), self.find('Rrs_547', day, i, j), \
            self.find('Rrs_555', day, i, j), self.find('Rrs_667', day, i, j), self.find('Rrs_678', day, i, j)

    def find(self, key, day, lat, lon):
        for step in range(7):
            # 往前后个寻找7天，如果找不到就返回空值
            if day - step >= 0 and self.data[key][day - step][lat][lon] != 0:
                return self.data[key][day - step][lat][lon]
            if day + step < self.days and self.data[key][day + step][lat][lon] != 0:
                return self.data[key][day + step][lat][lon]
        return -9999


if __name__ == '__main__':
    ear = EAR5(datetime.date(2004, 1, 1), datetime.date(2004, 1, 31))
    ear.get(12, 49.23, 123.8784)
    ear.get(12, -49.23, 123.8784)
    ear.get(12, 49.23, -123.8784)
    ear.get(12, -49.23, -123.8784)

    gopr = GlobalOceanPhysicsReanalysis(datetime.date(2004, 1, 1), datetime.date(2004, 1, 31))
    gopr.get(12, 49.23, 123.8784)
    gopr.get(12, -49.23, 123.8784)
    gopr.get(12, 49.23, -123.8784)
    gopr.get(12, -49.23, -123.8784)

    oc = OceanColor(datetime.date(2004, 1, 1), datetime.date(2004, 1, 3))
    oc.get(2, 49.23, 123.8784)
    oc.get(2, -49.23, 123.8784)
    oc.get(2, 49.23, -123.8784)
    oc.get(2, -49.23, -123.8784)
