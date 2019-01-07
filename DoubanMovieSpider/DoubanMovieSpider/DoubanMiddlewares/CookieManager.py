"""
@author: Alfons
@contact: alfons_xh@163.com
@file: CookieManager.py
@time: 19-1-7 下午9:31
@version: v1.0 
"""
import requests
from lxml import etree
from PIL import Image
from ConfigManager.ConfigManager import ConfigManagerInstance as ConfigManager

douban_login_url = "https://accounts.douban.com/login"


def GetCookie(login_url=douban_login_url):
    headers = {
        'Host': 'accounts.douban.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://www.douban.com',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    if login_url != douban_login_url:
        headers.update({'Referer': login_url})

    form_data = {
        "source": "movie",
        "redir": "https://movie.douban.com/",
        "form_email": ConfigManager.login_username,
        "form_password": ConfigManager.login_password,
        "remember": "on",
        "login": "登录"
    }

    session = requests.Session()
    login_page = session.get(login_url, timeout=3).content

    root_node = etree.HTML(login_page)
    captcha_node = root_node.xpath('//img[@id="captcha_image"]')
    if len(captcha_node) > 0:
        ParseCaptchaImg(root_node, form_data)

    session.post(login_url, headers=headers, data=form_data)

    return session.cookies.get_dict()


def ParseCaptchaImg(root_node, form_data):
    captcha_url = root_node.xpath('//img[@id="captcha_image"]/@src')[0]
    captcha_id = root_node.xpath('//div[@class="captcha_block"]/input[@name="captcha-id"]/@value')[0]

    with open('captcha.jpg', 'wb') as f:
        captcha_request = requests.get(captcha_url)
        f.write(captcha_request.content)

    Image.open('captcha.jpg').show()
    captcha_solution = input()

    form_data.update({'captcha-solution': captcha_solution, 'captcha-id': captcha_id})


if __name__ == '__main__':
    # cookie = GetCookie()
    # print(cookie)

    with open("./error.html") as f:
        root = etree.HTML(f.read())

    ParseCaptchaImg(root, dict())
