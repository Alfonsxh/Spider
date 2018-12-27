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
    movies_link_urls = "https://movie.douban.com/subject/26363254/"

    content = requests.get(movies_link_urls).content
    content_dict = json.loads(content)
    print(content_dict)
    pass


if __name__ == '__main__':
    cookie = """viewed="4138920"; bid=KO_0e4bcvRU; gr_user_id=51a51ee5-8a9c-4a91-b59e-182d6bb14d50; _vwo_uuid_v2=D8059E57EC3BFCE723594EB2EA32B60ED|681f342c5aff5e561f566ee8bff70df8; __utmz=30149280.1545553515.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmz=223695111.1545553515.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ll="118172"; ct=y; __utmc=30149280; __utmc=223695111; ap_v=0,6.0; as="https://sec.douban.com/b?r=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26363254%2F"; ps=y; dbcl2="169205187:QvGF2w41YMk"; ck=fccS; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1545924324%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.100001.4cf6=37a8a7c714942962.1545553515.7.1545924324.1545922186.; _pk_ses.100001.4cf6=*; __utma=30149280.1726212544.1545056561.1545921215.1545924324.8; __utmb=30149280.0.10.1545924324; __utma=223695111.973629989.1545553515.1545921215.1545924324.7; __utmb=223695111.0.10.1545924324"""

    cookie_dict = {value.split('=', 1)[0].strip(): value.split('=', 1)[-1].strip() for value in  cookie.split(';')}
    print(cookie_dict)

    start_requests()
