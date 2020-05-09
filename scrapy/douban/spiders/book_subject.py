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

class BookSubjectSpider(CrawlSpider):
    name = 'book_subject'
    allowed_domains = ['book.douban.com']
    # 爬取入口点
    start_urls = ['https://book.douban.com/subject/1300000','https://book.douban.com/subject/1300001','https://book.douban.com/subject/1300002']
    def process_value(value):
        #print("dsmalvbnufeoabvfahucdsnajchdsauivbfahvudsahvufhave9faihvf0jvif")
        m=re.findall("\d+", value)
        if m:
            sql = 'SELECT id FROM subjects WHERE type="book" and douban_id=%s' % m[0]
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
        Rule(LinkExtractor(allow=('/subject/\d+/$'),process_value = process_value),
             callback='parse_item', follow=True, process_request='cookie'),
    )

    def cookie(self, request):
        # 设置随机数
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
        request.cookies['bid'] = bid
        request = request.replace(url=request.url.replace('?', '/?'))
        return request

    def start_requests(self):
        for url in self.start_urls:
            bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
            yield Request(url, cookies={'bid': bid})

    def get_douban_id(self, subject, response):
        subject['douban_id'] = re.search('\d+',response.url,re.M|re.I).group()
        return subject

    def parse_item(self, response):
        subject = Subject()
        self.get_douban_id(subject, response)
        subject['type'] = 'book'
        return subject
