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
df = pd.read_csv("cleaned_global_water_consumption.csv")

# =========================
# TITLE
# =========================
st.title("💧 AI Water Analytics Dashboard")
st.subheader("Water Consumption Analysis & Prediction System")

# =========================
# SIDEBAR
# =========================
country = st.sidebar.selectbox(
    "Select Country",
    df["Country"].unique()
)

filtered_df = df[df["Country"] == country]

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Avg Total Consumption",
        f"{filtered_df['Total Water Consumption (BCM)'].mean():.2f} BCM"
    )

with col2:
    st.metric(
        "Per Capita Usage",
        f"{filtered_df['Per Capita Usage (Liters per day)'].mean():.2f} L/day"
    )

with col3:
    st.metric(
        "Agriculture Usage",
        f"{filtered_df['Agriculture Water Usage (%)'].mean():.2f}%"
    )

# =========================
# LINE CHART
# =========================
st.header("📈 Water Consumption Trend")

fig = px.line(
    filtered_df,
    x="Year",
    y="Total Water Consumption (BCM)",
    markers=True,
    title="Yearly Water Consumption"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# BAR CHART
# =========================
st.header("🏭 Sector-wise Water Usage")

sector_data = {
    "Sector": ["Agriculture", "Industrial", "Domestic"],
    "Usage": [
        filtered_df["Agriculture Water Usage (%)"].mean(),
        filtered_df["Industrial Water Usage (%)"].mean(),
        filtered_df["Domestic Water Usage (%)"].mean()
    ]
}

sector_df = pd.DataFrame(sector_data)

bar_fig = px.bar(
    sector_df,
    x="Sector",
    y="Usage",
    title="Sector-wise Water Usage (%)"
)

st.plotly_chart(bar_fig, use_container_width=True)

# =========================
# AI PREDICTION
# =========================
st.header("🤖 AI Water Prediction")

year_input = st.number_input(
    "Enter Future Year",
    min_value=2025,
    max_value=2100,
    value=2030
)

prediction = np.random.randint(500, 800)

st.success(
    f"Predicted Water Consumption for {year_input}: {prediction} BCM"
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
st.markdown("Made with ❤️ using Streamlit")