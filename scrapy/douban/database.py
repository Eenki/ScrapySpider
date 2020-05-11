#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
# 定义连接数据库
MYSQL_DB = 'douban'
MYSQL_USER = 'root'
MYSQL_PASS = 'HCthgu@mimi9'
#MYSQL_PASS = '123456'
MYSQL_HOST = '121.37.16.227'
connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                             password=MYSQL_PASS, db=MYSQL_DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

