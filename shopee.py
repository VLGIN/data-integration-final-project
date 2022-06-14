import requests
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os


def call_api(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url).json()
    time.sleep(2)
    return r
    
def crawlShopee():
    threads = []
    result = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        start = time.time()
        temp = 0

        for page in range(30):
            url = 'https://shopee.vn/api/v4/search/search_items?&by=relevancy&limit=100&match_id=11036031&newest={page}&order=desc&page_type=search'.format(page = page*100)
            threads.append(executor.submit(call_api, url))

        with open('shopee.json', 'w') as f:
            for task in as_completed(threads):
                try:
                    if len(task.result()['items']) != 0 :
                        items = task.result()['items']
                        for item in items:
                            json.dump(item,f)
                            f.write('\n')
                        
                except Exception as e:
                    print(e)

        df = pd.read_json('shopee.json', lines= True)
        df.to_csv('shopee.csv', index = False)
        os.remove('shopee.json')
        print(f'Crawler took {time.time()-start}s')

if __name__ =='__main__':
    crawlShopee()