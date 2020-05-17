# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import douban.database as db
from douban.items import ArticleItem

cursor = db.connection.cursor()
class JsSpiderSpider(CrawlSpider):
    name = 'jianshu_article'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}$'), callback='parse_detail', follow=True),
    #     # 通过对url分析，文章id是由0-9数字和a-z小写字母组成。正则表达式里面.*表示可有可无
    # )
    def process_value(value):
        #print("dsmalvbnufeoabvfahucdsnajchdsauivbfahvudsahvufhave9faihvf0jvif")
        m=re.findall("[0-9a-z]{12}", value)
        if m:
            sql = 'SELECT id FROM article WHERE article_id=\'%s\'' % m[0]
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
        Rule(LinkExtractor(allow=(r'.*/p/[0-9a-z]{12}$')), callback='parse_detail', follow=True),
        # 通过对url分析，文章id是由0-9数字和a-z小写字母组成。正则表达式里面.*表示可有可无 ,process_value = process_value
    )

    def parse_detail(self, response):
        title = response.xpath("//h1/text()").get()
        avatar = response.xpath("//a/img/@src").get()
        author = response.xpath("//span/a/text()").get()
        pub_time = response.xpath("//time/text()").get()
        origin_url = response.url
        # url被问号？分割后返回一个列表['https://www.jianshu.com/p/a0199fe1507c', 'utm_campaign=maleskine&utm_content=note&utm_medium=pc_all_hots&utm_source=recommendation']
        # 或者得到列表['https://www.jianshu.com/p/a0199fe1507c']
        url = origin_url.split('?')[0]
        article_id = url.split('/')[-1]
        # 文章内容，包括所有的纯文本信息
        content = "".join(response.xpath("//article//text()").getall())
        words_count = response.xpath("//div/span/text()").get()
        like_count = response.xpath("//span[@class='_1LOh_5']/text()").get()
        read_count = response.xpath("//div/span[last()]/text()").get()
        # '字数 1657'、'评论 38'、'喜欢 244'、'阅读 8292' 需要用空格符分隔开
        words_count = words_count.split(" ")[-1]
        like_count = like_count.split("人")[0]
        read_count = read_count.split(" ")[-1]
        # 让返回来的列表变成字符串，以逗号分开
        subjects = ",".join(response.xpath("//div[@class='_2Nttfz']/a/span/text()").getall())

        item = ArticleItem(
            title = title,
            content = content,
            avatar = avatar,
            author = author,
            pub_time = pub_time,
            origin_url = origin_url,
            article_id = article_id,
            words_count = words_count,
            like_count = like_count,
            read_count = read_count,
            subjects = subjects
        )
        yield item

