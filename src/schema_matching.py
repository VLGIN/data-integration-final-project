import json
import pandas as pd

from valentine import algorithms
from valentine import valentine_match
from decouple import config
from pymongo import MongoClient
from datetime import date


def schema_matching(df1, df2, matcher, fn1, fn2, keep_feats=False):
    if "source" in list(df1):
        source1 = df1["source"]
    else:
        source1 = pd.Series([fn1]*df1.shape[0])
    if "source" in list(df2):
        source2 = df2["source"]
    else:
        source2 = pd.Series([fn2] * df2.shape[0])

    source = pd.concat([source1, source2]).reset_index(drop=True)
    matches = valentine_match(df1, df2, matcher)
    column_df1 = []
    column_df2 = []
    for item in matches.items():
        cand1 = item[0][0][1]
        cand2 = item[0][1][1]
        if cand1 not in column_df1 and cand2 not in column_df2:
            column_df1.append(cand1)
            column_df2.append(cand2)
    mapping = {column_df1[i]: column_df2[i] for i in range(len(column_df1))}
    if keep_feats:
        other_feats = [item for item in list(df1) if item not in column_df1]
    else:
        other_feats = []
    df1 = df1[column_df1 + other_feats]
    df_renew2 = pd.DataFrame()
    for i, each in enumerate(column_df1):
        df_renew2[each] = df2[column_df2[i]]
    for each in other_feats:
        df_renew2[each] = pd.Series([None]*df_renew2.shape[0])
    with open(f"mapping_{fn1}_{fn2}.json", "w+") as f:
        json.dump(mapping, f)
    result = pd.concat([df1, df_renew2], axis=0)
    if "source" in list(result):
        result = result.drop(["source"], axis=1)
    result["source"] = source
    return df1, df2, result


if __name__ == "__main__":
    collection_name = ["didongviet", "mediamart", "thegioididong", "tiki", "viettel_store"]
    client = MongoClient("mongodb+srv://data-integration:data-integration@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration"]

    df_list = {}

    for item in collection_name:
        collec = db[item]
        # "date": str(date.today())
        data = collec.find({})
        df = pd.DataFrame(list(data))
        df_list[item] = df

    cupid = algorithms.Cupid()
    jacard = algorithms.JaccardLevenMatcher()

    _, __, didongviet_viettel_store = schema_matching(df_list["didongviet"], df_list["viettel_store"],
                                                      cupid, "didongviet", "viettel_store")
    _, __, mediamart_tgdd = schema_matching(df_list["mediamart"], df_list["thegioididong"],
                                            jacard, "mediamart", "thegioididong", keep_feats=True)
    _, __, cummulative = schema_matching(mediamart_tgdd, didongviet_viettel_store, jacard,
                                         "mediamart_tgdd", "didongviet_viettel_store", keep_feats=True)
    _, __, final = schema_matching(cummulative, df_list["tiki"], jacard, "the_rest", "tiki", keep_feats=True)

    final.reset_index(inplace=True)
    final = final.drop(["index", "level_0", "_id"], axis=1)
    data_dict = final.to_dict('records')
    collec = db["unify_schema"]
    collec.insert_many(data_dict)
