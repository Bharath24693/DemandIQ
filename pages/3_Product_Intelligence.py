# pages/3_Product_Intelligence.py
import streamlit as st
import pandas as pd
import plotly.express as px
from components.styling import apply_enterprise_theme, render_alert

# Apply Theme
st.set_page_config(page_title="Product Intelligence", page_icon="📦", layout="wide")
apply_enterprise_theme()

st.title("📦 Product Intelligence & SKU Analytics")
st.markdown("Analyze historical performance, demand scores, and growth trends for individual products.")
st.write("")

# Load Data
try:
    df = pd.read_csv('data/cleaned_retail_data.csv') 
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
except FileNotFoundError:
    st.error("⚠️ 'cleaned_retail_data.csv' not found. Please ensure the file exists in the data/ folder.")
    st.stop()

# Get valid products and create the search bar
valid_products = df['Description'].dropna().unique()
valid_products.sort()

# UI: SKU Selector
selected_product = st.selectbox("🔍 Search and Select a Product (SKU)", options=valid_products, index=0)

if selected_product:
    # Filter data for the selected product
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
    
    # Calculate growth (handle division by zero)
    growth_pct = ((last_30_rev - prev_30_rev) / prev_30_rev) * 100 if prev_30_rev > 0 else 0.0

    avg_daily_qty = daily_product_df['Quantity'].mean() if not daily_product_df.empty else 0
    demand_score = min(100, int((avg_daily_qty / df['Quantity'].mean()) * 50))

    # --- Dynamic Product Alert ---
    # Generate an alert based on the 30-day growth of this specific product
    if growth_pct > 20:
        render_alert("healthy", "High Growth Detected", f"This SKU is experiencing a {growth_pct:.1f}% surge in revenue over the last 30 days.", "Capturing new market share.", "Review pricing strategy to maximize margins during surge.")
    elif growth_pct < -20:
        render_alert("warning", "Declining Demand", f"Revenue has dropped by {abs(growth_pct):.1f}% in the last 30 days.", "Potential dead stock accumulation.", "Consider bundling with high-velocity items or applying a discount.")

    # --- Render KPI Cards ---
    st.subheader(f"Performance Metrics: {selected_product.title()}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Lifetime SKU Revenue", f"${total_rev:,.2f}")
    with col2:
        st.metric("Demand Score", f"{demand_score} / 100", "Based on relative velocity")
    with col3:
        st.metric("30-Day Growth", f"${last_30_rev:,.2f}", f"{growth_pct:.1f}% vs previous 30 days", delta_color="normal" if growth_pct >= 0 else "inverse")

    st.divider()

    # --- Render Charts ---
    st.subheader("📈 Historical Trends")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig_qty = px.line(daily_product_df, x='Date', y='Quantity', title='Units Sold Over Time', markers=True, line_shape='spline')
        fig_qty.update_traces(line_color='#FF7F0E')
        fig_qty.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)') # Transparent background for SaaS look
        st.plotly_chart(fig_qty, use_container_width=True)

    with chart_col2:
        fig_rev = px.area(daily_product_df, x='Date', y='Revenue', title='Revenue Generated ($)', line_shape='spline')
        fig_rev.update_traces(line_color='#1F77B4', fillcolor='rgba(31, 119, 180, 0.3)')
        fig_rev.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_rev, use_container_width=True)