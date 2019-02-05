import re
import datetime
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from  weibo_spider.items import WeiboItem

class weiboSpider(Spider):
    name = "weibo_spider"
    start_urls = [
        "http://weibo.cn/guokr42"
    ]
    host = "http://weibo.cn"

    def parse(self, response):
        sel = Selector(response)
        weibos = sel.xpath('body/div[@class="c" and @id]')
        for weibo in weibos:
            weiboitem = WeiboItem()
            content = weibo.xpath('div/span[@class="ctt"]/text()').extract()  # 微博内容
            date = weibo.xpath('div/span[@class="ct"]/text()').re(r'\d+月\d+日 \d+:\d+')
            weiboitem['date'] = date
            weiboitem['text'] = content
            print(content)
            print(date)
        next_url = sel.xpath(
            u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if next_url:
            yield Request(url=self.host + next_url[0], callback=self.parse)