import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from sklearn.linear_model import LinearRegression

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
# SIMPLE ML MODEL
# =========================

X = np.array([[100], [200], [300], [400], [500], [600]])

y = np.array([120, 220, 320, 420, 520, 620])

simple_model = LinearRegression()

simple_model.fit(X, y)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🌍 Filters")

country = st.sidebar.selectbox(
    "Select Country",
    df["Country"].unique()
)

country_data = df[df["Country"] == country]

# =========================
# MENU
# =========================

menu = st.sidebar.radio(
    "Select Option",
    ["Dashboard", "Prediction"]
)

# =========================
# TITLE
# =========================

st.title("💧 AI Water Analytics Dashboard")

st.write("Water Consumption Analysis & Prediction System")

# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Avg Total Consumption",
            f"{country_data['Total Water Consumption (Billion Cubic Meters)'].mean():.2f} BCM"
        )

    with col2:
        st.metric(
            "Per Capita Usage",
            f"{country_data['Per Capita Water Use (Liters per Day)'].mean():.2f} L/day"
        )

    with col3:
        st.metric(
            "Agriculture Usage",
            f"{country_data['Agricultural Water Use (%)'].mean():.2f}%"
        )

    # LINE CHART

    st.header("📈 Water Consumption Trend")

    line_fig = px.line(
        country_data,
        x="Year",
        y="Total Water Consumption (Billion Cubic Meters)",
        markers=True,
        title="Yearly Water Consumption"
    )

    st.plotly_chart(line_fig, use_container_width=True)

    # BAR CHART

    st.header("📊 Water Usage Analysis")

    bar_fig = px.bar(
        country_data,
        x="Year",
        y="Per Capita Water Use (Liters per Day)",
        color="Water Scarcity Level",
        barmode="group",
        title="Per Capita Water Usage"
    )

    st.plotly_chart(bar_fig, use_container_width=True)

    # PIE CHART

    st.header("🌍 Water Scarcity Distribution")

    scarcity_count = country_data["Water Scarcity Level"].value_counts()

    pie_fig = px.pie(
        values=scarcity_count.values,
        names=scarcity_count.index,
        title="Water Scarcity Levels"
    )

    st.plotly_chart(pie_fig, use_container_width=True)

    # AREA CHART

    st.header("🌧 Agricultural Water Usage")

    area_fig = px.area(
        country_data,
        x="Year",
        y="Agricultural Water Use (%)",
        title="Agriculture Water Usage Over Years"
    )

    st.plotly_chart(area_fig, use_container_width=True)

    # DATASET

    st.header("📋 Dataset Preview")

    st.dataframe(country_data)

# =========================================================
# PREDICTION
# =========================================================

elif menu == "Prediction":

    st.header("🔮 Water Usage Prediction")

    st.sidebar.header("📅 Enter 7 Days Water Usage")

    day1 = st.sidebar.number_input("Day 1 Usage", min_value=0.0)
    day2 = st.sidebar.number_input("Day 2 Usage", min_value=0.0)
    day3 = st.sidebar.number_input("Day 3 Usage", min_value=0.0)
    day4 = st.sidebar.number_input("Day 4 Usage", min_value=0.0)
    day5 = st.sidebar.number_input("Day 5 Usage", min_value=0.0)
    day6 = st.sidebar.number_input("Day 6 Usage", min_value=0.0)
    day7 = st.sidebar.number_input("Day 7 Usage", min_value=0.0)

    user_input = [
        day1, day2, day3,
        day4, day5, day6, day7
    ]

    if st.button("Predict Water Usage"):

        avg_usage = sum(user_input) / len(user_input)

        prediction = simple_model.predict([[avg_usage]])[0]

        st.success(
            f"Predicted Next Day Water Usage: {prediction:.2f} Litres"
        )

        if prediction > 500:

            st.error(
                "⚠ High Water Usage Predicted. Please conserve water."
            )

        elif prediction > 300:

            st.warning(
                "💧 Moderate Usage. Try saving more water."
            )

        else:

            st.success(
                "✅ Great! Water usage is under control."
            )

# =========================================================
# FOOTER
# =========================================================

st.success("✅ AI Water Dashboard Running Successfully")