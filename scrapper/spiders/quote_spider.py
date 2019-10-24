import scrapy
import requests
from datetime import datetime
import logger
from scrapper.items import OutputTable, ProductItemLoader


class WebsiteBankSpider(scrapy.Spider):
    name = "bank_website"

    def __init__(self, *args, **kwargs):
        super(WebsiteBankSpider, self).__init__(**kwargs)
        self.my_logger = logger.get_logger('my_log')

        # download the jsons from the http request
        resp = requests.get('http://127.0.0.1:8000/banks')
        self.data = resp.json()

    def start_requests(self):
        for index in range(len(self.data)):
            print(f"Starting request for {self.data[index]['pageurl']}")
            yield scrapy.Request(url=self.data[index]['pageurl'], callback=self.parse, meta=self.data[index])

    def parse(self, response):

        loader = ProductItemLoader(item=OutputTable(), response=response)
        timestamp = datetime.now()
        meta = response.meta

        loader.add_value('name', meta['name'])
        loader.add_value('country', meta['country'])
        loader.add_value('time', timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)"))
        # loader.add_value('unit', meta['unit'])
        loader.add_xpath('toCurrency', meta['toCurrencyXpath'])
        loader.add_value('fromCurrency', meta['fromCurrency'])
        loader.add_xpath('buyMargin', meta['buyxpath'])
        loader.add_xpath('sellMargin', meta['sellxpath'])

        return loader.load_item()
