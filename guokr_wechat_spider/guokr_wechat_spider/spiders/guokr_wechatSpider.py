import scrapy
from scrapy.selector import Selector
from guokr_wechat_spider.items import GuokrWechatContentItem
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class guokr_wechatSpider(scrapy.Spider):
    name = 'guokr_wechat_spider'
    start_urls = ['http://chuansong.me/account/Guokr42?start=12']
    _domain = 'http://chuansong.me'
    #for start_index in range(12, 48, 12):
    #    start_urls.append('http://chuansong.me/account/Guokr42?start=%d'%start_index)

    def parse(self, response):
        #print (response.body)
        selector = Selector(response)
        for article_link_url in selector.xpath('//*[@class="question_link"]/@href').extract():
            detail_url = '%s%s'%(self._domain, article_link_url)
            print(detail_url)
            request = scrapy.Request(detail_url, callback = self.parse_article, errback = self.errback_httpbin)
            yield request
        
        next_page_url = '%s%s'%(
            self._domain, 
            selector.xpath('//*[@class="w4_5"]/a[2]/@href').extract()[0]
            )
        #print(next_page_url)
        #爬取页码小于500的页面
        page_num = int(re.search(r'\d+$', next_page_url).group()) / 12
        if page_num < 1:
            request = scrapy.Request(next_page_url, callback = self.parse)
            yield request

    def parse_article(self, response):
        #print('0000000000000000000000000xxxxxxxxxxxxxxxxxxxxxxxxxx')
        selector = Selector(response)
        item = GuokrWechatContentItem()
        para = selector.xpath('//*[@id="page-content"]/descendant::p/text()').extract()
        print(para)
        #item['content'] = selector
        return item
    
    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)