from multiprocessing import Process
from .API import api
from .IP_get.crawler import crawler, check

def run_proxypool():
    api_process = Process(target=api)
    crawler_process = Process(target=crawler)
    check_process = Process(target=check)

    api_process.start()
    crawler_process.start()
    check_process.start()

    api_process.join()
    crawler_process.join()
    check_process.join()
