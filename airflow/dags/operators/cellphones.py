def crawlCellphones():
    import requests
    import time
    import pandas as pd

    from bs4 import BeautifulSoup
    from pymongo import MongoClient
    from datetime import date, timedelta
    from tqdm import tqdm

    base_url = "https://cellphones.com.vn/lapi/LoadMoreProductCate/index/?page={" \
               "}&id=3&order=view_count2&dir=desc&fearture=flashsale_samsung "

    def get_detail(url):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88."
                          "0.4324.182 Safari/537.36"}
        webpage = requests.get(url, headers=headers).text
        soup = BeautifulSoup(webpage, 'html.parser')
        try:
            price_tag = soup.find("div", {"class": "box-info__box-price"})
            price = price_tag.find("p", {"class": "special-price"}).text
        except:
            return {}
        name_tag = soup.find("div", {"class": "box-name__box-product-name"})
        name = name_tag.find("h1").text
        technical_detail = soup.find("div", {"id": "technicalInfoModal"})
        try:
            img_container = soup.find("div", {"class": "box-ksp"})
            img_url = img_container.find("img").src
        except:
            img_url = None
        detail = {"price": price,
                  "name": name,
                  "img_url": img_url}
        tr_list = technical_detail.find_all("tr")
        try:
            for tr in tr_list:
                th_list = tr.find_all("th")
                detail[th_list[0].text.strip().lower()] = th_list[1].text.strip().lower()
                detail["url"] = url
        except:
            return []

        color_options = soup.find("ul", {"id": "configurable_swatch_color"})
        print(color_options)
        if color_options is not None:
            detail_list = []
            options = color_options.find_all("li")
            for each in options:
                try:
                    content = each.find("p")
                    detail["color"] = content.find("strong").text.strip().replace("\n", "")
                    detail["price"] = content.find("span").text
                except:
                    continue
                try:
                    detail["img_url"] = content.find("img")["data-src"]
                except:
                    detail["img_url"] = None
            detail_list.append(detail.copy())
            return detail_list
        detail["color"] = None
        return detail

    urls = []

    for i in tqdm(range(20)):
        try:
            url = base_url.format(i)
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                              "/88.0.4324.182 Safari/537.36"}
            product_list = requests.get(url, headers=headers).json()

            urls += [item["url"] for item in product_list]
        except:
            break

    product_detail = []

    for url in tqdm(urls):
        detail = get_detail(url)
        if isinstance(detail, list):
            product_detail += detail
        else:
            product_detail.append(detail)

    df = pd.DataFrame(product_detail)
    df.rename(columns={"dung lượng ram": "ram", "bộ nhớ trong": "bộ nhớ"}, inplace=True)
    df.drop_duplicates(inplace=True)
    client = MongoClient("mongodb+srv://longgiang:longgiang2010@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration2"]
    collec = db["cellphones"]

    date_save = date.today()
    df["date"] = [str(date_save)] * df.shape[0]
    df.reset_index(drop=True, inplace=True)
    data_dict = df.to_dict("records")
    collec.insert_many(data_dict)


if __name__ == "__main__":
    crawlCellphones()
