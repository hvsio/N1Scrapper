import json
import scrapy
from scrapper import banks_data
import requests
from scrapper.items import OutputTable, ProductItemLoader


class WebsiteBankSpider(scrapy.Spider):
    name = "bank_website"

    def __init__(self, *args, **kwargs):
        super(WebsiteBankSpider, self).__init__(**kwargs)

        # download the jsons from the http request
        resp = requests.get('http://127.0.0.1:8000/banks')
        # for some reason when it sees format [{"..." : "...", so one}] it wants to parse it into a list instead of dict
        self.data = json.loads(resp.text.strip("[]"))

    def start_requests(self):
        #start_urls = self.data['url']
        start_urls = banks_data.jyske_url

        yield scrapy.Request(url=start_urls, callback=self.parse)

    def parse(self, response):
        #xpaths = banks_data.nordea_xpaths
        xpaths = banks_data.jyske_xpaths

        loader = ProductItemLoader(item=OutputTable(), response=response)

        loader.add_xpath('to_currency', xpaths[1])
        loader.add_value('from_currency', ["DKK"] * len(response.xpath(xpaths[1]).getall()))
        loader.add_xpath('buy_margin', xpaths[2])
        loader.add_xpath('sell_margin', xpaths[3])

        return loader.load_item()