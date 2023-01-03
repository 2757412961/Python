# -*- coding: utf-8 -*-
import numpy as np
from torch.utils.data import DataLoader
import xarray as xr
from netCDF4 import Dataset
import torch
import datetime
import scipy.stats as sps
# from DataLoaderFunc import ENSODataset
from torch.utils.data import DataLoader
import pickle
from CNNClass import ConvNetwork

"""
only use past 3 month soda SST to predict future 23 month nino index. 
Considering SODA.shape = (100,36,:,:) , so SST has 102 years, which equals to 1224 months:
total_time_sequence = 1224 -3 -23 +1 = 1199
train_sequence = 1199 *0.9 = 1079
valid_sequence = 1199 *0.1 = 120
"""
soda_label_path = r'D:\GIS\enso\enso_round1_train_20210201\SODA_label.nc'
soda_train_path = r'D:\GIS\enso\enso_round1_train_20210201\SODA_train.nc'
soda_label_nc = Dataset(soda_label_path)
soda_train_nc = Dataset(soda_train_path)
NINO = soda_label_nc.variables['nino'][:]
SST = soda_train_nc.variables['sst'][:]
T300 = soda_train_nc.variables['t300'][:]
lat = soda_train_nc.variables['lat'][:]
lon = soda_train_nc.variables['lon'][:]
"""
Transform (100,36,lat,lon) shape to (1200,lat,lon) shape
"""
sequence_SST = []
sequence_NINO = []
sequence_T300 = []
for year_index in range(100):
    if year_index == 99:
        NINO_year = NINO[year_index, :36]
        SST_year = SST[year_index, :36, :]
        T300_year = T300[year_index, :36, :]
        sequence_SST.append(SST_year[:12, :])
        sequence_NINO.append(NINO_year[:12])
        sequence_T300.append(T300_year[:12])
        sequence_SST.append(SST_year[12:24, :])
        sequence_NINO.append(NINO_year[12:24])
        sequence_T300.append(T300_year[12:24])
        sequence_SST.append(SST_year[24:36, :])
        sequence_NINO.append(NINO_year[24:36])
        sequence_T300.append(T300_year[24:36])
    else:
        NINO_year = NINO[year_index, :12]
        SST_year = SST[year_index, :12, :]
        T300_year = T300[year_index, :12, :]
        sequence_SST.append(SST_year)
        sequence_NINO.append(NINO_year)
        sequence_T300.append(T300_year)

sequence_SST = np.array(sequence_SST).reshape(-1, 24, 72)  # (1224,24,72)
sequence_T300 = np.array(sequence_T300).reshape(-1, 24, 72)  # (1224,24,72)
sequence_NINO = np.array(sequence_NINO).reshape(-1, )  # (1224)

sequence_SST_nc_path = r'D:\GIS\enso\enso_round1_train_20210201\SODA_sst_a.nc'
sequence_T300_nc_path = r'D:\GIS\enso\enso_round1_train_20210201\SODA_t300_a.nc'
sequence_NINO_nc_path = r'D:\GIS\enso\enso_round1_train_20210201\nino34.nc'

sequence_SST_nc = Dataset(sequence_SST_nc_path, 'w')
sequence_SST_nc.createDimension('time', 1224)
sequence_SST_nc.createDimension('lat', 24)
sequence_SST_nc.createDimension('lon', 72)
sequence_SST_nc.createVariable('time', 'd', ('time'))
sequence_SST_nc.createVariable('lat', 'd', ('lat'))
sequence_SST_nc.createVariable('lon', 'd', ('lon'))
sequence_SST_nc.createVariable('sst', 'f', ('time', 'lat', 'lon'), fill_value=-9.99E33)
sequence_SST_nc.variables['time'][:] = np.arange(0, 1224, 1) + 1
sequence_SST_nc.variables['lat'][:] = lat
sequence_SST_nc.variables['lon'][:] = lon
sequence_SST_nc.variables['sst'][:] = sequence_SST

sequence_T300_nc = Dataset(sequence_T300_nc_path, 'w')
sequence_T300_nc.createDimension('time', 1224)
sequence_T300_nc.createDimension('lat', 24)
sequence_T300_nc.createDimension('lon', 72)
sequence_T300_nc.createVariable('time', 'd', ('time'))
sequence_T300_nc.createVariable('lat', 'd', ('lat'))
sequence_T300_nc.createVariable('lon', 'd', ('lon'))
sequence_T300_nc.createVariable('t300', 'f', ('time', 'lat', 'lon'), fill_value=-9.99E33)
sequence_T300_nc.variables['time'][:] = np.arange(0, 1224, 1) + 1
sequence_T300_nc.variables['lat'][:] = lat
sequence_T300_nc.variables['lon'][:] = lon
sequence_T300_nc.variables['t300'][:] = sequence_T300

sequence_NINO_nc = Dataset(sequence_NINO_nc_path, 'w')
sequence_NINO_nc.createDimension('time', 1224)
sequence_NINO_nc.createVariable('time', 'd', ('time'))
sequence_NINO_nc.createVariable('nino', 'f', ('time'), fill_value=-9.99E33)
sequence_NINO_nc.variables['time'][:] = np.arange(0, 1224, 1) + 1
sequence_NINO_nc.variables['nino'][:] = sequence_NINO

# sequence_len = 1224 - 3 - 23 + 1
# train_X = []
# train_Y = []
# for time_index in range(sequence_len):
#     past_X = sequence_SST[time_index:time_index + 3, :]
#     # past_Y = sequence_Y[time_index:time_index+3,:]
#     # future_X = sequence_X[time_index+3:time_index+26]
#     future_Y = sequence_NINO[time_index + 3:time_index + 26]
#
#     train_X.append(past_X)
#     train_Y.append(future_Y)
#
# train_X = np.array(train_X)  # (1199,3,24,72)
# train_Y = np.array(train_Y)  # (1199,23)
#
# train_len = int(sequence_len * 0.9)  # 1079
#
# valid_X = train_X[train_len:, :]  # (120,3,24,72)
# valid_Y = train_Y[train_len:]  # (120,23)
# train_X = train_X[:train_len, :]  # (1079,3,24,72)
# train_Y = train_Y[:train_len]  # (1079,23)
# print(train_Y.shape)
# print(train_X.shape)
# valid_X_path = r'D:\GIS\enso\enso_round1_train_20210201\valid_X.nc'
# valid_Y_path = r'D:\GIS\enso\enso_round1_train_20210201\valid_Y.nc'
# train_X_path = r'D:\GIS\enso\enso_round1_train_20210201\train_X.nc'
# train_Y_path = r'D:\GIS\enso\enso_round1_train_20210201\train_Y.nc'
#
# np.save(valid_X_path, valid_X)
# np.save(valid_Y_path, valid_Y)
# np.save(train_X_path, train_X)
# np.save(train_Y_path, train_Y)
