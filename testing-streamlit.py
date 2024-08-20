import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd

st.set_page_config(layout="wide")

container_pdf, container_data = st.columns(2)

with container_pdf:
    pdf_viewer('documents/income-statement-3.pdf', width=700)

with container_data:
    database = pd.read_csv('balance-sheet-1.csv', sep=',')
    st.text('TABLE 1')
    st.dataframe(database, width=700, height=700)
    st.text('TABLE 2')
    st.dataframe(database, width=700, height=700)
