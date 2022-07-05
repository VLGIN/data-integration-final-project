import pandas as pd

from utils import process_name, process_text


def preprocess(df):
    df['name'] = df['name'].apply(process_name())
    df.reset_index(inplace=True)

    for index, row in df.iterrows():
        if row["Mã sản phẩm"] is None:
            row["Mã sản phẩm"] = row["name"]
        elif row["name"] is None:
            row["name"] = row["Mã sản phẩm"]

    return df


def preprocess_thegioididong(df):
    df["Name"] = df["Name"].apply(process_name)
    df.rename(columns={item: str(item).strip().lower() for item in list(df)}, inplace=True)
    return df


def preprocess_mediamart(df):
    df["name"] = df["name"].apply(process_name)
    df.rename(columns={item: str(item).strip().lower() for item in list(df)}, inplace=True)
    return df

def preprocess_tiki(df):
    df = df.dropna(thresh=15)
    df.reset_index(drop=True, inplace=True)
    df.rename(columns={"Model": "name", "ROM": "Bộ nhớ"}, inplace=True)
    print(list(df))
    df["name"] = df["name"].apply(process_name)
    df.rename(columns={item: str(item).strip().lower() for item in list(df)}, inplace=True)
    return df
