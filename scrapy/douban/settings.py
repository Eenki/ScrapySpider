# -*- coding: utf-8 -*-

import random


BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

LOG_LEVEL = 'DEBUG'
IMAGES_STORE = '../storage/'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5'

# 违背 robots.txt 协议
ROBOTSTXT_OBEY = False

# 设置下载延迟
DOWNLOAD_DELAY = 0

#多线程
#每个IP并发请求数
CONCURRENT_REQUESTS_PER_IP = 30
CONCURRENT_REQUESTS = 300
CONCURRENT_REQUESTS_PER_DOMAIN = 100

# 启用Cookie
COOKIES_ENABLED = False
RETRY_ENABLED = False

# 设置超时
DOWNLOAD_TIMEOUT = 15

# 设置启用下载器中间件
DOWNLOADER_MIDDLEWARES = {
    'douban.middlewares.ProxyMiddleware': 543,
    'douban.middlewares.SeleniumDownloadMiddleware': 543,
    # 'douban.middlewares.RandomUserAgentMiddleware': 543,
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# RANDOM_UA_TYPE = 'random'

# 打开管道
ITEM_PIPELINES = {
    'douban.pipelines.CoverPipeline': 1,
    'douban.pipelines.DoubanPipeline': 300,
}