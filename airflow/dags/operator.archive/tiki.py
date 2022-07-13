def crawlTiki():
    import requests
    import pandas as pd
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import json
    import os
    import sys
    from pymongo import MongoClient
    from datetime import date

    def call_api(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers).json()
        time.sleep(2)
        return r

    def get_detail_tiki(url, idx):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get(url, headers=headers)
            spec = r.json()['specifications'][0]['attributes']
            time.sleep(2)

        except Exception as e:
            print(e)
            spec = 'None'
        return spec, idx

    threads = []
    result = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        start = time.time()
        temp = 0

        for page in range(1, 10):
            url = 'https://tiki.vn/api/personalish/v1/blocks/listings?limit=100&2&category=1789&page={page}&urlKey=dien-thoai-may-tinh-bang'.format(
                page=page)
            threads.append(executor.submit(call_api, url))

        with open('tiki.json', 'w') as f:
            for task in as_completed(threads):
                try:
                    if len(task.result()['data']) != 0:
                        items = task.result()['data']
                        for item in items:
                            json.dump(item, f)
                            f.write('\n')
                except:
                    print(task.result())

        df = pd.read_json('tiki.json', lines=True)

        df = df[['price', 'id']]
        threads = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            length_product = len(df)
            for row in range(length_product):
                try:
                    itemid = df.loc[row, 'id']
                except:
                    print(row)
                url = 'https://tiki.vn/api/v2/products/{itemid}'.format(itemid=itemid)
                threads.append(executor.submit(get_detail_tiki, url, row))

            for task in as_completed(threads):
                spec, row = task.result()
                if spec is not None:
                    try:
                        temp = pd.DataFrame(spec)

                        names = temp['name']
                        values = temp['value']

                        s = {name: value for name, value in zip(names, values)}
                        temp = pd.DataFrame(s, index=[0])
                        for col in temp.columns:
                            df.loc[row, col] = temp.loc[0, col]
                        # df.loc[row, 'specifications'] = str(spec)
                    except:
                        pass
                sys.stdout.write('\rLoading... %.2f percent' % (100 * row / length_product))
        df = df.dropna(axis=1, thresh=int(len(df) * 0.5))
        # df.to_csv('tiki.csv', index=False)
        df["date"] = [str(date.today())]*df.shape[0]
        df.reset_index(inplace=True)
        data_dict = df.to_dict('records')

        client = MongoClient("mongodb+srv://data-integration:data-integration@cluster0.npw0zsg.mongodb.net/")
        db = client["data-integration"]
        collec = db["tiki"]

        collec.insert_many(data_dict)
        try:
            os.remove('tiki.json')
        except:
            pass
        sys.stdout.write('\rCrawler took %.2f seconds' % (time.time() - start))


if __name__ == '__main__':
    crawlTiki()
