# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=440000&city=441900&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'

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
            #芝麻代理
            url = 'http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=440000&city=441900&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
            html_one = urllib.request.Request(url)
            html_one.add_header('User-Agent', 'Mozilla/6.0')
            html_one = urllib.request.urlopen(html_one)
            html = html_one.read()
            html = str(html).split('\'')[1].split("\\")[0]
            print(str(html).split('\'')[1].split("\\")[0])

            #自己的代理IP池
            # url = 'http://127.0.0.1:5000/get/'
            # html_one = urllib.request.Request(url)
            # html_one.add_header('User-Agent', 'Mozilla/6.0')
            # html_one = urllib.request.urlopen(html_one)
            # html = html_one.read()
            # print(str(html).split('\'')[1])
            # html = str(html).split('\'')[1]

        except Exception as e:
            print("fffkkk")
        #赋值
        chromeOptions = webdriver.ChromeOptions()
        # #跳过ssl校验
        #chromeOptions.add_argument('--ignore-certificate-errors')
        # # 注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
        #chromeOptions.add_argument("--proxy-server=http://"+html)
        # 加代理
        self.driver = webdriver.Chrome(executable_path=r"C:\Users\Eenki\AppData\Local\Google\Chrome\Application\chromedriver.exe",chrome_options = chromeOptions)
        # 打开超时时间

        #self.driver = webdriver.Chrome(executable_path=r" ")

    # 发出请求前
    def process_request(self,request,spider):
        # 过滤豆瓣普通页面，不用selenium加载
        if "tags=" in request.url:
            self.driver.get('https://www.douban.com/')
            time.sleep(1)
            ## 切换iframe子框架
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[0])
            # self.driver.maximize_window()  # 最大化窗口
            self.driver.find_element_by_css_selector('li.account-tab-account').click()  # 点击密码登录的标签
            self.driver.find_element_by_id('username').send_keys('13667831367')
            self.driver.find_element_by_id('password').send_keys('122306')
            # 点击‘登录豆瓣’按钮
            # 这里需要注意，当元素的class属性有好几个的时候，此函数的参数填class的第一个就好
            self.driver.find_element_by_class_name('btn').click()  # 元素的class属性：btn btn-account
            # 获取cookies,字典推导式
            cookies = {i['name']: i['value'] for i in self.driver.get_cookies()}
            # cookies = self.driver.get_cookies()
            print(cookies)
            time.sleep(1)
        if  "https://movie.douban.com" in request.url and request.url != "https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=2000%E5%B9%B4%E4%BB%A3" and request.url != "https://movie.douban.com/tag/#/?sort=S":
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
                if request.url != "https://www.jianshu.com/" and request.url != "https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=2000%E5%B9%B4%E4%BB%A3" and request.url != "https://movie.douban.com/tag/#/?sort=S":
                    break
                #两次下拉操作
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
                    if num>30:
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

    # 换代理
    def process_response(self, request, response, spider):
        #对返回的response处理
        # 如果返回状态不是200，重新生成当前request对象，更换代理
        if response.status != 200 and response.status != 404 or "login" in request.url:
            try:
                self.driver.get('https://www.douban.com/')
                time.sleep(1)
                ## 切换iframe子框架
                self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[0])
                # self.driver.maximize_window()  # 最大化窗口
                self.driver.find_element_by_css_selector('li.account-tab-account').click()  # 点击密码登录的标签
                self.driver.find_element_by_id('username').send_keys('13667831367')
                self.driver.find_element_by_id('password').send_keys('122306')
                # 点击‘登录豆瓣’按钮
                # 这里需要注意，当元素的class属性有好几个的时候，此函数的参数填class的第一个就好
                self.driver.find_element_by_class_name('btn').click()  # 元素的class属性：btn btn-account
                # 获取cookies,字典推导式
                cookies = {i['name']: i['value'] for i in self.driver.get_cookies()}
                # cookies = self.driver.get_cookies()
                print(cookies)
                time.sleep(1)
                return request
            except Exception as e:
                return response
        return response


# 设置随机useragent
class UserAgentMiddleware(object):
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
        print(agent)
        request.headers['User-Agent'] = agent

#随机IP代理，
class ProxyMiddleware(object):
    # 随机IP代理
    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200 and response.status != 404:
            try:
                # 芝麻代理
                url = 'http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=440000&city=441900&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
                html_one = urllib.request.Request(url)
                html_one.add_header('User-Agent', 'Mozilla/6.0')
                html_one = urllib.request.urlopen(html_one)
                html = html_one.read()
                print(html)
                html = str(html).split('\'')[1].split("\\")[0]
                # 获取到一个代理IP
                #print(str(html).split('\'')[1].split("\\")[0])

                # 自己的代理IP池
                # url = 'http://127.0.0.1:5000/get/'
                # html_one = urllib.request.Request(url)
                # html_one.add_header('User-Agent', 'Mozilla/6.0')
                # html_one = urllib.request.urlopen(html_one)
                # html = html_one.read()
                # print(str(html).split('\'')[1])
                # html = str(html).split('\'')[1]

                # 把request的proxy参数替换
                request.meta['proxy'] = html
                return request
            except Exception as e:
                return response
        return response




