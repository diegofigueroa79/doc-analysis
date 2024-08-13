import pandas as pd
import numpy as np
import streamlit as st


data1 = [["alex1", "", "", ""], ["diego1", "19,177", "(51,100)", "-"]]
data2 = [["alex2", np.nan, np.nan, np.nan], ["diego2", 19177.0, -51100.0, np.nan]]

df1 = pd.DataFrame(data=data1, columns=["col0", "col1", "col2", "col3"])
df2 = pd.DataFrame(data=data2, columns=["col0", "col1-DB", "col2-DB", "col3-DB"])

# convert string numbers to numbers
#df1 = df1.apply(lambda x: x.str.replace(',', ''))
#df1 = df1.apply(lambda x: x.str.replace('(', '-'))
#df1 = df1.apply(lambda x: x.str.replace(')', ''))
#df1 = df1.replace({"": np.nan, "-": np.nan})
#df1 = df1.apply(pd.to_numeric)

df1 = df1.set_index(df1.columns[0])
print(df1)
df2 = df2.set_index(df1.index)
df2 = df2.drop(columns=df2.columns[0], axis=1)
print(df2)

df3 = pd.concat([df1, df2], axis=1)
df3 = df3[[item for items in zip(df1.columns, df2.columns) for item in items]]

print(df3)

# highlight mismatched values
def custom_style(row):
    styles = []
    for i in range(0,len(row),2):
        styles.append('')
        if row.values[i] == row.values[i+1]:
            styles.append('background-color: tomato')
        else:
            styles.append('')
    return styles

def database_retrieval(tuples_list, extracted_data, db_path, database_df):
    database_df = pd.read_csv(db_path, sep=',', index_col=0)
    database_df.set_index(extracted_data.index)

    # remove special characters and convert string numbers to numbers
    extracted_data = extracted_data.apply(lambda x: x.str.replace(',', ''))
    extracted_data = extracted_data.apply(lambda x: x.str.replace('(', '-'))
    extracted_data = extracted_data.apply(lambda x: x.str.replace(')', ''))
    extracted_data = extracted_data.replace({"": np.nan, "-": np.nan})
    extracted_data = extracted_data.apply(pd.to_numeric)

    final_df = pd.concat([extracted_data, database_df], axis=1)
    final_df = final_df[[item for items in zip(extracted_data.columns, database_df.columns) for item in items]]
    return final_df

fdf = database_retrieval(None, extracted_data=df1, db_path=None, database_df=df2)

st.dataframe(fdf.style.apply(custom_style, axis=1), width=700, height=700)