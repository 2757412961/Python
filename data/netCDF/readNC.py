# -*- coding: utf-8 -*-
# @File  : readNC.py
# @Author: Zjh
# @Date  : 2022/11/27
# @Update: 2022/11/27
# @Desc  :
import netCDF4

if __name__ == '__main__':
    nc_file = netCDF4.Dataset('F:\Ocean\JMA_Ocean_CO2_Map\JMA_co2map_1990.nc')
    print(nc_file)

    # 查看nc文件中的变量
    print(nc_file.variables.keys())

    # 查看变量的信息
    print(nc_file.variables['CHL_OC4ME'])

    # 查看每个变量的属性
    print(nc_file.variables['CHL_OC4ME'].ncattrs())

    # 读取nc文件数据值
    lat = nc_file.variables['CHL_OC4ME'][:]

    print(lat)