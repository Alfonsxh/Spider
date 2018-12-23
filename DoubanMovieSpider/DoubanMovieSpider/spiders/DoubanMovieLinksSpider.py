"""
@author: Alfons
@contact: alfons_xh@163.com
@file: DoubanMovieSpider.py
@time: 18-12-23 下午4:12
@version: v1.0 
"""
import json
import scrapy
from items import DoubanMovieLinksSpiderItem

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}


class DoubanMovieLinksSpider(scrapy.Spider):
    name = "DoubanMovieLinks"

    def start_requests(self):
        movies_link_urls = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={page}"
        for page in range(1):
            yield scrapy.Request(movies_link_urls.format(page=page * 20), headers=headers, callback=self.parse)

    def parse(self, response):
        try:
            movie_list = json.loads(response.text)["data"]

            for movie in movie_list:
                movie_id = movie["id"]
                movie_title = movie["title"]
                movie_url = movie["url"]

                yield DoubanMovieLinksSpiderItem(id=movie_id, title=movie_title, url=movie_url)

        except:
            print("Error when parse {}.".format(response.url))
