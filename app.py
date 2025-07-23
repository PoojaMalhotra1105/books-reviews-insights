import streamlit as st
import pandas as pd

st.set_page_config(page_title="Books, Reviews & Insights", layout="wide")

st.title("📚 Books, Reviews & Insights")
st.markdown("Explore Goodreads data to uncover top-rated books, genre trends, and review insights.")

uploaded_file = st.file_uploader("Upload your Goodreads dataset", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
    st.write("Preview of data:", df.head())
