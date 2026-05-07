import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="AI Water Analytics Dashboard",
    layout="wide"
)

# LOAD DATA
df = pd.read_csv("dataset.csv")

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip()

# SHOW ORIGINAL COLUMNS
st.write("Dataset Columns:", df.columns)

# AUTO DETECT COLUMNS
country_col = df.columns[0]
year_col = df.columns[1]
water_col = df.columns[2]

# RENAME
df.rename(columns={
    country_col: "Country",
    year_col: "Year",
    water_col: "Water Consumption"
}, inplace=True)

# SIDEBAR
st.sidebar.title("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    df["Country"].unique()
)

filtered_df = df[df["Country"] == country]

# TITLE
st.title("💧 AI Water Analytics Dashboard")

st.subheader(
    "Water Consumption Analysis & Prediction System"
)

# METRICS
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Consumption",
        f"{filtered_df['Water Consumption'].mean():.2f} BCM"
    )

with col2:
    st.metric(
        "Maximum Consumption",
        f"{filtered_df['Water Consumption'].max():.2f} BCM"
    )

with col3:
    st.metric(
        "Minimum Consumption",
        f"{filtered_df['Water Consumption'].min():.2f} BCM"
    )

# LINE CHART
st.header("📈 Water Consumption Trend")

fig = px.line(
    filtered_df,
    x="Year",
    y="Water Consumption",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# BAR CHART
st.header("📊 Water Consumption Chart")

bar_fig = px.bar(
    filtered_df,
    x="Year",
    y="Water Consumption",
    color="Water Consumption"
)

st.plotly_chart(bar_fig, use_container_width=True)

# PREDICTION
st.header("🔮 Future Prediction")

future_year = st.slider(
    "Select Future Year",
    2025,
    2035,
    2026
)

last_value = filtered_df["Water Consumption"].iloc[-1]

predicted_value = last_value + (
    (future_year - 2024) * 2
)

st.success(
    f"Predicted Water Consumption for {future_year}: "
    f"{predicted_value:.2f} BCM"
)

# DATASET
st.header("📋 Dataset")

st.dataframe(filtered_df)

# FOOTER
st.markdown("---")
st.markdown(
    "Developed with Streamlit, Python, Pandas & Plotly 🚀"
)