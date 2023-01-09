# -*- coding: utf-8 -*-
"""
@File  : 2TansformDataToDB.py
@Author: zjh
@Date  : 2023/1/8
@Update: 2023/1/8
@Desc  :
"""

import pandas as pd
from utils import LogUtil
from utils import FileUtil
from utils.PostgresUtil import PostgresqlDB

# 日志
LOG_URL = FileUtil.generate_logfile_url("logs/tansformDataToDB.log")
logger = LogUtil.Logger(LOG_URL)


def f(a):
    a = str(a)
    if a == 'nan':
        return 'null'
    return a


def createTable(pg, isCreate=True):
    if isCreate:
        r = pg.execute('''
                    -- ----------------------------
                    -- Table structure for SOCATv3_v2022
                    -- ----------------------------
                    DROP TABLE IF EXISTS "public"."SOCATv3_v2022";
                    CREATE TABLE "public"."SOCATv3_v2022" (
                      "id" serial primary key,
                      "expocode" varchar(255) COLLATE "pg_catalog"."default",
                      "qcflag" varchar(255) COLLATE "pg_catalog"."default",
                      "year" int4,
                      "month" int4,
                      "day" int4,
                      "hh" int4,
                      "mm" int4,
                      "ss" int4,
                      "lon" float8,
                      "lat" float8,
                      "depth" float8,
                      "sss" float8,
                      "sst" float8,
                      "pco2" float8,
                      "fco2" float8,
                      "fco2rec" float8,
                      "fco2recsrc" int4
                    )
                    ;
                ''')
        logger.info(r)


if __name__ == '__main__':
    pg = PostgresqlDB(host="10.130.11.4", port=5433, user="postgres", password="postgres", database="postgres")

    # 建表
    createTable(pg, True)

    ####################################################################################################################
    # 读取 csv 文件
    # 需要安装dask模块：pip install dask
    import dask.dataframe as dd

    # 对于超过千万行的csv进行统计 可以尝试使用dask模块的read_csv进行统计。
    df = dd.read_csv('/home/zjh/Ocean/SOCAT/SOCATv3_v2022.csv', usecols=['year'])  # 需要统计的列名
    total = len(df)  # 33698458
    logger.info(f"总行数为:{total}")

    # 导入部分数据进行测试，这里导入 10000 行
    chunksize = 10000
    for step, df in enumerate(pd.read_csv('/home/zjh/Ocean/SOCAT/SOCATv3_v2022.csv', chunksize=chunksize)):
        logger.info(f"=== Read chunk: {step}/{total//chunksize} ===")

        values = ""
        for index, row in df.iterrows():
            logger.info(f"Read chunk: {step}/{total//chunksize} no.{index}")
            values += f"('{f(row[0])}','{f(row[1])}',{','.join([f(item) for item in row[2:]])}),"

        insertsSQL = f"INSERT INTO \"SOCATv3_v2022\"(expocode,qcflag,year,month,day,hh,mm,ss,lon,lat,depth,sss,sst,pco2,fco2,fco2rec,fco2recsrc)" \
                     f"VALUES " + values[:-1]
        r = pg.execute(insertsSQL)
        logger.info(f"=== Read chunk: {step}/{total//chunksize} sql result: {r} ===")

    logger.info("=====================================================================================================")
