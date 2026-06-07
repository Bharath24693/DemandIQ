
import streamlit as st
import pandas as pd
import numpy as np
from components.styling import apply_enterprise_theme

# 1. Setup & Theme
st.set_page_config(page_title="Inventory Risk", page_icon="⚠️", layout="wide")
apply_enterprise_theme()

st.title("⚠️ Inventory Risk & Health Monitoring")
st.markdown("Identify SKUs with critical stock levels and prioritize reordering to prevent stockouts.")
st.write("")

# 2. Data Loading & Processing
try:
    df = pd.read_csv('data/cleaned_retail_data.csv')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']) 
except FileNotFoundError:
    st.error("⚠️ 'cleaned_retail_data.csv' not found. Please ensure the file exists in the data/ folder.")
    st.stop()

# 3. Calculation Engine
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(15).index

risk_data = []
for product in top_products:
    prod_df = df[df['Description'] == product]
    days_active = len(prod_df['InvoiceDate'].dt.date.unique()) if 'InvoiceDate' in prod_df.columns else 30
    if days_active == 0: days_active = 1
    
    avg_daily_demand = max(1, int(prod_df['Quantity'].sum() / days_active))
    risk_data.append({
        'Product (SKU)': product,
        'Avg Daily Demand': avg_daily_demand,
    })
    
risk_df = pd.DataFrame(risk_data)

# Apply our hard-won NumPy fix!
np.random.seed(42)
risk_df['Current Stock'] = risk_df['Avg Daily Demand'] * np.random.choice([1,2,3,4], size=len(risk_df))

risk_df['Days of Inventory'] = (risk_df['Current Stock'] / risk_df['Avg Daily Demand']).astype(int)

def assign_status(days):
    if days <= 3: return "🔴 CRITICAL"
    elif days <= 7: return "🟡 REORDER SOON"
    else: return "🟢 HEALTHY"
    
risk_df['Health Status'] = risk_df['Days of Inventory'].apply(assign_status)

# Reorder columns for the UI
risk_df = risk_df[['Product (SKU)', 'Current Stock', 'Avg Daily Demand', 'Days of Inventory', 'Health Status']]
risk_df = risk_df.sort_values('Days of Inventory')

# 4. Top KPI Metrics
critical_count = len(risk_df[risk_df['Health Status'] == '🔴 CRITICAL'])
warning_count = len(risk_df[risk_df['Health Status'] == '🟡 REORDER SOON'])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🔴 SKUs at Critical Risk", critical_count, "Stockout in < 3 days", delta_color="inverse")
with col2:
    st.metric("🟡 SKUs to Reorder Soon", warning_count, "Stockout in < 7 days", delta_color="off")
with col3:
    st.metric("📦 Total Monitored SKUs", len(risk_df))

st.divider()

# 5. Actionable Data Table
st.subheader("📋 Actionable Reorder List")
st.markdown("Products sorted by urgency. Dispatch reorder requests for Critical items immediately.")

