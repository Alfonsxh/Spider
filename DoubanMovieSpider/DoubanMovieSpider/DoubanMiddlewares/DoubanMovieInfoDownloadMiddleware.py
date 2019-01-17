"""
@author: Alfons
@contact: alfons_xh@163.com
@file: DoubanMovieInfoMiddleware.py
@time: 18-12-28 下午10:04
@version: v1.0 
"""
import random
import string
import requests
from lxml import etree
from DoubanMiddlewares.CookieManager import GetCookie


class CookieMiddleware(object):
    cookies = None
    error_num = 0

    def __init__(self):
        self.cookies = GetCookie()

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        request.cookies = self.cookies
        pass

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        if response.status == 302:
            # content = requests.get(response.url)
            # target_node = etree.HTML(content.text)
            # login_url = target_node.xpath("//@href")[0]

            if self.error_num % 20 == 0:
                self.cookies = GetCookie()
                print("[Middleware] response.status == 302 {}. New cookie is {}.".format(request.url, self.cookies))

            self.error_num += 1
            return request

        return response

    def process_exception(self, request, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass


class UserAgentMiddleware(object):

    def __init__(self):
        with open("/home/alfons/.Spiders/Douban/useragents.txt", 'r') as f:
            self.user_agents = [user_agent.strip() for user_agent in f.readlines()]
            pass

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # request.headers['User-Agent'] = ["Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"]
        request.headers['User-Agent'] = random.choice(self.user_agents)
        pass


class ProxyMiddleware(object):
    proxy_url = "http://127.0.0.1:5010/get/"

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # request.headers['User-Agent'] = ["Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"]
        # if not request.url.startswith("https://movie.douban.com/j/new_search_subjects"):
        proxy = requests.get(self.proxy_url, timeout=3).content.strip().decode()
        request.meta['proxy'] = "http://{proxy}".format(proxy=proxy)
        pass


class ConnectionMiddleware(object):
    def process_exception(self, request, exception, spider):
        print(request.url, type(exception))
        # return scrapy.Request(url = request)
        return request
