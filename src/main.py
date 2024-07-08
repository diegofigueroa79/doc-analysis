from dotenv import load_dotenv
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import numpy as np

from data import getsql


st.set_page_config(layout="wide")

st.header('Doc Analysis', divider='blue')

container_pdf, container_data = st.columns(2)

with container_pdf:
    pdf_viewer("documents/balance-sheet-1.pdf", width=700)

with container_data:

    st.markdown("Document Type: `Balance Sheet`")
    st.markdown("Company Name: `Example Corporation`")
    st.markdown("Financial Quarter: `December 31, 2023`")

    tab1, tab2, tab3 = st.tabs(["Textract Data", "Generated SQL", "Data Comparisons"])

    with tab1:
        df = pd.read_csv("balance-sheet-1.csv", sep='\t', names=["col1", "col2"])
        st.dataframe(df, width=700, height=700)

    with tab2:
        tuples = getsql()
        code = ""
        for t in tuples:
            code += t[1] + '\n'
        st.code(code, language='sql')
    
    with tab3:
        results_df = pd.DataFrame(columns=['fieldname', 'document', 'database'])
        for t in tuples:
            value = df.loc[df['col1'] == t[0]].values[0][1]
            row = [t[0], value, value]
            results_df.loc[len(results_df.index)] = row
        st.dataframe(results_df, width=700, height=700)

if __name__ == '__main__':
    load_dotenv()