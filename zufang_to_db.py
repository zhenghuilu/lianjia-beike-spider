#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# read data from csv, write to database
# database includes: mysql/mongodb/excel/json/csv

import os
import pymysql
from lib.utility.path import DATA_PATH
from lib.zone.city import *
from lib.utility.date import *
from lib.utility.version import PYTHON_3
from lib.spider.base_spider import SPIDER_NAME
import records

pymysql.install_as_MySQLdb()


def create_prompt_text():
    city_info = list()
    num = 0
    for en_name, ch_name in cities.items():
        num += 1
        city_info.append(en_name)
        city_info.append(": ")
        city_info.append(ch_name)
        if num % 4 == 0:
            city_info.append("\n")
        else:
            city_info.append(", ")
    return 'Which city data do you want to save ?\n' + ''.join(city_info)


if __name__ == '__main__':

    ##################################
    db = None
    collection = None
    workbook = None
    csv_file = None
    datas = list()
    # 目标数据库 mysql
    db = records.Database('mysql://root:pass1234@localhost/house_data?charset=utf8&autocommit=True'
                          ,pool_size=5
                          ,max_overflow=-1
                          ,pool_timeout=5
                          )

    city = get_city()
    # 准备日期信息，爬到的数据存放到日期相关文件夹下
    date = get_date_string()
    # 获得 csv 文件路径
    # date = "20180331"   # 指定采集数据的日期
    # city = "sh"         # 指定采集数据的城市
    city_ch = get_chinese_city(city)
    csv_dir = "{0}/{1}/zufang/{2}/{3}".format(DATA_PATH, SPIDER_NAME, city, date)

    files = list()
    if not os.path.exists(csv_dir):
        print("{0} does not exist.".format(csv_dir))
        print("Please run 'python zufang.py' firstly.")
        print("Bye.")
        exit(0)
    else:
        print('OK, start to process ' + get_chinese_city(city))
    for csv in os.listdir(csv_dir):
        data_csv = csv_dir + "/" + csv
        # print(data_csv)
        files.append(data_csv)

    # 清理数据
    count = 0
    row = 0
    col = 0
    for csv in files:
        with open(csv, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                count += 1
                text = line.strip()
                try:
                    # 如果小区名里面没有逗号，那么总共是6项
                    if text.count(',') == 6:
                        date, district, area, xiaoqu_full_name, layout, building_space, price = text.split(',')
                    else:
                        print("数据解析异常：{0}".format(text))
                    ## 解析出租类型与小区名
                    if(xiaoqu_full_name.count("·") == 1):
                        rent_type, xiaoqu = xiaoqu_full_name.split('·')
                    else:
                        rent_type = xiaoqu_full_name.split('·')[0]
                        xiaoqu = xiaoqu_full_name.replace(rent_type+"·","")
                    price = price.replace(r'暂无数据', '0')
                    if ("-" in price):
                        price = price.split("-")[0]
                    price = int(price)
                    building_space = building_space.replace(r'平米', '')
                    if("-" in building_space):
                        building_space = building_space.split("-")[0]
                    try:
                        building_space = float(building_space)
                    except Exception as ex:
                        print(text)
                        print(ex)
                        continue;
                    print("count({0}):{1}:{2}:{3}:{4}:{5}:{6}:{7}:{8}".format(count, city_ch, date, district, area, xiaoqu, rent_type,
                                                                   building_space, price))
                    # 写入mysql数据库
                    db.query('INSERT INTO zufang (city, date, district, area, xiaoqu, rent_type, layout, building_space, price)'
                             'VALUES(:city, :date, :district, :area, :xiaoqu, :rent_type, :layout, :building_space, :price)',
                             city=city_ch, date=date, district=district, area=area, xiaoqu=xiaoqu, rent_type=rent_type,
                             layout=layout, building_space=building_space, price=price)
                except Exception as e:
                    print(text)
                    print(e)
                    ## raise e

    # 写入，并且关闭句柄
    db.close()
    print("Total write {0} items to database.".format(count))
