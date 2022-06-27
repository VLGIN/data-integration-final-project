def crawlTiki():
    import requests
    import pandas as pd
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import json
    import os
    import sys

    def call_api(url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers = headers).json()
        time.sleep(2)
        return r

    def get_detail_tiki(url, idx):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get(url, headers = headers)
            spec = r.json()['specifications']
            description = r.json()['description']
            time.sleep(2)
            
        except Exception as e:
            print(e)
            spec = 'None'
            description = 'None'
        return spec, description, idx

    threads = []
    result = [] 
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

        df = pd.read_json('tiki.json', lines= True)
        

        threads = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            length_product = len(df)
            for row in range(length_product):
                try:
                    itemid = df.loc[row, 'id']
                except:
                    print(row)
                url = 'https://tiki.vn/api/v2/products/{itemid}'.format(itemid = itemid)
                threads.append(executor.submit(get_detail_tiki, url, row))

            for task in as_completed(threads):
                spec, description, row = task.result()
                df.loc[row, 'description'] = str(description)
                df.loc[row, 'specifications'] = str(spec)
                sys.stdout.write('\rLoading... %.2f percent' %(100*row/length_product))                

        df.to_csv('/opt/airflow/dags/tiki.csv', index = False)
        os.remove('tiki.json')
        sys.stdout.write('\rCrawler took %.2f seconds' %(time.time()-start))

if __name__ =='__main__':
    crawlTiki()