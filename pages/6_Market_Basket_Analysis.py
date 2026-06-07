# pages/6_Market_Basket_Analysis.py
import streamlit as st
import pandas as pd
from itertools import combinations
from collections import Counter
from components.styling import apply_enterprise_theme, render_alert, render_download_button

st.set_page_config(page_title="Market Basket Analysis", page_icon="🛒", layout="wide")
apply_enterprise_theme()

st.title("🛒 Market Basket Analysis & Cross-Selling Engine")
st.markdown("Discover high-affinity product pairs frequently purchased together to optimize product bundling and placement.")
st.write("")

try:
    # 1. Load and prepare transaction data
    df = pd.read_csv('data/cleaned_retail_data.csv')
    
    # Drop rows missing crucial connection keys
    df = df.dropna(subset=['InvoiceNo', 'Description'])
    df['InvoiceNo'] = df['InvoiceNo'].astype(str)
    
    # Filter out common generic strings that introduce statistical noise
    noise_words = ['postage', 'manual', 'discount', 'fee', 'shipping']
    df = df[~df['Description'].str.lower().str.contains('|'.join(noise_words))]

except FileNotFoundError:
    st.error("⚠️ 'cleaned_retail_data.csv' not found. Please ensure the file exists in the data/ folder.")
    st.stop()

# 2. Optimized Association Mining Engine
@st.cache_data
def calculate_product_affinities(data):
    # Group items by invoice to build transaction baskets
    baskets = data.groupby('InvoiceNo')['Description'].apply(set).tolist()
    total_transactions = max(1, len(baskets))
    
    # Count individual item frequencies for item base support
    item_counts = Counter()
    for basket in baskets:
        item_counts.update(basket)
    
    # Generate and count pairs
    pair_counts = Counter()
    for basket in baskets:
        if len(basket) > 1:
            # Sort to keep pair combinations uniform (A, B)
            pair_counts.update(combinations(sorted(basket), 2))
            
    # Compile metrics for the top associated product pairs
    rules = []
    for pair, count in pair_counts.most_common(50):
        item_a, item_b = pair
        
        support_both = count / total_transactions
        confidence_a_to_b = count / item_counts[item_a]
        confidence_b_to_a = count / item_counts[item_b]
        
        rules.append({
            'Product A': item_a,
            'Product B': item_b,
            'Co-Occurrence Count': count,
            'Pair Support': support_both,
            'Confidence (A → B)': confidence_a_to_b,
            'Confidence (B → A)': confidence_b_to_a
        })
        
    return pd.DataFrame(rules), total_transactions

# Run computation
rules_df, total_baskets = calculate_product_affinities(df)

# 3. Dynamic Executive Notification
if not rules_df.empty:
    # FIX: Convert the dataframe row to a standard Python dictionary to bypass Pandas indexing bugs
    top_pair = rules_df.to_dict('records')[0]
    
    render_alert(
        type="healthy",
        title="High-Affinity Cross-Sell Pathway Discovered",
        description=f"Customers purchasing '{top_pair['Product A']}' show a {top_pair['Confidence (A → B)']:.1%} probability of adding '{top_pair['Product B']}' to the same order.",
        impact=f"Pair co-occurred {top_pair['Co-Occurrence Count']} times across historical baskets.",
        action="Deploy an automated product bundle recommendation banner on checkout pages for these SKUs."
    )
else:
    render_alert(
        type="warning",
        title="Insufficient Transaction Density",
        description="Not enough overlapping multi-item baskets detected to generate statistical confidence thresholds.",
        impact="Cross-selling algorithms cannot establish baseline recommendations.",
        action="Verify transactional diversity or lower minimum volume filtering metrics."
    )

st.divider()

# 4. KPI Briefing Cards
st.subheader("📊 Cross-Sell Health Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Baskets Analyzed", f"{total_baskets:,}", "Unique transactional orders")
with col2:
    if not rules_df.empty:
        max_conf = max(rules_df['Confidence (A → B)'].max(), rules_df['Confidence (B → A)'].max())
        st.metric("Peak Rule Confidence", f"{max_conf:.1%}", "Strongest probabilistic link")
    else:
        st.metric("Peak Rule Confidence", "0.0%")
with col3:
    st.metric("Identified Rule Paths", len(rules_df), "Top high-velocity associations")

st.write("")
st.write("")

# 5. Association Matrix Manifest Table
st.subheader("📋 Top 50 High-Affinity Product Pairs")
st.markdown("Review actionable product connections. High Confidence scores signal direct bundling opportunities.")

def highlight_high_confidence(val):
    if isinstance(val, float) and val > 0.5:
        return 'background-color: rgba(22, 163, 74, 0.15); color: #22c55e; font-weight: bold;'
    return ''

# Format column percentages smoothly for corporate review
formatted_df = rules_df.style.map(
    highlight_high_confidence, 
    subset=['Confidence (A → B)', 'Confidence (B → A)']
).format({
    'Pair Support': '{:.2%}',
    'Confidence (A → B)': '{:.1%}',
    'Confidence (B → A)': '{:.1%}',
    'Co-Occurrence Count': '{:,}'
})

st.dataframe(formatted_df, use_container_width=True, hide_index=True)

st.write("")

# 6. Universal Download Integration
render_download_button(rules_df, "Market_Basket_Affinities.csv", "📥 Export Product Affinities (CSV)")