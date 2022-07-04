def crawlPhongVu():
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import time
    from pymongo import MongoClient
    from datetime import date

    devices = ['iphone-scat.01-N004-01', 'samsung-scat.05-N001-02', 'asus-scat.05-N001-12',
               'xiaomi-scat.05-N001-17']
    # devices = ['iphone-scat.01-N004-01']

    def get_detail(sku):
        url = "https://public-setting.tekoapis.com/api/v1/sku-details?sku={}&terminalCode=phongvu&location=".format(sku)
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        detail = requests.get(url, headers=headers).json()
        time.sleep(0.5)
        productinfo = detail["data"]["productInfo"]
        if "error" in detail.keys():
            return {"error": True}
        return_dict = {}
        return_dict["name"] = productinfo["name"]
        return_dict["Thương hiệu"] = productinfo["brand"]["name"]
        return_dict["price"] = detail["data"]["prices"][0]["latestPrice"]
        product_detail = detail["data"]["productDetail"]["attributeGroups"]
        for item in product_detail:
            return_dict[item["name"]] = item["value"]
        return return_dict

    final_data = []
    for i in range(len(devices)):
        url = "https://phongvu.vn/" + devices[i]
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        webpage = requests.get(url, headers=headers).text
        time.sleep(0.5)
        soup = BeautifulSoup(webpage, 'html.parser')
        data = soup.find_all('div', {"class": "css-13w7uog"})
        skus = []
        for each_item in data:
            try:
                a_tag = each_item.find('a', {"class": "css-cbrxda"})['href']
                sku = a_tag.split("=")[-1]
                print(sku)
                skus.append(sku)
            except:
                pass
        for sku in skus:
            detail = get_detail(sku)
            if "error" in detail:
                pass
            final_data.append(detail)

    df = pd.DataFrame(final_data)
    print(df)
    client = MongoClient("mongodb+srv://longgiang:longgiang2010@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration"]
    collec = db["phongvu"]

    df["date"] = [str(date.today())] * df.shape[0]
    df.reset_index(inplace=True)
    data_dict = df.to_dict("records")
    collec.insert_many(data_dict)


if __name__ == "__main__":
    crawlPhongVu()
