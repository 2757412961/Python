# -*- coding: utf-8 -*-
"""
DataLoaderFunc.py
数据加载模块,用来加载数据
"""

import torch
import torch.nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
import xarray as xr

# CIMPTosLoc = "../TrainData/TosA.nc"
# CIMPZosLoc = "../TrainData/ZosA.nc"
# CIMPNinoLoc = "../TrainData/Cmip6Nino34I.nc"
# OBSTrainSSTALoc = r'D:\GIS\enso\enso_round1_train_20210201\SODA_sst_a.nc'
# OBSTrainSSHALoc = r'D:\GIS\enso\enso_round1_train_20210201\SODA_t300_a.nc'
# OBSTrainNinoLoc = r'D:\GIS\enso\enso_round1_train_20210201\nino34.nc'
OBSTrainSSTALoc = r'/home/zjh/cnm/soda/SODA_sst_a.nc'
OBSTrainSSHALoc = r'/home/zjh/cnm/soda/SODA_t300_a.nc'
OBSTrainNinoLoc = r'/home/zjh/cnm/soda/nino34.nc'


# OBSValSSTALoc = "../ValidationData/ersstv5ssta.nc"
# OBSValSSHALoc = "../ValidationData/GODASssha.nc"
# OBSValNinoLoc = "../ValidationData/ersstv5Nino34.nc"


class ENSODataset(Dataset):
    """
    type_ : 需要加载的数据类型，分为
        CMIP 加载训练数据
        OBSTrain 加载观测数据
        OBSVal 加载观测验证数据
    T_begin 开始时间
    T_end 结束时间
    其中，后两个参数只适用于 CMIP数据
    """

    def __init__(self, type_, T_begin=None, T_end=None):
        super().__init__()
        self.Type = type_
        # if type_ == "CMIP":
        #     self.IniSSTA = xr.open_dataset(CIMPTosLoc)["TosA"].fillna(0)  # 去掉 nan
        #     self.IniSSHA = xr.open_dataset(CIMPZosLoc)["ZosA"].fillna(0)  # 去掉 nan
        #     self.IniNino = xr.open_dataset(CIMPNinoLoc)["Nino34I"]  # 注意开头末尾都为0
        #     if T_begin is not None:
        #         # 选择合适的时间
        #         TimeNeed = (self.IniSSTA["time"].dt.year >= T_begin) & (self.IniSSTA["time"].dt.year <= T_end)
        #         self.IniSSTA = self.IniSSTA[TimeNeed]
        #         self.IniSSHA = self.IniSSHA[TimeNeed]
        #         self.IniNino = self.IniNino[TimeNeed]
        #     self.DataTimeLen = self.IniNino.shape[0]
        if type_ == "OBSTrain":
            SSTA = xr.open_dataset(OBSTrainSSTALoc)["sst"]
            SSHA = xr.open_dataset(OBSTrainSSHALoc)["t300"]
            NINO34 = xr.open_dataset(OBSTrainNinoLoc)["nino"]
            # TimeNeedSSTA = (SSTA["time"].dt.year >= 1871) & (SSTA["time"].dt.year <= 1973)
            # TimeNeedSSHA = (SSHA["time"].dt.year >= 1871) & (SSHA["time"].dt.year <= 1973)
            self.IniSSTA = SSTA[0:1079]
            self.IniSSHA = SSHA[0:1079]
            self.IniNino = NINO34[0:1079]
            self.DataTimeLen = self.IniNino.shape[0]
        elif type_ == "OBSVal":
            SSTA = xr.open_dataset(OBSTrainSSTALoc)["sst"]
            SSHA = xr.open_dataset(OBSTrainSSHALoc)["t300"]
            NINO34 = xr.open_dataset(OBSTrainNinoLoc)["nino"]
            # TimeNeedSSTA = (SSTA["time"].dt.year >= 1984) & (SSTA["time"].dt.year <= 2017)
            # TimeNeedSSHA = (SSHA["time"].dt.year >= 1984) & (SSHA["time"].dt.year <= 2017)
            self.IniSSTA = SSTA[1079:]
            self.IniSSHA = SSHA[1079:]
            self.IniNino = NINO34[1079:]
            self.DataTimeLen = self.IniNino.shape[0]
        else:
            raise ValueError("必须是 CMIP,OBSTrain,OBSVal 其中之一")
        # 及时检查数据的最大值、最小值
        print("数据集名称", type_)
        print("数据最大值:", self.IniSSTA.max().item(), self.IniSSHA.max().item(), self.IniNino.max().item())
        print("数据最小值:", self.IniSSTA.min().item(), self.IniSSHA.min().item(), self.IniNino.min().item())

    def __getitem__(self, index):
        """
        index 指的是 一个样本在 数据集中的索引
        """
        DataX1 = np.array(self.IniSSTA[index:index + 3])
        DataX2 = np.array(self.IniSSHA[index:index + 3])
        DataX = torch.stack((torch.tensor(DataX1, dtype=torch.float32), torch.tensor(DataX2, dtype=torch.float32)), 1)
        DataY = np.array(self.IniNino[index + 3:index + 3 + 23])
        DataY = torch.tensor(DataY, dtype=torch.float32)
        return DataX, DataY

    def __len__(self):
        if self.Type == "CMIP":
            return int(self.DataTimeLen - 3 - 23)  # 开头三个月、末尾 二十四个月，注意到CMIP最后一个月数据为NAN

        else:
            return int(self.DataTimeLen - 3 - 23 + 1)
