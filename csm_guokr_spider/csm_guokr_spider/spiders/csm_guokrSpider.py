# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import re

from csm_guokr_spider.items import CsmGuokrSpiderItem

class csm_guokrSpider(scrapy.Spider):
    name = 'csm_guokr_spider'
    start_urls = ['http://chuansong.me/account/kepubolan?start=0']
    _domain = 'http://chuansong.me'

    def parse(self, response):
        selector = Selector(response)
        article_ids = selector.xpath('//*[@class="question_link"]/@href').extract()
        for _id in article_ids:
            article_url = self._domain + _id
            #print(article_url)
            request = scrapy.Request(article_url, callback = self.parse_article, errback = self.error_parse)
            yield request
        
        #page not ends
        if len(article_ids) > 10:
            #next_page_url = self._domain + selector.xpath('//*[@class="w4_5"]/a[2]/@href').extract()[0]
            next_page_url = re.sub(r'\d+$', lambda m:str(int(m.group())+12), response.url)
            #print(next_page_url)
            request = scrapy.Request(next_page_url, callback = self.parse, errback = self.error_parse)
            yield request
        else:
            self.logger.info('EEEEEEEEEEEEEEEEEEEEnd of pages.XD bye bye')

    def parse_article(self, response):
        selector = Selector(response)
        item = CsmGuokrSpiderItem()
        item['title'] = ''.join(selector.xpath('//*[@id="activity-name"]/text()').extract()).strip()
        item['post_date'] = ''.join(selector.xpath('//*[@id="post-date"]/text()').extract()).strip()
        item['_id'] = re.search(r'/n/\d+', response.url).group()
        whole_content = ''
        for para in response.xpath('//p/descendant-or-self::text()').extract():
            #段落需大于20字才可被标记为段落
            if len(para) > 20:
                whole_content = whole_content + para.strip() + '\n'
        item['content'] = whole_content
        return item

    def error_parse(self, failure):
        #TODO
        pass