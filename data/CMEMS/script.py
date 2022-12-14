# -*- coding: utf-8 -*-
"""
@File  : script.py
@Author: Zjh
@Date  : 2022/12/13
@Update: 2022/12/13
@Desc  :
"""

import datetime
import pandas as pd

"""
Sample
motuclient --motu https://nrt.cmems-du.eu/motu-web/Motu --service-id GLOBAL_ANALYSIS_FORECAST_BIO_001_028-TDS --product-id global-analysis-forecast-bio-001-028-daily --date-min "2021-01-01 00:00:00" --date-max "2021-02-01 23:59:59" --depth-min 0.49402499198913574 --depth-max 0.49402499198913574 --variable chl --variable dissic --variable ph --variable talk --variable spco2 --out-dir "F:\Ocean\CMEMS\Global Ocean Biogeochemistry Analysis and Forecast" --out-name MULTIOBS_GLO_BIO_CARBON_SURFACE_REP_015_008-2021-01.nc --user aturing1 --pwd MoYan0000
"""

if __name__ == '__main__':
    begin = datetime.date(2003, 1, 1)
    end = datetime.date(2022, 1, 1)

    for i in range((end - begin).days + 1):
        time = begin + datetime.timedelta(days=i)
        year = time.strftime("%Y")  # 2003
        month = time.strftime("%m")  # 01
        day = time.strftime("%d")  # 01

    periods = (end.year - begin.year) * 12 + (end.month - begin.month)
    time_series = pd.period_range(begin, periods=periods, freq='M')

    for t in time_series:  # 2003-08
        start_time = t.start_time  # 2003-08-01
        end_time = t.end_time  # 2003-08-31
        ############################################
        year = start_time.strftime("%Y")  # 2003
        month = start_time.strftime("%m")  # 01
        day = start_time.strftime("%d")  # 01

    print(f'motuclient'
          f' --motu https://nrt.cmems-du.eu/motu-web/Motu'
          f' --service-id GLOBAL_ANALYSIS_FORECAST_BIO_001_028-TDS'
          f' --product-id global-analysis-forecast-bio-001-028-daily'
          f' --date-min "2021-01-01 00:00:00"'
          f' --date-max "2021-02-01 00:00:00"'
          f' --depth-min 0.49402499198913574'
          f' --depth-max 0.49402499198913574'
          f' --variable chl'
          f' --variable dissic'
          f' --variable ph'
          f' --variable talk'
          f' --variable spco2'
          f' --out-dir "F:\Ocean\CMEMS\Global Ocean Biogeochemistry Analysis and Forecast"'
          f' --out-name MULTIOBS_GLO_BIO_CARBON_SURFACE_REP_015_008-2021-01.nc'
          f' --user aturing1'
          f' --pwd MoYan0000')
