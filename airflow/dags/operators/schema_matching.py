def schema_matching(**kwargs):
    import json
    import os
    import pandas as pd


    from datetime import date
    from pymongo import MongoClient

    coll1 = kwargs["collection1"]
    coll2 = kwargs["collection2"]
    matcher_type = kwargs["matcher"]
    #keep_feats = kwargs["keep_feats"]
    keep_feats=False

    df1 = pd.read_csv(f"/opt/airflow/dags/data/{coll1}.csv")
    df2 = pd.read_csv(f"/opt/airflow/dags/data/{coll2}.csv")
    #df1 = pd.read_csv(f"data/{coll1}.csv")
    #df2 = pd.read_csv(f"data/{coll2}.csv")

    if "source" in list(df1):
        source1 = df1["source"]
        df1 = df1.drop(["source"], axis=1)
    else:
        source1 = pd.Series([coll1] * df1.shape[0])
    if "source" in list(df2):
        source2 = df2["source"]
        df2 = df2.drop(["source"], axis=1)
    else:
        source2 = pd.Series([coll2] * df2.shape[0])
    print(source2)
    source = pd.concat([source1, source2]).reset_index(drop=True)

    if not os.path.exists(f"/opt/airflow/dags/data/mapping_{coll1}_{coll2}.json"):
    #if not os.path.exists(f"data/mapping_{coll1}_{coll2}.json"):
        from valentine import algorithms
        from valentine import valentine_match
        if matcher_type == "jaccard":
            matcher = algorithms.JaccardLevenMatcher()
        elif matcher_type == "cupid":
            matcher = algorithms.Cupid()
        else:
            raise NotImplementedError

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
        with open(f"/opt/airflow/dags/data/mapping_{coll1}_{coll2}.json", "w+") as f:
        #with open(f"data/mapping_{coll1}_{coll2}.json", "w+") as f:
            json.dump(mapping, f)
    else:
        with open(f"/opt/airflow/dags/data/mapping_{coll1}_{coll2}.json") as f:
        #with open(f"data/mapping_{coll1}_{coll2}.json") as f:
            mapping = json.load(f)

        column_df1 = list(mapping.keys())
        column_df2 = list(mapping.values())

    if keep_feats:
        other_feats = [item for item in list(df1) if item not in column_df1]
    else:
        other_feats = []
    df1 = df1[column_df1 + other_feats]
    df_renew2 = pd.DataFrame()
    for i, each in enumerate(column_df1):
        df_renew2[each] = df2[column_df2[i]]
    for each in other_feats:
        df_renew2[each] = pd.Series([None] * df_renew2.shape[0])

    result = pd.concat([df1, df_renew2], axis=0)
    if "source" in list(result):
        result = result.drop(["source"], axis=1)

    result.reset_index(drop=True, inplace=True)
    result["source"] = source

    #result["date"] = [str(date.today())]*result.shape[0]

    result.to_csv(f"/opt/airflow/dags/data/{coll1}_{coll2}.csv", index=False)
    #result.to_csv(f"data/{coll1}_{coll2}.csv", index=False)


if __name__ == "__main__":
    schema_matching(**{"collection1": "cellphones_didongthongminh_mediamart_thegioididong", "collection2": "phongvu", "remote": True, "matcher": "jaccard",
                       "keep_feats": False})
