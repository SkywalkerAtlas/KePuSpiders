# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from guokr_spider.ICTkeywords import key_words
from scrapy.exceptions import DropItem
from guokr_spider.settings import _contents_save_path

class GuokrFilterPipeline(object):
    def process_item(self, item, spider):
        matched_pattern = 0
        whole_paragaph = ''
        for parse in item['content']:
            whole_paragaph = whole_paragaph + parse + '\n'
        for key_word in key_words:
            if key_word in whole_paragaph:
                matched_pattern = matched_pattern + 1
        
        if  matched_pattern <= 2:
            raise DropItem("not talking about ICT")
        
        with open(_contents_save_path + item['publish_date'][0] + '_' + item['url'] + '.txt', 'w') as f:
            f.write('title:\n')
            for title in item['title']:
                f.write(title)
                f.write('\n')
            f.write('content:\n')
            
            f.write(whole_paragaph)
        return item
