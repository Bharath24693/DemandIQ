# pages/5_Feature_Importance.py
import streamlit as st
import pandas as pd
import plotly.express as px
from components.styling import apply_enterprise_theme, render_alert

# Apply Theme
st.set_page_config(page_title="Feature Importance", page_icon="🔍", layout="wide")
apply_enterprise_theme()

st.title("🔍 Feature Importance & Drivers")
st.markdown("Understand which variables have the biggest impact on our machine learning predictions.")
st.write("")

# 1. Feature Importance Data
importance_data = {
    'Feature': ['Rolling_Mean_7 (Past Week Avg)', 'Lag_7 (Sales 7 Days Ago)', 'Lag_1 (Yesterday Sales)', 'Day_of_Week', 'Month', 'Is_Weekend'],
    'Importance': [0.45, 0.25, 0.15, 0.08, 0.05, 0.02]
}
importance_df = pd.DataFrame(importance_data).sort_values(by='Importance', ascending=True)

# 2. Executive Summary Alert
render_alert(
    type="healthy",
    title="Key Driver: Short-Term Momentum",
    description="The average sales over the last 7 days (Rolling_Mean_7) drives 45% of the model's prediction accuracy.",
    impact="The business relies heavily on short-term velocity rather than long-term seasonal trends.",
    action="Focus marketing spend on sustaining week-over-week growth to maximize inventory turnover."
)

st.divider()

# 3. Data Visualization
st.subheader("What drives our predicted revenue?")

fig = px.bar(
    importance_df, 
    x='Importance', 
    y='Feature', 
    orientation='h',
    color='Importance',
    color_continuous_scale='Blues' 
)

# Apply transparent backgrounds for the SaaS aesthetic
fig.update_layout(
    xaxis_tickformat='.0%', 
    showlegend=False, 
    xaxis_title="Impact on Prediction (%)", 
    yaxis_title="",
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig, use_container_width=True)