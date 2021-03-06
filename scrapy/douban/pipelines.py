#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 对爬取数据进行进一步处理存储、

import hashlib
import douban.database as db
import pymysql
from twisted.enterprise import adbapi   # 此模块专门用来做数据库处理
from pymysql import cursors
from douban.items import MovieMeta, Subject,ArticleItem
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import to_bytes
from twisted.internet.defer import DeferredList
# 连接数据库
cursor = db.connection.cursor()


class DoubanPipeline(object):
    def get_subject(self, item):
        sql = 'SELECT id FROM subjects WHERE douban_id=%s' % item['douban_id']
        cursor.execute(sql)
        return cursor.fetchone()

    def save_subject(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO subjects (%s) VALUES (%s)' % (fields, temp)
        cursor.execute(sql, values)
        return db.connection.commit()

    def get_movie_meta(self, item):
        sql = 'SELECT id FROM movies WHERE douban_id=%s' % item['douban_id']
        cursor.execute(sql)
        return cursor.fetchone()

    def save_movie_meta(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO movies (%s) VALUES (%s)' % (fields, temp)
        cursor.execute(sql, tuple(i.strip() for i in values))
        return db.connection.commit()

    def update_movie_meta(self, item):
        douban_id = item.pop('douban_id')
        keys = item.keys()
        values = list(item.values())
        values.append(douban_id)
        fields = ['%s=' % i + '%s' for i in keys]
        sql = 'UPDATE movies SET %s WHERE douban_id=%s' % (','.join(fields), '%s')
        cursor.execute(sql, tuple(i.strip() for i in values))
        return db.connection.commit()

    def get_ArticleItem(self,item):
        sql = 'SELECT id FROM article WHERE article_id=\'%s\'' % (item['article_id'])
        print(sql)
        cursor.execute(sql)
        return cursor.fetchone()

    def insert_item(self,item):
        sql = 'insert into article(title,content,author,avatar,pub_time,article_id,origin_url,read_count,like_count,words_count,subjects) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (item['title'],item['content'],item['author'],item['avatar'],item['pub_time'],item['article_id'],item['origin_url'],item['read_count'],item['like_count'],item['words_count'],item['subjects'])
        cursor.execute(sql)
        return db.connection.commit()

    def update_item(self, item):
        sql = 'update article set title=\'%s\',content=\'%s\',author=\'%s\',avatar=\'%s\',pub_time=\'%s\',article_id=\'%s\',origin_url=\'%s\',read_count=\'%s\',like_count=\'%s\',words_count=\'%s\',subjects=\'%s\' where article_id=\'%s\''  % (item['title'],item['content'],item['author'],item['avatar'],item['pub_time'],item['article_id'],item['origin_url'],item['read_count'],item['like_count'],item['words_count'],item['subjects'],item['article_id'])
        cursor.execute(sql)
        return db.connection.commit()

    # 写入数据库操作
    def process_item(self, item, spider):
        # 比较
        if isinstance(item, Subject):
            '''
            subject
            '''
            exist = self.get_subject(item)
            if not exist:
                self.save_subject(item)
                print('新数据入库')
            else:
                print('已存在')
        elif isinstance(item, MovieMeta):
            '''
            meta
            '''
            exist = self.get_movie_meta(item)
            if not exist:
                try:
                    self.save_movie_meta(item)
                    print('***********新数据入库***********')
                except Exception as e:
                    print(e)
            else:
                self.update_movie_meta(item)
                print('***********更新数据*************')
        elif isinstance(item, ArticleItem):
            '''
            ArticleItem
            '''
            exist = self.get_ArticleItem(item)
            if not exist:
                try:
                    self.insert_item(item)
                    print('***********新数据入库***********')
                except Exception as e:
                    print(e)
            else:
                self.update_item(item)
                print('***********更新数据*************')
        return item


class CoverPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        if 'meta' not in spider.name:
            return item
        info = self.spiderinfo
        requests = arg_to_iter(self.get_media_requests(item, info))
        dlist = [self._process_request(r, info) for r in requests]
        dfd = DeferredList(dlist, consumeErrors=1)
        return dfd.addCallback(self.item_completed, item, info)

    def file_path(self, request, response=None, info=None):
        # start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        # end of deprecation warning block

        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()
        return '%s%s/%s%s/%s.jpg' % (image_guid[9], image_guid[19], image_guid[29], image_guid[39], image_guid)

    def get_media_requests(self, item, info):
        if item['cover']:
            return Request(item['cover'])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['cover'] = image_paths[0]
        else:
            item['cover'] = ''
        return item


