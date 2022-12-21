# -*- coding: utf-8 -*-
"""
@File  : PostgresUtil.py
@Author: Zjh
@Date  : 2022/12/20
@Update: 2022/12/20
@Desc  : asyncpg：异步操作PostgreSQL

https://www.programminghunter.com/article/60711104018/
"""

import asyncio
import asyncpg

'''
我们看到在获取记录的时候使用的都是fetchrow和fetch，但是除了这两个之外，还有conn.execute和conn.executemany
除了增删改之外，像什么建表语句、修改表字段、类型等等，都使用execute，执行多条的话使用executemany。
至于fetch和fetchrow是专门针对select查询使用的，还有execute和executemany针对的是select语句之外的其它语句
'''


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
