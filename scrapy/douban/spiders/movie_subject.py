#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import re
import string
import douban.database as db
from douban.items import Subject
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule


cursor = db.connection.cursor()

class MovieSubjectSpider(CrawlSpider):
    name = 'movie_subject'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/tag/#/?sort=S']
    # rules定义进行内容页字段的提取规则
    # Link Extractor定义从爬取到的页面使用正则匹配提取以/ subject /开头、以subject-page结尾的豆瓣id，每一个爬取到的url页面数据使用callback解析
    # follow=True(跟进), 爬虫会在爬取的页面中再寻找符合规则的url，如此循环，直到把全站爬取完毕
    # , process_value = self.process_value
    def process_value(value):
        #print("dsmalvbnufeoabvfahucdsnajchdsauivbfahvudsahvufhave9faihvf0jvif")
        m=re.findall("\d+", value)
        if m:
            sql = 'SELECT id FROM subjects WHERE douban_id=%s' % m[0]
            #print(sql)
            cursor.execute(sql)
            exist = cursor.fetchone()
            if not exist:
                return value
            else:
                return None
        else:
            return None


    rules = (
        Rule(LinkExtractor(allow=('https://movie.douban.com/subject/\d+/.*')),callback='parse_item', follow=True, process_request='cookie'),
    )


    def cookie(self, request):
        # 随机生成字符串
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
        request.cookies['bid'] = bid
        request = request.replace(url=request.url.replace('?', '/?'))
        return request


    # 构造将要爬的网页URL
    def start_requests(self):
        for url in self.start_urls:
            bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
            yield Request(url, cookies={'bid': bid})

    #正则匹配获取各网页id
    def get_douban_id(self, subject, response):
        try:
            subject['douban_id'] = re.search('\d+',response.url,re.M|re.I).group()
            return subject
        except:
            return None

    # 回调函数
    # 定义返回响应之后如何解析
    # 解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象
    def parse_item(self, response):
        subject = Subject()
        self.get_douban_id(subject, response)
        subject['type'] = 'movie'
        return subject

