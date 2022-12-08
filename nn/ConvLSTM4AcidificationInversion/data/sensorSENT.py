# -*- coding: utf-8 -*-
# @File  : sensor.py
# @Author: Zjh
# @Date  : 2022/12/6
# @Update: 2022/12/6
# @Desc  : 遥感卫星数据集，主要包含数据有：FLH叶绿素、KD反射系数、POC、PIC有机碳、SST温度、IOP吸收系数、RRS遥感反射率

import os
import math
import time
import gzip
import random
import datetime

import numpy
import numpy as np
import transformers.utils
from PIL import Image
import matplotlib.pyplot as plt
import netCDF4 as nc
from netCDF4 import Dataset
import torch
import torchvision.transforms as transforms

from utils import FileUtil, LogUtil

# 日志
LOG_URL = FileUtil.generate_logfile_url("logs/convLstm.sensor.log")
logger = LogUtil.Logger(LOG_URL)
PARAMETERS = {
    'FLH': ['ipar'],
    'KD': ['Kd_490'],
    'PAR': ['par'],
    'POC': ['poc'],
    'PIC': ['pic'],
    'SST': ['sst'],
    'SST4': ['sst4'],
    'IOP': [
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


class SensorDataset(torch.utils.data.Dataset):
    def __init__(self, root, start_date, end_date, n_frames_input, n_frames_output, data_type):
        self.root = root
        self.begin = start_date
        self.end = end_date
        self.n_frames_input = n_frames_input  # seq 长度
        self.n_frames_output = n_frames_output  # seq 长度
        self.n_frames_total = self.n_frames_input + self.n_frames_output
        self.data_type = data_type
        props = {
            'train': 0.8,
            'valid': 0.1,
            'test': 0.1
        }
        total = (end_date - start_date).days
        if data_type == 'train':
            self.begin = start_date
        elif data_type == 'valid':
            self.begin = start_date + datetime.timedelta(days=total * props['train'])
        elif data_type == 'test':
            self.begin = start_date + datetime.timedelta(days=total * (props['train'] + props['valid']))
        self.end = self.begin + datetime.timedelta(days=total * props[data_type])
        self.transform = transforms.ToTensor()

    def __getitem__(self, index):
        input = []
        output = []
        for i in range(self.n_frames_input):
            time = self.begin + datetime.timedelta(days=index + i)
            year = time.strftime("%Y")
            month = time.strftime("%m")
            day = time.strftime("%d")

            # 输入
            src_list = []
            for k, vs in PARAMETERS.items():
                for v in vs:
                    # logger.info(f"{year}-{month}-{day}:classification:{k} in parameter:{v} start to train")
                    file_path = self.get_file_path_png(k, v, year, month, day)
                    # 读取图像
                    # H,W,C
                    im = plt.imread(file_path)
                    # 灰度化
                    # H,W
                    im_gray = 0.299 * im[:, :, 0] + 0.587 * im[:, :, 1] + 0.114 * im[:, :, 2]
                    # H,W,C
                    src_list.append(im_gray)
                    # print(f'max:{np.max(im)},min:{np.min(im)},val:{np.sum(im > 0)}/{im.size}')
            # 输出
            tar_list = []
            for k, vs in {'CHL': ['chlor_a']}.items():
                for v in vs:
                    file_path = self.get_file_path_png(k, v, year, month, day)
                    # 读取图像
                    # H,W,C
                    im = plt.imread(file_path)
                    # 灰度化
                    # H,W
                    im_gray = 0.299 * im[:, :, 0] + 0.587 * im[:, :, 1] + 0.114 * im[:, :, 2]
                    # C,H,W
                    tar_list.append(im_gray)

            # input.append(np.concatenate(src_list, axis=2).transpose((2, 0, 1)))
            # output.append(np.concatenate(tar_list, axis=2).transpose((2, 0, 1)))
            # S,C,H,W
            input.append(src_list)
            output.append(tar_list)
        # B,S,C,H,W
        return [index, torch.from_numpy(np.array(input)), torch.from_numpy(np.array(output))]

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

    train = SensorDataset(
        root='/home/zjh/Ocean',
        start_date=begin,
        end_date=end,
        n_frames_input=1,
        n_frames_output=1,
        data_type='train'
    )
    print(train.begin, train.end)
    print(len(train))
    print(train[523][1].size())

    valid = SensorDataset(
        root='/home/zjh/Ocean',
        start_date=begin,
        end_date=end,
        n_frames_input=10,
        n_frames_output=10,
        data_type='valid'
    )
    print(valid.begin, valid.end)
    print(len(valid))
    print(valid[523][1].size())

    test = SensorDataset(
        root='/home/zjh/Ocean',
        start_date=begin,
        end_date=end,
        n_frames_input=10,
        n_frames_output=10,
        data_type='test'
    )
    print(test.begin, test.end)
    print(len(test))
    print(test[523][1].size())
