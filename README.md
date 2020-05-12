# test scrapy111
## 1. 修改selenium中间件中chromedriver.exe的位置信息

middlewares.py 21行，改成自己的chromedriver.exe 地址，用everything搜索可找到。

## 2. 修改最新的代理IP

## 3. 默认打开selenium功能，可以直接爬取简书，如果爬取其他网站，请注释掉setting.py中的相关配置项