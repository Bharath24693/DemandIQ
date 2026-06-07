# pages/1_Executive_Overview.py
import streamlit as st
import pandas as pd
import numpy as np

# Import our UI theme AND our new Logic Engine
from components.styling import apply_enterprise_theme, render_alert
from components.insights_engine import generate_inventory_alerts

# Apply theme
st.set_page_config(page_title="Executive Overview", page_icon="📈", layout="wide")
apply_enterprise_theme()

st.title("Executive Intelligence Brief")
st.markdown("Automated insights and strategic forecasting.")
st.write("") 

# ==========================================
# 1. ACTIONABLE INSIGHTS ENGINE (Dynamic)
# ==========================================
try:
    # Load data
    df = pd.read_csv('data/cleaned_retail_data.csv')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # RUN THE ENGINE: Get alerts based on real data
    alerts = generate_inventory_alerts(df)
    
    # Loop through whatever alerts the engine found and display them!
    for alert in alerts:
        render_alert(
            type=alert["type"],
            title=alert["title"],
            description=alert["description"],
            impact=alert["impact"],
            action=alert["action"]
        )
except FileNotFoundError:
    st.error("⚠️ 'cleaned_retail_data.csv' not found. Please ensure the file exists in the data/ folder.")

st.divider()

# ... (Keep the rest of your KPI cards and charts down here exactly as they were) ...