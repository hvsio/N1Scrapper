# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import requests
import urllib.request


class DeleteEmptyFields(object):
    def process_item(self, item, spider):
        temp = []
        for index in range(len(item['toCurrency'])):
            if not item['toCurrency'][index] == '':
                temp.append(item['toCurrency'][index])
        item['toCurrency'] = temp

        temp = []
        for index in range(len(item['buyMargin'])):
            if not item['buyMargin'][index] == '':
                temp.append(item['buyMargin'][index])
        item['buyMargin'] = temp

        temp = []
        for index in range(len(item['sellMargin'])):
            if not item['sellMargin'][index] == '':
                temp.append(item['sellMargin'][index])
        item['sellMargin'] = temp

        item['fromCurrency'] = item['fromCurrency'] * len(item['toCurrency'])

        return item


class SendData(object):
    url = 'http://localhost:5000/margin'

    def process_item(self, item, spider):  # this method is prepared for sending data to "margin saver"
        print("------------------ PROCESS_ITEM -------- SEND DATA - CLASS")
        data = json.dumps(dict(item))
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post(self.url, data=data, headers=headers)
        return item
