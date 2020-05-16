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

#简书
class ArticleItem(Item):
    # 标题
    title = Field()
    # 内容
    content = Field()
    # 文章id
    article_id = Field()
    # 文章url
    origin_url = Field()
    # 作者
    author = Field()
    # 头像
    avatar = Field()
    # 发表时间
    pub_time = Field()
    # 阅读数
    read_count = Field()
    # 喜欢数
    like_count = Field()
    # 字数
    words_count = Field()
    # 评论数
    comment_count = Field()
    # 专题
    subjects = Field()
