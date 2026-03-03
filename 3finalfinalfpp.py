import streamlit as st
import math
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Fast Pass Pricing Optimization Model",
    page_icon="🎢",
    layout="wide"
)

# -----------------------------
# APP TITLE
# -----------------------------
st.title("Fast Pass Pricing Model")

st.write("""
Theme park revenue optimization model for dynamic Fast Pass pricing.
Adjust operational inputs to estimate the optimal price and projected revenue from fast pass sales.
This model uses preset guest behavioral factors to calculate the results.
""")

# -----------------------------
# USER INPUTS
# -----------------------------
st.sidebar.header("Operational Inputs")

attendance = st.sidebar.number_input(
    "Projected Attendance", min_value=1000, max_value=100000, value=30000, step=500
)

capacity = st.sidebar.number_input(
    "Park Capacity", min_value=5000, max_value=100000, value=42000, step=1000
)

hours = st.sidebar.number_input(
    "Operating Hours", min_value=1, max_value=24, value=12
)

ride_hr = st.sidebar.number_input(
    "Ride Capacity per Hour", min_value=100, max_value=20000, value=5000, step=500
)

allocation = st.sidebar.slider(
    "Fast Pass Allocation %",
    min_value=1,
    max_value=50,
    value=10,
    step=1
) / 100

# -----------------------------
# FIXED MODEL PARAMETERS
# -----------------------------
QUALITY = 0.7
MAX_PEN = 0.12
BASE_SENS = 0.018
BOOST = 2

# -----------------------------
# CALCULATIONS
# -----------------------------

# Supply
supply = hours * ride_hr * allocation

# Market penetration
penetration = MAX_PEN * QUALITY

# Adjusted sensitivity (crowd effect)
crowd_ratio = attendance / capacity
adj_sens = BASE_SENS / (1 + BOOST * crowd_ratio)

# Price search
prices = np.arange(0, 201, 1)

revenues = []
sold_continuous_list = []

for p in prices:
    buyers = attendance * penetration * math.exp(-adj_sens * p)
    sold_continuous = min(buyers, supply)

    revenue = p * sold_continuous

    revenues.append(revenue)
    sold_continuous_list.append(sold_continuous)

revenues = np.array(revenues)
sold_continuous_list = np.array(sold_continuous_list)

# Optimal price (continuous optimization)
idx = np.argmax(revenues)
opt_price = prices[idx]

# Round tickets for display realism
opt_sold_display = round(sold_continuous_list[idx])

# Make revenue match displayed tickets exactly
opt_revenue_display = opt_price * opt_sold_display

# -----------------------------
# OUTPUT RESULTS (STACKED CLEANLY)
# -----------------------------
st.header("Results")

st.metric("Fast Pass Supply", f"{int(supply):,} tickets")
st.write("")
st.metric("Demand Ceiling", f"{int(attendance * penetration):,} potential buyers")

st.divider()

st.metric("Optimal Price", f"${opt_price}")
st.write("")
st.metric("Tickets Sold at Optimal Price", f"{opt_sold_display:,}")
st.write("")
st.metric("Expected Revenue", f"${opt_revenue_display:,}")

# -----------------------------
# REVENUE CHART
# -----------------------------
st.subheader("Revenue vs Price")
st.line_chart(revenues)

# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.markdown("""
### About this model

This tool estimates optimal Fast Pass price points using user inputs such as crowd index and throughput to project supply and demand. Guests are modeled with set variables such as market penetration (0.12) and consumer sensitivity (0.018). Supply is calculated using park hours, ride throughput, and the % of seats allocated to fast pass riders. The goal is to identify a price that maximizes revenue while keeping lines short for guests who utilize fast pass. I hope you can find some enjoyment playing with this model, and maybe it can provide some insight.

Note: The revenue curve is continous, with no rounding involved. The displayed outcomes above the graph are rounded to whole numbers to demonstrate realistic outcomes.
""")

st.caption("Model Created by Cooper Hill")