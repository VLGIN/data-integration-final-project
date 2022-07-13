import json
import pandas as pd
import recordlinkage

from valentine import algorithms
from valentine import valentine_match
from decouple import config
from pymongo import MongoClient
from datetime import date


if __name__ == "__main__":
    collection_name = ["didongviet", "mediamart", "thegioididong", "tiki", "viettel_store"]
    client = MongoClient("mongodb+srv://data-integration:data-integration@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration"]

    collec = db["unify_schema"]
    data = collec.find({})

    df = pd.DataFrame(list(data))
    df.drop(["_id"], axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)

    #df["id"] = pd.Series(list(range(df.shape[0])))
    #df.set_index('id')
    #df.drop(["index"], axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(df.index)
    dupe_indexer = recordlinkage.Index()
    dupe_indexer.sortedneighbourhood(left_on="Mã sản phẩm")
    dupe_candidate_links = dupe_indexer.index(df)

    compare_dupes = recordlinkage.Compare()
    compare_dupes.string("Mã sản phẩm", "Mã sản phẩm", threshold=0.8, label="Mã sản phẩm")
    compare_dupes.string('RAM',
                         'RAM',
                         threshold=0.7,
                         label='RAM')
    compare_dupes.string("Bộ nhớ",
                         "Bộ nhớ",
                         threshold=0.7,
                         label="Bộ nhớ")
    compare_dupes.string("Bộ nhớ trong",
                         "Bộ nhớ trong",
                         threshold=0.7,
                         label="Bộ nhớ trong")
    compare_dupes.string("Thương hiệu",
                         "Thương hiệu",
                         threshold=0.8,
                         label="Thương hiệu")
    dupe_features = compare_dupes.compute(dupe_candidate_links, df)
    potential_dupes = dupe_features[dupe_features.sum(axis=1) > 1].reset_index()
    potential_dupes['Score'] = potential_dupes.loc[:, 'Mã sản phẩm':'Bộ nhớ trong'].sum(axis=1)

    potential_dupes = potential_dupes.where(potential_dupes["Score"] > 2).dropna()
    level0 = list(potential_dupes["level_0"])
    level1 = list(potential_dupes["level_1"])

    keys = level0 + level1
    value = level1 + level0
    mapping = {}
    for i, key in enumerate(keys):
        if key not in mapping.keys():
            mapping[key] = [value[i]]
        else:
            print(mapping[key])
            print(value[i])
            mapping[key].append(value[i])

    def visit(i, mapping, visited, cluster):
        if i in visited:
            pass
        else:
            visited.append(i)
            cluster.append(i)
            for each in mapping[i]:
                visit(each, mapping, visited, cluster)

    clusters = {}

    visited = []
    for i in list(set(keys)):
        cluster = []
        visit(i, mapping, visited, cluster)
        if len(cluster) > 0:
            clusters[f"cluster{len(list(clusters.keys()))}"] = cluster
    print(clusters)
    collec = db["data_matching"]
    for cluster in clusters.values():
        data = df.iloc[[int(item) for item in cluster]]

        data.reset_index(drop=True, inplace=True)
        if "_id" in data:
            data.drop(["_id"], axis=1, inplace=True)
        data_dict = data.to_dict('records')
        print(type(data_dict))
        collec.insert_one({"data": data_dict})
