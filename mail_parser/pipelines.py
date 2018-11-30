# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from mail_parser.constants import TOP_LEVEL_DOMAINS
from urllib.parse import urljoin


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['mail'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['mail'])
            return item


class CleanMailPipeline(object):

    def __init__(self):
        self.domains = TOP_LEVEL_DOMAINS

    def process_item(self, item, spider):
        if item['mail'].split(".")[-1] not in self.domains:
            raise DropItem("Top-Level-Domain does not exist: %s" % item)
        else:
            return item
