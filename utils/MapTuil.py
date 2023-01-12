# -*- coding: utf-8 -*-
"""
@File  : MapTuil.py
@Author: zjh
@Date  : 2023/1/11
@Update: 2023/1/11
@Desc  :
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import numpy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import pandas as pd
import numpy as np

mpl.rcParams["font.family"] = 'Arial'  # 默认字体类型
mpl.rcParams["mathtext.fontset"] = 'cm'  # 数学文字字体
mpl.rcParams["font.size"] = 13


def map_Robinson_coastlines():
    # set projection
    ax = plt.axes(projection=ccrs.Robinson(central_longitude=150))
    # plot coastlines & gridlines
    ax.coastlines()
    ax.gridlines(linestyle='--')
    plt.show()


def map_PlateCarree_coastlines():
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    plt.show()


def map_Mollweide_stock():
    ax = plt.axes(projection=ccrs.Mollweide())
    ax.stock_img()
    plt.show()


def main_points():
    # 3.3 建立画布，绘制地图
    # set projection
    ax = plt.axes(projection=ccrs.Robinson())
    # plot coastlines & gridlines
    ax.coastlines()
    ax.gridlines(linestyle='--')

    # 3.4 添加经纬度
    # add lon and lat
    gl = ax.gridlines(draw_labels=True, linestyle=":", linewidth=0.3, x_inline=False, y_inline=False, color='k')
    gl.top_labels = False  # 关闭上部经纬标签
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER  # 使横坐标转化为经纬度格式
    gl.yformatter = LATITUDE_FORMATTER
    # gl.xlocator = mticker.FixedLocator(np.arange(114, 120, 1))
    # gl.ylocator = mticker.FixedLocator(np.arange(38, 43, 1))
    gl.xlabel_style = {'size': 11}  # 修改经纬度字体大小
    gl.ylabel_style = {'size': 11}
    # ax.set_extent([114.99, 118.01, 39.3, 41.3], crs=ccrs.PlateCarree())
    # Set figure extent
    ax.set_global()

    # 3.5 画图打点
    ax.plot([0, 13], [0, 3], 'o', markersize=4, color='tomato', label='MGEX', transform=ccrs.Geodetic())
    ax.plot([-122, -13], [11, -3], 'x', markersize=4, color='tomato', label='MGEX', transform=ccrs.Geodetic())
    # ax.plot(1, 0, 'o', color='red', label='Station 1', transform=ccrs.Geodetic())
    # ax.plot(0, 0, 'o', markersize=4, color='red', label='Station 1', transform=ccrs.Geodetic())
    # plt.plot([65, 0], [205, 0], color='blue', linewidth=2, marker='o', transform=ccrs.Geodetic())
    # plt.plot(0, 0, markersize=4, color='blue', marker='o', transform=ccrs.Geodetic())
    # plt.plot(65, 12, markersize=4, color='blue', marker='o', transform=ccrs.Geodetic())
    # plt.plot([65, 0, 12], [25, 0, 12], color='blue', linewidth=2, marker='o', transform=ccrs.Geodetic())

    # 3.6 添加标题和legend
    # add title
    ax.set_title('Location', fontsize=13)
    # add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 0.75), borderaxespad=0, frameon=False, markerscale=2)

    # 3.7 图片输出
    # show figure
    plt.show()


def main_points2():
    import numpy as np
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature

    fig = plt.figure(figsize=[9, 6])
    # Set projection
    ax = plt.axes(projection=ccrs.Robinson())
    # Add ocean and land
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    # Add MGEX & IGS core sites
    ax.plot([0], [0], 'o', color='tomato', label='MGEX', transform=ccrs.Geodetic())
    # Plot gridlines
    ax.gridlines(linestyle='--')
    # Set figure extent
    ax.set_global()
    # Set legend location
    plt.legend(loc='lower right')
    # Show figure
    plt.show()


def draw_points(lons, lats):
    # 3.3 建立画布，绘制地图
    ax = plt.axes(projection=ccrs.Robinson())
    # plot coastlines & gridlines
    ax.coastlines()
    ax.gridlines(linestyle='--')

    # 3.4 添加经纬度
    gl = ax.gridlines(draw_labels=True, linestyle=":", linewidth=0.3, x_inline=False, y_inline=False, color='k')
    gl.top_labels = False  # 关闭上部经纬标签
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER  # 使横坐标转化为经纬度格式
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 11}  # 修改经纬度字体大小
    gl.ylabel_style = {'size': 11}
    # Set figure extent
    ax.set_global()

    # 3.5 画图打点
    ax.plot(lons, lats, 'o', markersize=4, color='tomato', label='MGEX', transform=ccrs.Geodetic())

    # 3.6 添加标题和legend
    # add title
    ax.set_title('Location', fontsize=13)
    # add legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 0.75), borderaxespad=0, frameon=False, markerscale=2)

    # 3.7 图片输出
    plt.show()


if __name__ == '__main__':
    # map_Robinson_coastlines()
    # map_PlateCarree_coastlines()
    # map_Mollweide_stock()
    main_points()
    # main_points()
