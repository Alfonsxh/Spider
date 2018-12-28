"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ProxyMiddleware.py
@time: 18-12-27 下午10:56
@version: v1.0 
"""

from scrapy import signals


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        request.meta['proxy'] = "http://127.0.0.1:1080"
