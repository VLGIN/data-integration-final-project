url_phone = "https://cellphones.com.vn/lapi/LoadMoreProductCate/index/?page={" \
            "}&id=3&order=view_count2&dir=desc&fearture=flashsale_samsung "
url_laptop = "https://cellphones.com.vn/lapi/LoadMoreProductCate/index/?page={" \
             "}&id=380&order=view_count2&dir=desc&fearture=flashsale_laptop "

def crawlCellphones():
    import requests
    import time
    import pandas as pd

    from bs4 import BeautifulSoup
    from pymongo import MongoClient
    from datetime import date
    from tqdm import tqdm

    base_url = "https://cellphones.com.vn/lapi/LoadMoreProductCate/index/?page={" \
                "}&id=3&order=view_count2&dir=desc&fearture=flashsale_samsung "

    def get_detail(url):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        webpage = requests.get(url, headers=headers).text
        time.sleep(0.5)
        soup = BeautifulSoup(webpage, 'html.parser')
        technical_detail = soup.find("div", {"id": "technicalInfoModal"})
        detail = {}
        tr_list = technical_detail.find_all("tr")
        for tr in tr_list:
            th_list = tr.find_all("th")
            detail[str(th_list[0])[4:-5]] = str(th_list[1])[4:-5]
        return detail

    urls = []

    for i in range(200):
        try:
            url = base_url.format(i)
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
            product_list = requests.get(url, headers=headers).json()
            time.sleep(0.5)

            urls += [item["url"] for item in product_list]
        except:
            break

    product_detail = []

    for url in tqdm(urls):
        detail = get_detail(url)
        product_detail.append(detail)

    df = pd.DataFrame(product_detail)
    print(df)
    client = MongoClient("mongodb+srv://longgiang:longgiang2010@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration"]
    collec = db["cellphones"]

    df["date"] = [str(date.today())] * df.shape[0]
    df.reset_index(inplace=True)
    data_dict = df.to_dict("records")
    collec.insert_many(data_dict)


if __name__ == "__main__":
    crawlCellphones()
