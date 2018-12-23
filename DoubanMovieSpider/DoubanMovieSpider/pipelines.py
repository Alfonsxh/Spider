# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import DoubanMovieLinksSpiderItem
from SqlManager.DoubanMovieLinksSqlManager import (
    StartDB as StartMovieLinksDB,
    InsertData as InsertMovieLinksData
)

from scrapy.exceptions import DropItem


class DoubanMovieSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class DoubanMovieLinksSpiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, DoubanMovieLinksSpiderItem):
            InsertMovieLinksData(movie_id=item["id"], movie_title=item["title"], movie_url=item["url"])
        else:
            raise DropItem("Item type not allow!")

    def open_spider(self, spider):
        print("Begin Spider!")
        StartMovieLinksDB()
