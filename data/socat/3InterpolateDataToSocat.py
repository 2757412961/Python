# -*- coding: utf-8 -*-
"""
@File  : 3InterpolateDataToGlodap.py
@Author: zjh
@Date  : 2023/1/8
@Update: 2023/1/8
@Desc  :
"""

import numpy as np
import pandas as pd
import datetime
from utils import LogUtil
from utils import FileUtil
from utils.PostgresUtil import PostgresqlDB
from utils import MapTuil
from data.DataCollection import EAR5, GlobalOceanPhysicsReanalysis, OceanColor

# 日志
LOG_URL = FileUtil.generate_logfile_url("logs/3InterpolateOtherDataToDB.log")
logger = LogUtil.Logger(LOG_URL)


def f(a):
    a = str(a)
    if a == 'nan' or a == '--' or a == 'None':
        return '-9999'
    return a


def createTable(pg, isCreate=True):
    # 建表
    if isCreate:
        r = pg.execute('''
            -- ----------------------------
            -- Table structure for SOCAT_Interpolate
            -- ----------------------------
            DROP TABLE IF EXISTS "public"."SOCAT_Interpolate";
            CREATE TABLE "public"."SOCAT_Interpolate" (
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
                
                ,"u10" float8
                ,"v10" float8
                ,"pressureear" float8
                ,"sstear" float8
                ,"precipitation" float8
                
                ,"mld" float8
                ,"sid" float8
                ,"ssh" float8
                
                ,"chlora" float8
                ,"kd" float8
                ,"poc" float8
                ,"pic" float8
                ,"sstoc" float8
                ,"bbp" float8
                ,"rrs412" float8
                ,"rrs443" float8
                ,"rrs469" float8
                ,"rrs488" float8
                ,"rrs531" float8
                ,"rrs547" float8
                ,"rrs555" float8
                ,"rrs667" float8
                ,"rrs678" float8
            )
            ;
            ''')
        logger.info(r)


if __name__ == '__main__':
    pg = PostgresqlDB(host="10.130.11.4", port=5433, user="postgres", password="postgres", database="postgres")

    # 建表
    createTable(pg, False)

    ####################################################################################################################
    # title = pg.title('SOCATv3_v2022')
    # sample = pg.search('Select * From "SOCATv3_v2022" Limit 10')

    ####################################################################################################################
    begin = datetime.date(2003, 1, 1)
    end = datetime.date(2004, 1, 1)

    for i in range((end - begin).days + 1):
        time = begin + datetime.timedelta(days=i)
        year = time.strftime("%Y")  # 2003
        month = time.strftime("%m")  # 01
        day = time.strftime("%d")  # 01
        ############################################
        # 各种变量
        ear = EAR5(year, month, day)
        gopr = GlobalOceanPhysicsReanalysis(year, month, day)
        oc = OceanColor(year, month, day)
        # oc = 1

        ############################################
        values = ""
        lines = pg.search(f'SELECT * FROM "SOCATv3_v2022" '
                          f'WHERE "year" = {str(time.year)} AND "month" = {str(time.month)} AND "day" = {str(time.day)}')
        ############################################
        # lats = np.array(lines)[:, 10]
        # lons = np.array(lines)[:, 9]
        # MapTuil.draw_points(lons, lats)
        # continue
        ############################################
        for i in range(len(lines)):
            row = lines[i]
            day, lat, lon = row[3] - 1, row[10], row[9] - 180
            u10, v10, pressureear, sstear, precipitation = ear.get(lat, lon)
            mld, sid, ssh = gopr.get(lat, lon)
            chlora, kd, poc, pic, sstoc, bbp, rrs412, rrs443, rrs469, rrs488, rrs531, rrs547, rrs555, rrs667, rrs678 \
                = oc.get(lat, lon)
            values += f"('{f(row[1])}','{f(row[2])}',{f(row[3])},{f(row[4])},{f(row[5])},{f(row[6])},{f(row[7])}," \
                      f"{f(row[8])},{f(row[9])},{f(row[10])},{f(row[11])},{f(row[12])},{f(row[13])},{f(row[14])}," \
                      f"{f(row[15])},{f(row[16])},{f(row[17])}" \
                      f",{f(u10)},{f(v10)},{f(pressureear)},{f(sstear)},{f(precipitation)}" \
                      f",{f(mld)},{f(sid)},{f(ssh)}" \
                      f",{f(chlora)},{f(kd)},{f(poc)},{f(pic)},{f(sstoc)},{f(bbp)},{f(rrs412)},{f(rrs443)},{f(rrs469)},{f(rrs488)},{f(rrs531)},{f(rrs547)},{f(rrs555)},{f(rrs667)},{f(rrs678)}" \
                      f"),"
            logger.info(f"{year}-{month}-{day}:step({i + 1})/total({len(lines)})")
            if i % 100 == 0:
                r = pg.execute(f'INSERT INTO "SOCAT_Interpolate"'
                               f'(expocode,qcflag,year,month,day,hh,mm,ss,'
                               f'lon,lat,depth,sss,sst,pco2,fco2,fco2rec,fco2recsrc'
                               f',u10, v10, pressureear, sstear, precipitation'
                               f',mld, sid, ssh'
                               f',chlora, kd, poc, pic, sstoc, bbp, rrs412, rrs443, rrs469, rrs488, rrs531, rrs547, rrs555, rrs667, rrs678'
                               f') VALUES ' + values[:-1])
                values = ""
        r = pg.execute(f'INSERT INTO "SOCAT_Interpolate"'
                       f'(expocode,qcflag,year,month,day,hh,mm,ss,'
                       f'lon,lat,depth,sss,sst,pco2,fco2,fco2rec,fco2recsrc'
                       f',u10, v10, pressureear, sstear, precipitation'
                       f',mld, sid, ssh'
                       f',chlora, kd, poc, pic, sstoc, bbp, rrs412, rrs443, rrs469, rrs488, rrs531, rrs547, rrs555, rrs667, rrs678'
                       f') VALUES ' + values[:-1])

logger.info("=====================================================================================================")
