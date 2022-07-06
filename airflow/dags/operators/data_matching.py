def data_matching():
    import pandas as pd
    import recordlinkage

    from pymongo import MongoClient

    client = MongoClient("mongodb+srv://longgiang:longgiang2010@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration"]
    df = pd.read_csv(f"/opt/airflow/dags/data/cellphones_didongthongminh_mediamart_thegioididong_phongvu.csv")

    df.reset_index(drop=True)
    data_dict = df.to_dict('records')
    collec = db["unify_schema"]
    collec.insert_many(data_dict)

    dupe_indexer = recordlinkage.Index()
    dupe_indexer.sortedneighbourhood(left_on="name")
    dupe_candidate_links = dupe_indexer.index(df)

    compare_dupes = recordlinkage.Compare()
    compare_dupes.string("name", "name", threshold=0.7, label="name")
    compare_dupes.string('ram',
                         'ram',
                         threshold=0.8,
                         label='ram')
    compare_dupes.string("bộ nhớ",
                         "bộ nhớ",
                         threshold=0.8,
                         label="bộ nhớ")
    dupe_features = compare_dupes.compute(dupe_candidate_links, df)
    potential_dupes = dupe_features[dupe_features.sum(axis=1) == 3].reset_index()
    potential_dupes['Score'] = potential_dupes.loc[:, 'name':'bộ nhớ'].sum(axis=1)

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
        data = data.groupby(["source"], as_index=False).first().reset_index(drop=True)
        if data.shape[0] == 1:
            continue
        print(data)

        data.reset_index(drop=True, inplace=True)
        if "_id" in data:
            data.drop(["_id"], axis=1, inplace=True)
        data_dict = data.to_dict('records')
        collec.insert_one({data_dict[0]["name"]: data_dict})


if __name__ == "__main__":
    data_matching()
