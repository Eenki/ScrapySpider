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
        self.driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

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
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 下载器中间件
class DoubanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
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
        #request.meta['proxy'] ="127.0.0.1:1080"
        # 随机选取一个useragent
        agent = random.choice(self.userAgentList)
        print(agent)
        request.headers['User-Agent'] = agent


# 代理扫描检测
class ProxyScanVerification():
    def __init__(self):
        self.IPList_61()

    def IPList_61(self):
        for q in [1, 2,3,4,5,6,7,8,9]:
            url = 'http://www.66ip.cn/' + str(q) + '.html'
            html_one  = urllib.request.Request(url)
            html_one .add_header('User-Agent', 'Mozilla/6.0')
            html_one  = urllib.request.urlopen(html_one)
            html = html_one.read().decode('utf-8')
            if html != None:
                print(html)
                iplist = BeautifulSoup(html, 'lxml')
                iplist = iplist.find_all('tr')
                i = 2
                for ip in iplist:
                    if i <= 0:
                        loader = ''
                        # print(ip)
                        j = 0
                        for ipport in ip.find_all('td', limit=2):
                            if j == 0:
                                loader += ipport.text.strip() + ':'
                            else:
                                loader += ipport.text.strip()
                            j = j + 1
                        # .inspect_ip(loader)
                    i = i - 1
            time.sleep(1)



