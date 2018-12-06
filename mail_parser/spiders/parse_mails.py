# -*- coding: utf-8 -*-

import re

from scrapy import Spider
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlsplit
from mail_parser.items import MailParserItem
from mail_parser.homepages import DICT_OF_HOMEPAGES
from collections import defaultdict
from w3lib.html import remove_tags, remove_tags_with_content
from scrapy import Selector



class ParseMailsSpider(Spider):
    name = 'parse_mails'
    start_urls = [DICT_OF_HOMEPAGES[i][1] for i in DICT_OF_HOMEPAGES]

    allowed_domains = [urlsplit(i).netloc for i in start_urls]

    def parse(self, response):

        refs = response.xpath("*//@href").extract()

        for i in refs:
            if i.startswith("/"):
                url = response.urljoin(i)
                yield Request(url, callback=self.parse_mail)


    def parse_mail(self, response):

        try:
            product = MailParserItem()
            mail_regex = re.compile(r"[\w\.-]+@[\w\.-]+")
            mails = mail_regex.findall(response.text)
            for mail in mails:
                url = response.url
                domain = urlsplit(url).netloc.replace("www.", "")
                mail_domain = mail.partition("@")[-1]

                product['mail'] = mail
                product['url'] = url
                product['domain'] = domain
                product['mail_equal_domain'] = domain == mail_domain

                try:
                    parent = response.xpath(
                        "//*[contains(., '{}')]".format(mail))[-2]
                    parent =  parent.xpath(".//text()").extract()
                    parent = ' | '.join(
                        [i.strip() for i in parent if i.strip()])
                    product['parent_html'] = parent
                except IndexError:
                    product['parent_html'] = ''

                yield dict(product)

        except AttributeError:
            product['mail'] = ''
            pass
