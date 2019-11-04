# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import configparser
import json
import requests
from environment import environment


class DisplayItem(object):
    def process_item(self, item, spider):

        the_longest = max(len(item['toCurrency']), max(len(item['sellMargin']), len(item['buyMargin'])))

        print(f'PARSED---------{item["name"]}------------')
        for i in range(the_longest):

            string = f"{i}.\t{item['fromCurrency']}"
            if len(item['toCurrency']) > i:
                string += f"\t\t{item['toCurrency'][i]}"
            if len(item['sellMargin']) > i:
                string += f"\t\t{item['sellMargin'][i]}"
            if len(item['buyMargin']) > i:
                string += f"\t\t{item['buyMargin'][i]}"

            print(string)

        item['fromCurrency'] = item['fromCurrency'] * len(item['toCurrency'])

        return item


class DropEmptyRows(object):
    def process_item(self, item, spider):
        the_longest = max(len(item['toCurrency']), max(len(item['sellMargin']), len(item['buyMargin'])))

        temp_to_currency = []
        temp_buy_margin = []
        temp_sell_margin = []

        for i in range(the_longest):
            if len(item['toCurrency']) > i and len(item['sellMargin']) > i and len(item['buyMargin']) > i:
                if item['toCurrency'][i] == '' and item['sellMargin'][i] == '' and item['buyMargin'][i] == '':
                    pass
                else:
                    temp_to_currency.append(item['toCurrency'][i])
                    temp_sell_margin.append(item['sellMargin'][i])
                    temp_buy_margin.append(item['buyMargin'][i])
            else:
                if len(item['toCurrency']) > i:
                    temp_to_currency.append(item['toCurrency'][i])
                if len(item['sellMargin']) > i:
                    temp_sell_margin.append(item['sellMargin'][i])
                if len(item['buyMargin']) > i:
                    temp_buy_margin.append(item['buyMargin'][i])

        item['toCurrency'] = temp_to_currency
        item['sellMargin'] = temp_sell_margin
        item['buyMargin'] = temp_buy_margin
        return item


class LevelColumns(object):
    def process_item(self, item, spider):

        the_longest = max(len(item['toCurrency']), max(len(item['sellMargin']), len(item['buyMargin'])))

        temp_to_currency = []
        temp_buy_margin = []
        temp_sell_margin = []

        for i in range(the_longest):
            if len(item['toCurrency']) > i and item['toCurrency'][i] != '':
                temp_to_currency.append(item['toCurrency'][i])
            if len(item['sellMargin']) > i and item['sellMargin'][i] != '':
                temp_sell_margin.append(item['sellMargin'][i])
            if len(item['buyMargin']) > i and item['buyMargin'][i] != '':
                temp_buy_margin.append(item['buyMargin'][i])

        item['toCurrency'] = temp_to_currency
        item['sellMargin'] = temp_sell_margin
        item['buyMargin'] = temp_buy_margin

        return item


class DropRowsWithNoMargin(object):
    def process_item(self, item, spider):
        the_longest = max(len(item['toCurrency']), max(len(item['sellMargin']), len(item['buyMargin'])))

        temp_to_currency = []
        temp_buy_margin = []
        temp_sell_margin = []

        for i in range(the_longest):
            if item['toCurrency'][i] != '' and item['sellMargin'][i] == '-' and item['buyMargin'][i] == '-':
                pass
            else:
                temp_to_currency.append(item['toCurrency'][i])
                temp_sell_margin.append(item['sellMargin'][i])
                temp_buy_margin.append(item['buyMargin'][i])

        item['toCurrency'] = temp_to_currency
        item['sellMargin'] = temp_sell_margin
        item['buyMargin'] = temp_buy_margin
        return item


class SendData(object):
    def process_item(self, item, spider):  # this method is prepared for sending data to "margin saver"
        item['fromCurrency'] = item['fromCurrency'] * len(item['toCurrency']) # to fill the from currency column

        url = environment.margin_saver_service_url() + "/margin"

        data = json.dumps(dict(item))
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post(url, data=data, headers=headers)
        return item
