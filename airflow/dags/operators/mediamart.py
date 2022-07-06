def crawl_mediaMart():
    import requests
    from bs4 import BeautifulSoup
    import json
    import pandas as pd
    import time
    from datetime import date, timedelta
    from pymongo import MongoClient

    def crawl_item(url_input):
        try:
            url = 'https://mediamart.vn' + url_input
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
                'X-Requested-With': 'XMLHttpRequest',
            }
            r = requests.get(url, headers=headers)
            data = {}
            soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), 'html.parser')
            data["name"] = soup.find_all("div", class_="pdetail-name")[0].text.split('\n')[1]
            try:
                data["img_url"] = soup.find("div", {"class": "pdetail-slideproduct owl-loaded owl-drag"}).find("img").src
            except:
                data["img_url"] = None
            x = 0
            key = ''
            for tr in soup.find_all('td'):
                if (len(tr.get_text()) > 0):
                    if (x % 2) == 0:
                        key = tr.get_text()
                    else:
                        data[key] = tr.get_text()
                    x = x + 1
            data["price"] = soup.find("div", class_="pdetail-price-box").text
            data["url"] = url
            time.sleep(10)
            return data
        except:
            pass

    data = []
    df = pd.read_csv('/opt/airflow/dags/mediamart.csv')  # duong dan file csv
    url = 'https://mediamart.vn/smartphones'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'X-Requested-With': 'XMLHttpRequest',
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    for div in soup.find_all("div", class_="col-6 col-md-3 col-lg-3"):
        data.append(crawl_item(div.find("a", href=True)['href']))
    pd.concat([pd.DataFrame(data), df], ignore_index=True)

    date_save = date.today()
    df["date"] = [str(date_save)] * df.shape[0]
    df.reset_index(inplace=True)

    data_dict = df.to_dict('records')
    client = MongoClient("mongodb+srv://longgiang:longgiang2010@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration"]
    collec = db["mediamart"]

    collec.insert_many(data_dict)
