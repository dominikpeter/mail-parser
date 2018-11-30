from scrapy import Selector
import requests


def get_top_level_domain():
    req = requests.get(
        "https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains")
    selector = Selector(text=req.text)
    domains = selector.xpath("*//table/tbody/tr/td[1]/a/text()").extract()
    domains = [i[1:] for i in domains]
    return domains


TOP_LEVEL_DOMAINS = get_top_level_domain()
