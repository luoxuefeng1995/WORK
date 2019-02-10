# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThescondItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    question = scrapy.Field()
    question_time = scrapy.Field()
    question_man = scrapy.Field()
    answer = scrapy.Field()
    co_answer_content_man_time = scrapy.Field()
    # answer_man = scrapy.Field()
    # answer_time = scrapy.Field()

