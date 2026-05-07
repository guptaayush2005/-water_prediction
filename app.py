import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="AI Water Analytics Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("cleaned_global_water_consumption.csv")

# Sidebar
st.sidebar.title("🌍 Filters")

country = st.sidebar.selectbox(
    "Select Country",
    df["Country"].unique()
)

country_data = df[df["Country"] == country]

menu = st.sidebar.radio(
    "Select Option",
    ["Dashboard", "Prediction"]
)

# Title
st.title("💧 AI Water Analytics Dashboard")
st.write("Water Consumption Analysis & Prediction System")

# Dashboard
if menu == "Dashboard":

    st.subheader("📊 Country Water Data")

    st.dataframe(country_data)

    fig = px.line(
        country_data,
        x="Year",
        y="Total Water Consumption (Billion Cubic Meters)",
        markers=True,
        title="Water Consumption Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

# Prediction
elif menu == "Prediction":

    st.subheader("🔮 Water Usage Prediction")

    usage = st.number_input(
        "Enter Average Water Usage",
        min_value=0.0
    )

    # Simple ML Model
    X = np.array([[100], [200], [300], [400], [500]])
    y = np.array([120, 220, 320, 420, 520])

    model = LinearRegression()
    model.fit(X, y)

    if st.button("Predict"):

        prediction = model.predict([[usage]])[0]

        st.success(
            f"Predicted Water Usage: {prediction:.2f} Litres"
        )

st.success("✅ Dashboard Running Successfully")