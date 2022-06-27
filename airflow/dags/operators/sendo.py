def crawlSendo():
    import requests 
    import time
    import requests
    import pandas as pd
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import json
    import os
    def call_api(url):
        r = requests.get(url).json()
        time.sleep(2)
        return r
    threads = []
    result = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        start = time.time()
        temp = 0

        for page in range(25):
            url = 'https://recommend-api.sendo.vn/web/listing/recommend/internal?p={page}&s=100&cate_path=cong-nghe&sort_type=vasup_desc'.format(page = page)
            threads.append(executor.submit(call_api, url))

        with open('sendo.json', 'w') as f:
            for task in as_completed(threads):
                try:
                    if len(task.result()['data']) != 0 :
                        items = task.result()['data']
                        for item in items:
                            try:
                                i = item['item']
                                json.dump(i, f)
                                f.write('\n')
                            except:
                                pass
                        
                except Exception as e:
                    print(e)

        df = pd.read_json('sendo.json', lines= True)
        df.to_csv('/opt/airflow/dags/sendo.csv', index = False)
        os.remove('sendo.json')
        print(f'Crawler took {time.time()-start}s')

if __name__ == '__main__':
    crawlSendo()