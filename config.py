# -*- coding: utf-8 -*-
# @File  : config.py
# @Author: Zjh
# @Date  : 2022/11/23
# @Update: 2022/11/23
# @Desc  : Configuration

'''
Global Variables
'''
PROJECT_ROOT = ''
DATA_ROOT = ''


def local():
    global PROJECT_ROOT, DATA_ROOT
    PROJECT_ROOT = 'E:/Github/Python'
    DATA_ROOT = 'F:/Ocean'


def temp():
    global PROJECT_ROOT, DATA_ROOT
    PROJECT_ROOT = 'E:/Github/Python'
    DATA_ROOT = 'F:/TEMP'


def linux():
    global PROJECT_ROOT, DATA_ROOT
    PROJECT_ROOT = '/tmp/pycharm_project_395'
    DATA_ROOT = '/home/zjh/Ocean'


#######
# local()
# temp()
linux()
#######
