import scrapy
import requests
from datetime import datetime

from scrapy_splash import SplashRequest

import logger
from scrapper.items import OutputTable, ProductItemLoader
from environment import environment


class WebsiteBankSpider(scrapy.Spider):
    name = "bank_website"

    def __init__(self, *args, **kwargs):
        super(WebsiteBankSpider, self).__init__(**kwargs)
        self.my_logger = logger.get_logger('my_log')

        url = environment.scrapper_service_url() + "/banks"

        # download the jsons from the http request
        resp = requests.get(url)
        self.data = resp.json()

        for index in range(len(self.data)):
            self.data[index]['toCurrencyXpath'] = self.data[index]['toCurrencyXpath'] + '/text()'
            self.data[index]['buyxpath'] = self.data[index]['buyxpath'] + '/text()'
            self.data[index]['sellxpath'] = self.data[index]['sellxpath'] + '/text()'

    def start_requests(self):
        for index in range(len(self.data)):
            print(f"Starting request for {self.data[index]['pageurl']}")
            # yield scrapy.Request(url=self.data[index]['pageurl'], callback=self.parse, meta=self.data[index])
            yield SplashRequest(url=self.data[index]['pageurl'], callback=self.parse, meta=self.data[index],
                                args={'wait': 1.0})

    def parse(self, response):
        loader = ProductItemLoader(item=OutputTable(), response=response)
        timestamp = datetime.now()
        meta = response.meta

        loader.add_value('name', meta['name'])
        loader.add_value('country', meta['country'])
        loader.add_value('time', timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)"))
        loader.add_value('unit', meta['unit'])
        loader.add_xpath('toCurrency', meta['toCurrencyXpath'])
        loader.add_value('fromCurrency', meta['fromCurrency'])
        loader.add_xpath('buyMargin', meta['buyxpath'])
        loader.add_xpath('sellMargin', meta['sellxpath'])

        toCur = response.xpath(meta['toCurrencyXpath']).getall()
        buy = response.xpath(meta['buyxpath']).getall()
        sell = response.xpath(meta['sellxpath']).getall()

        # if meta['name'] == 'Uni Credit':
        #     print(meta['name'])
        #     print(toCur)
        #     print(buy)
        #     print(sell)

        return loader.load_item()
