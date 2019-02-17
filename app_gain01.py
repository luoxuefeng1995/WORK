import requests
import json
from queue import Queue
from multiprocessing.pool import ThreadPool
from pymysql import connect
import pymysql

class Fruit_Cook(object):
    def __init__(self, data, url):
        self.headers = {
            'user-agent': 'Mozilla/5.0(Linux;Android 4.4.2; SM-G955F Build/JLS36C) AppleWebKit/537.36 (KHTML,like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
            'version': '6916.2',
            'client': '4',
            'device': 'SM-G955F',
            'sdk': '19,4.4.2',
            'imei': '355757011801970',
            'channel': 'zhuzhan',
            'mac': '80:C5:F2:D2:41:FF',
            'resolution': '1280*720',
            'dpi': '1.5',
            'android-id': '180c5f2d241ff405',
            'pseudo-id': 'f2d241ff405180c5',
            'brand': 'samsung',
            'scale': '1.5',
            'timezone': '28800',
            'language': 'zh',
            'cns': '3',
            'carrier': 'CMCC',
            'imsi': '460071801972422',
            'reach': '1',
            'newbie': '1',
            'lon': '112.561432',
            'lat': '29.975866',
            'cid': '421000',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Accept-Encoding': 'gzip,deflate',
            'Connection': 'Keep-Alive',
            'Cookie': 'duid = 58526885',
            'Host': 'api.douguo.net',
            'Content-Length': '68',

        }
        self.data = data
        self.url = url
        self.Th = ThreadPool()
        self.Q1 = Queue()
        self.Q2 = Queue()
        self.count = 0
        self.db_config = {
            'host': '127.0.0.1',
            'user': 'admin',
            'password': 'Root110qwe',
            'db': 'total_detail',
            # 'charset': 'utf-8'
        }
        self.conn1 = connect(**self.db_config)
        self.conn2 = connect(**self.db_config)

    def send_req01(self):

        response = requests.post(url=self.url, headers=self.headers, data=self.data)

        return response

    def parse_resp_L1(self,response):
        data_list = []
        total_data = json.loads(response.text)
        data01 = total_data['result']['cs'][1:]
        for vege in data01:
            data = {}
            total_cs = vege['name']
            data['total_cs'] = total_cs
            vege_cs = vege['cs']
            for i in vege_cs:
                data = data.copy()
                vege_cs_name = i['name']
                data['vege_cs_name'] = vege_cs_name
                vege_de_cs = i['cs']
                for j in vege_de_cs:
                    data = data.copy()
                    vege_name = j['name']
                    data['vege_name'] = vege_name
                    try:
                        with self.conn1.cursor() as cursor:
                            sql = "INSERT INTO total_cs (totalcs, vegecsname, vegename) VALUES(%s,%s,%s)"
                            cursor.execute(sql, (data['total_cs'], data['vege_cs_name'], data['vege_name']))
                            self.conn1.commit() #提交数据
                    except pymysql.err.IntegrityError:
                        pass
                    data_list.append(data)

        return data_list

    def send_req02(self, data, vege_name):

            i = 0#只爬取前三页的内容,若要爬取更多内容改变判断条件即可
            while True:
                tem_data = {}
                url = 'http://api.douguo.net/recipe/s/{}/20'.format(i)
                response = requests.post(url=url, headers=self.headers, data=data).text
                i += 20
                tem_data['vege_name'] = vege_name
                tem_data['response'] = response
                self.Q1.put(tem_data)
                if i == 60:
                    break
            # break

    def parse_resp_L2(self):
        while True:
            tem_data = self.Q1.get()
            response = tem_data['response']
            response = json.loads(response)
            total_data = response['result']['list']
            for i in total_data:
                data = {}
                data['vege_name'] = tem_data['vege_name']
                data['type'] = i['type']
                j = i['r']
                data['id'] = j['id']
                data['name'] = j['n']
                data['cook_df'] = j['cook_difficulty']
                data['cook_time'] = j['cook_time']
                data['rate'] = j['rate']

                self.count += 1 #记录数据条数
                self.Q2.put(data)
                print(data, self.count)
            self.Q1.task_done()
            if self.Q1.qsize() == 0:
                break
    def save_mysql(self):
        while True:
            data = self.Q2.get()
            pt_list = []
            pt = (data['vege_name'], data['type'], data['id'], data['name'], data['cook_df'], data['cook_time'], data['rate'])
            pt_list.append(pt)
            try:
                with self.conn2.cursor() as cursor:
                    sql = "INSERT INTO detaildata (vege_name, type, id_number,name, cook_df, cook_time, rate) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                    cursor.executemany(sql, pt_list)
                    self.conn2.commit()  # 提交数据
            except pymysql.err.IntegrityError:
                print('重复条目')
            self.Q2.task_done()
            if self.Q2.qsize() == 0:
                break
    def run(self):

        pool =ThreadPool(50)
        response = self.send_req01()
        response = self.parse_resp_L1(response)
        for i in response:
            vege_name = i['vege_name']
            data = {
                'client': '4',
                '_session': '1550294408077355757011801970',
                'keyword': vege_name,
                'order': '0',
                '_vs': '400'
            }
            pool.apply_async(self.send_req02, args=(data, vege_name))
            pool.apply_async(self.parse_resp_L2)
        pool.close()
        pool.join()
        self.save_mysql()

if __name__ == '__main__':
    data = {
        'client': '4',
        '_session': '1550294408077355757011801970',
        'v': '1503650468',
        '_vs': '2305'
    }
    url = 'http://api.douguo.net/recipe/flatcatalogs'
    douguo = Fruit_Cook(data, url)

    douguo.run()
