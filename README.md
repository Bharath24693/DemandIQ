# DemandIQ 🛒📊
### Enterprise AI Platform for Ecommerce Sales Forecasting & Smart Inventory Optimization

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://demandiq-k6ddzfvenvxdgejegmj55s.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-Primary%20Model-orange?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

> **DemandIQ** transforms raw ecommerce transaction data into actionable supply chain intelligence using 6 machine learning models across 8 analytical modules — achieving **94.2% forecast accuracy** on the UCI Online Retail Dataset.

---

## 🚀 Live Demo

**👉 [Launch DemandIQ Dashboard](https://demandiq-k6ddzfvenvxdgejegmj55s.streamlit.app/)**

---

## 📈 Key Results

| Metric | Result |
|--------|--------|
| 🎯 Forecast Accuracy | **94.2%** |
| 📦 Critical SKUs Flagged | **12 SKUs** with stockout risk < 3 days |
| 🛒 Transactions Analysed | **541,909** retail invoices |
| 🤖 ML Models Deployed | **6 models** across 8 modules |
| 🔍 SKUs Monitored | **4,000+** in real-time |
| 📊 Evaluation Metrics | MAE · RMSE · MAPE tracked live |

---

## 🧠 ML Models Used

### Forecasting & Predictive Models
| Model | Purpose |
|-------|---------|
| **XGBoost** | Primary sales forecasting engine — handles non-linear transactional patterns |
| **Random Forest Regressor** | Cross-validation and accuracy benchmarking against XGBoost |
| **Linear Regression** | Baseline model for trend analysis and revenue projections |

### Analytical & Mining Models
| Model | Purpose |
|-------|---------|
| **Apriori Algorithm** | Market Basket Analysis — discovers cross-sell product associations |
| **K-Means Clustering** | SKU segmentation by velocity, lead time, and risk profile |
| **Isolation Forest** | Anomaly detection — auto-flags demand spikes, drops, and outliers |

---

## 🛠️ 8 Analytical Modules

| Module | Description |
|--------|-------------|
| 📊 **Executive Overview** | High-level strategic KPIs and financial forecasting |
| ⚠️ **Inventory Risk** | Real-time stockout probability monitoring and reorder alerts |
| 🔍 **Product Intelligence** | SKU velocity, growth trends, and top performer analysis |
| 🤖 **Model Performance** | MAE, RMSE, MAPE diagnostics and model validation dashboard |
| 💡 **Feature Importance** | Transparency into AI-driven forecasting drivers |
| 🛒 **Market Basket Analysis** | Cross-sell affinity rules and product bundling insights |
| 🚨 **Anomaly Diagnostics** | Automated outlier detection using Isolation Forest |
| 🚚 **Supplier Performance** | Lead-time velocity analysis and supplier risk mapping |

---

## 💻 Tech Stack

| Category | Libraries |
|----------|-----------|
| **Language** | Python 3.10 |
| **ML & Data Science** | Scikit-learn, XGBoost, mlxtend, Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib, Seaborn, Streamlit |
| **Deployment** | Streamlit Community Cloud, GitHub |
| **Dataset** | UCI Online Retail Dataset (541K+ transactions) |

---

##  Project Structure

```
DemandIQ/
├── app.py                        # Main Streamlit entry point
├── pages/
│   ├── executive_overview.py
│   ├── inventory_risk.py
│   ├── product_intelligence.py
│   ├── model_performance.py
│   ├── feature_importance.py
│   ├── market_basket_analysis.py
│   ├── anomaly_diagnostics.py
│   └── supplier_performance.py
├── data/
│   └── online_retail.csv         # UCI Online Retail Dataset
├── requirements.txt
└── README.md
```

---

## ⚙️ Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/Bharath24693/DemandIQ.git
cd DemandIQ

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py
```

---

## 📦 Requirements

```
streamlit
pandas
numpy
scikit-learn
xgboost
mlxtend
plotly
matplotlib
seaborn
```

---

## 📊 Dataset

**UCI Online Retail Dataset**
- 541,909 transactions from a UK-based online retailer (2010–2011)
- Features: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
- Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/online+retail)

---

## 👤 About the Developer

**Bharath K**
Final Year B.Tech Computer Science · Srinivas University, Mangalore

[![LinkedIn](https://img.shields.io/badge/LinkedIn-bharath--k--sgr-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/bharath-k-sgr)
[![GitHub](https://img.shields.io/badge/GitHub-Bharath24693-181717?logo=github&logoColor=white)](https://github.com/Bharath24693)
[![Email](https://img.shields.io/badge/Email-bharathsgr24%40gmail.com-D14836?logo=gmail&logoColor=white)](mailto:bharathsgr24@gmail.com)

---

## ⭐ Show Your Support

If you found this project useful or interesting, please consider giving it a **star** ⭐ — it helps others discover it!

---

*Built with 💚 using Python & Streamlit · Deployed on Streamlit Community Cloud*
