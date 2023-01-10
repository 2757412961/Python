# -*- coding: utf-8 -*-
"""
@File  : InterpolateDataToDB.py
@Author: zjh
@Date  : 2023/1/8
@Update: 2023/1/8
@Desc  :
"""

import pandas as pd
import datetime
from utils import LogUtil
from utils import FileUtil
from utils.PostgresUtil import PostgresqlDB
from DataCollection import EAR5, GlobalOceanPhysicsReanalysis, OceanColor

# 日志
LOG_URL = FileUtil.generate_logfile_url("logs/InterpolateOtherDataToDB.log")
logger = LogUtil.Logger(LOG_URL)


def f(a):
    a = str(a)
    if a == 'nan' or a == '--':
        return '-9999'
    return a


def createTable(pg, isCreate=True):
    # 建表
    if isCreate:
        r = pg.execute('''
                -- ----------------------------
                -- Table structure for GLODAP_Interpolate
                -- ----------------------------
                DROP TABLE IF EXISTS "public"."GLODAP_Interpolate";
                CREATE TABLE "public"."GLODAP_Interpolate" (
                  "id" serial primary key,
                  "expocode" varchar(255) COLLATE "pg_catalog"."default",
                  "year" int4,
                  "month" int4,
                  "day" int4,
                  "hh" int4,
                  "mm" int4,
                  "lat" float8,
                  "lon" float8,
                  
                  "pressure" float8,
                  "depth" float8,
                  "temperature" float8,
                  "salinity" float8,
                  "oxygen" float8,
                  "nitrate" float8,
                  "nitrite" float8,
                  "silicate" float8,
                  
                  "phosphate" float8,
                  "tco2" float8,
                  "talk" float8,
                  "fco2" float8,
                  "phts25p0" float8,
                  "phtsinsitutp" float8,
                  "toc" float8,
                  "doc" float8,
                  
                  "chla" float8
                  
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
                  ,"sst" float8
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
    createTable(pg, True)

    ####################################################################################################################
    # title = pg.title('GLODAPv2022')
    # sample = pg.search('Select * From "GLODAPv2022" Limit 10')

    ####################################################################################################################
    begin = datetime.date(2004, 1, 1)
    end = datetime.date(2022, 1, 1)
    periods = (end.year - begin.year) * 12 + (end.month - begin.month)
    time_series = pd.period_range(begin, periods=periods, freq='M')

    for t in time_series:  # 2003-08
        start_time = t.start_time  # 2003-08-01
        end_time = t.end_time  # 2003-08-31
        year = start_time.strftime("%Y")  # 2003
        month = start_time.strftime("%m")  # 01
        monthSimple = start_time.month  # 1
        ############################################
        # 各种变量
        ear = EAR5(start_time, end_time)
        gopr = GlobalOceanPhysicsReanalysis(start_time, end_time)
        oc = OceanColor(start_time, end_time)

        ############################################
        values = ""
        lines = pg.search(f'SELECT * FROM "GLODAPv2022" WHERE "G2year" = {year} AND "G2month" = {monthSimple}')
        for i in range(len(lines)):
            row = lines[i]
            day, lat, lon = row[7] - 1, row[10], row[11]
            u10, v10, pressureear, sstear, precipitation = ear.get(day, lat, lon)
            mld, sid, ssh = gopr.get(day, lat, lon)
            chlora, kd, poc, pic, sst, bbp, rrs412, rrs443, rrs469, rrs488, rrs531, rrs547, rrs555, rrs667, rrs678 \
                = oc.get(day, lat, lon)
            values += f"('{f(row[0])}',{f(row[5])},{f(row[6])},{f(row[7])},{f(row[8])},{f(row[9])},{f(row[10])},{f(row[11])}," \
                      f"{f(row[15])},{f(row[16])},{f(row[17])},{f(row[19])},{f(row[28])},{f(row[33])},{f(row[36])},{f(row[38])}," \
                      f"{f(row[41])},{f(row[44])},{f(row[47])},{f(row[50])},{f(row[53])},{f(row[55])},{f(row[98])},{f(row[100])}," \
                      f"{f(row[106])}" \
                      f",{f(u10)},{f(v10)},{f(pressureear)},{f(sstear)},{f(precipitation)}" \
                      f",{f(mld)},{f(sid)},{f(ssh)}" \
                      f",{f(chlora)},{f(kd)},{f(poc)},{f(pic)},{f(sst)},{f(bbp)},{f(rrs412)},{f(rrs443)},{f(rrs469)},{f(rrs488)},{f(rrs531)},{f(rrs547)},{f(rrs555)},{f(rrs667)},{f(rrs678)}" \
                      f"),"
            logger.info(f"{year}-{month}:step({i + 1})/total({len(lines)})")
            if i % 100 == 0:
                r = pg.execute(f'INSERT INTO "GLODAP_Interpolate"'
                               f'(expocode,year,month,day,hh,mm,lat,lon,'
                               f'pressure,depth,temperature,salinity,oxygen,nitrate,nitrite,silicate,'
                               f'phosphate,tco2,talk,fco2,phts25p0,phtsinsitutp,toc,doc,'
                               f'chla'
                               f',u10, v10, pressureear, sstear, precipitation'
                               f',mld, sid, ssh'
                               f',chlora, kd, poc, pic, sst, bbp, rrs412, rrs443, rrs469, rrs488, rrs531, rrs547, rrs555, rrs667, rrs678'
                               f') VALUES ' + values[:-1])
                values = 0
        r = pg.execute(f'INSERT INTO "GLODAP_Interpolate"'
                       f'(expocode,year,month,day,hh,mm,lat,lon,'
                       f'pressure,depth,temperature,salinity,oxygen,nitrate,nitrite,silicate,'
                       f'phosphate,tco2,talk,fco2,phts25p0,phtsinsitutp,toc,doc,'
                       f'chla'
                       f',u10, v10, pressureear, sstear, precipitation'
                       f',mld, sid, ssh'
                       f',chlora, kd, poc, pic, sst, bbp, rrs412, rrs443, rrs469, rrs488, rrs531, rrs547, rrs555, rrs667, rrs678'
                       f') VALUES ' + values[:-1])

logger.info("=====================================================================================================")
