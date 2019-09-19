import scrapy
from scrapper import banks_data, items


# xpaths = [0.from x currency name, 1. to y currency name,2. xpath to buy row,3. xpath to sell,4. unit]

class WebsiteBankSpider(scrapy.Spider):
    name = "website_bank_spider"

    def start_requests(self):
        start_urls = banks_data.jyske_url
        yield scrapy.Request(url=start_urls, callback=self.parse)

    def parse(self, response):
        xpaths = banks_data.jyske_xpaths

        column_one = response.xpath(xpaths[1]).getall()
        column_zero = ["DKK"] * len(column_one)
        column_two = response.xpath(xpaths[2]).getall()
        column_three = response.xpath(xpaths[3]).getall()
        out = [column_zero, column_one, column_two, column_three]

        item = items.OutputTable()
        item['from_currency'] = column_zero
        item['to_currency'] = column_one
        item['buy_margin'] = column_two
        item['sell_margin'] = column_three
        # print(out)
        # print(item)
        return item
