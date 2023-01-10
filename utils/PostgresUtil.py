# -*- coding: utf-8 -*-
"""
@File  : PostgresUtil.py
@Author: Zjh
@Date  : 2022/12/20
@Update: 2022/12/20
@Desc  : asyncpg：异步操作PostgreSQL

https://www.programminghunter.com/article/60711104018/
"""

import psycopg2

'''
psycopg2 是一个通过python连接postgreSQL的库, 不要被它的名称蒙蔽了，你可能发现它的版本是psyconpg2.7.*, 以为它只能在python2上使用，实际上，这只是一个巧合而已，它也可以在python3上使用。
'''
import asyncio
import asyncpg

'''
我们看到在获取记录的时候使用的都是fetchrow和fetch，但是除了这两个之外，还有conn.execute和conn.executemany
除了增删改之外，像什么建表语句、修改表字段、类型等等，都使用execute，执行多条的话使用executemany。
至于fetch和fetchrow是专门针对select查询使用的，还有execute和executemany针对的是select语句之外的其它语句
'''

'''
1 psycopg2.connect(database="testdb", user="postgres", password="cohondob", host="127.0.0.1", port="5432")
　　这个API打开一个连接到PostgreSQL数据库。如果成功打开数据库时，它返回一个连接对象。
2 connection.cursor()
　　该程序创建一个光标将用于整个数据库使用Python编程。
3 cursor.execute(sql [, optional parameters])
　　此例程执行SQL语句。可被参数化的SQL语句（即占位符，而不是SQL文字）。 psycopg2的模块支持占位符用％s标志
　　例如：cursor.execute("insert into people values (%s, %s)", (who, age))
4 curosr.executemany(sql, seq_of_parameters)
　　该程序执行SQL命令对所有参数序列或序列中的sql映射。
5 curosr.callproc(procname[, parameters])
　　这个程序执行的存储数据库程序给定的名称。该程序预计为每一个参数，参数的顺序必须包含一个条目。
6 cursor.rowcount
　　这个只读属性，它返回数据库中的行的总数已修改，插入或删除最后 execute*().
7 connection.commit()
　　此方法提交当前事务。如果不调用这个方法，无论做了什么修改，自从上次调用commit()是不可见的，从其他的数据库连接。
8 connection.rollback()
　　此方法会回滚任何更改数据库自上次调用commit（）方法。
9 connection.close()
　　此方法关闭数据库连接。请注意，这并不自动调用commit（）。如果你只是关闭数据库连接而不调用commit（）方法首先，那么所有更改将会丢失！
10 cursor.fetchone()
　　这种方法提取的查询结果集的下一行，返回一个序列，或者无当没有更多的数据是可用的。
11 cursor.fetchmany([size=cursor.arraysize])
　　这个例程中取出下一个组的查询结果的行数，返回一个列表。当没有找到记录，返回空列表。该方法试图获取尽可能多的行所显示的大小参数。
12 cursor.fetchall()
　　这个例程获取所有查询结果（剩余）行，返回一个列表。空行时则返回空列表。
'''


class PostgresqlDB(object):
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def search(self, sql):
        """
        Args:
            sql: 查询语句，必须是SELECT

        Returns:
        """
        try:
            # （一）连接数据库：
            conn = psycopg2.connect(host=self.host, port=self.port,
                                    user=self.user, password=self.password, database=self.database)
            # （二）创建光标：
            cur = conn.cursor()
            # （三）执行SQL指令：
            cur.execute(sql)
            # （四）获取所有结果（比如使用了select语句）：
            results = cur.fetchall()
            # （五）提交当前事务：
            # （六）关闭光标 & 关闭数据库连接
            cur.close()
            conn.close()
            return results
        except IOError as e:
            print(e)

    def execute(self, sql):
        """
        Args:
            sql: 执行语句，不能是SELECT

        Returns:
        """
        try:
            # （一）连接数据库：
            conn = psycopg2.connect(host=self.host, port=self.port,
                                    user=self.user, password=self.password, database=self.database)
            # （二）创建光标：
            cur = conn.cursor()
            # （三）执行SQL指令：
            cur.execute(sql)
            # （四）获取所有结果（比如使用了select语句）：
            # （五）提交当前事务：
            conn.commit()
            # （六）关闭光标 & 关闭数据库连接
            cur.close()
            conn.close()
            return cur.rowcount
        except IOError as e:
            print(e)

    def length(self, table):
        """
        Args:
            table: 表明

        Returns: 返回表的长度
        """
        try:
            # （一）连接数据库：
            conn = psycopg2.connect(host=self.host, port=self.port,
                                    user=self.user, password=self.password, database=self.database)
            # （二）创建光标：
            cur = conn.cursor()
            # （三）执行SQL指令：
            cur.execute(f'SELECT * FROM "{table}"')
            # （四）获取所有结果（比如使用了select语句）：
            # （五）提交当前事务：
            # （六）关闭光标 & 关闭数据库连接
            cur.close()
            conn.close()
            return cur.rowcount
        except IOError as e:
            print(e)

    def title(self, table):
        try:
            # （一）连接数据库：
            conn = psycopg2.connect(host=self.host, port=self.port,
                                    user=self.user, password=self.password, database=self.database)
            # （二）创建光标：
            cur = conn.cursor()
            # （三）执行SQL指令：
            cur.execute("select * "
                        "from information_schema.columns "
                        "where table_schema='public' and table_name='GLODAPv2022' ")
            # （四）获取所有结果（比如使用了select语句）：
            results = cur.fetchall()
            # （五）提交当前事务：
            # （六）关闭光标 & 关闭数据库连接
            cur.close()
            conn.close()
            return results
        except IOError as e:
            print(e)


