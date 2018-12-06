# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MailParserItem(scrapy.Item):
    # define the fields for your item here like:
    mail = scrapy.Field()
    url = scrapy.Field()
    domain = scrapy.Field()
    mail_equal_domain = scrapy.Field()
    parent_html = scrapy.Field()
