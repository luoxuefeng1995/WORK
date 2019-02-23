# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import pymongo
import random



class BossProxyMiddleware(object):
    '''
    使用免费代理IP
    '''
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['proxypool']
        self.proxies = self.db['proxies']

    def process_request(self, request, spider):
            a = self.proxies.find({'delay': {'$lt': 2}}, {'_id': 0, 'delay': 0})
            b = random.choices(list(a))[0]['proxy']
            request.meta['proxy'] = b

