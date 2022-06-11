import requests
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

threads = []
result = []

def call_api(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers = headers).json()
    time.sleep(2)
    return r

def crawlTiki():
    with ThreadPoolExecutor(max_workers=10) as executor:
        start = time.time()
        temp = 0

        for page in range(1,10):
            url = 'https://tiki.vn/api/personalish/v1/blocks/listings?limit=100&2&category=1789&page={page}&urlKey=dien-thoai-may-tinh-bang'.format(page = page)
            threads.append(executor.submit(call_api, url))

        with open('tiki.json', 'w') as f:
            for task in as_completed(threads):
                try:
                    if len(task.result()['data']) != 0 :
                        items = task.result()['data']
                        for item in items:
                            json.dump(item,f)
                            f.write('\n')
                        
                except:
                    print(task.result())


        print(f'Crawler took {time.time()-start}s')

if __name__ =='__main__':
    crawlTiki()