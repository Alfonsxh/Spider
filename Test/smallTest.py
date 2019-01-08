"""
@author: Alfons
@contact: alfons_xh@163.com
@file: smallTest.py
@time: 19-1-3 下午10:58
@version: v1.0 
"""
import json

error_json = """{
    "@context": "http://schema.org",
    "name": "铁线虫入侵 연가시",
    "url": "/subject/6839145/",
    "image": "https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1588680264.webp",
    "director": [
        {
            "@type": "Person",
            "url": "/celebrity/1324714/",
            "name": "朴正祐 Jeong-woo Park "
        }
    ],
    "author": [
        {
            "@type": "Person",
            "url": "/celebrity/1324714/",
            "name": "朴正祐 Jeong-woo Park	"
        }
    ],
    "actor": [
        {
            "@type": "Person",
            "url": "/celebrity/1275746/",
            "name": "金明民 Myeong-min Kim"
        },
        {
            "@type": "Person",
            "url": "/celebrity/1043642/",
            "name": "金烔完 Dong-wan Kim"
        },
        {
            "@type": "Person",
            "url": "/celebrity/1175765/",
            "name": "文晶熙 Jung-Hee Moon"
        },
        {
            "@type": "Person",
            "url": "/celebrity/1324715/",
            "name": "李荷妮 Ha-nui Lee"
        },
        {
            "@type": "Person",
            "url": "/celebrity/1381299/",
            "name": "郭仁俊 In-jun Gwak"
        },
        {
            "@type": "Person",
            "url": "/celebrity/1374620/",
            "name": "赵德贤 Deok-hyeon Jo"
        },
        {
            "@type": "Person",
            "url": "/celebrity/1375770/",
            "name": "周锡泰 Suk-tae Joo"
        },
        {
            "@type": "Person",
            "url": "/celebrity/1351949/",
            "name": "严智星 Ji-seong Eom"
        },
        {
            "@type": "Person",
            "url": "/celebrity/1320459/",
            "name": "郑仁基 In-gi Jeong"
        },
        {
            "@type": "Person",
            "url": "/celebrity/1373552/",
            "name": "闵庆珍 Kyoung-jin Min"
        }
    ],
    "datePublished": "2012-06-28",
    "genre": [
        "\u5267\u60c5",
        "\u60ca\u609a",
        "\u707e\u96be"
    ],
    "duration": "PT1H49M",
    "description": "制药公司小职员医学博士出身的宰赫（金明民 饰）早些年被弟弟宰弼（金烔完 饰）劝诱炒股，结果赔得精光，如今委身于一家毫无前景的制药公司做推销员，在外低声下气，看客户脸色行事，心中的郁结只有向家中妻儿宣泄...",
    "@type": "Movie",
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingCount": "36593",
        "bestRating": "10",
        "worstRating": "2",
        "ratingValue": "6.6"
    }
}"""

from urllib import parse

target = error_json
# print(target)
error_dict = json.loads(target, strict=False)
print(error_dict)

from lxml import etree

target = "window.location.href="
redirct = """<script>var d=[navigator.platform,navigator.userAgent,navigator.vendor].join("|");window.location.href="https://sec.douban.com/a?c=5038cd&d="+d+"&r=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F10441599%2F&k=FGJxcekzGhEO942gNNp6Re6TqnZTdGkmdlM5jIp%2BqiA";</script>"""

redirct_url = redirct[redirct.find(target) + len(target): redirct.find(";</script>")].strip('\"')
print(redirct_url)

import execjs
root_node = etree.HTML(redirct)
script = root_node.xpath("//script/text()")[0]

execjs.eval(script)
pass