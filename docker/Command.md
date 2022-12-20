# 创建postgres数据库
- 开放端口：5433
- 密码：123456
docker pull postgres:12
docker run --name postgres4OA -d -p 5433:5432 -e POSTGRES_PASSWORD=123456 postgres:12

# 安装postgis（包含了postgres,无须安装pg）
- POSTGRES_USER: postgres
- POSTGRES_PASSWORD: postgres
- POSTGRES_DBNAME: gis_db
- port: 5433
- volume: /home/zjh/postgres/postgis_data:/var/lib/postgis/data
- volume: /home/zjh/postgres/pg_data:/var/lib/postgresql/data
docker pull postgis/postgis:12-3.3
docker run --name postgres4OA --restart=always -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DBNAME=gis_db -p 5433:5432 -v /home/zjh/postgres/postgis_data:/var/lib/postgis/data -v /home/zjh/postgres/pg_data:/var/lib/postgresql/data -d postgis/postgis:12-3.3





