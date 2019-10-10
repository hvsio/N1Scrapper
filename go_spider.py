from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet.task import deferLater
from scrapper.spiders.website_spider import WebsiteBankSpider
import requests

#TIMEOUT_seconds = 30

# Please find the documentation here: http://crawl.blog/scrapy-loop/


def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(reactor, seconds, lambda: None)


process = CrawlerProcess(get_project_settings())


def crash(failure):
    # TODO: send more meaningful notification, eg. email
    print('oops, spider crashed')
    print(failure.getTraceback())


def _crawl(result, spider):
    # maybe we can get timeout here from http request ?
    resp = requests.get('http://127.0.0.1:8070/timeout')
    TIMEOUT_seconds = int(resp.text)

    deferred = process.crawl(spider)
    deferred.addCallback(lambda results: print(f'waiting {TIMEOUT_seconds} seconds before restart...'))
    deferred.addErrback(crash)  # <-- add errback here
    deferred.addCallback(sleep, seconds=TIMEOUT_seconds)
    deferred.addCallback(_crawl, spider)
    return deferred


_crawl(None, WebsiteBankSpider)
process.start()