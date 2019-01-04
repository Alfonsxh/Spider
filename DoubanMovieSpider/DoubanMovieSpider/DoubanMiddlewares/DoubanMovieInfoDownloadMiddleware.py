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
from ConfigManager.ConfigManager import ConfigManagerInstance as ConfigManager


def GetNewCookie():
    return {
        "bid": "".join(random.sample(string.ascii_letters + string.digits, 11)),
        "ck": "".join(random.sample(string.ascii_letters + string.digits, 4))
    }


def Login(login_url, cookies):
    headers = {
        'Host': 'accounts.douban.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://www.douban.com',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': login_url,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    form_data = {
        # "ck": cookies["ck"],
        # "bid": cookies["bid"],
        "source": "None",
        "redir": login_url.split("redir=")[-1],
        "form_email": ConfigManager.login_username,
        "form_password": ConfigManager.login_password,
        "remember": "on",
        "login": "登录"
    }

    login_page = requests.get(login_url, timeout = 3)

    content = requests.post(login_url, headers=headers, data=form_data)
    pass


class CookieMiddleware(object):
    cookie_change = False
    # cookies = {"bid": "KO_0e4bcvRU", "ck": "e2Fh"}
    cookies = {"bid": "KO_0e4bcvRU"}

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # if len(request.meta['redirect_urls']) > 3:
        #     login_url = "https://www.douban.com/accounts/login?redir={redir}".format()
        #     requests.post()

        # if self.cookie_change:
        #     self.cookies = GetNewCookie()

        # request.cookies = self.cookies

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
            #
            # print("[Begin login in] {}".format(login_url))
            # Login(login_url, request.cookies)
            return request

        return response

    def process_exception(self, request, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        self.cookie_change = True
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
        if not request.url.startswith("https://movie.douban.com/j/new_search_subjects"):
            proxy = requests.get(self.proxy_url, timeout=3).content.strip().decode()
            request.meta['proxy'] = "http://{proxy}".format(proxy=proxy)
        pass


import twisted
import scrapy


class ConnectionMiddleware(object):
    def process_exception(self, request, exception, spider):
        print(type(exception))
        if exception:
            # return scrapy.Request(url = request)
            return request
        pass
