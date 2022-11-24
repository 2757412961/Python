# -*- coding: utf-8 -*-
# @File  : FileUtil.py
# @Author: Zjh
# @Date  : 2022/11/23
# @Update: 2022/11/23
# @Desc  :

import os
import config

PROJECT_ABS_PATH = os.path.abspath(config.PROJECT_PATH)

'''
1、获取工作目录
print(os.getcwd())

2、创建目录
os.mkdir(‘test_dir’)

3、删除目录
os.rmdir()

4、切换工作路径
os.chdir()

5、列举当前路径下的所有文件以及目录列表
os.listdir()

6、判断当前文件是否是目录
os.path.isdir()

7、判断当前文件是否是文件，返回True
os.path.isfile()

8、文件拼接
os.path.join(dir_name, 'pac01', 'demo.txt')
'''


def exist(file):
    is_exist = os.path.exists(file)
    return is_exist


def check_generate_dirs(dir):
    """
    检查并创建文件夹完整目录
    :param dir:
    :return:
    """
    if not os.path.exists(dir):
        os.makedirs(dir)


def check_generate_files(file):
    """
    检查并创建文件完整目录
    :param file:
    :return:
    """
    work_dir = get_work_dir(file)
    check_generate_dirs(work_dir)


def get_work_dir(abs_path):
    """
    获取文件目录的路径
    :param abs_path:
    :return:
    """
    # 用绝对路径获取
    dir_name = os.path.dirname(abs_path)
    return dir_name


def generate_logfile_url(filename, base_dir=PROJECT_ABS_PATH):
    """
    获取日志文件绝对路径，从项目文件开始
    :param sub_dir: logs
    :param filename: a.log
    :return:
    """
    # 拼接
    file_path = os.path.join(base_dir, filename)
    # 检查
    check_generate_files(file_path)
    return file_path
