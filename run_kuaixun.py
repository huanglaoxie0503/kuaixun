#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from scrapy import cmdline

if __name__ == '__main__':
    file_log = os.getcwd() + "/info.log"
    if os.path.exists(file_log):
        os.remove(file_log)
        print("每次运行前把之前的日志文件删除,保留最新日志即可")

    cmdline.execute('scrapy crawl notice_spider'.split())








