import requests
import re
from PIL import Image
from chaojiying import Chaojiying_Client
from lxml import etree
from io import BytesIO

def process_response():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'

    }
    url = 'https://www.zhipin.com/captcha/popUpCaptcha?redirect=https%3A%2F%2Fwww.zhipin.com%2Fc101010100-p100507%2F'
    response01 = requests.get(url, headers=headers)
    response = response01.text
    base_url = 'https://www.zhipin.com/'
    capycha = re.findall(r'popUpCaptcha', response01.url)
    response = etree.HTML(response)
    if capycha:
        # print('<<', response.url, '>>')
        print('开始验证登录验证码')
        post_url = response.xpath('//form[@method="post"]/@action')[0]
        post_url = base_url+post_url
        print(post_url)
        captcha_url = response.xpath('//img[@class="code"]/@src')[0]
        captcha_url = base_url+captcha_url
        print(captcha_url)
        randomKey = re.findall(r'randomKey=(.*)', captcha_url)
        img = requests.get(captcha_url).content
        image = BytesIO(img)

        img1 = Image.open(image)
        img1.show()
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
    return response

if __name__ == '__main__':
    a = process_response()

    print(a)