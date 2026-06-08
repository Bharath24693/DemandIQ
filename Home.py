import streamlit as st
from streamlit_option_menu import option_menu
from components.styling import apply_enterprise_theme, show_welcome, render_sidebar_header

# 1. Page Configuration
st.set_page_config(page_title="DemandIQ | AI Forecasting", page_icon="⚡", layout="wide")

# 2. Styling
apply_enterprise_theme()

# 3. Sidebar Branding
render_sidebar_header()

# --- Burger Menu Logic ---
if "menu_expanded" not in st.session_state:
    st.session_state.menu_expanded = False

# The "Burger" Button
if st.button("≡ MENU"):
    st.session_state.menu_expanded = not st.session_state.menu_expanded

# Show menu only if expanded
if st.session_state.menu_expanded:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Executive Overview", "Inventory Risk", "Product Intelligence", 
                 "Model Performance", "Feature Importance", "Market Basket Analysis", "Anomaly Diagnostics"],
        icons=["house", "bar-chart", "exclamation-triangle", "box-seam", "graph-up", "key", "cart", "shield"],
        orientation="horizontal"
    )
    
    # Routing Logic
    if selected != "Home":
        page_map = {
            "Executive Overview": "pages/1_Executive_Overview.py",
            "Inventory Risk": "pages/2_Inventory_Risk.py",
            "Product Intelligence": "pages/3_Product_Intelligence.py",
            "Model Performance": "pages/4_Model_Performance.py",
            "Feature Importance": "pages/5_Feature_Importance.py",
            "Market Basket Analysis": "pages/6_Market_Basket_Analysis.py",
            "Anomaly Diagnostics": "pages/7_Anomaly_Diagnostics.py"
        }
        st.switch_page(page_map[selected])

# 4. Main Dashboard Content
show_welcome()