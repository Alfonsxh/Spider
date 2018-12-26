"""
@author: Alfons
@contact: alfons_xh@163.com
@file: DoubanMovieSpider.py
@time: 18-12-23 下午4:12
@version: v1.0 
"""
import scrapy
import json
import logging
import traceback
from urllib.parse import quote
from items import DoubanMovieLinksSpiderItem

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}


class DoubanMovieSpider(scrapy.Spider):
    name = "DoubanMovieSpider"
    start_urls = ["https://movie.douban.com/subject/26363254/"]

    # def start_requests(self):
    #     base_url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={page}&genres={type}"
    #     type_list = ["剧情", "喜剧", "动作", "爱情", "科幻", "动画", "悬疑", "惊悚", "恐怖", "犯罪", "同性", "音乐", "歌舞", "传记", "历史", "战争", "西部", "奇幻", "冒险", "灾难", "武侠", "情色"]
    #
    #     movies_link_urls_list = [base_url.format(page="{page}", type=quote(t)) for t in type_list]
    #     movies_link_urls_list.append("https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={page}")
    #
    #     for movies_link_urls in movies_link_urls_list:
    #         for page in range(10000):
    #             # yield scrapy.Request(movies_link_urls.format(page=page * 20), headers=headers, callback=self.parse)
    #             yield scrapy.Request(movies_link_urls.format(page=page * 20), callback=self.parse)

    def parse(self, response):
        """
        电影链接处理
        :param response: 爬取到的数据
        :return:
        """
        self.movie_info_parse(response)
        # try:
        #     movie_list = json.loads(response.text)["data"]
        #
        #     for movie in movie_list:
        #         movie_id = movie["id"]
        #         movie_title = movie["title"]
        #         movie_url = movie["url"]
        #
        #         yield DoubanMovieLinksSpiderItem(id=movie_id, title=movie_title, url=movie_url)
        #         yield scrapy.Request(movie_url, callback=self.movie_info_parse)
        # except:
        #     logging.error("[Movie link spider] Error when parse {}.\n{}".format(response.url, traceback.format_exc()))

    def movie_info_parse(self, response: scrapy.http.response.Response):
        try:
            context = response.xpath("//script[@type='application/ld+json']/text()").extract()
            context = context[0].strip() if len(context) > 0 else ""

            movie_info = json.loads(context)
            context_type = movie_info.get("@type", None) if isinstance(movie_info, dict) else None
            if context_type != "Movie":
                return

            movie_url = movie_info.get("url", None)
            movie_id = movie_url.split("/")[-2]
            movie_image = movie_info.get("image", None)
            movie_director = [d.get("url", "").split("/")[-2] for d in movie_info.get("director", list())]
            movie_author = [a.get("url", "").split("/")[-2] for a in movie_info.get("author", list())]
            # movie_actor = movie_info.get("actor", list())
            movie_datePublished = movie_info.get("datePublished", None)
            movie_genre = movie_info.get("genre", list())
            movie_duration = movie_info.get("duration", None)
            movie_description = movie_info.get("description", None)

            pass
        except:
            logging.error("[Movie info spider] Error when parse {}.\n{}".format(response.url, traceback.format_exc()))
