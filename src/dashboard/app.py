import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set up the page layout (This must be the very first Streamlit command)
st.set_page_config(page_title="Enterprise AI Dashboard", page_icon="📈", layout="wide")


# ==========================================
# PAGE 1: EXISTING EXECUTIVE FORECAST
# ==========================================
def render_executive_forecast():
    st.title("📈 Executive Sales & Inventory Dashboard")
    st.markdown("This dashboard displays the 7-day revenue forecast and recommended inventory levels.")

    st.sidebar.header("⚙️ Inventory Controls")
    safety_stock_percent = st.sidebar.slider(
        "Safety Stock Buffer (%)", 
        min_value=0, max_value=50, value=34, step=1
    ) / 100.0 

    try:
        forecast_df = pd.read_csv('data/forecast_7_days.csv')
        inventory_df = pd.read_csv('data/inventory_plan.csv')
        
        st.header("📦 Inventory Optimization Plan")
        est_units = inventory_df[inventory_df['Metric'] == 'Estimated Units To Sell']['Value'].values[0]
        dynamic_safety_stock = int(est_units * safety_stock_percent)
        dynamic_target = int(est_units + dynamic_safety_stock)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Estimated Units to Sell", f"{int(est_units):,}")
        col2.metric(f"Safety Stock ({int(safety_stock_percent * 100)}%)", f"{dynamic_safety_stock:,}")
        col3.metric("🎯 Recommended Reorder Target", f"{dynamic_target:,}")
        
        st.divider()
        st.header("🔮 7-Day Revenue Forecast Analysis")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            fig_line = px.line(forecast_df, x='Date', y='Predicted_Revenue', markers=True, title="Daily Revenue Trend")
            fig_line.update_traces(line_color='#1f77b4')
            st.plotly_chart(fig_line, use_container_width=True)
            
        with chart_col2:
            forecast_df['Day_Name'] = pd.to_datetime(forecast_df['Date']).dt.day_name()
            fig_pie = px.pie(forecast_df, values='Predicted_Revenue', names='Day_Name', 
                             title="Revenue Distribution by Day", hole=0.45, 
                             color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with st.expander("View Raw Forecast Data"):
            st.dataframe(forecast_df, use_container_width=True)
            
    except FileNotFoundError:
        st.error("⚠️ Forecast data files not found. Please run your ML scripts first!")


# ==========================================
# PAGE 2: NEW PRODUCT INTELLIGENCE
# ==========================================
def render_product_intelligence():
    st.title("📦 Product Intelligence & SKU Analytics")
    st.markdown("Analyze historical performance, demand scores, and growth trends for individual products.")

    try:
        # Load the raw historical data (update the path if your raw data has a different name)
        df = pd.read_csv('data/cleaned_retail_data.csv') 
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    except FileNotFoundError:
        st.error("⚠️ 'cleaned_retail_data.csv' not found in the data folder. Please ensure the file exists.")
        return

    # Drop missing descriptions to clean up the dropdown
    valid_products = df['Description'].dropna().unique()
    valid_products.sort()

    selected_product = st.selectbox("🔍 Search and Select a Product (SKU)", options=valid_products, index=0)

    if selected_product:
        product_df = df[df['Description'] == selected_product].copy()
        product_df = product_df.sort_values('InvoiceDate')
        
        # Aggregate by day for smoother charts
        daily_product_df = product_df.groupby(product_df['InvoiceDate'].dt.date).agg({
            'Quantity': 'sum',
            'TotalAmount': 'sum'
        }).reset_index()
        daily_product_df.columns = ['Date', 'Quantity', 'Revenue']
        daily_product_df['Date'] = pd.to_datetime(daily_product_df['Date'])

        # --- KPI CALCULATIONS ---
        total_rev = daily_product_df['Revenue'].sum()

        cutoff_30 = daily_product_df['Date'].max() - pd.Timedelta(days=30)
        cutoff_60 = daily_product_df['Date'].max() - pd.Timedelta(days=60)
        
        last_30_rev = daily_product_df[daily_product_df['Date'] >= cutoff_30]['Revenue'].sum()
        prev_30_rev = daily_product_df[(daily_product_df['Date'] >= cutoff_60) & (daily_product_df['Date'] < cutoff_30)]['Revenue'].sum()
        
        growth_pct = ((last_30_rev - prev_30_rev) / prev_30_rev) * 100 if prev_30_rev > 0 else 0.0

        avg_daily_qty = daily_product_df['Quantity'].mean() if not daily_product_df.empty else 0
        demand_score = min(100, int((avg_daily_qty / df['Quantity'].mean()) * 50))

        # --- RENDER KPI CARDS ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Lifetime SKU Revenue", f"${total_rev:,.2f}")
        col2.metric("Demand Score (0-100)", f"{demand_score} / 100")
        col3.metric("30-Day Growth", f"${last_30_rev:,.2f}", f"{growth_pct:.1f}% vs previous 30 days")

        st.divider()

        # --- RENDER CHARTS ---
        st.subheader(f"📈 Performance Trends: {selected_product.title()}")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            fig_qty = px.line(daily_product_df, x='Date', y='Quantity', title='Units Sold Over Time', markers=True, line_shape='spline')
            fig_qty.update_traces(line_color='#FF7F0E')
            st.plotly_chart(fig_qty, use_container_width=True)

        with chart_col2:
            fig_rev = px.area(daily_product_df, x='Date', y='Revenue', title='Revenue Generated ($)', line_shape='spline')
            fig_rev.update_traces(line_color='#1F77B4', fillcolor='rgba(31, 119, 180, 0.3)')
            st.plotly_chart(fig_rev, use_container_width=True)


# ==========================================
# MAIN NAVIGATION CONTROLLER
# ==========================================
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["Executive Forecast", "Product Intelligence"])

st.sidebar.divider()

# Route the user to the correct page based on their selection
if page == "Executive Forecast":
    render_executive_forecast()
elif page == "Product Intelligence":
    render_product_intelligence()


    