# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class OutputTable(Item):
    from_currency = Field()
    to_currency = Field()
    buy_margin = Field()
    sell_margin = Field()

