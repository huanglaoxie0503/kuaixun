# -*- coding: utf-8 -*-
import scrapy
import re
import logging

from kuaixun.common import get_html_tag, operation
from kuaixun.items import KuaixunItem
from kuaixun.settings import headers


logging.basicConfig(
    filename="info.log",
    level=logging.INFO,
    format="%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s",
)


class StcnSpider(scrapy.Spider):
    name = 'stcn_spider'
    allowed_domains = ['kuaixun.stcn.com']
    start_urls = ['https://kuaixun.stcn.com/index.html']

    def parse(self, response):
        infos = response.xpath('//*[@id="news_list2"]/li')
        for info in infos:
            title = info.xpath('a/text()').extract_first()
            link = info.xpath('a/@href').extract_first()
            time_p = info.xpath('span/text()').extract_first()
            minute = info.xpath('i/text()').extract_first()
            publish_time = time_p + ' ' + minute

            temp = link.split("/")
            detail_url = "/".join(temp[1:])
            detail_url = "https://kuaixun.stcn.com/{0}".format(detail_url)
            article_id = temp[-1:]
            article_id = "".join(article_id).split(".")[0].replace('_', '')

            judge_id = operation.judge_article_id(article_id=article_id)
            if judge_id:
                logging.info('数据库返回值为：{0}，article_id为：{0}，已经存在该数据。'.format(judge_id, article_id))
                continue

            item = KuaixunItem()
            # 新闻id
            item['article_id'] = article_id
            # 新闻标题
            item['title'] = title
            # 新闻发布时间
            item['publish_time'] = publish_time

            yield scrapy.Request(detail_url, headers=headers, meta={"item": item}, callback=self.get_content)

    def get_content(self, response):
        item = response.meta['item']

        content = response.xpath('//*[@id="ctrlfscont"]/text()'
                                 '|//*[@id="ctrlfscont"]/p/text()'
                                 '|//*[@id="ctrlfscont"]/p/span/text()').extract()
        content = ''.join(content).strip()
        if len(content) == 0:
            return

        content_p_div = get_html_tag.get_tag_id(response.text, 'div', 'ctrlfscont')
        content_p = re.findall(r'<div class="txt_con" id="ctrlfscont">\s+(.*?)\s+</div>', str(content_p_div))
        if len(content_p) > 0:
            content_p = content_p[0]
        else:
            content_p = content

        # 新闻内容
        item['content'] = content
        # # 带标签的新闻内容
        item['content_p'] = content_p
        # 来源
        item['art_source'] = '证券时报网'
        # # 新闻详细链接
        item['url'] = response.url

        yield item
