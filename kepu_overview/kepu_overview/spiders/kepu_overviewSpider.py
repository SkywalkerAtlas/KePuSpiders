# -*- coding: utf-8 -*-
import scrapy
from kepu_overview.items import KepuOverviewItem
from scrapy.selector import Selector
import re

class kepu_overviewSpider(scrapy.Spider):
    name = 'kepu_overview'
    start_urls = [
        'http://www.kepu.net.cn/gb/technology/telecom/multimedia/mlt100.html',
        'http://www.kepu.net.cn/gb/technology/telecom/multimedia/mlt200.html',
        'http://www.kepu.net.cn/gb/technology/telecom/multimedia/mlt300.html',
        'http://www.kepu.net.cn/gb/technology/telecom/multimedia/mlt400.html',
        'http://www.kepu.net.cn/gb/technology/telecom/multimedia/mlt500.html',
        'http://www.kepu.net.cn/gb/technology/telecom/multimedia/mlt600.html',
        'http://www.kepu.net.cn/gb/technology/telecom/multimedia/mlt700.html',
        'http://www.kepu.net.cn/gb/technology/telecom/wireless/wrl100.html',
        'http://www.kepu.net.cn/gb/technology/telecom/wireless/wrl200.html',
        'http://www.kepu.net.cn/gb/technology/telecom/wireless/wrl300.html',
        'http://www.kepu.net.cn/gb/technology/telecom/wireless/wrl400.html',
        'http://www.kepu.net.cn/gb/technology/telecom/wireless/wrl500.html',
        'http://www.kepu.net.cn/gb/technology/telecom/network/net100.html',
        'http://www.kepu.net.cn/gb/technology/telecom/network/net200.html',
        'http://www.kepu.net.cn/gb/technology/telecom/network/net300.html',
        'http://www.kepu.net.cn/gb/technology/telecom/network/net400.html',
        'http://www.kepu.net.cn/gb/technology/telecom/network/net500.html',
        'http://www.kepu.net.cn/gb/technology/telecom/network/net600.html',
        'http://www.kepu.net.cn/gb/technology/telecom/network/net700.html',
        'http://www.kepu.net.cn/gb/technology/telecom/network/net800.html',
        'http://www.kepu.net.cn/gb/technology/telecom/network/net900.html',
        'http://www.kepu.net.cn/gb/technology/telecom/intelligent/itl100.html',
        'http://www.kepu.net.cn/gb/technology/telecom/fiber/fbr100.html',
        'http://www.kepu.net.cn/gb/technology/telecom/fiber/fbr200.html',
        'http://www.kepu.net.cn/gb/technology/telecom/fiber/fbr300.html',
        'http://www.kepu.net.cn/gb/technology/telecom/fiber/fbr400.html',
        'http://www.kepu.net.cn/gb/technology/telecom/fiber/fbr500.html',
        'http://www.kepu.net.cn/gb/technology/telecom/fiber/fbr600.html',
        'http://www.kepu.net.cn/gb/technology/telecom/microwave/mrw100.html',
        'http://www.kepu.net.cn/gb/technology/telecom/microwave/mrw200.html',
        'http://www.kepu.net.cn/gb/technology/telecom/microwave/mrw300.html',
        'http://www.kepu.net.cn/gb/technology/telecom/microwave/mrw400.html',
        'http://www.kepu.net.cn/gb/technology/telecom/microwave/mrw500.html',
        'http://www.kepu.net.cn/gb/technology/telecom/satellite/stl100.html',
        'http://www.kepu.net.cn/gb/technology/telecom/satellite/stl200.html',
        'http://www.kepu.net.cn/gb/technology/telecom/satellite/stl300.html',
        'http://www.kepu.net.cn/gb/technology/telecom/satellite/stl400.html',
        'http://www.kepu.net.cn/gb/technology/telecom/satellite/stl500.html',
        'http://www.kepu.net.cn/gb/technology/telecom/satellite/stl600.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swt100.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swt200.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swt300.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swt400.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swt500.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swt600.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swt700.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swt800.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swt900.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swta00.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swtb00.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swtc00.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swtd00.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swte00.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swtf00.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swtg00.html',
        'http://www.kepu.net.cn/gb/technology/telecom/switch/swth00.html',
        'http://www.kepu.net.cn/gb/technology/telecom/access/acc100.html',
        'http://www.kepu.net.cn/gb/technology/telecom/access/acc200.html',
        'http://www.kepu.net.cn/gb/technology/telecom/tmn/tmn100.html'
    ]

    def parse(self, response):
        selector = Selector(response)
        for _href in selector.xpath('/html/body/center/table/tr/td[2]/table/tr[2]//a/@href').extract():
            arti_url = re.sub(r'\w+\.html', _href, response.url)
            request = scrapy.Request(arti_url, callback = self.parse_article)
            yield request
    
    def parse_article(self, response):
        item = KepuOverviewItem()
        selector = Selector(response)
        item['title'] = ''.join(selector.xpath('//h2//text()').extract()).strip()
        #item['post_date']
        #item['content'] = ''.join(selector.xpath('//h2/../p/text()').extract())
        whole_para = ''
        for para in selector.xpath('//h2/../p/text()').extract():
            whole_para = whole_para + para.strip() + '\n'
        item['content'] = whole_para
        item['_id'] = re.search(r'\w+\.html', response.url).group().replace('.html', '')
        return item