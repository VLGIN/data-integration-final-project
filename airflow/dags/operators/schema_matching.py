def schema_matching(**kwargs):
    import pandas as pd
    import json
    from valentine import algorithms
    from valentine import valentine_match
    def schema_matching(df1, df2, matcher, keep_feats=False):
        matches = valentine_match(df1, df2, matcher)
        # print(matches)
        column_df1 = []
        column_df2 = []
        for item in matches.items():
            cand1 = item[0][0][1]
            cand2 = item[0][1][1]
            if cand1 not in column_df1 and cand2 not in column_df2:
                column_df1.append(cand1)
                column_df2.append(cand2)
        mapping = {column_df1[i]: column_df2[i] for i in range(len(column_df1))}
        if keep_feats == True:
            other_feats = [item for item in list(df1) if item not in column_df1]
        else:
            other_feats = []
        df1 = df1[column_df1 + other_feats]
        df_renew2 = pd.DataFrame()
        for i, each in enumerate(column_df1):
            df_renew2[each] = df2[column_df2[i]]
        for each in other_feats:
            df_renew2[each] = pd.Seires([None]*df_renew2.shape[0])
        with open(f"mapping_{kwargs['filename1']}_{kwargs['filename2']}.json", "w+") as f:
            json.dump(mapping, f)
        return df1, df2, pd.concat([df1, df_renew2], axis = 0)
    
    df1 = pd.read_csv(kwargs['filename1'], header=None)
    df2 = pd.read_csv(kwargs['filename2'], header=None)
    if kwargs['matcher'] == "cupid":
        matcher = algorithms.Cupid()
    elif kwargs['matcher'] == 'jaccard':
        matcher = algorithms.JaccardLevenMatcher()
    else:
        raise NotImplementedError("Choose between cupid and jaccard")
    
    _, __, schema_match = schema_matching(df1, df2, matcher, kwargs['keep_feats'])
    schema_match.to_csv(f"{kwargs['filename1']}_{kwargs['filename2']}.csv", index=False)
