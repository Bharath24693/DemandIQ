import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv('data/cleaned_retail_data.csv')