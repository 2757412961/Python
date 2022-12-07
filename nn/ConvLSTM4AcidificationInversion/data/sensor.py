# -*- coding: utf-8 -*-
# @File  : sensor.py
# @Author: Zjh
# @Date  : 2022/12/6
# @Update: 2022/12/6
# @Desc  :

import os
import math
import time
import gzip
import random
import datetime

import numpy
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import netCDF4 as nc
from netCDF4 import Dataset
import torch
import torchvision.transforms as transforms

from utils import FileUtil, LogUtil

# 日志
LOG_URL = FileUtil.generate_logfile_url("logs/convLstm.main.log")
logger = LogUtil.Logger(LOG_URL)
PARAMETERS = {
    'FLH': ['ipar'],
    'KD': ['Kd_490'],
    # 'PAR': ['par'],
    # 'POC': ['poc'],
    # 'PIC': ['pic'],
    # 'SST': ['sst'],
    # 'SST4': ['sst4'],
    # 'IOP': [
    #     'a_412',
    #     'a_443',
    #     'a_469',
    #     'a_488',
    #     'a_531',
    #     'a_547',
    #     'a_555',
    #     'a_667',
    #     'a_678'],
    # 'RRS': [
    #     'aot_869',
    #     'Rrs_412',
    #     'Rrs_443',
    #     'Rrs_469',
    #     'Rrs_488',
    #     'Rrs_531',
    #     'Rrs_547',
    #     'Rrs_555',
    #     'Rrs_667',
    #     'Rrs_678']
}


class SensorDataset(torch.utils.data.Dataset):
    def __init__(self, root, start_date, end_date, data_type):
        self.root = root
        self.begin = start_date
        self.end = end_date
        self.transform = transforms.ToTensor()
        self.props = {
            'train': 0.8,
            'valid': 0.1,
            'test': 0.1
        }
        self.data_type = data_type
        total = (self.end - self.begin).days
        if data_type == 'train':
            self.begin = self.begin
        elif data_type == 'valid':
            self.begin = self.begin + datetime.timedelta(days=total * self.props['train'])
        elif data_type == 'test':
            self.begin = self.begin + datetime.timedelta(days=total * (self.props['train'] + self.props['valid']))
        self.end = self.begin + datetime.timedelta(days=total * self.props[data_type])

    def __getitem__(self, index):
        time = self.begin + datetime.timedelta(days=index)
        year = time.strftime("%Y")
        month = time.strftime("%m")
        day = time.strftime("%d")

        # 输入
        src_list = []
        for k, vs in PARAMETERS.items():
            for v in vs:
                logger.info(f"classification:{k} in parameter:{v} start to train")
                file_path = self.get_file_path_png(k, v, year, month, day)
                img_plt = plt.imread(file_path)
                src_list.append(img_plt[..., 0:3])

        # 输出
        tar_list = []
        for k, vs in {'CHL': ['chlor_a']}.items():
            for v in vs:
                file_path = self.get_file_path_png(k, v, year, month, day)
                img_plt = plt.imread(file_path)
                tar_list.append(img_plt[..., 0:3])

        src = np.concatenate(src_list, axis=2)
        tar = np.concatenate(tar_list, axis=2)
        return self.transform(src), self.transform(tar)

    def __len__(self):
        return (self.end - self.begin).days

    def get_file_path_png(self, classification, parameter, year, month, day):
        # https://oceancolor.gsfc.nasa.gov/showimages/MODISA/IMAGES/CHL/L3/2002/0716/AQUA_MODIS.20020716.L3m.DAY.CHL.chlor_a.4km.nc.png
        return f'{self.root}/MODIS_AQUA_{classification}_{parameter}' \
               f'/AQUA_MODIS.{year}{month}{day}.L3m.DAY.{classification}.{parameter}.4km.nc.png'


if __name__ == '__main__':
    ##################
    begin = datetime.date(2003, 1, 1)
    end = datetime.date(2022, 1, 1)

    train = SensorDataset('/home/zjh/Ocean', begin, end, 'train')
    print(train.begin, train.end)
    print(len(train))

    valid = SensorDataset('/home/zjh/Ocean', begin, end, 'valid')
    print(valid.begin, valid.end)
    print(len(valid))

    test = SensorDataset('/home/zjh/Ocean', begin, end, 'test')
    print(test.begin, test.end)
    print(len(test))

    print(train[523])
    print(valid[523])
    print(test[523])
