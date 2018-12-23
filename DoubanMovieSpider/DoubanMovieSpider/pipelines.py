# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import DoubanMovieLinksSpiderItem

class DoubanMovieSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class DoubanMovieLinksSpiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, DoubanMovieLinksSpiderItem):

        return item


    def open_spider(self, spider):
        print("Begin Spider!")
        QidianDb.OpenDB()

    def close_spider(self, spider):
        print("End Spider!")
        QidianDb.CloseDB()
