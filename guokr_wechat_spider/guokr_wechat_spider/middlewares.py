# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy.http import HtmlResponse
import time
#from guokr_wechat_spider.settings import DOWNLOAD_DELAY
from selenium.webdriver.support.wait import WebDriverWait

class chuangsong_guokrMiddleware(object):
    'use PhantomJS to load urls (need to change default settings)'
    #dcap = dict(DesiredCapabilities.PHANTOMJS)
    #dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')

    def process_request(self, request, spider):
        #print ("PhantomJS is starting...")
        #print ("访问"+request.url)
        driver = webdriver.PhantomJS() #指定使用的浏览器
        driver.set_window_size(1200,800)
        driver.implicitly_wait(30)
        # driver = webdriver.Firefox()
        driver.get(request.url)
        #time.sleep(DOWNLOAD_DELAY)
        #js = "var q=document.documentElement.scrollTop=10000" 
        #driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。       
        #time.sleep(3)
        body = driver.page_source
        driver.quit()
        #print(request.url+'finiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiish')
        return HtmlResponse(request.url, body=body, encoding='utf-8', request=request)
        