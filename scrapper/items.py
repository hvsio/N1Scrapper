# -*- coding: utf-8 -*-

# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# also more relevant here: https://docs.scrapy.org/en/latest/topics/loaders.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapper import banks_data


class ProductItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class StripText:
    def __init__(self, chars='% +-\t\n'):
        self.chars = chars

    def __call__(self, value):  # This makes an instance callable
        try:
            return value.strip(self.chars)
        except:
            return value


class ParseCurrencyNameToISO:
    def __call__(self, value):  # This makes an instance callable
        try:
            for key in banks_data.currency_name_iso.keys():
                if key in value:
                    value = key
            return value
        except:
            return value


class ParseComaIntoDot:
    def __call__(self, value):  # This makes an instance callable
        try:
            if "," in value:
                value = value.replace(",", ".")
            return value
        except:
            return value


class OutputTable(scrapy.Item):
    name = scrapy.Field()
    country = scrapy.Field()
    time = scrapy.Field()
    # unit = scrapy.Field()

    fromCurrency = scrapy.Field(
        output_processor=MapCompose(StripText())
    )
    toCurrency = scrapy.Field(
        output_processor=MapCompose(StripText())
    )
    buyMargin = scrapy.Field(
        output_processor=MapCompose(StripText(), ParseComaIntoDot())
    )
    sellMargin = scrapy.Field(
        output_processor=MapCompose(StripText(), ParseComaIntoDot())
    )
