/*
 Navicat Premium Data Transfer

 Source Server         : 10.130.11.4
 Source Server Type    : PostgreSQL
 Source Server Version : 120013
 Source Host           : 10.130.11.4:5433
 Source Catalog        : postgres
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120013
 File Encoding         : 65001

 Date: 09/01/2023 00:22:53
*/


-- ----------------------------
-- Table structure for SOCATv3_v2022
-- ----------------------------
DROP TABLE IF EXISTS "public"."SOCATv3_v2022";
CREATE TABLE "public"."SOCATv3_v2022" (
  "id" int4 NOT NULL DEFAULT nextval('"SOCATv3_v2022_id_seq"'::regclass),
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

-- ----------------------------
-- Primary Key structure for table SOCATv3_v2022
-- ----------------------------
ALTER TABLE "public"."SOCATv3_v2022" ADD CONSTRAINT "SOCATv3_v2022_pkey" PRIMARY KEY ("id");
