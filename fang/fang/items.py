# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 新房标记
    new = scrapy.Field()
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 居室
    rooms = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 销售情况
    sale = scrapy.Field()
    # 详细页面的url
    detail_url = scrapy.Field()


class EsfHouseItem(scrapy.Item):

    # 二手房房标记
    old = scrapy.Field()
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名
    name = scrapy.Field()
    # 几居室
    rooms = scrapy.Field()
    # 楼层情况
    floor = scrapy.Field()
    # 朝向
    toward = scrapy.Field()
    # 年代
    year = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 建筑面积
    area = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 单价
    per_price = scrapy.Field()
    # 详情链接
    detail_url = scrapy.Field()