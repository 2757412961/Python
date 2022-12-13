# -*- coding: utf-8 -*-
# @File  : TimeUtil.py
# @Author: Zjh
# @Date  : 2022/11/28
# @Update: 2022/11/28
# @Desc  :
import time
import datetime
import pandas as pd


def get_time():
    return time.time()


def get_format_time():
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return currentTime


def traversal_days():
    begin = datetime.date(2003, 1, 1)
    end = datetime.date(2022, 1, 1)

    for i in range((end - begin).days + 1):
        time = begin + datetime.timedelta(days=i)
        year = time.strftime("%Y")  # 2003
        month = time.strftime("%m")  # 01
        day = time.strftime("%d")  # 01
        print(time)


def traversal_months():
    begin = datetime.date(2003, 8, 1)
    end = datetime.date(2004, 4, 1)

    periods = (end.year - begin.year) * 12 + (end.month - begin.month)
    time_series = pd.period_range(begin, periods=periods, freq='M')

    for t in time_series:  # 2003-08
        start_time = t.start_time  # 2003-08-01
        end_time = t.end_time  # 2003-08-31
        ############################################
        year = start_time.strftime("%Y")  # 2003
        month = start_time.strftime("%m")  # 01
        day = start_time.strftime("%d")  # 01
        print(t, year, month, day)
