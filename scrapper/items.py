# -*- coding: utf-8 -*-

# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# also more relevant here: https://docs.scrapy.org/en/latest/topics/loaders.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapper import iso_data


class ProductItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class StripText:
    def __init__(self, chars='% +\t\n'):
        self.chars = chars

    def __call__(self, value):
        value = value.strip(self.chars)

        if value == '-':
            return '-'
        else:
            value = value.strip('-')
            return value
        #
        # if any((c in self.chars) for c in value):
        #     value = value.strip(self.chars)
        #     if value == '-':
        #         return '-'
        #     else:
        #         value = value.strip('-')
        #         return value
        # else:
        #     return value


class ParseCurrencyNameToISO:
    def __call__(self, value):  # This makes an instance callable
        for key in iso_data.currency_name_iso.keys():
            if key in value:
                value = key
                return value
        return ''


class ParseComaIntoDot:
    def __call__(self, value):  # This makes an instance callable
        index = value.find(',')
        if index == -1:
            return value
        else:
            value = value.replace(",", ".")
            value = value.replace(".", "", value.count(".") - 1)
        return value


class PrepareMargin:
    def __call__(self, value):  # This makes an instance callable
        if not value == '-':
            try:
                value = float(value)
                return str(value)
            except ValueError:
                return ''
        return value


class PrepareCurrency:
    def __call__(self, value):  # This makes an instance callable
        return value


class OutputTable(scrapy.Item):
    name = scrapy.Field()
    country = scrapy.Field()
    time = scrapy.Field()
    unit = scrapy.Field()
    fromCurrency = scrapy.Field(
        output_processor=MapCompose()
    )
    toCurrency = scrapy.Field(
        output_processor=MapCompose(StripText(), ParseCurrencyNameToISO())
    )
    buyMargin = scrapy.Field(
        output_processor=MapCompose(StripText(), ParseComaIntoDot(), PrepareMargin())
    )
    sellMargin = scrapy.Field(
        output_processor=MapCompose(StripText(), ParseComaIntoDot(), PrepareMargin())
    )
