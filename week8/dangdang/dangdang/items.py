# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Demo1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()#标题
    author = scrapy.Field()#作者
    date = scrapy.Field()#发布日期
    publisher = scrapy.Field()#出版社
    detail = scrapy.Field()#细节介绍
    price = scrapy.Field()#价格
    #pass

