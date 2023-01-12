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
    def __init__(self, year, month, day):
        # 2003-08-31
        time = datetime.date(int(year), int(month), int(day))
        year = time.strftime("%Y")  # 2003
        month = time.strftime("%m")  # 01
        day = time.strftime("%d")  # 02

        base_dir = config.DATA_ROOT + "/ERA5"
        nc_path = base_dir + f"/ERA5_hourly_{year}{month}{day}.nc"
        self.data = nc.Dataset(nc_path, 'r')

    def get(self, lat, lon):
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
        nf = self.data
        i = 720 - int((lat + 90) / 180 * 720)
        j = int((lon + 180) / 360 * 1440)
        return nf.variables['u10'][0][i][j], nf.variables['v10'][0][i][j], \
            nf.variables['msl'][0][i][j], nf.variables['sst'][0][i][j], nf.variables['tp'][0][i][j]


class GlobalOceanPhysicsReanalysis(object):
    def __init__(self, year, month, day):
        # 2003-08-31
        time = datetime.date(int(year), int(month), int(day))
        year = time.strftime("%Y")  # 2003
        month = time.strftime("%m")  # 01
        day = time.strftime("%d")  # 02

        base_dir = config.DATA_ROOT + "/CMEMS/Global Ocean Physics Reanalysis"
        nc_path = base_dir + f"/MULTIOBS_GLO_BIO_CARBON_SURFACE_REP_{year}_{month}.nc"
        self.data = nc.Dataset(nc_path, 'r')
        self.day = int(day) - 1  # 每个月的第i天，转下标

    def get(self, lat, lon):
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
        return nf.variables['mlotst'][self.day][i][j], \
            nf.variables['sithick'][self.day][i][j], \
            nf.variables['zos'][self.day][i][j]


class OceanColor(object):
    def __init__(self, year, month, day):
        # 2003-08-31
        time = datetime.date(int(year), int(month), int(day))
        year = time.strftime("%Y")  # 2003
        month = time.strftime("%m")  # 01
        day = time.strftime("%d")  # 02

        print(t.strftime('%Y-%m-%d %H:%M:%S', t.localtime(t.time())))
        self.data = {}
        for k, vs in data.MODIS.L3.modisl3Download.PARAMETERS.items():
            for v in vs:
                print(f"{year}-{month}-{day}:classification:{k} in parameter:{v}")
                file_path = data.MODIS.L3.modisl3Download.get_file_path_daily_png(k, v, year, month, day)
                im = plt.imread(file_path)
                im_gray = 0.299 * im[:, :, 0] + 0.587 * im[:, :, 1] + 0.114 * im[:, :, 2]  # 灰度化
                self.data[v] = np.array(im_gray, dtype="float16")
        print(t.strftime('%Y-%m-%d %H:%M:%S', t.localtime(t.time())))

    def get(self, lat, lon):
        '''
        获取某个时间点（天）下的经纬度网格数据
        lat:-90~90
        lon:-180~180
        '''
        im_gray = self.data
        i = 4320 - int((lat + 90) / 180 * 4320)
        j = int((lon + 180) / 360 * 8640)
        # return data['chlor_a'][day][i][j], data['Kd_490'][day][i][j], data['poc'][day][i][j], \
        #     data['pic'][day][i][j], data['sst'][day][i][j], data['bbp_443'][day][i][j], \
        #     data['Rrs_412'][day][i][j], data['Rrs_443'][day][i][j], data['Rrs_469'][day][i][j], \
        #     data['Rrs_488'][day][i][j], data['Rrs_531'][day][i][j], data['Rrs_547'][day][i][j], \
        #     data['Rrs_555'][day][i][j], data['Rrs_667'][day][i][j], data['Rrs_678'][day][i][j]
        return self.find('chlor_a', i, j), self.find('Kd_490', i, j), self.find('poc', i, j), \
            self.find('pic', i, j), self.find('sst', i, j), self.find('bbp_443', i, j), \
            self.find('Rrs_412', i, j), self.find('Rrs_443', i, j), self.find('Rrs_469', i, j), \
            self.find('Rrs_488', i, j), self.find('Rrs_531', i, j), self.find('Rrs_547', i, j), \
            self.find('Rrs_555', i, j), self.find('Rrs_667', i, j), self.find('Rrs_678', i, j)

    def find(self, key, lat, lon):
        if self.data[key][lat][lon] != 0:
            return self.data[key][lat][lon]
        # for step in range(7):
        #     # 往前后个寻找7天，如果找不到就返回空值
        #     if day - step >= 0 and self.data[key][day - step][lat][lon] != 0:
        #         return self.data[key][day - step][lat][lon]
        #     if day + step < self.days and self.data[key][day + step][lat][lon] != 0:
        #         return self.data[key][day + step][lat][lon]
        return -9999


if __name__ == '__main__':
    print("=====================================================================================================")
    ear = EAR5(2004, 1, 1)
    print(ear.get(49.23, 123.8784))
    print(ear.get(-49.23, 123.8784))
    print(ear.get(49.23, -123.8784))
    print(ear.get(-49.23, -123.8784))

    print("=====================================================================================================")
    gopr = GlobalOceanPhysicsReanalysis(2004, 1, 1)
    print(gopr.get(49.23, 123.8784))
    print(gopr.get(-49.23, 123.8784))
    print(gopr.get(49.23, -123.8784))
    print(gopr.get(-49.23, -123.8784))

    print("=====================================================================================================")
    oc = OceanColor(2004, 1, 1)
    print(oc.get(49.23, 123.8784))
    print(oc.get(-49.23, 123.8784))
    print(oc.get(49.23, -123.8784))
    print(oc.get(-49.23, -123.8784))
