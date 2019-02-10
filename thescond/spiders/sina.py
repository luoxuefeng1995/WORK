# -*- coding: utf-8 -*-
import scrapy
from ..items import ThescondItem

class SinaSpider(scrapy.Spider):
    name = 'sina'
    # allowed_domains = ['dddd']
    start_urls = ['https://iask.sina.com.cn/c/74.html']
    basic_url = 'https://iask.sina.com.cn'
    def parse(self, response):
        url_list = response.xpath('//li[@class="list"]')
        for i in url_list:
            item = ThescondItem()
            item['question'] = i.xpath('.//div[@class="question-title"]/a/text()').extract_first()
            item['question_time'] = i.xpath('.//div[@class="queation-other"]/span[2]/text()').extract_first()
            item['question_man'] = i.xpath('.//img/@alt').extract_first()
            url = i.xpath('.//div[@class="question-title"]/a/@href').extract_first()
            if url:
                yield scrapy.Request(url=self.basic_url+url, callback=self.detail_answer, meta={'items': item})
        next_page = response.xpath('//a[@class="btn-page"]/@href').extract()
        if next_page:
            yield scrapy.Request(url=self.basic_url+next_page[-1], callback=self.parse)

    def detail_answer(self, response):
        items = response.meta.get('items')
        title_1 = response.xpath('//h1//pre[@class="question-text"]/text()').extract_first()
        title_2 = response.xpath('//h1/div[@class="title-f22"]/pre/text()').extract_first()
        title_3 = response.xpath('//h3[@class="brand-answer-tatle"]/text()').extract_first()
        if title_1 is not None:
            self.first(response,items)
            yield items

        elif title_2 is not None:
            self.second(response,items)
            yield items

        elif title_3 is not None:
            self.third(response,items)
            yield items

    def first(self,response,items):
        data_list = response.xpath('//ul[@class="new-answer-list"]/li[@t="disploy"]')
        detail_list = []
        for i in data_list:
            item = {}
            answer_content = i.xpath('.//pre/text()').extract()
            answer_time = i.xpath('.//p[@class="time"]/text()').extract()
            use_name = i.xpath('.//p[@class="user-name"]//text()').extract()
            item['answer'] = list(zip(use_name, answer_time, answer_content))
            detail_list.append(item['answer'])
        items['answer'] = detail_list

    def second(self,response,items):
        data_list = response.xpath('//li[@t="disploy"]')
        detail_list = []
        for i in data_list:
            item = {}
            answer_content = i.xpath('.//div[@class="answer_text"]//pre/text()').extract()
            answer_time = i.xpath('.//span[@class="answer_t"]/text()').extract()
            use_name = i.xpath('.//a[@class="author_name"]/text()').extract()
            item['answer'] = list(zip(use_name, answer_time, answer_content))
            detail_list.append(item['answer'])
        items['answer'] = detail_list

    def third(self, response,items):
        items = response.meta.get('items')
        answer_content = response.xpath('//p[@class="brand-answer-text"]/text()').extract()
        answer_co_name = response.xpath('//div[@class="brand-answer-txt01"]/h2/text()').extract()
        answer_co_time = response.xpath('//div[@class="brand-answer-txt01"]/text()').extract()
        items['co_answer_content_man_time'] = list(zip(answer_co_name, answer_co_time, answer_content))
        data_list = response.xpath('//li[@class="brand-otherAmswer-li"]')
        detail_list = []
        for i in data_list:
            item = {}
            answer_content = i.xpath('.//p[@class="otherAmswer-list-txt"]/text()').extract()
            answer_time = i.xpath('.//span[@class="otherAmswer-user-time"]/text()').extract()
            use_name = i.xpath('.//p[@class="otherAmswer-user-name"]/a/text()').extract()
            item['answer'] = list(zip(use_name, answer_time, answer_content))
            detail_list.append(item['answer'])
        items['answer'] = detail_list


