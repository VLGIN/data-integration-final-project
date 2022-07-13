def clean_data():
    import pandas as pd
    import re
    import json

    from pymongo import MongoClient
    from datetime import date, timedelta

    def process_name(tex):
        tex = str(tex)
        # punctuations = "\+/-.,{}|();:\"'` []"
        with open("/opt/airflow/dags/data/brand_name") as f:
            brand_name = f.read().splitlines()
        with open("/opt/airflow/dags/data/color") as f:
            colors = f.read().splitlines()
        with open("/opt/airflow/dags/data/distraction.txt") as f:
            distraction = f.read().splitlines()
        tex = re.sub("\n", "", tex).lower()

        # remove detail
        tex = re.sub("[0-9]+ gb", "", tex)
        tex = re.sub("[0-9]+gb", "", tex)
        tex = re.sub("[0-9]+g", "", tex)
        tex = re.sub("[0-9]+ g", "", tex)
        tex = re.sub("[0-9]+tb", "", tex)
        tex = re.sub("[0-9]+ tb", "", tex)
        tex = re.sub("điện thoại", "", tex)
        tex = re.sub("[\+\\\.{}\-()/|]", "", tex)
        tex = re.sub(" i ", "", tex)
        tex = re.sub("Chính Hãng vna".lower(), "", tex)
        tex = re.sub("Chính Hãng".lower(), "", tex)
        tex = re.sub("di động", "", tex)
        tex = re.sub("điện thoại", "", tex)

        for item in brand_name:
            tex = re.sub(item, "", tex)
        for item in distraction:
            tex = re.sub(item, "", tex)
        for item in colors:
            tex = re.sub(item, "", tex)
        tex = re.sub(" +", " ", tex)
        tex = tex.strip()
        # if tex[-3:] == "vna":
        #     tex = " ".join(tex.split(" ")[:-1])

        word_list = tex.split(" ")
        if "vna" in word_list[-1] or "vn/a" in word_list[-1]:
            del word_list[-1]
        if word_list[-1] == "-":
            del word_list[-1]

        return " ".join(word_list)

    def process_text(tex):
        tex = str(tex)
        tex = re.sub("\n", "", tex)
        tex = tex.strip().lower()
        return tex

    def generic_format(df):
        df.rename(columns={item: re.sub("\n", "", str(item)).strip().lower() for item in list(df)}, inplace=True)
        list_column = list(df)
        for col in list_column:
            df[col] = df[col].apply(process_text)
        return df

    # def preprocess(df):
    #     df['name'] = df['name'].apply(process_name())
    #     df.reset_index(inplace=True)
    #
    #     for index, row in df.iterrows():
    #         if row["Mã sản phẩm"] is None:
    #             row["Mã sản phẩm"] = row["name"]
    #         elif row["name"] is None:
    #             row["name"] = row["Mã sản phẩm"]
    #     return df

    def preprocess(df):
        df = generic_format(df)
        df["name"] = df["name"].apply(process_name)
        df.rename(columns={item: str(item).strip().lower() for item in list(df)}, inplace=True)
        return df

    coll = ["cellphones", "thegioididong", "didongthongminh", "mediamart", "phongvu", "didongviet"]

    client = MongoClient("mongodb+srv://data-integration:data-integration@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration2"]
    with open("/opt/airflow/dags/data/color") as f:
        color_list = f.read().splitlines()

    def extract_color(sent):
        sent = sent.lower()
        for item in color_list:
            if item in sent:
                return item
        return None

    with open("/opt/airflow/dags/data/mapping_color.json") as f:
        mapping_color = json.load(f)

    reverse_mapping_color = {}
    for item in mapping_color.items():
        list_color = item[1]
        for each in list_color:
            reverse_mapping_color[each] = item[0]

    def process_price(sen):
        if isinstance(sen, str):
            sen = re.sub("\n", "", sen)
            sen = re.sub("\r", "", sen)
            sen = re.sub(" +", " ", sen)
            word_list = sen.split(" ")
            for word in word_list:
                if any(char.isdigit() for char in word):
                    result = "".join([char for char in word if char.isdigit() or char == "."]).split(".")
                    components = word.split(".")
                    if len(components[-1]) < 3:
                        new_word = "".join(components[:-1])
                    else:
                        new_word = word
                    return "".join([char for char in new_word if char.isdigit()])
        return sen

    def process_color(sen):
        if isinstance(sen, str):
            for item in reverse_mapping_color.keys():
                if item in sen:
                    return reverse_mapping_color[item]
        return sen

    for item in coll:
        collec = db[item]
        date_save = date.today()
        data = collec.find({"date": str(date_save)})

        df = pd.DataFrame(list(data)).drop(["_id"], axis=1)

        if item == "mediamart":
            color = df["name"].apply(extract_color)
            df["color"] = color
        df = preprocess(df)
        df["color"] = df["color"].apply(process_color)
        df["price"] = df["price"].apply(process_price)
        df.to_csv(f'/opt/airflow/dags/data/{item}.csv')


if __name__ == "__main__":
    clean_data()
