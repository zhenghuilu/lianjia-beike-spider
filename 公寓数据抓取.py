#!/usr/bin/env python
# coding=utf-8
# author: Peter Lu
# 此代码仅供学习与交流，请勿用于商业用途。
# 获得指定城市的二手房数据和租房数据
# tag为过滤条件，多可条件可合并， 不加条件最多可爬100页，多于100页的数据爬不到

from lib.spider.ershou_spider import *
from lib.spider.zufang_spider import *

if __name__ == "__main__":
    # 二手房数据抓取
    spider = ErShouSpider(SPIDER_NAME)
    spider.tag = "sf2"
    spider.start()
    # 租房数据抓取
    spider = ZuFangBaseSpider(SPIDER_NAME)
    # rt200600000001为整租，l0l1为一室二室
    spider.tag = "rt200600000001l0l1"
    spider.start()