async def record():
    conn = await asyncpg.connect("postgres://postgres:zgghyys123@localhost:5432/postgres")
    row = await conn.fetchrow("select * from t1")

    print(type(row))  # <class 'asyncpg.Record'>
    print(row)  # <Record pk=1 name='古明地觉'>

    # 这个Record对象可以想象成一个字典
    # 我们说表中有两个字段，分别是pk和name
    print(row["pk"], row["name"])  # 1 古明地觉

    # 除此之外，还可以通过get获取
    print(row.get("pk"), row.get("name"))  # 1 古明地觉

    # 除此之外还可以调用keys、values、items，这个不用我说，都应该知道意味着什么
    # 只不过返回的是一个迭代器
    print(row.keys())  # <tuple_iterator object at 0x000001D6FFDAE610>
    print(row.values())  # <tuple_iterator object at 0x000001D6FFDAE610>
    print(row.items())  # <RecordItemsIterator object at 0x000001D6FFDF20C0>

    # 我们需要转成列表或者元组
    print(list(row.keys()))  # ['pk', 'name']
    print(list(row.values()))  # [1, '古明地觉']
    print(dict(row.items()))  # {'pk': 1, 'name': '古明地觉'}

    # 关闭连接
    await conn.close()


async def execute():
    conn = await asyncpg.connect("postgres://postgres:zgghyys123@localhost:5432/postgres")

    # executemany：第一条参数是一个模板，第二条命令是包含多个元组的列表
    # 执行多条记录的话，返回的结果为None

    row = await conn.executemany("insert into t1 values($1, $2)",
                                 [(8, "琪露诺"), (9, "八意永琳")]
                                 )
    print(row)  # None

    row = await conn.executemany("update t1 set pk = $1 where name = $2",
                                 [(88, "琪露诺"), (99, "八意永琳")]
                                 )
    print(row)  # None

    row = await conn.executemany("delete from t1 where pk = $1",
                                 [(88,), (99,)])  # 即使是一个值也要写成元组
    print(row)  # None

    # 关闭连接
    await conn.close()


async def connectionpool():
    pool = await asyncpg.create_pool(
        "postgres://postgres:zgghyys123@localhost:5432/postgres",
        min_size=10,  # 连接池初始化时默认的最小连接数, 默认为10
        max_size=10,  # 连接池的最大连接数, 默认为10
        max_queries=5000,  # 每个链接最大查询数量, 超过了就换新的连接, 默认5000
        # 最大不活跃时间, 默认300.0, 超过这个时间的连接就会被关闭,传入0的话则永不关闭
        max_inactive_connection_lifetime=300.0
    )
    # 如果还有其它什么特殊参数，也可以直接往里面传递，因为设置了**connect_kwargs
    # 专门用来设置一些数据库独有的某些属性

    # 从池子中取出一个连接
    async with pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow("select '100'::int + 200")
            # 我们看到没有指定名字，随意返回字段名叫做?column?
            # 不要慌，PostgreSQL中返回的也是这个结果
            print(row)  # <Record ?column?=300>

            # 解决办法就是起一个别名
            row = await conn.fetchrow("select '100'::int + 200 as result")
            print(row)  # <Record result=300>

    # 这里就不需要关闭了，因为我们的连接是从池子里面取出的
    # 上下文结束之后就放回到池子里面了
    # await conn.close()


async def main():
    # 创建连接数据库的驱动，创建连接的时候要使用await
    conn = await asyncpg.connect(host="10.130.11.4",
                                 port=5433,
                                 user="postgres",
                                 password="postgres",
                                 database="postgres")
    # 除了上面的方式，还可以使用类似于sqlalchemy的方式创建
    # await asyncpg.connect("postgres://user:password@localhost:5432/postgres")

    # 调用await conn.fetchrow执行select语句，获取满足条件的单条记录
    # 调用await conn.fetch执行select语句，获取满足条件的全部记录
    row1 = await conn.fetchrow("select * from test")
    row2 = await conn.fetch("select * from test")

    # 返回的是一个Record对象，这个Record对象等于将返回的记录进行了一个封装
    # 至于怎么用后面会说。
    print(row1)
    """
    <Record pk=1 name='古明地觉'>
    """
    print(row2)
    """
    [<Record pk=1 name='古明地觉'>, <Record pk=2 name='雾雨魔理沙'>, 
     <Record pk=3 name='芙兰朵露'>, <Record pk=4 name='十六夜咲夜'>,
     <Record pk=5 name='风见幽香'>, <Record pk=6 name='博丽灵梦'>, 
     <Record pk=7 name='藤原妹红'>, <Record pk=8 name='琪露诺'>]
    """
    # 关闭连接
    await conn.close()


if __name__ == '__main__':
    asyncio.run(main())
