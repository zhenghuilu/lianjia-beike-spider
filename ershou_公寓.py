#!/usr/bin/env python
# coding=utf-8
# author: Peter Lu
# 此代码仅供学习与交流，请勿用于商业用途。
# 获得指定城市的二手房数据
# tag为过滤条件，多可条件可合并， 不加条件最多可爬100页，多于100页的数据爬不到

from lib.spider.ershou_spider import *

if __name__ == "__main__":
    spider = ErShouSpider(SPIDER_NAME)
    spider.tag = "sf2"
    spider.start()

