# pages/4_Model_Performance.py
import streamlit as st
import pandas as pd
import plotly.express as px
from components.styling import apply_enterprise_theme, render_alert

# Apply Theme
st.set_page_config(page_title="Model Performance", page_icon="🧠", layout="wide")
apply_enterprise_theme()

st.title("🧠 ML Diagnostics & Model Evaluation")
st.markdown("Compare the performance of our predictive models to understand why the final algorithm was selected.")
st.write("")

# 1. Model Evaluation Data
metrics_data = {
    'Model': ['Linear Regression', 'Random Forest', 'XGBoost'],
    'MAE': [2450.50, 2890.15, 2750.80],      
    'RMSE': [3150.75, 4100.20, 3950.60],     
    'R² Score': [0.82, 0.74, 0.76]           
}
metrics_df = pd.DataFrame(metrics_data)

# 2. Executive Summary Alert
render_alert(
    type="healthy",
    title="Winning Algorithm: Linear Regression",
    description="Linear Regression outperformed complex tree-based models on our time-series data.",
    impact="Highest variance explained (R²) with the lowest financial error margin (MAE & RMSE).",
    action="Linear Regression pipeline has been approved and deployed to production."
)

st.divider()

# 3. KPI Cards
st.subheader("🏆 Primary Evaluation Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Accuracy (R² Score)", "0.82", "Highest variance explained")
with col2:
    st.metric("Avg Error (MAE)", "$2,450.50", "-$300 vs XGBoost", delta_color="inverse")
with col3:
    st.metric("Max Error Penalty (RMSE)", "$3,150.75", "-$800 vs XGBoost", delta_color="inverse")

st.write("")
st.write("")

# 4. Data Visualization
st.subheader("📊 Model Comparison Analysis")
chart_col1, chart_col2 = st.columns(2)

# Custom color mapping to highlight the winner and mute the losers
color_map = {'Linear Regression': '#16a34a', 'XGBoost': '#94a3b8', 'Random Forest': '#cbd5e1'}

with chart_col1:
    fig_r2 = px.bar(
        metrics_df, x='Model', y='R² Score', 
        title='Model Accuracy (R² Score) - Higher is Better',
        color='Model', 
        color_discrete_map=color_map
    )
    # Transparent background for SaaS look
    fig_r2.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_r2, use_container_width=True)

with chart_col2:
    fig_rmse = px.bar(
        metrics_df, x='Model', y='RMSE', 
        title='Prediction Error (RMSE) - Lower is Better',
        color='Model',
        color_discrete_map=color_map
    )
    fig_rmse.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_rmse, use_container_width=True)