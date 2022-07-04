def crawlCellphones():
    import requests
    import time
    import pandas as pd

    from bs4 import BeautifulSoup
    from pymongo import MongoClient
    from datetime import date
    from tqdm import tqdm

    base_url = "https://didongthongminh.vn/index.php?module=products&view=cat&task=fetch_pages&raw=1&pagecurrent={}&filter=&cid=1&order="

    def get_detail(url):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        webpage = requests.get(url, headers=headers).text
        time.sleep(0.5)
        soup = BeautifulSoup(webpage, 'html.parser')
        technical_detail = soup.find("table", {"class": "charactestic_table_detail"})
        detail = {}
        try:

            tr_list = technical_detail.find_all("tr", {"class": True})
            for tr in tr_list:
                try:
                    td_list = tr.find_all("td")
                    print(td_list[0].text)
                    detail[td_list[0].text] = td_list[1].text
                except:
                    detail= {}
                    pass
        except:
            pass
        return detail

    urls = []

    for i in range(50):
        try:
            url = base_url.format(i*25)
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
            webpage = requests.get(url, headers=headers).json()['content']
            time.sleep(0.5)
            soup = BeautifulSoup(webpage, 'html.parser')
            a_list = soup.find_all('a', {'href': True})

            urls += [item["href"] for item in a_list]
            print("ok")
        except:
            break

    product_detail = []
    urls = list(set(urls))
    for url in tqdm(urls):
        detail = get_detail(url)
        if len(list(detail.keys())) > 0:
            product_detail.append(detail)

    df = pd.DataFrame(product_detail)
    print(df)
    client = MongoClient("mongodb+srv://longgiang:longgiang2010@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration"]
    collec = db["didongthongminh"]

    df["date"] = [str(date.today())] * df.shape[0]
    df.reset_index(inplace=True)
    data_dict = df.to_dict("records")
    collec.insert_many(data_dict)


if __name__ == "__main__":
    crawlCellphones()
