import numpy as np
import pandas as pd
import netCDF4 as nc
from netCDF4 import Dataset
import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置

'''
https://blog.csdn.net/weixin_43646592/article/details/113427937
NetCDF(network Common Data Form)网络通用数据格式是一种面向数组型并适于网络共享的数据的描述和编码标准。
目前，NetCDF广泛应用于大气科学、水文、海洋学、环境模拟、地球物理等诸多领域。用户可以借助多种方式方便地管理和操作 NetCDF 数据集。
'''

# 导入（.nc文件）数据集：
nc_path = r'bb3695506m_1_1.nc'
nf = nc.Dataset(nc_path, 'r')

# 直接输出查看nf会比较杂，先直接看下有什么变量：
nf.variables.keys()
'''
输出：
可见这个数据集无非4项数据：纬度，经度，时间，降水量
'''

# 查看一下time的属性
nf.variables['JULD_DESCENDING']
nf.variables['CYCLE_NUMBER']
nf.variables['DRIFT_TEMP']
nf.variables['VELOCITY_ZONAL']
nf.variables['VELOCITY_MERIDIONAL']
'''
输出：
<class ‘netCDF4._netCDF4.Variable’>
float64 time(time)
long_name: Time
units: days since 1800-1-1 00:00:00
delta_t: 0000-01-00 00:00:00
avg_period: 0000-01-00 00:00:00
standard_name: time
axis: T
coordinate_defines: start
actual_range: [33237. 79227.]
unlimited dimensions: time
current shape = (1512,)
filling on, default _FillValue of 9.969209968386869e+36 used
'''

# 查看一下time的数据
nf.variables['JULD_DESCENDING'][:]
'''
输出：
masked_array(data=[33237., 33268., 33296., …, 79166., 79197., 79227.],
mask=False,
fill_value=1e+20)
'''

# 将time转换成时间格式，因为看上面time的属性可以知道：units: days since 1800-1-1 00:00:00
# 是以从1800-1-1 00:00:00的天数累记储存的。
# 用.data直接把masked_array中的data数据读出。
time = nc.num2date(nf.variables['JULD_DESCENDING'][:], 'days since 1800-1-1 00:00:00').data
'''
输出：
array([cftime.DatetimeGregorian(1891, 1, 1, 0, 0, 0, 0),
cftime.DatetimeGregorian(1891, 2, 1, 0, 0, 0, 0),
cftime.DatetimeGregorian(1891, 3, 1, 0, 0, 0, 0), …,
cftime.DatetimeGregorian(2016, 10, 1, 0, 0, 0, 0),
cftime.DatetimeGregorian(2016, 11, 1, 0, 0, 0, 0),
cftime.DatetimeGregorian(2016, 12, 1, 0, 0, 0, 0)], dtype=object)
'''

# 把剩下的数据读出：
lats = nf.variables['lat'][:].data
lons = nf.variables['lon'][:].data
