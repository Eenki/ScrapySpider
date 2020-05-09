#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy import Item, Field
# 定义爬虫需要采集的字段
# 类目id
class Subject(Item):
    # 豆瓣id
    douban_id = Field()
    # 类型
    type = Field()


# 电影源数据
class MovieMeta(Item):
    # 豆瓣id
    douban_id = Field()
    # 分类 电影
    type = Field()
    # 封面照
    cover = Field()
    # 电影名称
    name = Field()
    # slug
    slug = Field()
    # 上映年份
    year = Field()
    # 导演
    directors = Field()
    # 主演
    actors = Field()
    # 类型
    genres = Field()
    # 官方网站
    official_site = Field()
    # 制片国家/地区
    regions = Field()
    # 语言
    languages = Field()
    # 上映日期
    release_date = Field()
    # 片长
    mins = Field()
    # 别名
    alias = Field()
    # IMDb链接
    imdb_id = Field()
    # 豆瓣id
    douban_id = Field()
    # 豆瓣评分
    douban_score = Field()
    # 评价人次
    douban_votes = Field()
    # 标签
    tags = Field()
    # 剧情简介
    storyline = Field()


# 书籍源数据
class BookMeta(Item):
    # 豆瓣id
    douban_id = Field()
    # slug
    slug = Field()
    # 书名
    name = Field()
    # 子名称
    sub_name = Field()
    # 原作名
    alt_name = Field()
    # 封面照
    cover = Field()
    # 内容简介
    summary = Field()
    # 作者
    authors = Field()
    # 作者简介
    author_intro = Field()
    # 译者
    translators = Field()
    # 丛书
    series = Field()
    # 出版社
    publisher = Field()
    # 出版年
    publish_date = Field()
    # 页数
    pages = Field()
    # 定价
    price = Field()
    # 装帧
    binding = Field()
    # ISBN
    isbn = Field()
    # 豆瓣id
    douban_id = Field()
    # 豆瓣评分
    douban_score = Field()
    # 评价人次
    douban_votes = Field()
    # 标签
    tags = Field()


# 评论
class Comment(Item):
    # 豆瓣id
    douban_id = Field()
    # 评论id
    douban_comment_id = Field()
    # 评论昵称
    douban_user_nickname = Field()
    # 评论头像
    douban_user_avatar = Field()
    # 平论url
    douban_user_url = Field()
    # 内容
    content = Field()
    # 票数
    votes = Field()

#简书
class ArticleItem(Item):
    title = Field()
    content = Field()
    article_id = Field()
    origin_url = Field()
    author = Field()
    avatar = Field()
    pub_time = Field()
    read_count = Field()
    like_count = Field()
    words_count = Field()
    comment_count = Field()
    subjects = Field()
