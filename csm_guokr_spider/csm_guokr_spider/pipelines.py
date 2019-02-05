# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from csm_guokr_spider.ICTkeywords import key_words
from scrapy.exceptions import DropItem
from csm_guokr_spider.settings import _all_contents_save_path, _ict_contents_save_path
import re

class ICT_FilterPipeline(object):
    def process_item(self, item, spider):
        matched_pattern = 0
        whole_paragaph = item['content']
        matched_word = []
        for key_word in key_words:
            if key_word in whole_paragaph:
                matched_pattern = matched_pattern + 1
                matched_word.append(key_word)
        
        if  matched_pattern < 2:
            raise DropItem("not talking about ICT at all, %s pattern matched"%str(matched_pattern))
        else:
            spider.logger.info('Find an ICT article, %s pattern matched, key words are:%s'%(str(matched_pattern), ''.join(matched_word)))
            return item

class All_post_saverPipeline(object):
    def process_item(self, item, spider):
        with open(_all_contents_save_path + ''.join(item['post_date']) + '_' + re.search(r'\d+$', item['_id']).group() + '_' + 'wechat' + '.txt', 'w') as f:
            f.write('title:\n')
            f.write(item['title'])
            f.write('\n')
            f.write('content:\n')
            f.write(item['content'])
        return item

class ICT_post_savePipeline(object):
    def process_item(self, item, spider):
        with open(_ict_contents_save_path + ''.join(item['post_date']) + '_' + re.search(r'\d+$', item['_id']).group() + '_'  + 'wechat' + '.txt', 'w') as f:
            f.write('title:\n')
            f.write(item['title'])
            f.write('\n')
            f.write('content:\n')
            f.write(item['content'])
        #return item