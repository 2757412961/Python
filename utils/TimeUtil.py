# -*- coding: utf-8 -*-
# @File  : TimeUtil.py
# @Author: Zjh
# @Date  : 2022/11/28
# @Update: 2022/11/28
# @Desc  :
import time

def get_time():
    return time.time()

def get_format_time():
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return currentTime

