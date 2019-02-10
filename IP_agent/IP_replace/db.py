import pymongo
import random

class MongoDB():
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['proxypool']
        self.proxies = self.db['proxies']
        self.proxies.ensure_index('proxy',unique=True)

    def insert(self,proxy):
        try:
            self.proxies.insert_one(proxy)
        except pymongo.errors.DuplicatekeyError:
            pass
    def delete(self,proxy):
        self.proxies.delete_one(proxy)

    def update(self,proxy, value):
        self.proxies.update_one(proxy, {'$set': value})

    def get(self,count):
        proxies = self.proxies.find({},limit=count)

        return [proxy['proxy']for proxy in proxies]

    def get_random_proxy(self):
        proxies = self.proxies.find({})

        return random.choice([proxy['proxy'] for proxy in proxies])

    def get_fastest_proxy(self):
        proxies = self.proxies.find({}).sort('delay')

        return [proxy['proxy'] for proxy in proxies][0]

