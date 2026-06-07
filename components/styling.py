import streamlit as st
import pandas as pd
import plotly.io as pio

def apply_enterprise_theme():
    st.markdown("""
        <style>
        .stApp {background-color: #0e0e1a; color: #e2e8f0;}
        [data-testid="stSidebar"] {background-color: #1a1a2e; border-right: 1px solid #2a2a3e; padding-top: 1rem;}
        [data-testid="stSidebarNav"] li a:hover {background-color: #2a2a3e !important; border-left: 3px solid #1D9E75 !important;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stAlert {background-color: #1a1a2e; border: 1px solid #2a2a3e;}
        </style>
    """, unsafe_allow_html=True)

def render_sidebar_header():
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="color: #1D9E75; margin: 0;">⚡ DemandIQ</h2>
                <div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 2px;">Enterprise Ops</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("---")

def render_alert(type, title, description, impact, action):
    colors = {"critical": "#ef4444", "warning": "#f59e0b", "healthy": "#22c55e"}
    color = colors.get(type, "#64748b")
    st.markdown(f"""
        <div style="background-color: #1a1a2e; border-left: 5px solid {color}; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <h4 style="color: {color}; margin-top: 0; margin-bottom: 0.5rem;">{title}</h4>
            <p style="margin-bottom: 0.5rem;">{description}</p>
            <p style="font-size: 0.85rem; margin-bottom: 0.5rem;"><b>Impact:</b> {impact}</p>
            <p style="font-size: 0.85rem; margin-bottom: 0;"><b>Action:</b> {action}</p>
        </div>
    """, unsafe_allow_html=True)

def render_download_button(df, file_name, button_text="📥 Download Data (CSV)"):
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(label=button_text, data=csv_data, file_name=file_name, mime="text/csv", type="primary")

def show_welcome():
    st.markdown("""
        <style>
        .hero-title {color: #1D9E75; font-size: 2.6rem; font-weight: 800; margin-bottom: 0.5rem;}
        .hero-sub {color: #94a3b8; font-size: 1.1rem; margin-bottom: 2.5rem;}
        .stat-card {background-color: #1a1a2e; border: 1px solid #2a2a3e; padding: 1.5rem; border-radius: 0.5rem; text-align: center;}
        .stat-val {color: #1D9E75; font-size: 1.8rem; font-weight: 800;}
        .stat-lbl {color: #64748b; font-size: 0.8rem; text-transform: uppercase;}
        .grid-card {background-color: #1a1a2e; border: 1px solid #2a2a3e; padding: 1rem; border-radius: 0.4rem; height: 100%;}
        .card-title {color: #e2e8f0; font-size: 0.95rem; font-weight: 600; margin-bottom: 0.2rem;}
        .card-desc {color: #64748b; font-size: 0.78rem;}
        .pill {background-color: #1a1a2e; color: #1D9E75; border: 1px solid #1D9E75; padding: 0.2rem 0.6rem; border-radius: 1rem; font-size: 0.75rem; margin-right: 0.4rem; display: inline-block; margin-bottom: 0.5rem;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hero-title">DemandIQ: Enterprise AI Forecasting</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Predictive supply chain intelligence and automated operational analytics.</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    stats = [("1.2M+", "Transactions"), ("450", "SKUs Tracked"), ("94.2%", "Accuracy"), ("8", "Modules")]
    for col, (val, lbl) in zip(cols, stats):
        col.markdown(f'<div class="stat-card"><div class="stat-val">{val}</div><div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("Platform Modules")
    modules = [("Executive Overview", "High-level strategic financial forecasting."), ("Inventory Risk", "Real-time stockout probability monitoring."), ("Product Intelligence", "Deep-dive SKU velocity and growth trends."), ("Model Performance", "ML evaluation metrics and validation."), ("Feature Importance", "AI driver transparency and analysis."), ("Market Basket Analysis", "Cross-sell affinity and bundling insights."), ("Anomaly Diagnostics", "Automated distribution outlier detection."), ("Supplier Performance", "Lead-time velocity and risk mapping.")]
    
    for i in range(0, len(modules), 4):
        row = st.columns(4)
        for j, (title, desc) in enumerate(modules[i:i+4]):
            row[j].markdown(f'<div class="grid-card"><div class="card-title">{title}</div><div class="card-desc">{desc}</div></div>', unsafe_allow_html=True)

    st.write("")
    st.subheader("Engineered With")
    pill_html = "".join([f'<span class="pill">{t}</span>' for t in ["Python", "Streamlit", "Pandas", "Scikit-learn", "Plotly", "NumPy", "mlxtend", "Matplotlib"]])
    st.markdown(pill_html, unsafe_allow_html=True)