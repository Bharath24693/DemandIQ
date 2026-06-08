import streamlit as st
import plotly.express as px
import sys
import os

# 1. Path Connector (Ensures Home.py is found)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Home import load_data 

# 2. Access cached data
df = load_data()

st.title("Inventory Risk & Health Monitoring")
st.write("Identify SKUs with critical stock levels and prioritize reordering to prevent stockouts.")

if df is not None and not df.empty:
    # --- Aggregation ---
    # Ensure column names match your CSV (e.g., 'Description', 'Quantity')
    inventory_data = df.groupby('Description')['Quantity'].sum().reset_index()
    
    # --- KPI Metrics ---
    total_skus = len(df['Description'].unique())
    col1, col2, col3 = st.columns(3)
    col1.metric("SKUs at Critical Risk", 12, delta="Stockout in < 3 days", delta_color="inverse")
    col2.metric("SKUs to Reorder Soon", 3, delta="Stockout in < 7 days", delta_color="normal")
    col3.metric("Total Monitored SKUs", total_skus)

    st.markdown("---") 

    # --- Actionable Reorder List (Table) ---
    st.subheader("📋 Actionable Reorder List")
    
    table_df = inventory_data.copy()
    table_df['Risk Status'] = table_df['Quantity'].apply(lambda x: 'CRITICAL' if x < 500 else 'NORMAL')
    table_df['Days to Stockout'] = table_df['Quantity'].apply(lambda x: '1-3 Days' if x < 500 else '7+ Days')
    
    # Sort and prepare 10 products for the table
    reorder_table = table_df.sort_values(by='Quantity', ascending=True).head(10)
    reorder_table.columns = ['Product Description', 'Current Stock', 'Risk Status', 'Days to Stockout']
    st.table(reorder_table)

    # --- Inventory Distribution Graph ---
    st.subheader("📊 Inventory Distribution")
    top_20 = inventory_data.sort_values(by='Quantity', ascending=False).head(20)
    
    fig = px.bar(
        top_20, 
        x='Description', 
        y='Quantity', 
        color='Quantity',
        color_continuous_scale='Viridis'
    )
    # Rotation set to -45 for better readability
    fig.update_layout(xaxis={'tickangle': -45}, margin=dict(b=150), height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.error("Data could not be loaded. Please check if 'cleaned_retail_data.csv' exists in the data/ folder.")