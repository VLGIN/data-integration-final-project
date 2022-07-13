def crawlShopee():
    from pydoc import describe
    import requests
    import pandas as pd
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import json
    import os
    import ast
    # from api import call_shopee_api, get_detail_shopee
    import sys
    from pymongo import MongoClient
    from datetime import date

    def call_shopee_api(url):
        r = requests.get(url).json()
        time.sleep(3)
        return r

    def get_detail_shopee(url, idx):
        try:
            r = requests.get(url)
            r = r.json()['data']['attributes']
            time.sleep(2)
        except:
            # print('bị chặn')
            r = None
        return r, idx

    threads = []
    result = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        start = time.time()
        temp = 0

        for page in range(30):
            url = 'https://shopee.vn/api/v4/search/search_items?&by=relevancy&limit=100&match_id=11036031&newest={page}&order=desc&page_type=search'.format(
                page=page * 100)
            threads.append(executor.submit(call_shopee_api, url))
        with open('shopee.json', 'w') as f:
            for task in as_completed(threads):
                try:
                    if len(task.result()['items']) != 0:
                        items = task.result()['items']
                        for item in items:
                            json.dump(item, f)
                            f.write('\n')

                except Exception as e:
                    print('Bị chặn mất rùi :)')

    df = pd.read_json('shopee.json', lines=True)
    try:
        old = pd.read_csv('old.csv')
        df = pd.concat([df, old])
        df = df.drop_duplicates(subset=['itemid', 'shopid'])
    except:
        pass
    df.to_csv('shopee.csv', index=False)
    os.remove('shopee.json')

    with open('shopee.json', 'w') as f:
        df = pd.read_csv('shopee.csv')['item_basic'].tolist()
        for line in df:
            try:
                json.dump(ast.literal_eval(line), f)
                f.write('\n')
            except:
                pass
    df = pd.read_json('shopee.json', lines=True)
    df = df.drop_duplicates(subset=['itemid'])
    threads = []
    df = df[['itemid', 'shopid', 'price']]
    with ThreadPoolExecutor(max_workers=20) as executor:
        length_product = len(df)
        for row in range(length_product):
            try:
                itemid = df.loc[row, 'itemid']
                shopid = df.loc[row, 'shopid']
            except:
                print(row)
            url = 'https://shopee.vn/api/v4/item/get?itemid={itemid}&shopid={shopid}'.format(itemid=itemid,
                                                                                             shopid=shopid)
            threads.append(executor.submit(get_detail_shopee, url, row))

        for task in as_completed(threads):
            try:
                attributes, row = task.result()
                sys.stdout.write('\rLoading... %.2f percent' % (100 * row / length_product))
                if attributes is not None:
                    df.loc[row, 'attributes'] = str(attributes)
                    temp = pd.DataFrame(attributes)
                    # print(temp.columns)
                    names = temp['name']
                    values = temp['value']
                    s = {name: value for name, value in zip(names, values)}
                    temp = pd.DataFrame(s, index=[0])
                    for col in temp.columns:
                        df.loc[row, col] = temp.loc[0, col]
            except Exception as e:
                print(e)
    shopee = df[df['attributes'].notnull()]
    shopee = shopee.drop('attributes', axis=1)
    shopee = shopee.dropna(thresh=int(len(shopee.columns) * 0.8))
    old = df[df['attributes'].isnull()]
    old = old.drop('attributes', axis=1)

    shopee["date"] = [str(date.today())]*shopee.shape[0]
    shopee.reset_index(inplace=True)
    data_dict = shopee.to_dict('records')

    client = MongoClient("mongodb+srv://data-integration:data-integration@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration"]
    collec = db["shopee"]

    collec.insert_many(data_dict)
    # shopee.to_csv('shopee.csv', index=False)
    # old.to_csv('old.csv', index=False)
    os.remove('shopee.json')
    sys.stdout.write('\r Crawler took %.2f seconds' % (time.time() - start))


if __name__ == '__main__':
    crawlShopee()