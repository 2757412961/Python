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

 Date: 09/01/2023 00:22:29
*/


-- ----------------------------
-- Table structure for GLODAPv2022
-- ----------------------------
DROP TABLE IF EXISTS "public"."GLODAPv2022";
CREATE TABLE "public"."GLODAPv2022" (
  "G2expocode" varchar(255) COLLATE "pg_catalog"."default",
  "G2cruise" varchar(255) COLLATE "pg_catalog"."default",
  "G2station" varchar(255) COLLATE "pg_catalog"."default",
  "G2region" varchar(255) COLLATE "pg_catalog"."default",
  "G2cast" varchar(255) COLLATE "pg_catalog"."default",
  "G2year" int4,
  "G2month" int4,
  "G2day" int4,
  "G2hour" int4,
  "G2minute" int4,
  "G2latitude" float8,
  "G2longitude" float8,
  "G2bottomdepth" float8,
  "G2maxsampdepth" float8,
  "G2bottle" varchar(255) COLLATE "pg_catalog"."default",
  "G2pressure" float8,
  "G2depth" float8,
  "G2temperature" float8,
  "G2theta" varchar(255) COLLATE "pg_catalog"."default",
  "G2salinity" float8,
  "G2salinityf" varchar(255) COLLATE "pg_catalog"."default",
  "G2salinityqc" varchar(255) COLLATE "pg_catalog"."default",
  "G2sigma0" varchar(255) COLLATE "pg_catalog"."default",
  "G2sigma1" varchar(255) COLLATE "pg_catalog"."default",
  "G2sigma2" varchar(255) COLLATE "pg_catalog"."default",
  "G2sigma3" varchar(255) COLLATE "pg_catalog"."default",
  "G2sigma4" varchar(255) COLLATE "pg_catalog"."default",
  "G2gamma" varchar(255) COLLATE "pg_catalog"."default",
  "G2oxygen" varchar(255) COLLATE "pg_catalog"."default",
  "G2oxygenf" varchar(255) COLLATE "pg_catalog"."default",
  "G2oxygenqc" varchar(255) COLLATE "pg_catalog"."default",
  "G2aou" varchar(255) COLLATE "pg_catalog"."default",
  "G2aouf" varchar(255) COLLATE "pg_catalog"."default",
  "G2nitrate" varchar(255) COLLATE "pg_catalog"."default",
  "G2nitratef" varchar(255) COLLATE "pg_catalog"."default",
  "G2nitrateqc" varchar(255) COLLATE "pg_catalog"."default",
  "G2nitrite" varchar(255) COLLATE "pg_catalog"."default",
  "G2nitritef" varchar(255) COLLATE "pg_catalog"."default",
  "G2silicate" varchar(255) COLLATE "pg_catalog"."default",
  "G2silicatef" varchar(255) COLLATE "pg_catalog"."default",
  "G2silicateqc" varchar(255) COLLATE "pg_catalog"."default",
  "G2phosphate" varchar(255) COLLATE "pg_catalog"."default",
  "G2phosphatef" varchar(255) COLLATE "pg_catalog"."default",
  "G2phosphateqc" varchar(255) COLLATE "pg_catalog"."default",
  "G2tco2" float8,
  "G2tco2f" varchar(255) COLLATE "pg_catalog"."default",
  "G2tco2qc" varchar(255) COLLATE "pg_catalog"."default",
  "G2talk" varchar(255) COLLATE "pg_catalog"."default",
  "G2talkf" varchar(255) COLLATE "pg_catalog"."default",
  "G2talkqc" varchar(255) COLLATE "pg_catalog"."default",
  "G2fco2" varchar(255) COLLATE "pg_catalog"."default",
  "G2fco2f" varchar(255) COLLATE "pg_catalog"."default",
  "G2fco2temp" varchar(255) COLLATE "pg_catalog"."default",
  "G2phts25p0" float8,
  "G2phts25p0f" varchar(255) COLLATE "pg_catalog"."default",
  "G2phtsinsitutp" float8,
  "G2phtsinsitutpf" varchar(255) COLLATE "pg_catalog"."default",
  "G2phtsqc" varchar(255) COLLATE "pg_catalog"."default",
  "G2cfc11" varchar(255) COLLATE "pg_catalog"."default",
  "G2pcfc11" varchar(255) COLLATE "pg_catalog"."default",
  "G2cfc11f" varchar(255) COLLATE "pg_catalog"."default",
  "G2cfc11qc" varchar(255) COLLATE "pg_catalog"."default",
  "G2cfc12" varchar(255) COLLATE "pg_catalog"."default",
  "G2pcfc12" varchar(255) COLLATE "pg_catalog"."default",
  "G2cfc12f" varchar(255) COLLATE "pg_catalog"."default",
  "G2cfc12qc" varchar(255) COLLATE "pg_catalog"."default",
  "G2cfc113" varchar(255) COLLATE "pg_catalog"."default",
  "G2pcfc113" varchar(255) COLLATE "pg_catalog"."default",
  "G2cfc113f" varchar(255) COLLATE "pg_catalog"."default",
  "G2cfc113qc" varchar(255) COLLATE "pg_catalog"."default",
  "G2ccl4" varchar(255) COLLATE "pg_catalog"."default",
  "G2pccl4" varchar(255) COLLATE "pg_catalog"."default",
  "G2ccl4f" varchar(255) COLLATE "pg_catalog"."default",
  "G2ccl4qc" varchar(255) COLLATE "pg_catalog"."default",
  "G2sf6" varchar(255) COLLATE "pg_catalog"."default",
  "G2psf6" varchar(255) COLLATE "pg_catalog"."default",
  "G2sf6f" varchar(255) COLLATE "pg_catalog"."default",
  "G2sf6qc" varchar(255) COLLATE "pg_catalog"."default",
  "G2c13" varchar(255) COLLATE "pg_catalog"."default",
  "G2c13f" varchar(255) COLLATE "pg_catalog"."default",
  "G2c13qc" varchar(255) COLLATE "pg_catalog"."default",
  "G2c14" varchar(255) COLLATE "pg_catalog"."default",
  "G2c14f" varchar(255) COLLATE "pg_catalog"."default",
  "G2c14err" varchar(255) COLLATE "pg_catalog"."default",
  "G2h3" varchar(255) COLLATE "pg_catalog"."default",
  "G2h3f" varchar(255) COLLATE "pg_catalog"."default",
  "G2h3err" varchar(255) COLLATE "pg_catalog"."default",
  "G2he3" varchar(255) COLLATE "pg_catalog"."default",
  "G2he3f" varchar(255) COLLATE "pg_catalog"."default",
  "G2he3err" varchar(255) COLLATE "pg_catalog"."default",
  "G2he" varchar(255) COLLATE "pg_catalog"."default",
  "G2hef" varchar(255) COLLATE "pg_catalog"."default",
  "G2heerr" varchar(255) COLLATE "pg_catalog"."default",
  "G2neon" varchar(255) COLLATE "pg_catalog"."default",
  "G2neonf" varchar(255) COLLATE "pg_catalog"."default",
  "G2neonerr" varchar(255) COLLATE "pg_catalog"."default",
  "G2o18" varchar(255) COLLATE "pg_catalog"."default",
  "G2o18f" varchar(255) COLLATE "pg_catalog"."default",
  "G2toc" varchar(255) COLLATE "pg_catalog"."default",
  "G2tocf" varchar(255) COLLATE "pg_catalog"."default",
  "G2doc" varchar(255) COLLATE "pg_catalog"."default",
  "G2docf" varchar(255) COLLATE "pg_catalog"."default",
  "G2don" varchar(255) COLLATE "pg_catalog"."default",
  "G2donf" varchar(255) COLLATE "pg_catalog"."default",
  "G2tdn" varchar(255) COLLATE "pg_catalog"."default",
  "G2tdnf" varchar(255) COLLATE "pg_catalog"."default",
  "G2chla" varchar(255) COLLATE "pg_catalog"."default",
  "G2chlaf" varchar(255) COLLATE "pg_catalog"."default",
  "G2doi" varchar(255) COLLATE "pg_catalog"."default"
)
;
