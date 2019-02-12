# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from .settings import USER_LIST

import random

class UserAgentDownloadMiddleware(object):

    user_list = USER_LIST
    def process_request(self,request,spider):

        user_agent = random.choice(self.user_list)

        request.headers['User-Agent'] = user_agent