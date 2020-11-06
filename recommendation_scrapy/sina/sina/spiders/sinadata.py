import scrapy
from selenium import webdriver
from scrapy.http import Request
from recommendation_scrapy.sina.sina.items import DataItem
from scrapy.selector import Selector
import time
import os
import pandas as pd
import datetime
import sys
import re



class SinadataSpider(scrapy.Spider):
    name = 'sinadata'
    #allowed_domains = ['sina.com.cn']

    def __init__(self, page = None,flag = None,*args,**kwargs):

        super(SinadataSpider, self).__init__(*args,**kwargs)
        self.page = int(page)
        self.flag = int(flag)  # 0是跑全量，1是跑增量

        self.start_urls = ["https://ent.sina.com.cn/film/",
                           "https://ent.sina.com.cn/zongyi/",
                           "https://news.sina.com.cn/china/"]


        self.option = webdriver.ChromeOptions()
        self.option.add_argument('headless') # 设置不打开浏览器
        self.option.add_argument('no=sandbox')
        self.option.add_argument('--blink-setting=imagesEnabled=false')  #不显示图片

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url,callback=self.parse)


    def parse(self, response):
        driver = webdriver.Chrome(chrome_options=self.option)
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30) # 网页加载等待时间
        driver.get(response.url)

        for i in range(self.page):
            # 如果找不到下一页按钮，就一直往下滑
            while not driver.find_element_by_xpath("//div[@class='feed-card-page']").text:

                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

            title = driver.find_elements_by_xpath("//h2[@class='undefined']/a[@target='_blank']")
            time = driver.find_elements_by_xpath("//h2[@class='undefined']/../div[@class='feed-card-a feed-card-clearfix']/div[@class='feed-card-time']")
            for i in range(len(title)):
                each_title = title[i].text
                each_time = time[i].text
                item = DataItem()
                if response.url == "https://ent.sina.com.cn/zongyi/":
                    item['type'] = 'zongyi'
                elif response.url == "https://news.sina.com.cn/china/":
                    item['type'] = 'news'
                else:
                    item['type'] = 'film'
                item['title'] = each_title
                item['desc'] = ''
                href = title[i].get_attribute('href')

                today = datetime.datetime.now()
                each_time = each_time.replace('今天',str(today.month)+'月'+str(today.day)+'日')
                if '分钟前' in each_time:
                    minute = int(each_time.split('分钟前')[0])
                    t = datetime.datetime.now() - datetime.timedelta(minutes=minute)
                    t2 = datetime.datetime(year=t.year , month=t.month, day=t.day , hour=t.hour,minute=t.minute)
                else:
                    if '年' not in each_time:
                        each_time = str(today.year) + '年' + each_time
                    t1 = re.split('[年月日:]',each_time)
                    t2 = datetime.datetime(year=int(t1[0]) ,month=int(t1[1]),day=int(t1[2]) ,hour=int(t1[3]),minute=int(t1[4]))

                item['times'] = t2

                if self.flag == 1:
                    today = datetime.datetime.now().strftime("%Y-%m-%d")
                    yesterday = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
                    if item['times'].strftime("%Y-%m-%d")<yesterday:
                        driver.close()
                        break
                    if yesterday <= item['times'].strftime("%Y-%m-%d") < today:
                        yield Request(url=response.urljoin(href), meta={'name': item}, callback = self.parse_namedetail)

                else:
                    yield Request(url = response.urljoin(href),meta={'name':item}, callback = self.parse_namedetail)

            # 翻页
            #driver.find_element_by_xpath("//div[@class='feed-card-page']/span[@class='pagebox_next']/a").click()
            element = driver.find_element_by_xpath("//div[@class='feed-card-page']/span[@class='pagebox_next']/a")

            driver.execute_script("arguments[0].click();", element)

    # 进入新闻内部 解析文本
    def parse_namedetail(self,response):

        selector = Selector(response)
        desc = selector.xpath("//div[@class='article']/p/text()").extract() #拿到具体的新闻描述
        item = response.meta['name']
        desc = list(map(str.strip, desc))
        item['desc'] = ''.join(desc)
        yield item



