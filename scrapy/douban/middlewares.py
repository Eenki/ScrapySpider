# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time
import urllib
import json
from bs4 import BeautifulSoup
from scrapy import signals
from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse

class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"C:\Users\Eenki\AppData\Local\Google\Chrome\Application\chromedriver.exe")
        #self.driver = webdriver.Chrome(executable_path=r" ")

    def process_request(self,request,spider):
        self.driver.get(request.url)
        time.sleep(1)
        try:
            while True:
                showMore = self.driver.find_element_by_class_name("show-more")
                showMore.click()
                #time.sleep(0.3)
                if not showMore:
                    break
        except:
            pass
        source = self.driver.page_source
        # 把网页源代码source封装成response对象，再返回给爬虫
        response = HtmlResponse(url=self.driver.current_url,body=source,request=request,encoding='utf-8')
        return response

# spider中间件
# 中间件使爬虫更加健硕
class DoubanSpiderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 下载器中间件
class DoubanDownloaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 设置随机IP代理，随机useragent
class ProxyMiddleware(object):
    def __init__(self):
        self.userAgentList = []
        # 取useragent
        with open('D:\\毕设\\userAgent.txt','r') as fr:
            for line in fr:
                self.userAgentList.append(line.strip())

    def process_request(self, request, spider):
        #设置代理
        # url = 'http://127.0.0.1:5010/get/'
        # html_one = urllib.request.Request(url)
        # html_one.add_header('User-Agent', 'Mozilla/6.0')
        # html_one = urllib.request.urlopen(html_one)
        # html = html_one.read()
        # print("1"+html.decode())
        # print(json.loads(html)["proxy"])
        # request.meta['proxy'] = json.loads(html)["proxy"]
        request.meta['proxy'] ="58.218.92.65:4814"
        # 随机选取一个useragent
        agent = random.choice(self.userAgentList)
        print(agent)
        request.headers['User-Agent'] = agent


