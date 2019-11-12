# -*- coding: utf-8 -*-

# Define your item pipelines here
# Docs: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

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
            if len(item['exchangeUnit']) > i and item['exchangeUnit'] != '':
                string += f"\t\t{item['exchangeUnit'][i]}"

            print(string)
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
        # TODO level if needs leveling only -> len = len = len
        the_longest = max(len(item['toCurrency']), max(len(item['sellMargin']), len(item['buyMargin'])))

        temp_to_currency = []
        temp_buy_margin = []
        temp_sell_margin = []
        #
        # if True:
        #     print(f'###########LEVEL--BEFORE-------{item["name"]}------------')
        #     for i in range(the_longest):
        #
        #         string = f"{i}.\t{item['fromCurrency']}"
        #         if len(item['toCurrency']) > i:
        #             string += f"\t\t{item['toCurrency'][i]}"
        #         if len(item['sellMargin']) > i:
        #             string += f"\t\t{item['sellMargin'][i]}"
        #         if len(item['buyMargin']) > i:
        #             string += f"\t\t{item['buyMargin'][i]}"
        #         if len(item['exchangeUnit']) > i and item['exchangeUnit'] != '':
        #             string += f"\t\t{item['exchangeUnit'][i]}"
        #         print(string)

        if len(item['toCurrency']) == len(item['sellMargin']) == len(item['buyMargin']):
            for i in range(the_longest):
                temp_to_currency.append('-' if item['toCurrency'][i] == '' else item['toCurrency'][i])
                temp_sell_margin.append('-' if item['sellMargin'][i] == '' else item['sellMargin'][i])
                temp_buy_margin.append('-' if item['buyMargin'][i] == '' else item['buyMargin'][i])
        else:
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
        #
        # if True:
        #     print(f'###########LEVEL--AFTER-------{item["name"]}------------')
        #     for i in range(the_longest):
        #
        #         string = f"{i}.\t{item['fromCurrency']}"
        #         if len(item['toCurrency']) > i:
        #             string += f"\t\t{item['toCurrency'][i]}"
        #         if len(item['sellMargin']) > i:
        #             string += f"\t\t{item['sellMargin'][i]}"
        #         if len(item['buyMargin']) > i:
        #             string += f"\t\t{item['buyMargin'][i]}"
        #         if len(item['exchangeUnit']) > i and item['exchangeUnit'] != '':
        #             string += f"\t\t{item['exchangeUnit'][i]}"
        #         print(string)

        return item


class DropRowsWithNoMargin(object):
    def process_item(self, item, spider):
        the_longest = max(len(item['toCurrency']), max(len(item['sellMargin']), len(item['buyMargin'])))

        temp_to_currency = []
        temp_buy_margin = []
        temp_sell_margin = []

        for i in range(the_longest):
            condition_one = item['toCurrency'][i] != '' and item['sellMargin'][i] != '-' and item['buyMargin'][i] == '-'
            condition_two = item['toCurrency'][i] != '' and item['sellMargin'][i] == '-' and item['buyMargin'][i] != '-'
            condition_three = item['toCurrency'][i] != '' and item['sellMargin'][i] == '-' and item['buyMargin'][i] == '-'

            if condition_one or condition_two or condition_three:
                pass
            else:
                temp_to_currency.append(item['toCurrency'][i])
                temp_sell_margin.append(item['sellMargin'][i])
                temp_buy_margin.append(item['buyMargin'][i])

        item['toCurrency'] = temp_to_currency
        item['sellMargin'] = temp_sell_margin
        item['buyMargin'] = temp_buy_margin
        return item


class CalculateExchangePerOneUnit(object):
    def process_item(self, item, spider):  # this method is prepared for sending data to "margin saver"
        if len(item['exchangeUnit']) > 1:
            the_longest = max(len(item['sellMargin']), len(item['buyMargin']))

            temp_buy_margin = []
            temp_sell_margin = []

            for i in range(the_longest):
                temp_sell_margin.append(str(round(float(item['sellMargin'][i])/float(item['exchangeUnit'][i]), 4)))
                temp_buy_margin.append(str(round(float(item['buyMargin'][i])/float(item['exchangeUnit'][i]), 4)))

            item['sellMargin'] = temp_sell_margin
            item['buyMargin'] = temp_buy_margin
        return item


class SendData(object):
    def process_item(self, item, spider):  # this method is prepared for sending data to "margin saver"
        item['fromCurrency'] = item['fromCurrency'] * len(item['toCurrency'])  # to fill the from currency column

        url = environment.margin_saver_service_url() + "/margin"

        results = dict(item)
        del results['exchangeUnit']
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post(url, data=json.dumps(results), headers=headers)
        return item
