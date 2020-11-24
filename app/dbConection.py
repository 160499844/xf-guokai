#!/usr/bin/env pytho
# -*- coding:utf-8 -*-
import pymysql
class SqlConection:
    def __init__(self):
        # 创建连接
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='python_home', charset='utf8')
        # 创建游标
        self.cursor = self.conn.cursor()
    def getConection(self):
        return self.cursor

    def close(self):
        self.conn.commit()
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()
"""查询结果集"""
def excute(sql):
    conection = SqlConection()
    con = conection.getConection()
    con.execute(sql)
    data = con.fetchone()
    # 使用fetall()获取全部数据
    conection.close()
    return data
"""插入数据"""
def add(sql):
    conection = SqlConection()
    con = conection.getConection()
    con.execute(sql)
    conection.close()