# pages/8_Supplier_Performance.py
import streamlit as st
import pandas as pd
import plotly.express as px
from components.styling import apply_enterprise_theme, render_alert

st.set_page_config(page_title="Supplier Matrix", page_icon="🚛", layout="wide")
apply_enterprise_theme()

st.title("🚛 Supplier Performance & Lead-Time Risk Matrix")
st.markdown("Track fulfillment velocities, risk profiles, and operational lead times by product group.")
st.write("")

# Synthetic high-quality supplier framework data
# Synthetic high-quality supplier framework data
supplier_data = {
    'Supplier Group': ['Global Logistics Ltd', 'EuroDistribution Corp', 'Pan-Asia Manufacturing', 'Domestic Apex Supplies', 'Oceanic Freight Partners'],
    'Primary Segment': ['High-Volume Plastics', 'Ceramics & Housewares', 'Electronics & Textiles', 'Paper & Stationary', 'Packaging Materials'],
    'Avg Lead Time (Days)': [12, 18, 25, 8, 30],
    'Fulfillment Rate (%)': [98.4, 91.2, 84.7, 99.1, 79.5],
    'Risk Level': ['🟢 LOW', '🟡 MEDIUM', '🔴 CRITICAL', '🟢 LOW', '🔴 CRITICAL']
}
sup_df = pd.DataFrame(supplier_data)

render_alert("critical", "Supplier Risk Threshold Breached", 
             "Two primary overseas fulfillment channels have crossed acceptable lead time limits.",
             "Potential supply chain delay could cause stockouts on 4 key categories next month.",
             "Route immediate purchase orders through alternative domestic suppliers.")

st.subheader("Strategic Fleet & Fulfillment Analytics")
fig = px.scatter(sup_df, x='Avg Lead Time (Days)', y='Fulfillment Rate (%)', size='Avg Lead Time (Days)',
                 color='Risk Level', text='Supplier Group', title="Lead Time Velocity vs Order Accuracy Rate",
                 color_discrete_map={'🟢 LOW': '#16a34a', '🟡 MEDIUM': '#d97706', '🔴 CRITICAL': '#dc2626'})

fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
fig.update_traces(textposition='top center')
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("📋 Supplier Risk Registry")
st.dataframe(sup_df, use_container_width=True, hide_index=True)