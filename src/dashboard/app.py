import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the page layout
st.set_page_config(page_title="Sales Forecasting Dashboard", page_icon="📈", layout="wide")

st.title("📈 E-Commerce Sales & Inventory Dashboard")
st.markdown("This dashboard displays the 7-day revenue forecast and recommended inventory levels.")

# --- NEW: SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ Dashboard Controls")
st.sidebar.markdown("Adjust the parameters below to see how they impact your inventory needs.")

# Create a slider from 0% to 50% (default is 20%)
safety_stock_percent = st.sidebar.slider(
    "Safety Stock Buffer (%)", 
    min_value=0, 
    max_value=50, 
    value=20, 
    step=1
) / 100.0  # Convert 20 to 0.20 for the math below

try:
    forecast_df = pd.read_csv('data/forecast_7_days.csv')
    inventory_df = pd.read_csv('data/inventory_plan.csv')
    
    # --- SECTION 1: INVENTORY METRICS ---
    st.header("📦 Inventory Optimization Plan")
    
    # Extract the base "Estimated Units" value
    est_units = inventory_df[inventory_df['Metric'] == 'Estimated Units To Sell']['Value'].values
    
    # DYNAMIC CALCULATION: These now update instantly when the slider moves!
    dynamic_safety_stock = int(est_units * safety_stock_percent)
    dynamic_target = int(est_units + dynamic_safety_stock)
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Estimated Units to Sell", f"{int(est_units):,}")
    
    # The label and number update based on the slider
    col2.metric(f"Safety Stock ({int(safety_stock_percent * 100)}%)", f"{dynamic_safety_stock:,}")
    col3.metric("🎯 Recommended Reorder Target", f"{dynamic_target:,}")
    
    st.divider()
    
    # --- SECTION 2: FORECAST CHART ---
    st.header("🔮 7-Day Revenue Forecast")
    fig = px.line(forecast_df, x='Date', y='Predicted_Revenue', markers=True)
    fig.update_traces(line_color='#1f77b4', line_dash='solid', marker=dict(size=8))
    fig.update_layout(yaxis_title='Predicted Revenue ($)', xaxis_title='Date')
    st.plotly_chart(fig, use_container_width=True)
    
    # --- SECTION 3: RAW DATA ---
    with st.expander("View Raw Forecast Data"):
        st.dataframe(forecast_df, use_container_width=True)
        
except FileNotFoundError:
    st.error("⚠️ Data files not found. Please ensure you have run the forecasting and inventory scripts first!")