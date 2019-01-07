"""
@author: Alfons
@contact: alfons_xh@163.com
@file: LoginTest.py
@time: 19-1-6 下午11:32
@version: v1.0 
"""
import requests
from DoubanMovieSpider.DoubanMovieSpider.ConfigManager.ConfigManager import ConfigManagerInstance as ConfigManager

DOUBAN_MOVIE_LOGIN_URL = 'https://accounts.douban.com/login'

login_form = {
    'source': 'movie',
    'redir': 'https://movie.douban.com/',
    'form_email': ConfigManager.login_username,
    'form_password': ConfigManager.login_password,
    'captcha-solution': '',
    'captcha-id': '',
    'remember': 'on',
    'login': '登录'
}

with requests.Session() as session:
    session.post(url=DOUBAN_MOVIE_LOGIN_URL, data=login_form)
    cookie = session.cookies.get_dict()
    print(cookie)
pass
