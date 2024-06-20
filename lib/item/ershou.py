#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 二手房信息的数据结构


class ErShou(object):
    def __init__(self, district, area, name, layout, building_space, price, total_price, desc):
        self.district = district
        self.area = area
        self.name = name
        self.layout = layout
        self.building_space = building_space
        self.price = price
        self.total_price = total_price
        self.desc = desc

    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.name + "," + \
                self.layout + "," + \
                self.building_space + "," + \
                self.price + "," + \
                self.desc
