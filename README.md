# test scrapy111
## 1.路径
### 1.1 修改selenium中间件中chromedriver.exe的位置信息
      在middlewares.py 32行 （需注意chrome driver版本与chrome相同）
### 1.2 useragent 路径
      在middlewares.py 84行
### 1.3 修改数据库连接信息
      在database.py文件
      
## 2. 打开selenium功能，爬取简书
      在settings.py 41行 取消注释，爬取豆瓣需注释
      
## 3.命令使用
      scrapy list：列出当前爬虫程序名字（需进入spiders文件夹下）
      scrapy crawl 爬虫名字：执行爬虫
## 4.执行过程
      1.豆瓣电影：先执行movie_subject爬取豆瓣id，再执行movie_meta爬取数据
      2.简书：直接执行jianshu_article