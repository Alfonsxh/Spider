"""
@author: Alfons
@contact: alfons_xh@163.com
@file: DoubanMovieSpider.py
@time: 18-12-23 下午4:12
@version: v1.0 
"""
import scrapy
import time
import json
import random
import logging
import traceback
from urllib.parse import quote
from items import DoubanMovieLinksSpiderItem, DoubanMovieInfoSpiderItem
from SqlManager.DoubanMovieInfoSqlManager import FetchData as IsMovieExist
from SqlManager.DoubanMovieLinksSqlManager import GetAllMovie

douban_main_url = "https://movie.douban.com"
finally_return = dict(status="over")


class DoubanMovieSpider(scrapy.Spider):
    name = "DoubanMovieSpider"

    # start_urls = ["https://movie.douban.com/subject/10439805/"]

    # def start_requests(self):
    #     base_url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={page}&genres={type}"
    #     type_list = ["剧情", "喜剧", "动作", "爱情", "科幻", "动画", "悬疑", "惊悚", "恐怖", "犯罪", "同性", "音乐", "歌舞", "传记", "历史", "战争", "西部", "奇幻", "冒险", "灾难", "武侠", "情色"]
    #
    #     movies_link_urls_list = [base_url.format(page="{page}", type=quote(t)) for t in type_list]
    #     movies_link_urls_list.append("https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={page}")
    #
    #     for movies_link_urls in movies_link_urls_list:
    #         for page in range(100):
    #             # yield scrapy.Request(movies_link_urls.format(page=page * 20), headers=headers, callback=self.parse)
    #             yield scrapy.Request(movies_link_urls.format(page=page * 20), callback=self.parse)

    def start_requests(self):
        i = 0
        for movie in GetAllMovie():
            if IsMovieExist(movie.id):
                continue

            # 限速
            if i % 5 == 0:
                time.sleep(random.randint(1, 2))
            i += 1

            yield scrapy.Request(movie.url, callback=self.parse)

    def parse(self, response):
        """
        电影链接处理
        :param response: scrapy返回的response
        :return:
        """
        #     try:
        #         movie_list = json.loads(response.text)["data"]
        #
        #         for movie in movie_list:
        #             movie_id = movie["id"]
        #             movie_title = movie["title"]
        #             movie_url = movie["url"]
        #
        #             yield DoubanMovieLinksSpiderItem(id=movie_id, title=movie_title, url=movie_url)
        #
        #             if not IsMovieExist(movie_id):
        #                 # logging.info("[Movie info spider] Parse movie id -> {}".format(movie_id))
        #                 yield scrapy.Request(movie_url, callback=self.movie_info_parse)
        #     except:
        #         logging.error("[Movie link spider] Error when parse {}.\n{}".format(response.url, traceback.format_exc()))
        #     finally:
        #         return finally_return
        #
        # def movie_info_parse(self, response: scrapy.http.response.Response):
        #     """
        #     电影信息处理
        #     :param response: scrapy返回的response
        #     :return:
        #     """
        context = ""
        try:
            context = response.xpath("//script[@type='application/ld+json']/text()").extract_first(default="{}").strip().replace('\n', '')

            movie_info = json.loads(context, strict=False)
            context_type = movie_info.get("@type", None) if isinstance(movie_info, dict) else None
            if context_type != "Movie":
                logging.warning("[Movie info spider] {url} not have movie({context})".format(url=response.url, context=response.text))
                # yield scrapy.Request(url = response.url, callback=self.movie_info_parse)
                if "window.location.href" in response.text:
                    target = "window.location.href="
                    href = response.text[response.text.find(target) + len(target): response.text.find(";</script>")].strip('\"')
                    yield scrapy.Request(url=href, callback=self.parse)

                yield scrapy.Request(url=response.url, callback=self.parse)
                return finally_return

            # movie_name = movie_info.get("name", None)
            movie_name = response.xpath("//title/text()").extract_first().strip().replace(" (豆瓣)", "")
            movie_url = douban_main_url + movie_info.get("url", None)
            movie_id = movie_url.split("/")[-2]
            movie_image = movie_info.get("image", None)
            movie_director = self.GetDirectorOrAuthorInfo('导演', response)
            movie_author = self.GetDirectorOrAuthorInfo('编剧', response)
            movie_actor = self.GetActorsInfo(response)
            movie_country = self.GetMovieCountry(response)
            movie_datePublished = movie_info.get("datePublished", None)
            movie_genre = movie_info.get("genre", list())
            movie_duration = movie_info.get("duration", None)
            movie_description = movie_info.get("description", None)
            movie_rateNumber, movie_rateDetails = self.GetRateInfo(response)
            movie_imdb = self.GetImdbLink(response)

            yield DoubanMovieInfoSpiderItem(id=movie_id,
                                            name=movie_name,
                                            url=movie_url,
                                            image=movie_image,
                                            director=movie_director,
                                            author=movie_author,
                                            actor=movie_actor,
                                            country=movie_country,
                                            datePublished=movie_datePublished,
                                            genre=movie_genre,
                                            duration=movie_duration,
                                            description=movie_description,
                                            rateDetails=movie_rateDetails,
                                            rateNumber=movie_rateNumber,
                                            imdb=movie_imdb)
        except:
            # with open("./1.txt", "w") as f:
            #     f.write(context)
            logging.error("[Movie info spider] Error when parse {}.\n{}".format(context, traceback.format_exc()))
        finally:
            return finally_return

    @staticmethod
    def GetDirectorOrAuthorInfo(key, response: scrapy.http.response.Response):
        """
        解析导演或编剧信息
        :param key: '导演'或'编剧'
        :param response: scrapy返回的response
        :return: 导演或编剧信息字典
        """
        try:
            info_list = response.xpath("//div[@id='info']//span[text()='{key}']/following-sibling::span[1]/a".format(key = key))
            return {info.xpath("text()").extract_first(): info.xpath("@href").extract_first() for info in info_list}
        except:
            return dict()

    @staticmethod
    def GetActorsInfo(response: scrapy.http.response.Response):
        """
        解析演员信息
        :param response: scrapy返回的response
        :return: 演员信息字典
        """
        try:
            actor_info_list = response.xpath("//span[@class='actor']//a")
            return {actor_info.xpath("text()").extract_first(): actor_info.xpath("@href").extract_first() for actor_info in actor_info_list}
        except:
            return dict()

    @staticmethod
    def GetMovieCountry(response: scrapy.http.response.Response):
        """
        解析制片国
        :param response: scrapy返回的response
        :return: 制片国家
        """
        return response.xpath("//div[@id='info']/span[text()='制片国家/地区:'][1]/following-sibling::text()[1]").extract_first(default="").strip()

    @staticmethod
    def GetRateInfo(response: scrapy.http.response.Response):
        """
        解析评分信息
        :param response: scrapy返回的response
        :return: 评分人数,评分信息
        """
        rateNumber = int(response.xpath("//a[@class='rating_people']/span/text()").extract_first(default=0))

        rateDetails_dict = dict()
        for start_num in range(1, 6):
            rate = response.xpath("//span[@class='stars{} starstop']/../span[@class='rating_per']/text()".format(start_num)).extract_first(default="0")
            rateDetails_dict.update({start_num: float(rate.strip('%')) / 100.0})
        return rateNumber, rateDetails_dict

    @staticmethod
    def GetImdbLink(response):
        """
        解析imdb链接
        :param response: scrapy返回的response
        :return: imdb链接
        """
        return response.xpath("//span[text()='IMDb链接:']/following-sibling::a/@href").extract_first(default="")
