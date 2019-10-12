# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import requests


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
    url = 'http://localhost:8070/upload'

    def process_item(self, item, spider):       # this method is prepared for sending data to "margin saver"
        print("------------------ PROCESS_ITEM -------- SEND DATA - CLASS")
        data = json.dumps(dict(item))
        response = requests.put(self.url, data=data)
        print(response.json())
        return item
