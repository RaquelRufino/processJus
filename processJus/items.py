# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProcessjusItem(scrapy.Item):
    
    classe = scrapy.Field()
    area = scrapy.Field()
    subject = scrapy.Field()
    distribuition_date = scrapy.Field()
    judge = scrapy.Field()
    share_value = scrapy.Field()
    parts = scrapy.Field()
    drives = scrapy.Field()