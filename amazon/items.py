# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    Book_Name = scrapy.Field()
    Book_Author = scrapy.Field()
    Book_Price = scrapy.Field()
    Book_Image = scrapy.Field()
