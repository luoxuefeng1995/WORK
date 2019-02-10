import requests
import logging
import chardet #识别编码方式

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)


class Downloader():
    def __init__(self):
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6776.400 QQBrowser/10.3.2601.400Name'
        }

    def download(self, url,rule):
        logger.info('Downloading:{}'.format(url))
        try:
            resp = requests.get(url, headers=self.headers)
            resp.encoding = chardet.detect(resp.content)['encoding']

            if resp.status_code ==200:
                return resp.text
            else:
                raise ConnectionError
        except Exception as e:
            logger.error(e)

if __name__ == '__main__':
    d = Downloader()
    d.download('https://www.xicidaili.com/nn/', 111)