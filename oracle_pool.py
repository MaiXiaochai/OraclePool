# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : oracle_pool.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@Created on : 2022/4/20 14:27
--------------------------------------
"""
from contextlib import contextmanager

import cx_Oracle as Oracle


class OraclePool:
    """
    1) 这里封装了一些有关oracle连接池的功能;
    2) sid和service_name，程序会自动判断哪个有值，
        若两个都有值，则默认使用service_name；
    3) 关于config的设置，注意只有 port 的值的类型是 int，以下是config样例:
        config = {
            'username':     'maixiaochai',
            'password':     'maixiaochai',
            'host':         '192.168.158.1',
            'port':         1521,
            'sid':          'maixiaochai',
            'service_name': 'maixiaochai'
        }
    """

    def __init__(self, username, password, host, port, sid=None, service_name=None):
        """
        sid 和 service_name至少存在一个, 若都存在，则默认使用service_name
        """
        self.__pool = self.__get_pool(username, password, host, port, sid=sid, service_name=service_name)

    @staticmethod
    def __get_pool(username, password, host, port, sid=None, service_name=None, min_size=8, max_size=8, increment=0):
        """
        以下设置，根据需要进行配置
        min_size            初始化时，连接池中至少创建的空闲连接。0表示不创建
        max_size            最大连接数
        increment           每次增加的连接数量

        官方推荐的是使用固定大小的连接池，即min_size=max_size，increment=0，为了连接池的性能，避免连接波动， 也是为了避免连接风暴。
        以下是相关原文
        https://cx-oracle.readthedocs.io/en/latest/user_guide/connection_handling.html#connpool
        The Oracle Real-World Performance Group’s recommendation is to use fixed size connection pools.
        The values of min and max should be the same (and the increment equal to zero).
        This avoids connection storms which can decrease throughput.

        连接风暴的产生过程：
        https://docs.oracle.com/en/database/oracle/oracle-database/21/adfns/connection_strategies.html#GUID-1B9A21E9-B8E6-4F75-AC9D-1F5D13A1F6F9
        A connection storm is a race condition in which application servers initiate an increasing number of connection requests,
        but the database server CPU is unable to schedule them immediately, which causes the application servers to create more connections.


        https://docs.oracle.com/en/database/oracle/oracle-database/21/adfns/connection_strategies.html#GUID-7DFBA826-7CC0-4D16-B19C-31D168069B54
        A prevalent myth is that a dynamic connection pool creates connections as required and reduces them when they are not needed.
        In reality, when the connection pool is exhausted, application servers enable the size of the pool of database connections to increase rapidly.
        The number of sessions increases with little load on the system, leading to a performance problem when all the sessions become active.

        连接数推荐：
        As a rule of thumb, the Oracle Real-World Performance group recommends a 90/10 ratio of %user to %system CPU utilization,
        and an average of no more than 10 processes per CPU core on the database server.
        The number of connections should be based on the number of CPU cores and not the number of CPU core threads.
        For example, suppose a server has 2 CPUs and each CPU has 18 cores.Each CPU core has 2 threads.
        Based on the Oracle Real-Wold Performance group guidelines,
        the application can have between 36 and 360 connections to the database instance.

        根据经验，Oracle Real-World Performance组建议用户和系统CPU利用率的比例为90:10，
        并且在数据库服务器上，平均每个CPU内核不超过10个进程。连接数应该以CPU核数为基础，而不是CPU内核线程数。
        例如，假设服务器有2个CPU，每个CPU有18个内核。每个CPU内核有2个线程。
        根据Oracle Real-Wold Performance组指南，应用程序可以有36到360个连接到数据库实例。
        """
        dsn = None
        if service_name:
            dsn = Oracle.makedsn(host, port, service_name=service_name)
        elif sid:
            dsn = Oracle.makedsn(host, port, sid=sid)

        # Oracle.SPOOL_ATTRVAL_WAIT: 从连接池中获取连接时，如果没有可用连接，进行等待，直到有可用连接
        return Oracle.SessionPool(user=username, password=password, dsn=dsn, min=min_size, max=max_size,
                                  increment=increment, getmode=Oracle.SPOOL_ATTRVAL_WAIT, encoding='UTF-8',
                                  threaded=True)

    @property
    @contextmanager
    def pool(self):
        _conn = None
        _cursor = None
        try:
            _conn = self.__pool.acquire()
            _cursor = _conn.cursor()
            yield _cursor
        finally:
            _conn.commit()
            # 释放连接
            self.__pool.release(_conn)

    def execute(self, sql: str, *args, **kwargs):
        """
        执行sql语句
        :param sql:     str     sql语句
        :param args:    list    sql语句参数列表
        :return:        conn, cursor
        """
        with self.pool as cursor:
            cursor.execute(sql, *args, **kwargs)

    def executemany(self, sql, *args, **kwargs):
        """
        批量执行。
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """
        with self.pool as cursor:
            cursor.executemany(sql, *args, **kwargs)

    def fetchone(self, sql, *args, **kwargs) -> tuple:
        """
        获取全部结果
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """
        with self.pool as cursor:
            cursor.execute(sql, *args, **kwargs)
            return cursor.fetchone()

    def fetchall(self, sql, *args, **kwargs):
        """
        获取全部结果
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """
        with self.pool as cursor:
            cursor.execute(sql, *args, **kwargs)
            return cursor.fetchall()

    def __del__(self):
        """
        关闭连接池。
        """
        self.__pool.close()
