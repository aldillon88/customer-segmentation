import streamlit as st


st.set_page_config(page_title="Customer Segmentation", layout="wide")

st.header('E-commerce :blue[***Customer Segmentation***] Dashboard', divider=True)

analysis_page = st.Page("page_1.py", title="Analysis")
project_page = st.Page("page_2.py", title="Project Description")

pg = st.navigation([analysis_page, project_page])

pg.run()