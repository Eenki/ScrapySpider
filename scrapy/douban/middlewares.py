# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time
import urllib
import requests
import time
import datetime
t = time.time()
from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse

class SeleniumDownloadMiddleware(object):
    def __init__(self):
        from selenium import webdriver
        # # 进入浏览器设置
        # options = webdriver.ChromeOptions()
        # # 设置中文
        # options.add_argument('lang=zh_CN.UTF-8')
        # # 更换头部
        # options.add_argument(
        #     'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
        # browser = webdriver.Chrome(chrome_options=options)
        self.driver = webdriver.Chrome(executable_path=r"C:\Users\Eenki\AppData\Local\Google\Chrome\Application\chromedriver.exe")
        self.driver.set_page_load_timeout(3)
        #self.driver = webdriver.Chrome(executable_path=r" ")

    def process_request(self,request,spider):
        if  "https://movie.douban.com" in request.url and request.url != "https://movie.douban.com/tag/#/" and request.url != "https://movie.douban.com/tag/#/?sort=S&range=0,10&tags=":
            return None
        self.driver.get(request.url)
        time.sleep(0.5)
        num=0
        # cookie = "__yadk_uid=yZQBCiZInGtHdBbredyvUqjEWWitjTFd; __gads=ID=1e0c7a9798948d90:T=1581307707:S=ALNI_MZWCLBm7hgTltsxAN-qxwxa__FEyg; _ga=GA1.2.1249327465.1583066825; read_mode=day; default_font=font2; locale=zh-CN; remember_user_token=W1s2MjE3MzY2XSwiJDJhJDEwJEllTDNCWWh3Ym0wRUpSUUkuVDhTQnUiLCIxNTg5MzA3NjgxLjgyMDEyNyJd--4099e468a5511a76cca3f85baf122fbb552c7618; _m7e_session_core=d6828bd9e4f092a98c3fb408e775d83f; _gid=GA1.2.236880248.1589307681; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1588865677,1589203478,1589213486,1589309379; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%226217366%22%2C%22first_id%22%3A%2216f4102ce63176-0fc9793dd3c8da-5f4e2917-2073600-16f4102ce648a4%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22recommendation%22%2C%22%24latest_utm_medium%22%3A%22pc_all_hots%22%2C%22%24latest_utm_campaign%22%3A%22maleskine%22%2C%22%24latest_utm_content%22%3A%22note%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%2C%22%24device_id%22%3A%2216f4102ce63176-0fc9793dd3c8da-5f4e2917-2073600-16f4102ce648a4%22%7D; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1589311137"
        # self.driver.add_cookie(cookie)
        try:
            while True:
                if request.url != "https://www.jianshu.com/" and request.url != "https://movie.douban.com/tag/#/" and request.url != "https://movie.douban.com/tag/#/?sort=S&range=0,10&tags=":
                    break
                for i in range(1000):
                    js = 'window.scrollTo(0,%s)' % (i * 100)
                self.driver.execute_script(js)
                time.sleep(1)
                for i in range(1000):
                    js = 'window.scrollTo(0,%s)' % (i * 100)
                self.driver.execute_script(js)
                time.sleep(1)
                if request.url == "https://www.jianshu.com/":
                    showMore = self.driver.find_element_by_class_name("load-more")
                else:
                    if num>30:
                        break
                    showMore = self.driver.find_element_by_class_name("more")
                    num=num+1
                showMore.click()

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
        #request.meta['proxy'] = "127.0.0.1:30808"
        # 随机选取一个useragent
        agent = random.choice(self.userAgentList)
        print(agent)
        request.headers['User-Agent'] = agent

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            try:
                url = 'http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=440000&city=441900&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
                html_one = urllib.request.Request(url)
                html_one.add_header('User-Agent', 'Mozilla/6.0')
                html_one = urllib.request.urlopen(html_one)
                html = html_one.read()
                print(html)
                print(str(html).split('\'')[1].split("\\")[0])
                request.meta['proxy'] = str(html).split('\'')[1].split("\\")[0]
                return request
            except Exception as e:
                return response
        return response




