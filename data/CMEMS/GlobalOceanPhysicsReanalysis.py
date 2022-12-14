# -*- coding: utf-8 -*-
"""
@File  : script.py
@Author: Zjh
@Date  : 2022/12/13
@Update: 2022/12/13
@Desc  : Global Ocean Physics Reanalysis

变量描述：
    Sea water potential temperature at sea floor bottomT [°C]
    Ocean mixed layer thickness defined by sigma theta mlotst [m]
    Sea ice area fraction siconc
    Sea ice thickness sithick [m]
    Sea water salinity so [10-3]
    Sea water potential temperature thetao [°C]
    Eastward sea water velocity uo [m/s]
    Eastward sea ice velocity usi [m/s]
    Northward sea water velocity vo [m/s]
    Northward sea ice velocity vsi [m/s]
    Sea surface height above geoid zos [m]
"""

import datetime
import pandas as pd

if __name__ == '__main__':
    begin = datetime.date(2003, 1, 1)
    end = datetime.date(2020, 1, 1)

    periods = (end.year - begin.year) * 12 + (end.month - begin.month)
    time_series = pd.period_range(begin, periods=periods, freq='M')

    for t in time_series:  # 2003-08
        start_time = t.start_time  # 2003-08-01
        next_time = t.end_time + datetime.timedelta(days=1)  # 2003-09-01
        ############################################
        this_year = start_time.strftime("%Y")  # 2003
        this_month = start_time.strftime("%m")  # 08
        next_year = next_time.strftime("%Y")  # 2003
        next_month = next_time.strftime("%m")  # 09
        print(f'motuclient'
              f' --motu https://my.cmems-du.eu/motu-web/Motu'
              f' --service-id GLOBAL_MULTIYEAR_PHY_001_030-TDS'
              f' --product-id cmems_mod_glo_phy_my_0.083_P1D-m'
              f' --date-min "{this_year}-{this_month}-01 00:00:00"'
              f' --date-max "{next_year}-{next_month}-01 00:00:00"'
              f' --depth-min 0.49402499198913574'
              f' --depth-max 0.49402499198913574'
              f' --variable sithick'
              f' --variable zos'
              f' --variable mlotst'
              f' --out-dir "F:\Ocean\CMEMS\Global Ocean Biogeochemistry Analysis and Forecast"'
              f' --out-name MULTIOBS_GLO_BIO_CARBON_SURFACE_REP_{this_year}_{this_month}.nc'
              f' --user aturing1'
              f' --pwd MoYan0000')
