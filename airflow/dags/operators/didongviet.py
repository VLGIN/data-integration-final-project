def crawlDiDongViet():
    import requests
    import pandas as pd

    from bs4 import BeautifulSoup
    from pymongo import MongoClient
    from datetime import date, timedelta

    def get_item_info(url):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88."
                          "0.4324.182 Safari/537.36"}
        webpage = requests.get(url, headers=headers).text
        soup = BeautifulSoup(webpage, "html.parser")
        try:
            name = soup.find("div", {"class": "heading-title"}).text
            price_tag = soup.find("span", {"class": "price"})
            price = soup.find("span", {"class": "price"}).text
        except:
            return []
        try:
            img_url = soup.find("img", {"class": "fotorama__img"}).src
        except:
            img_url = None
        detail = {}
        detail["name"] = name
        detail["url"] = url
        detail["price"] = price
        detail["img_url"] = img_url
        technical_detail = soup.find("div", {"id": "product-attribute-specs-table"})
        li_list = technical_detail.find_all("li")
        for each in li_list:
            title_p = each.find("p")
            detail_div = each.find("div")
            detail[title_p.text] = detail_div.text

        try:
            list_results = []
            colors = soup.find("div", {"class": "control-option"})
            label_list = colors.find_all("label")
            for each in label_list:
                detail["color"] = each.find("span", {"class": "name"}).text
                detail["price"] = each.find("span", {"class": "price"}).text
                list_results.append(detail.copy())
            return list_results
        except Exception as e:
            detail["color"] = None
            return [detail]

    def get_link(p):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88."
                          "0.4324.182 Safari/537.36"}
        data = requests.get("https://didongviet.vn/dien-thoai?total=167&ajax=1&limit=167&more=0&p={}&_=".format(p),
                            headers=headers).json()
        html = data["products_list"]
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a", {"class": "product-item-link"})
        results = [item["href"] for item in links]
        return results

    urls = []
    for i in range(15):
        urls += get_link(i)

    list_results = []
    for url in urls:
        list_results += get_item_info(url)

    df = pd.DataFrame(list_results)
    df.drop_duplicates(inplace=True)
    df.rename(columns={"Bộ nhớ trong": "bộ nhớ"}, inplace=True)
    date_save = date.today()
    df["date"] = [str(date_save)]*df.shape[0]
    df.reset_index(drop=True, inplace=True)
    data_dict = df.to_dict("records")
    client = MongoClient("mongodb+srv://data-integration:data-integration@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration2"]
    collec = db["didongviet"]
    collec.insert_many(data_dict)
