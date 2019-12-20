import pymysql
import time
from kuaixun.settings import (
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DBNAME,
    MYSQL_TABLE,
)

conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    db=MYSQL_DBNAME,
    charset="utf8",
    use_unicode=True,
)
cursor = conn.cursor()


def judge_article_id(article_id):
    """验证article_id数据库是否已经存在"""
    try:
        sql = "select * from {0} where article_id=%s;".format(MYSQL_TABLE)
        cursor.execute(sql, (article_id,))
        results = cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return None
    except pymysql.Error as e:
        print(e)


def convert_time(time_Stamp):
    try:
        time_array = time.localtime(int(time_Stamp))
        other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        print(other_style_time)
        return other_style_time
    except Exception as e:
        print(e)


if __name__ == '__main__':
    timeStamp = 1556090252
    convert_time(timeStamp)
