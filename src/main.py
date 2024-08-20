import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import numpy as np
from tools import connect_to_bedrock, extract_document, build_tables_dict, generate_sql, database_retrieval

from data import getsql


st.set_page_config(layout="wide")

FILEPATH = 'balance-sheet-1.pdf'
COMPANY_NAME = 'Example Corporation'
DOC_TYPE = 'Consolidating Balance Sheet'
CSV_PATH = 'path.csv'

llm = connect_to_bedrock()
document = extract_document(file_path=FILEPATH)
tables, financial_quarter = build_tables_dict(llm, document)
table = pd.concat(tables[COMPANY_NAME][DOC_TYPE])
table = table.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
table = table.set_index(table.columns[0])
sql_list = generate_sql(llm=llm, pd_table=table, db_path=CSV_PATH, company_name=COMPANY_NAME, financial_quarter=financial_quarter)


st.header('Doc Analysis', divider='blue')

container_pdf, container_data = st.columns(2)

with container_pdf:
    pdf_viewer(FILEPATH, width=700)

with container_data:

    st.markdown(f"Document Type: {DOC_TYPE}")
    st.markdown(f"Company Name: {COMPANY_NAME}")
    st.markdown(f"Financial Quarter: {financial_quarter}")

    tab1, tab2, tab3 = st.tabs(["Extracted Data", "Generated SQL", "Data Comparisons"])

    with tab1:
        st.dataframe(table, width=700, height=700)

    with tab2:
        st.markdown("*Individual SQL statements for demo purposes*")
        code = ""
        for t in sql_list:
            code += t[1] + '\n\n'
        st.code(code, language='sql')
    
    with tab3:
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

        results_df = database_retrieval(tuples_list=sql_list, extracted_data=table, db_path=CSV_PATH)

        st.dataframe(results_df.style.apply(custom_style, axis=1), width=700, height=700)