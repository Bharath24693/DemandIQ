import streamlit as st
from components.styling import apply_enterprise_theme, show_welcome, render_sidebar_header

# 1. Page Configuration
st.set_page_config(page_title="DemandIQ | AI Forecasting", page_icon="⚡", layout="wide")

# 2. Styling
apply_enterprise_theme()

# 3. Sidebar Branding (This puts DemandIQ at the top of your sidebar)
render_sidebar_header()

# 4. Main Dashboard Content
show_welcome()