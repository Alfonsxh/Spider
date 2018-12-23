"""
@author: Alfons
@contact: alfons_xh@163.com
@file: run.py
@time: 18-12-23 下午4:06
@version: v1.0 
"""
from scrapy.cmdline import execute

if __name__ == '__main__':
    spider_app = 'DoubanMovieLinks'
    cmd = 'scrapy crawl {0}'.format(spider_app)

    execute(cmd.split())
