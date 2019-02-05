# -*- coding: utf-8 -*-

import scrapy
from guokr_group_spider.items import GuokrArticleItem
from scrapy.selector import Selector

class guokr_groupSpider(scrapy.Spider):
    name = 'guokr_group_spider'
    _domain = 'http://www.guokr.com/post/'
    start_urls = []
    #TODO 将返回404的url添加到列表中
    _urls_404_tail = []

    #_id_iter = range(657210,777640)
    for _id in range(657210,777640):
        start_urls.append(_domain+str(_id)+'/')
    
    #def start_requests(self):
    #    for url in self.start_urls:
    #        yield scrapy.Request(url, callback = self.parse, errback = self.parse_error)

    def parse(self, response):
        selector = Selector(response)
        guokr_item = GuokrArticleItem()
        guokr_item['url'] = response.url.split('/')[-2]
        guokr_item['publish_date'] = selector.xpath(
            '//*[@class="post-info"]/meta/@content').re(r'\d+-\d+-\d+')
        guokr_item['title'] = selector.xpath('//*[@id="articleTitle"]/text()').re(r'[^\x00-\xff]+')

        parses = selector.xpath('//*[@id="articleContent"]/descendant::p/descendant::text()').extract()
        whole_paragaph = ''
        for parse in parses:
            whole_paragaph = whole_paragaph + parse + '\n'
        guokr_item['content'] = whole_paragaph

        return guokr_item
    
    #def parse_error(self, failure):
