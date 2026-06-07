# pages/7_Anomaly_Diagnostics.py
import streamlit as st
import pandas as pd
import plotly.express as px
from components.styling import apply_enterprise_theme, render_alert

st.set_page_config(page_title="Data Diagnostics", page_icon="🛡️", layout="wide")
apply_enterprise_theme()

st.title("🛡️ ML Pipeline Anomaly & Outlier Log")
st.markdown("Automated algorithmic detection of transactions deviating from expected distribution boundaries.")
st.write("")

try:
    df = pd.read_csv('data/cleaned_retail_data.csv')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
except FileNotFoundError:
    st.error("⚠️ Data files missing.")
    st.stop()

# IQR Outlier Detection Math Engine
q1 = df['Quantity'].quantile(0.25)
q3 = df['Quantity'].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + (3.0 * iqr) # Extreme outliers

outliers_df = df[df['Quantity'] > upper_bound].copy()
anomaly_rate = (len(outliers_df) / len(df)) * 100

render_alert("warning", "Data Profile Anomaly Warning", 
             f"The monitoring framework flagged {len(outliers_df):,} extreme transactional quantity spikes.",
             f"Outliers account for {anomaly_rate:.2f}% of baseline volume, inflating raw time-series trends.",
             "The production training architecture strips these anomalies dynamically to prevent prediction bias.")

col1, col2 = st.columns(2)
with col1:
    st.metric("Statistical Upper Threshold", f"{int(upper_bound)} units", "Extreme outlier limit")
with col2:
    st.metric("Total Anomaly Incidents Logged", f"{len(outliers_df):,}", f"{anomaly_rate:.2f}% data noise control")

st.divider()
st.subheader("📋 Flagged Anomaly Manifest")
st.dataframe(outliers_df[['InvoiceNo', 'Description', 'Quantity', 'UnitPrice', 'CustomerID']].head(100), use_container_width=True, hide_index=True)