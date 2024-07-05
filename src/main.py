from dotenv import load_dotenv
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import numpy as np


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
        df = pd.DataFrame(np.random.randn(10, 8), columns=("col %d" % i for i in range(8)))
        st.dataframe(df)

    with tab2:
        code = '''
        SELECT total_assets FROM table
        SELECT total_liabilities FROM table
        '''
        st.code(code, language='sql')
    
    with tab3:
        st.error('error here')

if __name__ == '__main__':
    load_dotenv()