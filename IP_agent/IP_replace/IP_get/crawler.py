from .config_rule import parse_rule
from .get_IP import  Downloader
from .my_parse import Parse
from .validate import valid,valid_many
from ..db import MongoDB
import logging
import time

logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)


def crawler():
    while True:
        logger.info('开始抓取代理。。。')
        for rule in parse_rule:
            for url in rule['url']:
                text = Downloader().download(url, rule)
                proxy_list = Parse().xpath_parse(text, rule)
                print(proxy_list)
                # for proxy in proxy_list:
                #     print(proxy)
                valid_many(proxy_list,'crawl')
        time.sleep(24*60*60)

def check():
    while True:
        logger.info('开始检测代理IP...')
        m = MongoDB()
        proxies = m.get(100000)
        if not len(proxies) == 0:
            logging.info('开始检测数据库中的代理IP...')
            valid_many(proxies,'check')
        time.sleep(30*60)


if __name__ == '__main__':
    pass