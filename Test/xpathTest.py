"""
@author: Alfons
@contact: alfons_xh@163.com
@file: xpathTest.py
@time: 18-12-26 下午11:45
@version: v1.0 
"""
import requests
from lxml import etree

session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

target_url = "https://movie.douban.com/subject/26363254/"
# target_url = "https://www.douban.com/accounts/login?redir=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26363254%2F"
content = session.get(target_url).content.strip().decode()

if "检测到有异常请求从你的 IP 发出" in content:
    login_node = etree.HTML(content)
    login_url = login_node.xpath("//a[text()='登录']/@href")[0]
    import webbrowser
    webbrowser.open(login_url)
    input("When u success login, press any key to continue.")
    content = session.get(target_url).content.strip().decode()


root_node = etree.HTML(content)

actors = root_node.xpath("//span[@class='actor']//a")
for actor in actors:
    url = actor.xpath("@href")
    actor_name = actor.xpath("text()")
    print(url, actor_name)

country = root_node.xpath("//div[@id='info']/text()[7]")[0].strip()
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
pass
