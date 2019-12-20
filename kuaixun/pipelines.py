# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymysql
import redis
import json
from kuaixun.settings import (
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DBNAME,
)
from kuaixun.settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, Condition_list
from kuaixun.items import KuaixunItem


class MysqlPipeline(object):
    """同步的方式将数据保存到数据库：方法二"""

    def __init__(self):
        self.conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            db=MYSQL_DBNAME,
            charset="utf8",
            use_unicode=True,
        )
        self.cursor = self.conn.cursor()
        self.redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)

    def process_item(self, item, spider):
        try:
            # 插入
            if isinstance(item, KuaixunItem):
                self.do_insert(item)

                self.redis_send_msg(item)
                self.redis_send_bot_news(item)
            else:
                logging.info('Error Data')
        except pymysql.Error as e:
            logging.error("-----------------insert faild-----------")
            logging.error(e)
            print(e)

        return item

    def close_spider(self, spider):
        try:
            self.conn.close()
            logging.info("mysql already close")
        except Exception as e:
            logging.info("--------mysql no close-------")
            logging.error(e)

    def do_insert(self, item):
        try:
            insert_sql, params = item.get_insert_sql()

            self.cursor.execute(insert_sql, params)
            self.conn.commit()
            logging.info("----------------insert success-----------")
        except pymysql.Error as e:
            print(e)

    def redis_send_msg(self, item):
        try:
            result = {
                 'art_source': item['art_source'],
                 'article_id': item['article_id'],
                 'content': item['content'],
                 'content_p': item['content_p'],
                 'publish_time': item['publish_time'],
                 'title': item['title'],
                 'url': item['url']
                      }
            result = json.dumps(result, ensure_ascii=False)

            back_info = self.redis_conn.publish('kuaixun_content', result)
            logging.info('redis publish info successful,redis返回信息为：{0},发布数据id为：{1}'.format(back_info, item['article_id']))
        except Exception as e:
            print(e)

    def redis_send_bot_news(self, item):
        title = item['title']
        content = item['content']
        for condition in Condition_list:
            if condition in content and 'e公司讯' in content and '申购代码' not in content:
                print(condition)
                result = {
                    'art_source': '证券时报',
                    'article_id': item['article_id'],
                    'content': content,
                    'publish_time': item['publish_time'],
                    'title': title,
                    'url': item['url']
                }
                result = json.dumps(result, ensure_ascii=False)

                back_info = self.redis_conn.publish('bot_news', result)

                logging.info('redis publish info successful,redis返回信息为：{0},发布数据id为：{1}'.format(back_info, item['article_id']))

                # 如果新闻符合多个条件，只发布一次
                Tag = True
                if Tag:
                    return
