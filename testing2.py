import pandas as pd
import numpy as np

data1 = [["alex1", "", "", ""], ["diego1", "19,177", "(51,100)", "-"], ['bahareh', "26,000", "85,000", "500"]]
data2 = [["alex2", np.nan, np.nan, np.nan], ["diego2", 19177.0, -51100.0, np.nan]]

df1 = pd.DataFrame(data=data1, columns=["col0", "col1", "col2", "col3"])
df2 = pd.DataFrame(data=data2, columns=["col0-DB", "col1-DB", "col2-DB", "col3-DB"])
df2 = df2.set_index(df2.columns[0])
df1 = df1.set_index(df1.columns[0])


mapping = [
    ["alex1", "alex2", "something"],
    ["diego1", "diego2", "somethingelse"]
]


def database_retrieval(tuples_list, extracted_data, db_path):
    #database = pd.read_csv(db_path, sep=',', index_col=0)
    database = db_path

    # remove special characters and convert string numbers to numbers
    extracted_data = extracted_data.apply(lambda x: x.str.replace(',', ''))
    extracted_data = extracted_data.apply(lambda x: x.str.replace('(', '-'))
    extracted_data = extracted_data.apply(lambda x: x.str.replace(')', ''))
    extracted_data = extracted_data.replace({"": np.nan, "-": np.nan})
    extracted_data.columns = extracted_data.iloc[0]
    extracted_data = extracted_data.drop("")
    extracted_data = extracted_data.apply(pd.to_numeric)

    columns = [item for items in zip(extracted_data.columns, database.columns) for item in items]
    final_df = pd.DataFrame(columns=columns)

    for item in tuples_list:
        if len(item) < 3:
            continue
        extracted_vals = extracted_data.loc[item[0]].values.flatten().tolist()
        db_vals = database.loc[item[1]].values.flatten().tolist()
        concat_values = [x for y in zip(extracted_vals, db_vals) for x in y]
        final_df.loc[item[0]] = concat_values

    return final_df

mydf = database_retrieval(tuples_list=mapping, extracted_data=df1, db_path=df2)
print(mydf)