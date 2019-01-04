"""
@author: Alfons
@contact: alfons_xh@163.com
@file: run.py
@time: 18-12-23 下午4:06
@version: v1.0 
"""
import time
from scrapy.cmdline import execute

if __name__ == '__main__':
    spider_app = 'DoubanMovieSpider'
    cmd = 'scrapy crawl {0} --loglevel INFO'.format(spider_app)

    start_time = time.time()
    execute(cmd.split())
    print("[*] use time: {}'s.".format(time.time() - start_time))
