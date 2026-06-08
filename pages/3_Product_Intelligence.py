import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# --- FIX: Connector (Allows this page to see root files) ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components.styling import apply_enterprise_theme, render_alert

# Apply Theme
st.set_page_config(page_title="Product Intelligence", page_icon="📦", layout="wide")
apply_enterprise_theme()

st.title("📦 Product Intelligence & SKU Analytics")
st.markdown("Analyze historical performance, demand scores, and growth trends for individual products.")

# Load Data
try:
    # Changed to use absolute path for reliability in Streamlit Cloud
    df = pd.read_csv('data/cleaned_retail_data.csv') 
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
except FileNotFoundError:
    st.error("⚠️ 'cleaned_retail_data.csv' not found.")
    st.stop()

# --- FIX: Sorting Safety Net ---
# Convert to list and sort safely
valid_products = df['Description'].dropna().unique()
valid_products = sorted(list(valid_products)) 

# UI: SKU Selector
selected_product = st.selectbox("🔍 Search and Select a Product (SKU)", options=valid_products, index=0)

if selected_product:
    # Filter data
    product_df = df[df['Description'] == selected_product].copy()
    product_df = product_df.sort_values('InvoiceDate')
    
    # Aggregate daily
    daily_product_df = product_df.groupby(product_df['InvoiceDate'].dt.date).agg({
        'Quantity': 'sum',
        'TotalAmount': 'sum'
    }).reset_index()
    daily_product_df.columns = ['Date', 'Quantity', 'Revenue']
    daily_product_df['Date'] = pd.to_datetime(daily_product_df['Date'])

    # --- KPI Calculations ---
    total_rev = daily_product_df['Revenue'].sum()
    cutoff_30 = daily_product_df['Date'].max() - pd.Timedelta(days=30)
    cutoff_60 = daily_product_df['Date'].max() - pd.Timedelta(days=60)
    
    last_30_rev = daily_product_df[daily_product_df['Date'] >= cutoff_30]['Revenue'].sum()
    prev_30_rev = daily_product_df[(daily_product_df['Date'] >= cutoff_60) & (daily_product_df['Date'] < cutoff_30)]['Revenue'].sum()
    
    growth_pct = ((last_30_rev - prev_30_rev) / prev_30_rev) * 100 if prev_30_rev > 0 else 0.0
    avg_daily_qty = daily_product_df['Quantity'].mean() if not daily_product_df.empty else 0
    demand_score = min(100, int((avg_daily_qty / df['Quantity'].mean()) * 50)) if df['Quantity'].mean() != 0 else 0

    # --- Dynamic Product Alert ---
    if growth_pct > 20:
        render_alert("healthy", "High Growth Detected", f"This SKU is experiencing a {growth_pct:.1f}% surge.", "Capturing new market share.", "Review pricing.")
    elif growth_pct < -20:
        render_alert("warning", "Declining Demand", f"Revenue dropped by {abs(growth_pct):.1f}%.", "Potential dead stock.", "Consider bundling.")

    # --- Render KPI Cards ---
    st.subheader(f"Performance Metrics: {selected_product.title()}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Lifetime SKU Revenue", f"${total_rev:,.2f}")
    col2.metric("Demand Score", f"{demand_score} / 100")
    col3.metric("30-Day Growth", f"${last_30_rev:,.2f}", f"{growth_pct:.1f}%")

    st.divider()

    # --- Render Charts ---
    st.subheader("📈 Historical Trends")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig_qty = px.line(daily_product_df, x='Date', y='Quantity', title='Units Sold Over Time', markers=True)
        st.plotly_chart(fig_qty, use_container_width=True)

    with chart_col2:
        fig_rev = px.area(daily_product_df, x='Date', y='Revenue', title='Revenue Generated ($)')
        st.plotly_chart(fig_rev, use_container_width=True)