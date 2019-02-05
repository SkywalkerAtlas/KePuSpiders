# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from guokr_group_spider.ICTkeywords import key_words
from scrapy.exceptions import DropItem
from guokr_group_spider.settings import _all_contents_save_path, _ict_contents_save_path


class GuokrFilterPipeline(object):
    def process_item(self, item, spider):
        matched_pattern = 0
        whole_paragaph = item['content']
        for key_word in key_words:
            if key_word in whole_paragaph:
                matched_pattern = matched_pattern + 1

        if matched_pattern < 2:
            raise DropItem("not talking about ICT at all, %s pattern matched" % str(matched_pattern))
        else:
            return item


class All_post_saverPipeline(object):
    def process_item(self, item, spider):
        with open(_all_contents_save_path + item['publish_date'][0] + '_' + item['url'] + '.txt', 'w') as f:
            f.write('title:\n')
            for title in item['title']:
                f.write(title)
                f.write('\n')
            f.write('content:\n')
            f.write(item['content'])
        return item


class ICT_post_savePipeline(object):
    def process_item(self, item, spider):
        with open(_ict_contents_save_path + item['publish_date'][0] + '_' + item['url'] + '.txt', 'w') as f:
            f.write('title:\n')
            for title in item['title']:
                f.write(title)
                f.write('\n')
            f.write('content:\n')
            f.write(item['content'])
        return item


class content_size_filterPipeline(object):
    def process_item(self, item, spider):
        content_length = len(item['content'].strip().lstrip())
        # print('Debug: test function, content_length = %d'%content_length)
        # print('type: %s'%type(item['content']))
        # print(item['content'].strip().lstrip())
        # print('-------------------------------------------')
        if content_length < 1000:
            raise DropItem('article not long enough, length:(%d), drop it.' % content_length)
        else:
            return item
