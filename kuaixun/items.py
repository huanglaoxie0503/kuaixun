# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


from kuaixun.settings import MYSQL_TABLE


class KuaixunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 新闻id
    article_id = scrapy.Field()
    # 新闻标题
    title = scrapy.Field()
    # 新闻发布时间
    publish_time = scrapy.Field()
    # 来源
    art_source = scrapy.Field()
    # 新闻内容
    content = scrapy.Field()
    # # 带标签的新闻内容
    content_p = scrapy.Field()
    # # 新闻详细链接
    url = scrapy.Field()

    def get_insert_sql(self):
        # 插入：sql语句
        insert_sql = """insert into {0} (article_id, title, url, source, key_word,publish_time,content,content_p) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""".format(MYSQL_TABLE)

        param = (
            self["article_id"],
            self["title"],
            self['url'],
            self["art_source"],
            None,
            self["publish_time"],
            self["content"],
            self['content_p'],
        )
        return insert_sql, param

