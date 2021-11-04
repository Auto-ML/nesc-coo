#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : nesc.
# @File         : hegui
# @Time         : 2021/11/4 上午10:33
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


from docxtpl import DocxTemplate, RichText

from meutils.pipe import *
from meutils.date_utils import date_difference

_mapping = '一二三四五六七八九十'

date = date_difference(fmt='%Y年%m月%d日')
year = date[:4]

############################################################
from meutils.request_utils.crawler import Crawler

url_ = "http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd"
c = Crawler(url_)

urls = c.xpath('//*[@id="myul"]/li[*]//@href')
titles = c.xpath('//*[@id="myul"]/li[*]/a//text()')

监管动态 = {}
for idx, title, url in tqdm(zip(_mapping, titles, urls)):
    url = url.replace('.', url_, 1)
    lines = Crawler(url).xpath("""//*[@class="Custom_UnionStyle"]//text()""")
    监管动态[f'{idx}、{title}'] = lines | xjoin('')
    # break


############################################################
context = {
    'year': year,
    'date': date,
    '监管动态': 监管动态,
    '法律法规跟踪': {},
}

doc = DocxTemplate('合规日报模板.docx')
doc.render(context)
doc.save('合规日报模板_.docx')
