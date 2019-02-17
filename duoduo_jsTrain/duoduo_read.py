import requests
import math
import random
import execjs
import re


#多多看书JS逆向（token的值）：  Math.floor(65536 * (1 + Math.random())).toString(16).substring(1)
class duoduo_Read(object):
    def __init__(self, username, password):
        self.session=requests.session()
        self.username = username
        self.password = password
        self.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6776.400 QQBrowser/10.3.2601.400Name'
}
        self.data = {
        'username':	self.username,
        'password':	self.password,
        'captcha':'',
        'autoLogin':'1',
        'client_id':'10026',
        'domain':'',
        'xd	https':'//xs.sogou.com/static/jump.html',
        'token': self.get_token()
    }

    def get_token(self):
        taken = ''
        for i in range(8):
            ctx = execjs.compile(
                'function a() { return Math.floor(65536 * (1 + Math.random())).toString(16).substring(1)}')

            data = ctx.call('a')
            taken += data

        return taken

    def login_step1(self):
        url = 'https://account.sogou.com/web/login'
        response = self.session.post(url, headers=self.headers, data=self.data, verify=False)

    # def login_step2(self):
    #     pass
    #
    # def login_step3(self):
    #     pass

    def login_veri(self):
        res4 = self.session.get('https://xs.sogou.com/api/pc/v1/user/info', headers=self.headers, verify=False)

        return res4.text

    def run(self):
        self.login_step1()
        response = self.login_veri()
        if re.findall(r'成功', response):
            print(response)
            print('登录成功')
        else:
            print('登录失败')


if __name__ == '__main__':
    duoduo = duoduo_Read('username', 'password')
    duoduo.run()

# params = {
#     'status': '0',
#     'api': '%2Fweb%2Flogin',
#     'cost': '679',
#     'limit': '6000',
#     '_': '1550550725976',
#     'appid': '10026',
#     'pt': 'xs.sogou.com',
#     'path': '/',
#     'fr': '',
#     'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
#     'ls': '1_1'
# }
# session = requests.session()
# res1 = session.get('https://account.sogou.com/static/js/lib/jquery-1.12.0.min.js ', headers=headers, verify=False)
# res2= session.get('https://xs.sogou.com/static/jump.html?status=0&needcaptcha=0&msg=', headers=headers, verify=False)
# res = session.get('https://account.sogou.com/web/slowinfo', params=params, headers=headers, verify=False)
# res3 = session.get('https://xs.sogou.com/api/pc/v1/user/info', headers=headers, verify=False)
