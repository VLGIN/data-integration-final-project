def crawlPhongVu():
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import time
    from pymongo import MongoClient
    from datetime import date, timedelta

    devices = ['iphone-scat.01-N004-01', 'samsung-scat.05-N001-02', 'asus-scat.05-N001-12',
               'xiaomi-scat.05-N001-17']
    # devices = ['iphone-scat.01-N004-01']

    def get_detail(sku):
        url = "https://public-setting.tekoapis.com/api/v1/sku-details?sku={}&terminalCode=phongvu&location=".format(sku)
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88."
                          "0.4324.182 Safari/537.36"}
        detail = requests.get(url, headers=headers).json()
        time.sleep(0.5)
        productinfo = detail["data"]["productInfo"]
        if "error" in detail.keys():
            return {"error": True}
        return_dict = {}
        return_dict["name"] = productinfo["name"]
        return_dict["img_url"] = productinfo["imageUrl"]
        return_dict["url"] = f"https://phongvu.vn/{productinfo['canonical']}?sku={sku}"
        return_dict["Thương hiệu"] = productinfo["brand"]["name"]
        return_dict["price"] = detail["data"]["prices"][0]["latestPrice"]
        product_detail = detail["data"]["productDetail"]["attributeGroups"]
        for item in product_detail:
            return_dict[item["name"].strip().lower()] = item["value"].strip().lower()
        return return_dict

    final_data = []
    for i in range(len(devices)):
        # url = "https://phongvu.vn/" + devices[i]
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88."
                          "0.4324.182 Safari/537.36"}
        # webpage = requests.get(url, headers=headers).text
        # time.sleep(0.5)
        # soup = BeautifulSoup(webpage, 'html.parser')
        # data = soup.find_all('div', {"class": "css-13w7uog"})
        url = "https://discovery.tekoapis.com/api/v1/search"
        json_data = {
            'filter': {
                'priceLte': '0',
                'priceGte': '0',
                'categories': [
                    devices[i].split(".")[-1],
                ],
                'hasPromotions': False,
                'attributes': [],
            },
            'pagination': {
                'itemsPerPage': '100',
            },
            'query': '',
            'sorting': {
                'sort': 'SORT_BY_SCORE',
                'order': 'ORDER_BY_DESCENDING',
            },
            'returnFilterable': [
                'FILTER_TYPE_BRAND',
                'FILTER_TYPE_PRICE',
                'FILTER_TYPE_ATTRIBUTE',
                'FILTER_TYPE_CLEARANCE',
            ],
            'terminalCode': 'phongvu',
            'block': {
                'blockId': '1011',
            },
        }
        skus = []
        response_data = requests.post(url, headers=headers, json=json_data).json()
        for each in response_data["result"]["products"]:
            try:
                skus.append(each["productInfo"]["sku"])
            except:
                pass
        print(len(skus))
        # for each_item in data:
        #     try:
        #         a_tag = each_item.find('a', {"class": "css-cbrxda"})['href']
        #         sku = a_tag.split("=")[-1]
        #         print(sku)
        #         skus.append(sku)
        #     except:
        #         pass
        for sku in skus:
            sku = int(sku)
            candidate = [sku-2, sku-1, sku, sku+1, sku+2]
            candidate = [str(item) for item in candidate]
            for each in candidate:
                try:
                    detail = get_detail(each)
                except:
                    continue
                if "error" in detail:
                    continue
                final_data.append(detail)

    df = pd.DataFrame(final_data)
    df.rename(columns={"dung lượng (rom)": "bộ nhớ"}, inplace=True)
    df.drop_duplicates(inplace=True)
    print(df)
    client = MongoClient("mongodb+srv://data-integration:data-integration@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration2"]
    collec = db["phongvu"]

    date_save = date.today()
    df["date"] = [str(date_save)] * df.shape[0]
    df.rename(columns={"màu sắc": "color"}, inplace=True)
    df.reset_index(drop=True, inplace=True)
    data_dict = df.to_dict("records")
    collec.insert_many(data_dict)


if __name__ == "__main__":
    crawlPhongVu()
