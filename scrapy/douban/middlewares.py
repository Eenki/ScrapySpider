# -*- coding: utf-8 -*-

# Define here the models for your spider middleware

import random
import time
import urllib
import requests
import datetime
t = time.time()
from scrapy import signals
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse

class SeleniumDownloadMiddleware(object):
    def __init__(self):
        from selenium import webdriver
        # 从芝麻代理获取一个代理IP
        try:
            url = 'http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=440000&city=441900&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
            html_one = urllib.request.Request(url)
            html_one.add_header('User-Agent', 'Mozilla/6.0')
            html_one = urllib.request.urlopen(html_one)
            html = html_one.read()
            print(str(html).split('\'')[1].split("\\")[0])
        except Exception as e:
            print("fff")
        #赋值
        chromeOptions = webdriver.ChromeOptions()
        #跳过ssl校验
        chromeOptions.add_argument('--ignore-certificate-errors')
        # 注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
        chromeOptions.add_argument("--proxy-server=http://"+str(html).split('\'')[1].split("\\")[0])
        # 加代理
        self.driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",chrome_options = chromeOptions)
        # 打开超时时间
        self.driver.set_page_load_timeout(20)
        #self.driver = webdriver.Chrome(executable_path=r" ")

    # 发出请求前
    def process_request(self,request,spider):
        "https: // movie.douban.com/subject/xxxxx"
        # 过滤豆瓣普通页面，不用selenium加载
        if  "https://movie.douban.com" in request.url and request.url != "https://movie.douban.com/tag/#/?sort=T&range=0,10&tags=%E7%9F%AD%E7%89%87,60%E5%B9%B4%E4%BB%A3" and request.url != "https://movie.douban.com/tag/#/?sort=S":
            return None
        # 发出请求
        self.driver.get(request.url)
        # 等待浏览器加载
        if request.url != "https://www.jianshu.com/" and "https://www.jianshu.com/" in request.url:
            time.sleep(1)
        else:
            time.sleep(7)

        # 点击“加载更多”次数变量num
        num=0
        try:
            while True:
                # 过滤简书普通页面 判断是简书首页
                if request.url != "https://www.jianshu.com/" and request.url != "https://movie.douban.com/tag/#/?sort=T&range=0,10&tags=%E7%9F%AD%E7%89%87,60%E5%B9%B4%E4%BB%A3" and request.url != "https://movie.douban.com/tag/#/?sort=S":
                    break
                # 下拉操作
                for i in range(1000):
                    js = 'window.scrollTo(0,%s)' % (i * 100)
                self.driver.execute_script(js)
                time.sleep(2)

                for i in range(1000):
                    js = 'window.scrollTo(0,%s)' % (i * 100)
                self.driver.execute_script(js)
                time.sleep(2)
                #判断是简书页面
                if request.url == "https://www.jianshu.com/":
                    showMore = self.driver.find_element_by_class_name("load-more")
                else:
                    # 豆瓣电影页面
                    if num>10:
                        break
                    showMore = self.driver.find_element_by_class_name("more")
                    num=num+1
                showMore.click()

                if not showMore:
                    break
        except:
            pass
        # 把网页源代码source封装成response对象，再返回给爬虫
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url,body=source,request=request,encoding='utf-8')
        return response

    # 处理前
    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回状态不是200，重新生成当前request对象，更换代理
        if response.status != 200 and response.status != 404 or "login" in request.url:
            try:
                url = 'http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=440000&city=441900&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
                html_one = urllib.request.Request(url)
                html_one.add_header('User-Agent', 'Mozilla/6.0')
                html_one = urllib.request.urlopen(html_one)
                html = html_one.read()
                print(html)
                # 赋值
                proxy = str(html).split('\'')[1].split("\\")[0]
                chromeOptions = webdriver.ChromeOptions()
                # 注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
                chromeOptions.add_argument("--proxy-server=http://" + proxy)
               # 浏览器打开
                self.driver = webdriver.Chrome(
                    executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",
                    chrome_options=chromeOptions)
                return request
            except Exception as e:
                return response
        return response





# spider中间件
# 中间件使爬虫更加健硕
# 下载器中间件


# 设置随机IP代理，随机useragent
class ProxyMiddleware(object):

    def __init__(self):
        self.userAgentList = []
        # 取useragent
        with open('D:\\毕设\\userAgent.txt','r') as fr:
            for line in fr:
                self.userAgentList.append(line.strip())

    # 请求前更换随机ua
    def process_request(self, request, spider):
        # 随机选取一个useragent
        agent = random.choice(self.userAgentList)
        #print(agent)
        request.headers['User-Agent'] = agent


    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200 and response.status != 404:
            try:
                url = 'http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=440000&city=441900&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
                html_one = urllib.request.Request(url)
                html_one.add_header('User-Agent', 'Mozilla/6.0')
                html_one = urllib.request.urlopen(html_one)
                html = html_one.read()
                print(html)
                # 获取到一个代理IP
                print(str(html).split('\'')[1].split("\\")[0])
                # 把request的proxy参数替换
                request.meta['proxy'] = str(html).split('\'')[1].split("\\")[0]
                return request
            except Exception as e:
                return response
        return response




