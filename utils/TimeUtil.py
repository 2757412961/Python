# -*- coding: utf-8 -*-
# @File  : TimeUtil.py
# @Author: Zjh
# @Date  : 2022/11/28
# @Update: 2022/11/28
# @Desc  :
import time
import datetime


def get_time():
    return time.time()


def get_format_time():
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return currentTime


def traversal_date():
    begin = datetime.date(2003, 1, 1)
    end = datetime.date(2022, 1, 1)

    for i in range((end - begin).days + 1):
        time = begin + datetime.timedelta(days=i)
        year = time.strftime("%Y")
        month = time.strftime("%m")
        day = time.strftime("%d")
        print(time)



