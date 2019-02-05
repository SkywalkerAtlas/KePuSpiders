# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class KepuOverviewItem(Item):
    # define the fields for your item here like:
    content = Field()
    #post_date = Field()
    title = Field()
    _id = Field()