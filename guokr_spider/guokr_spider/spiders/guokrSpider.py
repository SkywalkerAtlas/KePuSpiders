# -*- coding: utf-8 -*-

import scrapy
from guokr_spider.items import GuokrArticleItem
from scrapy.selector import Selector


#TODO
#加上对于标签的ICT分类权重

class guokrSpider(scrapy.Spider):
    name = 'guokr_spider'
    _domain = 'http://www.guokr.com/article/'
    start_urls = []
    for _id in range(441700,442060):
        start_urls.append(_domain+str(_id)+'/')

    def parse(self, response):
        selector = Selector(response)
        guokr_item = GuokrArticleItem()
        guokr_item['url'] = response.url.split('/')[-2]
        guokr_item['publish_date'] = selector.xpath(
            '//*[@class="content-th-info"]/meta/@content').re(r'\d+-\d+-\d+')
        guokr_item['title'] = selector.xpath('//*[@id = "articleTitle"]/text()').extract()
        guokr_item['content'] = selector.xpath('//*[@class="document"]/div/p/text()').extract()
        
        return guokr_item