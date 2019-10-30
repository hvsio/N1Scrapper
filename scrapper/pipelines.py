# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import configparser
import json
import requests
from environment import environment


class DeleteEmptyFields(object):
    def process_item(self, item, spider):

        print(f'---------{item["name"]}------------')
        print(item)
        print('---------------------')

        temp_toCurrency = []
        for index in range(len(item['toCurrency'])):
            if not item['toCurrency'][index] == '':
                temp_toCurrency.append(item['toCurrency'][index])
        item['toCurrency'] = temp_toCurrency

        temp_buyMargin = []
        for index in range(len(item['buyMargin'])):
            if not item['buyMargin'][index] == '':
                temp_buyMargin.append(item['buyMargin'][index])
        item['buyMargin'] = temp_buyMargin

        temp_sellMargin = []
        for index in range(len(item['sellMargin'])):
            if not item['sellMargin'][index] == '':
                temp_sellMargin.append(item['sellMargin'][index])
        item['sellMargin'] = temp_sellMargin

        item['fromCurrency'] = item['fromCurrency'] * len(item['toCurrency'])

        return item


class SendData(object):
    def process_item(self, item, spider):  # this method is prepared for sending data to "margin saver"

        # print(f'---------{item["name"]}------------')
        # print(item)
        # print('---------------------')

        url = environment.margin_saver_service_url() + "/margin"

        data = json.dumps(dict(item))
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post(url, data=data, headers=headers)
        return item
