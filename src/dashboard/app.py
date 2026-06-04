import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the page layout
st.set_page_config(page_title="Sales Forecasting Dashboard", page_icon="📈", layout="wide")

st.title("📈 E-Commerce Sales & Inventory Dashboard")
st.markdown("This dashboard displays the 7-day revenue forecast and recommended inventory levels.")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ Dashboard Controls")
st.sidebar.markdown("Adjust the parameters below to see how they impact your inventory needs.")

safety_stock_percent = st.sidebar.slider(
    "Safety Stock Buffer (%)", 
    min_value=0, 
    max_value=50, 
    value=34, # I set the default to your chosen 34%!
    step=1
) / 100.0 

try:
    forecast_df = pd.read_csv('data/forecast_7_days.csv')
    inventory_df = pd.read_csv('data/inventory_plan.csv')
    
    # --- SECTION 1: INVENTORY METRICS ---
    st.header("📦 Inventory Optimization Plan")
    
    est_units = inventory_df[inventory_df['Metric'] == 'Estimated Units To Sell']['Value'].values
    dynamic_safety_stock = int(est_units * safety_stock_percent)
    dynamic_target = int(est_units + dynamic_safety_stock)
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Estimated Units to Sell", f"{int(est_units):,}")
    col2.metric(f"Safety Stock ({int(safety_stock_percent * 100)}%)", f"{dynamic_safety_stock:,}")
    col3.metric("🎯 Recommended Reorder Target", f"{dynamic_target:,}")
    
    st.divider()
    
    # --- SECTION 2: ADVANCED VISUALIZATIONS ---
    st.header("🔮 7-Day Revenue Forecast Analysis")
    
    # NEW: We split the screen into two columns for our charts!
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Original Line Chart
        fig_line = px.line(forecast_df, x='Date', y='Predicted_Revenue', markers=True, title="Daily Revenue Trend")
        fig_line.update_traces(line_color='#1f77b4', line_dash='solid', marker=dict(size=8))
        fig_line.update_layout(yaxis_title='Predicted Revenue ($)', xaxis_title='Date')
        st.plotly_chart(fig_line, use_container_width=True)
        
    with chart_col2:
        # NEW: Donut Chart for Day of Week Breakdown
        # 1. Extract the Day Name (e.g., "Monday") from the Date
        forecast_df['Day_Name'] = pd.to_datetime(forecast_df['Date']).dt.day_name()
        
        # 2. Create the Pie Chart (with a hole in the middle to make it a Donut)
        fig_pie = px.pie(forecast_df, values='Predicted_Revenue', names='Day_Name', 
                         title="Revenue Distribution by Day",
                         hole=0.45, 
                         color_discrete_sequence=px.colors.sequential.Blues_r)
        
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # --- SECTION 3: RAW DATA ---
    with st.expander("View Raw Forecast Data"):
        st.dataframe(forecast_df, use_container_width=True)
        
except FileNotFoundError:
    st.error("⚠️ Data files not found. Please ensure you have run the forecasting and inventory scripts first!")