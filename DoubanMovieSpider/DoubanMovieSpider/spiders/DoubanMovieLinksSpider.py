"""
@author: Alfons
@contact: alfons_xh@163.com
@file: DoubanMovieSpider.py
@time: 18-12-23 下午4:12
@version: v1.0 
"""
import json
import scrapy
import traceback
from urllib.parse import quote
from items import DoubanMovieLinksSpiderItem

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}


class DoubanMovieLinksSpider(scrapy.Spider):
    name = "DoubanMovieLinks"

    def start_requests(self):
        base_url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={page}&genres={type}"
        type_list = ["剧情", "喜剧", "动作", "爱情", "科幻", "动画", "悬疑", "惊悚", "恐怖", "犯罪", "同性", "音乐", "歌舞", "传记", "历史", "战争", "西部", "奇幻", "冒险", "灾难", "武侠", "情色"]

        movies_link_urls_list = [base_url.format(page="{page}", type=quote(t)) for t in type_list]
        movies_link_urls_list.append("https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={page}")

        for movies_link_urls in movies_link_urls_list:
            for page in range(10000):
                # yield scrapy.Request(movies_link_urls.format(page=page * 20), headers=headers, callback=self.parse)
                yield scrapy.Request(movies_link_urls.format(page=page * 20), callback=self.parse)

    def parse(self, response):
        try:
            movie_list = json.loads(response.text)["data"]

            for movie in movie_list:
                movie_id = movie["id"]
                movie_title = movie["title"]
                movie_url = movie["url"]

                yield DoubanMovieLinksSpiderItem(id=movie_id, title=movie_title, url=movie_url)

        except:
            print("[*] Error when parse {}.\n{}".format(response.url, traceback.format_exc()))
