# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from douban.items import ArticleItem


class JsSpiderSpider(CrawlSpider):
    name = 'js_spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com']

    # rules = (
    #     Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}$'), callback='parse_detail', follow=True),
    #     # 通过对url分析，文章id是由0-9数字和a-z小写字母组成。正则表达式里面.*表示可有可无
    # )


    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}$'), callback='parse_detail', follow=True),
        # 通过对url分析，文章id是由0-9数字和a-z小写字母组成。正则表达式里面.*表示可有可无
    )

    def parse_detail(self, response):
        strs = str(response.body,'utf-8')

        title = response.xpath("//h1/text()").get()
        avatar = response.xpath("//a/img/@src").get()
        print(title)
        print(avatar)
        author = response.xpath("//span/a/text()").get()
        pub_time = response.xpath("//time/text()").get()
        print(author)
        print(pub_time)

        origin_url = response.url
        print(origin_url)
        # url被问号？分割后返回一个列表['https://www.jianshu.com/p/a0199fe1507c', 'utm_campaign=maleskine&utm_content=note&utm_medium=pc_all_hots&utm_source=recommendation']
        # 或者得到列表['https://www.jianshu.com/p/a0199fe1507c']
        url = origin_url.split('?')[0]
        article_id = url.split('/')[-1]
        # 文章内容，包括所有的html标签，而不是纯文本信息
        content = "".join(response.xpath("//article//text()").getall())
        print(content)

        words_count = response.xpath("//div/span/text()").get()
        print(words_count)
        # comment_count = response.xpath("//div/span[@class='_2R7vBo'][last()]/text()").get()
        # print(comment_count)
        like_count = response.xpath("//span[@class='_1LOh_5']/text()").get()
        print(like_count)
        read_count = response.xpath("//div/span[last()]/text()").get()
        print(read_count)
        #print(response.body)
        # print("words_count"+words_count)
        # print("comment_count"+comment_count)
        # print("like_count"+like_count)
        # print(read_count)
        # print(content)

        # '字数 1657'、'评论 38'、'喜欢 244'、'阅读 8292' 需要用空格符分隔开
        words_count = words_count.split(" ")[-1]
        # words_count = 121
        # print(words_count)
        # comment_count = comment_count.split(" ")[-1]
        like_count = like_count.split("人")[0]
        read_count = read_count.split(" ")[-1]
        # subjects = response.xpath("//div[@class='include-collection']/a/div/text()").getall()
        # subjects所有的主题返回的是一个列表，需要把列表转换成字符串（MySQL数据库中不支持列表）
        # 让返回来的列表变成字符串，以逗号分开
        subjects = ",".join(response.xpath("//div[@class='_2Nttfz']/a/span/text()").getall())
        print(subjects)


        item = ArticleItem(
            title = title,
            content = content,
            avatar = avatar,
            author = author,
            pub_time = pub_time,
            origin_url = origin_url,
            article_id = article_id,
            words_count = words_count,
            comment_count = "",
            like_count = like_count,
            read_count = read_count,
            subjects = subjects
        )
        yield item

