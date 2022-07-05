def clean_data():
    import pandas as pd
    import re

    from pymongo import MongoClient

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
        if tex[-3:] == "vna":
            tex = " ".join(tex.split(" ")[:-1])

        return tex

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

    coll = ["cellphones", "thegioididong", "didongthongminh", "mediamart", "phongvu"]

    client = MongoClient("mongodb+srv://longgiang:longgiang2010@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration"]

    for item in coll:
        collec = db[item]
        data = collec.find()

        df = pd.DataFrame(list(data)).drop(["_id", "index"], axis=1)

        df = preprocess(df)
        df.to_csv(f'/opt/airflow/dags/data/{item}.csv')

if __name__ == "__main__":
    clean_data()