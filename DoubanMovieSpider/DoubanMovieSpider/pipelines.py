# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from items import DoubanMovieLinksSpiderItem, DoubanMovieInfoSpiderItem
from SqlManager.DoubanMovieLinksSqlManager import (
    StartDB as StartMovieLinksDB,
    InsertData as InsertMovieLinksData
)
from SqlManager.DoubanMovieInfoSqlManager import (
    StartDB as StartMovieInfoDB,
    InsertData as InsertMovieInfoData
)

from scrapy.exceptions import DropItem


class DoubanMovieInfoSpiderPipeline(object):
    __doc__ = """处理电影信息"""

    def process_item(self, item, spider):
        if isinstance(item, DoubanMovieInfoSpiderItem):
            InsertMovieInfoData(movie_id=item["id"],
                                movie_name=item["name"],
                                movie_url=item["url"],
                                movie_image=item["image"],
                                movie_director=item["director"],
                                movie_author=item["author"],
                                movie_actor=item["actor"],
                                movie_country=item["country"],
                                movie_date_published=item["datePublished"],
                                movie_genre=item["genre"],
                                movie_duration=item["duration"],
                                movie_description=item["description"],
                                movie_rate_details=item["rateDetails"],
                                movie_rate_number=item["rateNumber"],
                                movie_imdb=item["imdb"])

        return item

    def open_spider(self, spider):
        StartMovieInfoDB()


class DoubanMovieLinksSpiderPipeline(object):
    __doc__ = """"处理电影链接信息"""

    def process_item(self, item, spider):
        if isinstance(item, DoubanMovieLinksSpiderItem):
            InsertMovieLinksData(movie_id=item["id"],
                                 movie_title=item["title"],
                                 movie_url=item["url"])

        return item

    def open_spider(self, spider):
        StartMovieLinksDB()
