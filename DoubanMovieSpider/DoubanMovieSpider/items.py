# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieLinksSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()


class DoubanMovieInfoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    director = scrapy.Field()
    author = scrapy.Field()
    actor = scrapy.Field()
    country = scrapy.Field()
    datePublished = scrapy.Field()
    genre = scrapy.Field()
    duration = scrapy.Field()
    description = scrapy.Field()
    aggregateRating = scrapy.Field()
    imdb = scrapy.Field()


class DoubanPersonInfoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
