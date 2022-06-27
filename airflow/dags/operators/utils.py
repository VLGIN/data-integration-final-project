def clean_data():
    import pandas as pd
    import re
    def preprocess(sen: str = ""):
        escape = "".join([chr(character) for character in range(1, 32)])
        translator = str.maketrans('', '', escape)
        clean_sen = sen.translate(translator)
        clean_sen = re.sub(" +", " ", clean_sen)
        return clean_sen.lower()

    def clean(file_name: str = ""):
        # Remove null column
        data = pd.read_csv(file_name)

        column_list = list(data)
        num_null = data.isna().sum().to_dict()
        num_item = data.shape[0]

        drop_list = []
        for item in num_null.items():
            if item[1] >= num_item * 0.8:
                drop_list.append(item[0])

        column_list = [item for item in column_list if item not in drop_list]
        clean_column = []
        for item in column_list:
            clean_column.append(preprocess(item))

        result_df = pd.DataFrame()
        for i, item in enumerate(clean_column):
            result_df[item] = data[column_list[i]]
        save_file = ".".join(file_name.split(".")[:-1]) + ".clean" + ".csv"
        result_df.to_csv(save_file, index=False)

    file_name = ["data-source/shopee/shopee_sample.csv", "data-source/tiki/tiki_sample.csv", "data-source/sendo/sendo_sample.csv", "mediamart.csv"]

    for each_file in file_name:
        clean(each_file)

def schema_matching():
    pass
