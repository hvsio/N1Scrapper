import smtplib
import ssl

import scrapy
import requests
from datetime import datetime
from scrapy_splash import SplashRequest
import logger
from scrapper.items import OutputTable, ProductItemLoader
from environment import environment
from scrapper.settings import ERROR_EMAIL_SMTP_SERVER, ERROR_EMAIL_PORT, ERROR_EMAIL_SENDER, ERROR_EMAIL_PASSWORD, \
    ERROR_EMAIL_RECEIVER


class WebsiteBankSpider(scrapy.Spider):
    name = "bank_website"

    def __init__(self, *args, **kwargs):
        super(WebsiteBankSpider, self).__init__(**kwargs)
        self.my_logger = logger.get_logger('my_log')

        url = environment.scrapper_service_url() + "/banks"

        resp = requests.get(url)
        self.data = resp.json()

        for index in range(len(self.data)):
            self.data[index]['toCurrencyXpath'] = self.data[index]['toCurrencyXpath'] + '/text()'
            self.data[index]['buyxpath'] = self.data[index]['buyxpath'] + '/text()'
            self.data[index]['sellxpath'] = self.data[index]['sellxpath'] + '/text()'
            self.data[index]['exchangeunitxpath'] = (self.data[index]['exchangeunitxpath'] + '/text()') if self.data[index]['exchangeunitxpath'] != '' else ''

    def start_requests(self):
        for index in range(len(self.data)):
            print(f"Starting request for {self.data[index]['pageurl']}")
            yield SplashRequest(url=self.data[index]['pageurl'], callback=self.parse, meta=self.data[index], args={'wait': 1.0})

    def parse(self, response):
        loader = ProductItemLoader(item=OutputTable(), response=response)
        timestamp = datetime.now()
        meta = response.meta

        # checks if xpaths to the elements of a table can be found.
        if response.xpath(meta['toCurrencyXpath']).getall() == [] or response.xpath(meta['buyxpath']).getall() == [] or response.xpath(meta['sellxpath']).getall() == []:
            self.send_email(response.meta)

        loader.add_value('name', meta['name'])
        loader.add_value('country', meta['country'])
        loader.add_value('time', timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)"))
        loader.add_value('unit', meta['unit'])
        loader.add_value('isCrossInverted', meta['iscrossinverted'])
        loader.add_xpath('toCurrency', meta['toCurrencyXpath'])
        loader.add_value('fromCurrency', meta['fromCurrency'])
        loader.add_xpath('exchangeUnit', meta['exchangeunitxpath']) if meta['exchangeunitxpath'] != '' else loader.add_value('exchangeUnit', '')
        loader.add_xpath('buyMargin', meta['buyxpath'])
        loader.add_xpath('sellMargin', meta['sellxpath'])

        return loader.load_item()

    # TODO: make general method/class to send alerts (similar method in "pipelines.py")
    def send_email(self, meta):
        message = f"""\
            Subject: Scraper error logs

        Bank: {meta['name']} \n
        Errors: Cannot find xpaths to the elements of a table. 
        Please check the URL and make sure it works!
        """
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(ERROR_EMAIL_SMTP_SERVER, ERROR_EMAIL_PORT, context=context) as server:
            server.login(ERROR_EMAIL_SENDER, ERROR_EMAIL_PASSWORD)
            server.sendmail(ERROR_EMAIL_SENDER, ERROR_EMAIL_RECEIVER, message)
