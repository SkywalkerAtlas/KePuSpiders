# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from kepu_overview.settings import _ict_arti_path

class KepuOverviewSaverPipeline(object):
    def process_item(self, item, spider):
        with open(_ict_arti_path + ''.join('1990-01-01') + '_' + item['_id'] + '.txt', 'w') as f:
            f.write('title:\n')
            f.write(item['title'])
            f.write('\n')
            f.write('content:\n')
            f.write(item['content'])
        return item
