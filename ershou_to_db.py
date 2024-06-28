#!/usr/bin/env python
# coding=utf-8
# author: peter lu
# 此代码仅供学习与交流，请勿用于商业用途。
# read data from csv, write to database(mysql)

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

    # 获取城市，默认杭州，如果需要其它城市，打开下面的注释
    # city = get_city()
    city = "hz"
    # 准备日期信息，爬到的数据存放到日期相关文件夹下
    date = get_date_string()
    # 获得 csv 文件路径
    # date = "20180331"   # 指定采集数据的日期
    # city = "sh"         # 指定采集数据的城市
    city_ch = get_chinese_city(city)
    csv_dir = "{0}/{1}/ershou/{2}/{3}".format(DATA_PATH, SPIDER_NAME, city, date)

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
    error_count = 0
    for csv in files:
        with open(csv, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                count += 1
                text = line.strip()
                try:
                    # 如果小区名里面没有逗号，那么总共是6项
                    if text.count(',') >= 7:
                        text_array = text.split(',')
                        date = text_array[0]
                        district = text_array[1]
                        area = text_array[2]
                        xiaoqu = text_array[3]
                        layout = text_array[4]
                        building_space = text_array[5]
                        price = text_array[6]
                        total_price = text_array[7]
                        desc = text_array[8]
                    else:
                        print("数据解析异常：{0}".format(text))
                        error_count = error_count + 1
                        continue
                    ## 建筑面积处理
                    building_space = building_space.replace(r"平米","")
                    building_space = float(building_space)
                    ## 单价处理
                    price = price.replace(r"元/平","")
                    price = int(price)
                    ## 总价处理 fixme
                    total_price = total_price.replace(r"万","")
                    print("count({0}):{1}:{2}:{3}:{4}:{5}:{6}:{7}:{8}:{9}:{10}"
                          .format(count, city_ch, date, district, area, xiaoqu, layout, building_space, price, total_price, desc))
                    # 写入mysql数据库
                    db.query('INSERT INTO ershou (city,date,district,area,xiaoqu,layout,building_space,price,total_price,`desc`)'
                             'VALUES(:city, :date, :district, :area, :xiaoqu, :layout, :building_space, :price, :total_price, :desc)',
                             city=city_ch, date=date, district=district, area=area, xiaoqu=xiaoqu, layout=layout, building_space=building_space, price=price, total_price=total_price, desc=desc)
                except Exception as e:
                    print(text)
                    print(e)
                    error_count = error_count + 1
                    raise e

    # 写入，并且关闭句柄
    db.close()
    print("Total write {0}, total error {1} items to database.".format(count, error_count))
