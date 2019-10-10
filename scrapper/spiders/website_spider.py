import scrapy
import requests
from scrapper.items import OutputTable, ProductItemLoader


class WebsiteBankSpider(scrapy.Spider):
    name = "bank_website"

    def __init__(self, *args, **kwargs):
        super(WebsiteBankSpider, self).__init__(**kwargs)

        # download the jsons from the http request
        resp = requests.get('http://127.0.0.1:8000/banks')
        self.data = resp.json()

    def start_requests(self):
        for index in range(len(self.data)):
            print(f"Starting request for {self.data[index]['pageurl']}")
            yield scrapy.Request(url=self.data[index]['pageurl'], callback=self.parse, meta=self.data[index])

    def parse(self, response):
        meta = response.meta
        loader = ProductItemLoader(item=OutputTable(), response=response)

        loader.add_xpath('toCurrency', meta['toCurrencyXpath'])
        loader.add_value('fromCurrency', ["DKK"] * len(meta['toCurrencyXpath']))
        loader.add_xpath('buyMargin', meta['buyXpath'])
        loader.add_xpath('sellMargin', meta['sellXpath'])

        return loader.load_item()
