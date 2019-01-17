"""
@author: Alfons
@contact: alfons_xh@163.com
@file: smallTest.py
@time: 19-1-3 下午10:58
@version: v1.0 
"""
import json

error_json = """{  "@context": "http://schema.org",  "name": "木偶奇遇记 Pinocchio",  "url": "/subject/4234368/",  "image": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2515485668.webp",  "director":   [  ],  "author":   [    {      "@type": "Person",      "url": "/celebrity/1033747/",      "name": "伊万·科特罗尼奥 Ivan Cotroneo"    }    ,    {      "@type": "Person",      "url": "/celebrity/1037925/",      "name": "卡洛·科洛迪 Carlo Collodi"    }  ],  "actor":   [    {      "@type": "Person",      "url": "/celebrity/1310480/",      "name": "罗比·凯 Robbie Kay"    }    ,    {      "@type": "Person",      "url": "/celebrity/1041156/",      "name": "鲍勃·霍斯金斯 Bob Hoskins"    }    ,    {      "@type": "Person",      "url": "/celebrity/1032253/",      "name": "亚历山德罗·加斯曼 Alessandro Gassman"    }    ,    {      "@type": "Person",      "url": "/celebrity/1212353/",      "name": "Domenico Balsamo"    }    ,    {      "@type": "Person",      "url": "/celebrity/1126276/",      "name": "弗朗西斯科·潘诺菲诺 Francesco Pannofino"    }    ,    {      "@type": "Person",      "url": "/celebrity/1087172/",      "name": "Rupert Degas"    }    ,    {      "@type": "Person",      "url": "/celebrity/1085124/",      "name": "毛里齐奥·多纳多尼 Maurizio Donadoni"    }    ,    {      "@type": "Person",      "url": "/celebrity/1050815/",      "name": "托尼·贝尔多瑞利 Toni Bertorelli"    }    ,    {      "@type": "Person",      "url": "/celebrity/1016669/",      "name": "托马斯·布罗迪-桑斯特 Thomas Brodie-Sangster"    }    ,    {      "@type": "Person",      "url": "/celebrity/1045058/",      "name": "维奥兰特·普拉奇多 Violante Placido"    }    ,    {      "@type": "Person",      "url": "/celebrity/1042032/",      "name": "Luciana Littizzetto"    }    ,    {      "@type": "Person",      "url": "/celebrity/1032034/",      "name": "乔斯·雅克兰德 Joss Ackland"    }    ,    {      "@type": "Person",      "url": "/celebrity/1016767/",      "name": "玛格丽塔·布伊 Margherita Buy"    }  ],  "datePublished": "2008-12-14",  "genre": ["\u5267\u60c5", "\u513f\u7ae5", "\u5947\u5e7b", "\u5192\u9669"],  "duration": "PT1H51M",  "description": "本片是华特迪士尼继『白雪公主』之后的又一杰作，故事叙述一个由老木匠 Geppetto 所雕塑的小木偶 pinocchio 如何学会\实、勇敢、不自私，而成为一个真正的男孩。迪士尼动画家\用进步的技术创...",  "@type": "Movie",  "aggregateRating": {    "@type": "AggregateRating",    "ratingCount": "221",    "bestRating": "10",    "worstRating": "2",    "ratingValue": "7.3"  }}"""

from urllib import parse

target = error_json.replace('\\', '')
# print(target)
error_dict = json.loads(target, strict=False)
print(error_dict)

from lxml import etree
from urllib.parse import unquote

redirct = """<script>var d=[navigator.platform,navigator.userAgent,navigator.vendor].join("|");window.location.href="https://sec.douban.com/a?c=5038cd&d="+d+"&r=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F10441599%2F&k=FGJxcekzGhEO942gNNp6Re6TqnZTdGkmdlM5jIp%2BqiA";</script>"""
target = "&r=https"
redirct_url = unquote(redirct[redirct.find(target) + 3: redirct.find(";</script>")].strip('\"'))

print(redirct_url)

import execjs

root_node = etree.HTML(redirct)
script = root_node.xpath("//script/text()")[0]

execjs.eval(script)
pass
