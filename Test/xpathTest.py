"""
@author: Alfons
@contact: alfons_xh@163.com
@file: xpathTest.py
@time: 18-12-26 下午11:45
@version: v1.0 
"""
import requests
from lxml import etree


def ContentWithNetwork():
    headers = {
        'Host': 'movie.douban.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://movie.douban.com/tag/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    session = requests.Session()
    session.headers = headers
    session.max_redirects = 100
    session.proxies = {'http': '127.0.0.1:1090'}

    target_url = "https://movie.douban.com/subject/10512661/"
    # target_url = "https://www.douban.com/accounts/login?redir=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26363254%2F"

    # content = session.get(target_url).content.strip().decode()
    return requests.get(target_url, headers=headers).content


def ContentWithTxt():
    with open("./movie_info_html.html", "r") as f:
        return f.read()


# content = ContentWithNetwork()
content = ContentWithTxt()

# if "检测到有异常请求从你的 IP 发出" in content:
#     login_node = etree.HTML(content)
#     login_url = login_node.xpath("//a[text()='登录']/@href")[0]
#     import webbrowser
#
#     webbrowser.open(login_url)
#     input("When u success login, press any key to continue.")
#     content = session.get(target_url).content.strip().decode()

root_node = etree.HTML(content)

title = root_node.xpath("//title/text()")[0].strip().replace(" (豆瓣)", "")

actors = root_node.xpath("//span[@class='actor']//a")
for actor in actors:
    url = actor.xpath("@href")
    actor_name = actor.xpath("text()")
    print(url, actor_name)

country = root_node.xpath("//div[@id='info']/span[text()='制片国家/地区:'][1]/following-sibling::text()[1]")
country = country[0].strip()
print(country)

five_rate = root_node.xpath("//span[@class='stars5 starstop']/../span[@class='rating_per']/text()")[0]
four_rate = root_node.xpath("//span[@class='stars4 starstop']/../span[@class='rating_per']/text()")[0]
three_rate = root_node.xpath("//span[@class='stars3 starstop']/../span[@class='rating_per']/text()")[0]
two_rate = root_node.xpath("//span[@class='stars2 starstop']/../span[@class='rating_per']/text()")[0]
one_rate = root_node.xpath("//span[@class='stars1 starstop']/../span[@class='rating_per']/text()")[0]

print(float(five_rate.strip('%')) / 100.0)
print(four_rate)
print(three_rate)
print(two_rate)
print(one_rate)

imdb_link = root_node.xpath("//span[text()='IMDb链接:']/following-sibling::a/@href")[0]

rate_people = root_node.xpath("//a[@class='rating_people']/span/text()")[0]
pass
