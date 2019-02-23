# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import requests
import re
from PIL import Image
from .chaojiying import Chaojiying_Client
from lxml import etree
from io import BytesIO

# https://www.zhipin.com/c101010100-p100506/
# https://www.zhipin.com/c101270100-p100101/?ka=sel-city-101270100
# https: // www.zhipin.com / captcha?randomKey = TFZqPSH5ThQLIkIZlDn6Axecnc0yQDiK

class BossSpider(CrawlSpider):
    name = 'BOSS'
    # allowed_domains = ['ddddd']
    start_urls = ['https://www.zhipin.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/c101010100-p100[15].*|/c101010100-p1013.*'), callback='parse_item'),
    )

    def parse_item(self, response):
        city_url = response.url.replace('c101010100', 'c101270100') + ('?ka=sel-city-101270100')
        yield scrapy.Request(city_url, callback=self.parse_step01)

    def parse_step01(self, response):
        job_main = response.xpath('//div[@id="main"]//div[@class="job-list"]/ul/li')
        for data in job_main:
            job_classify = data.xpath('.//div[@class="info-primary"]//div[@class="job-title"]/text()').extract_first()
            job_name = data.xpath('.//div[@class="info-company"]//h3[@class="name"]/a/text()').extract_first()
            job_address = data.xpath('.//div[@class="info-primary"]/p/text()').extract()
            if job_address:
                job_city = job_address[0]
                job_edu = job_address[2]
                job_experience = job_address[1]

            job_salary = data.xpath('.//div[@class="info-primary"]//span[@class="red"]/text()').extract_first()
            job_detail_url = data.xpath('.//div[@class="info-primary"]//a/@href').extract_first()
            if job_detail_url:
                job_detail_url = self.start_urls[0] + job_detail_url
            yield scrapy.Request(url=job_detail_url, callback=self.discription, meta={'meta': (job_classify, job_name, job_salary, job_city, job_edu, job_experience)})
        page_nexturl = response.xpath('//div[@class="page"]/a[@class="next"]/@href').extract_first()
        if page_nexturl:
            page_nexturl = self.start_urls[0].join(page_nexturl)
            yield scrapy.Request(page_nexturl, callback=self.parse_step01)

    def discription(self, response):
        meta = response.meta.get('meta')
        job_discription = response.xpath('//h3[text()="职位描述"]/../div/text()').extract()
        job_discription = list(map(lambda x: x.strip(), job_discription))
        capycha = re.findall(r'popUpCaptcha', response.url)
        if capycha:
            print('=========================')
            job_di = response.url
            resp = self.post_requests(job_di)
            resp = etree.HTML(resp)
            job_discription = resp.xpath('//h3[text()="职位描述"]/../div/text()')
            job_discription = list(map(lambda x: x.strip(), job_discription))
        meta = meta + (job_discription,)
        print('=======',meta, '===========')

    def post_requests(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'

        }
        # url = 'https://www.zhipin.com/captcha/popUpCaptcha?redirect=https%3A%2F%2Fwww.zhipin.com%2Fc101010100-p100507%2F'
        response01 = requests.get(url, headers=headers)
        response = response01.text
        base_url = 'https://www.zhipin.com/'
        capycha = re.findall(r'popUpCaptcha', response01.url)
        response = etree.HTML(response)
        if capycha:
            # print('<<', response.url, '>>')
            print('开始验证登录验证码')
            post_url = response.xpath('//form[@method="post"]/@action')[0]
            post_url = base_url + post_url
            print(post_url)
            captcha_url = response.xpath('//img[@class="code"]/@src')[0]
            captcha_url = base_url + captcha_url
            print(captcha_url)
            randomKey = re.findall(r'randomKey=(.*)', captcha_url)
            img = requests.get(captcha_url).content
            cjy = Chaojiying_Client('qq849885277', 'luoxuefeng520', 898671)
            result = cjy.PostPic(img, 1902).get('pic_str')
            data = {
                'randomKey': randomKey,
                'captcha': result,
            }
            response = requests.post(post_url, headers=headers, data=data)
            print(randomKey, result)
            print('验证成功')
            return response.text
