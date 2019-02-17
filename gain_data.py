import requests

from lxml import etree

class Gain_UA():
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'

        }

    def request(self):
        response = requests.get(url=self.url,headers=self.headers)

        return response

    def parse(self,reponse):
        user_agent = []
        resp = etree.HTML(reponse.text)
        ua_list = resp.xpath('//div[@id="liste"]/ul')
        for i in ua_list:
            ua = i.xpath('./li/a/text()')
            if ua:
                for j in ua:
                    user_agent.append(j)
        return user_agent

    def run(self):

        response = self.request()

        result = self.parse(response)

        return result


if __name__ == '__main__':
    get = Gain_UA('http://www.useragentstring.com/pages/useragentstring.php?name=Chrome')

    lit = get.run()
    print(lit)
    # for i in lit:
    #     print(i)