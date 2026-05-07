import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Water Analytics Dashboard",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("dataset.csv")

# =========================
# CLEAN COLUMN NAMES
# =========================
df.columns = df.columns.str.strip()

# =========================
# RENAME COLUMNS
# =========================
df.rename(columns={
    df.columns[0]: "Country",
    df.columns[1]: "Year",
    df.columns[2]: "Water Consumption",
}, inplace=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    df["Country"].unique()
)

filtered_df = df[df["Country"] == country]

# =========================
# TITLE
# =========================
st.title("💧 AI Water Analytics Dashboard")

st.subheader(
    "Water Consumption Analysis & Prediction System"
)

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Avg Total Consumption",
        f"{filtered_df['Water Consumption'].mean():.2f} BCM"
    )

with col2:
    st.metric(
        "Max Consumption",
        f"{filtered_df['Water Consumption'].max():.2f} BCM"
    )

with col3:
    st.metric(
        "Min Consumption",
        f"{filtered_df['Water Consumption'].min():.2f} BCM"
    )

# =========================
# TREND GRAPH
# =========================
st.header("📈 Water Consumption Trend")

fig = px.line(
    filtered_df,
    x="Year",
    y="Water Consumption",
    markers=True,
    title=f"{country} Water Consumption Trend"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# BAR CHART
# =========================
st.header("📊 Yearly Water Consumption")

bar_fig = px.bar(
    filtered_df,
    x="Year",
    y="Water Consumption",
    color="Water Consumption"
)

st.plotly_chart(bar_fig, use_container_width=True)

# =========================
# PREDICTION SECTION
# =========================
st.header("🔮 Future Water Prediction")

future_year = st.slider(
    "Select Future Year",
    2025,
    2035,
    2026
)

# Simple prediction logic
last_consumption = filtered_df["Water Consumption"].iloc[-1]

predicted_value = (
    last_consumption +
    ((future_year - 2024) * 2)
)

st.success(
    f"Predicted Water Consumption in {future_year}: "
    f"{predicted_value:.2f} BCM"
)

# =========================
# DATA TABLE
# =========================
st.header("📋 Dataset Preview")

st.dataframe(filtered_df)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "Developed using Streamlit, Python, Pandas and Plotly 🚀"
)