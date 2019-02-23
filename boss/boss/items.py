# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_classify = scrapy.Field()
    job_name = scrapy.Field()
    job_address = scrapy.Field()
    job_salary = scrapy.Field()
    job_discription = scrapy.Field()
    job_edu = scrapy.Field()
    job_city = scrapy.Field()
    job_experience = scrapy.Field()
    job_detail_url = scrapy.Field()