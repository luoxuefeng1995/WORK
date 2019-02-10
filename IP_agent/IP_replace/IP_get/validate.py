import requests
import time
from ..db import MongoDB
from multiprocessing.pool import ThreadPool
from requests.exceptions import ProxyError, ConnectTimeout
import logging

logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)


def valid_many(proxy_list, method):
    pool = ThreadPool(len(proxy_list))
    for proxy in proxy_list:
        pool.apply_async(valid, args=(proxy,method))
    pool.close()
    pool.join()

def valid(proxy, method, url='https://www.baidu.com'):
    proxies = {
        'http': 'http://' + proxy['proxy'],
        'https': 'https://' + proxy['proxy']
    }
    try:
        start = time.time()
        # print(proxies)
        resp = requests.get(url=url, proxies=proxies, timeout=5)
        delay = round(time.time() - start, 2)

        if resp.status_code == 200:
            proxy['delay'] = delay
            logger.info('此代理可用:{}'.format(proxy))
            # print('此代理可用:{}'.format(proxy))
            if method == 'crawl':
                ins = MongoDB()
                ins.insert(proxy)
            elif method == 'check':
                MongoDB().update({'proxy':proxy['proxy']}, {'delay':proxy['delay': proxy['delay']]})
        else:
            if method == 'check':
                logger.info("此代理失效：{}".format(proxy))
                MongoDB().delete({'proxy':proxy['proxy']})
    except (ProxyError, ConnectTimeout):
        if method == 'check':
            logger.info("此代理失效：{}".format(proxy))
            MongoDB().delete({'proxy': proxy['proxy']})