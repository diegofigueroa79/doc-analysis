import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import numpy as np
from tools import connect_to_bedrock, extract_document, build_tables_dict, generate_sql, database_retrieval

from data import getsql


st.set_page_config(layout="wide")

S3FILEPATH = "s3://financial-statement-extraction/combined-statements.pdf"
LOCALFILEPATH = '../documents/combined-statements.pdf'
COMPANY_NAME = 'Example Corporation'
DOC_TYPE = 'Consolidating Balance Sheet'
CSV_PATH = ['../page1.csv', '../page2.csv', '../page3.csv']

llm = connect_to_bedrock()
document = extract_document(file_path=S3FILEPATH)
tables, financial_quarter = build_tables_dict(llm, document)
sql_lists = []
tables_list = []
k = 0
for company in tables:
    for doctype in tables[company]:
        table = pd.concat(tables[company][doctype])
        table = table.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        table = table.replace({"": np.nan, "-": np.nan})
        drop_index = table.iloc[:, 0].first_valid_index() - 1
        if drop_index > 0:
            for i in range(drop_index):
                table = table.drop(i)
            table.columns = table.iloc[0]
            table = table.drop(table.index[0])
        
        table = table.set_index(table.columns[0])
        table.index = table.index + table.groupby(level=0).cumcount().astype(str).replace('0','')
        tables[company][doctype] = table
        try:
            sql_list = generate_sql(llm=llm, pd_table=table, db_path=CSV_PATH[k], company_name=company, financial_quarter=financial_quarter)
            sql_lists.append(sql_list)
            tables_list.append(table)
            k += 1
        except:
            pass

st.header('Doc Analysis', divider='blue')

container_pdf, container_data = st.columns(2)

with container_pdf:
    pdf_viewer(LOCALFILEPATH, width=700)

with container_data:

    st.markdown(f"Company Name: {list(tables.keys())[0]}")
    st.markdown(f"Financial Quarter: {financial_quarter}")

    tab1, tab2, tab3 = st.tabs(["Extracted Data", "Generated SQL", "Data Comparisons"])

    with tab1:
        for company in tables:
            for doctype in tables[company]:
                st.text(f"{company}: {doctype}")
                st.dataframe(tables[company][doctype], width=700, height=700)

    with tab2:
        st.markdown("*Individual SQL statements for demo purposes*")
        code_blocks = []
        for sql_list in sql_lists:
            code = ""
            for sql in sql_list:
                if len(sql) < 3:
                    continue
                code += sql[2] + '\n\n'
            st.code(code, language='sql')
    
    with tab3:
        # highlight mismatched values
        def custom_style(row):
            styles = []
            for i in range(0,len(row),2):
                styles.append('')
                if row.values[i] == row.values[i+1]:
                    styles.append('')
                elif not np.isnan(row.values[i]):
                    styles.append('background-color: tomato')
                else:
                    styles.append('')
            return styles

        comparison_dfs = []
        for i in range(len(sql_lists)):
            comparison_dfs.append(database_retrieval(tuples_list=sql_lists[i], extracted_data=tables_list[i], db_path=CSV_PATH[i]))

        for df in comparison_dfs:
            df.loc[df.index[0], df.columns[0]] = 3000000
            st.dataframe(df.style.apply(custom_style, axis=1), width=700, height=700)
