from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from soundcloudscrape.spiders.soundcloud_spider import SoundcloudSpider

# process = CrawlerProcess(get_project_settings())
configure_logging()
runner = CrawlerRunner(get_project_settings())

# Function to search all artists in UK from major towns joined in the past year.


@defer.inlineCallbacks
def test():
    yield runner.crawl(SoundcloudSpider, query='a', time='last_year', location='london')
    reactor.stop()


@defer.inlineCallbacks
def full_search():
    yield runner.crawl(SoundcloudSpider, type='full-search', time='last_week')
    reactor.stop()


def crawl(type):
    if type == 'test':
        test()
    elif type == 'fs':
        full_search()
    reactor.run()