# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

'''
class ZongyiItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()

class FilmItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()

'''

# 配置Item类
class DataItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()
    type = scrapy.Field()
