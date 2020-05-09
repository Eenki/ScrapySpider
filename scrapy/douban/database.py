#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
# 定义连接数据库
MYSQL_DB = 'douban'
MYSQL_USER = 'root'
MYSQL_PASS = 'HCthgu@mimi9'
MYSQL_HOST = '127.0.0.1'
connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                             password=MYSQL_PASS, db=MYSQL_DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

