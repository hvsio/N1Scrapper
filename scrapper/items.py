# -*- coding: utf-8 -*-

# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# also here: https://docs.scrapy.org/en/latest/topics/loaders.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapper import iso_data


class ProductItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class StripUnwantedChars:
    def __call__(self, value):
        self.chars = '% +\t\n'
        value = value.strip(self.chars)

        if value == '-':
            return '-'
        else:
            value = value.strip('-')
            return value


class ParseCurrencyNameToISO:
    def __call__(self, value):
        for key in iso_data.currency_name_iso.keys():
            if key in value:
                value = key
                return value
        return ''


class ParseComaIntoDot:
    def __call__(self, value):
        index = value.find(',')
        if index == -1:
            return value
        else:
            value = value.replace(",", ".")
            value = value.replace(".", "", value.count(".") - 1)   # Replace every dot to '' except last
        return value


class LeaveOnlyValidEntries:
    def __call__(self, value):
        if not value == '-':    # let the entries with '-' pass through the function
            try:
                value = float(value)
                return str(value)
            except ValueError:
                return ''
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
        output_processor=MapCompose(StripUnwantedChars(), ParseCurrencyNameToISO())
    )
    buyMargin = scrapy.Field(
        output_processor=MapCompose(StripUnwantedChars(), ParseComaIntoDot(), LeaveOnlyValidEntries())
    )
    sellMargin = scrapy.Field(
        output_processor=MapCompose(StripUnwantedChars(), ParseComaIntoDot(), LeaveOnlyValidEntries())
    )
