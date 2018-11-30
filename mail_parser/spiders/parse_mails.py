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


class ParseMailsSpider(Spider):
    name = 'parse_mails'
    start_urls = [DICT_OF_HOMEPAGES[i][1] for i in DICT_OF_HOMEPAGES]

    allowed_domains = [urlsplit(i).netloc for i in start_urls]

    # rules = (
    #     Rule(LinkExtractor(deny=('\?',)), follow=True,
    #             callback='parse_mail'),
    # )


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

                yield dict(product)

        except AttributeError:
            product['mail'] = ''
            pass
