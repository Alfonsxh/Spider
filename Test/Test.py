"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Test.py
@time: 18-12-23 下午4:44
@version: v1.0 
"""
import requests
import json


def start_requests():
    movies_link_urls = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={page}"
    for page in range(1):
        content = requests.get(movies_link_urls.format(page=page * 20)).content
        content_dict = json.loads(content)
        pass


if __name__ == '__main__':
    start_requests()
