import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Sales": [1200, 1500, 1800, 1600, 2000, 2200],
    "Profit": [300, 400, 450, 380, 520, 610],
    "Customers": [50, 60, 75, 70, 90, 110],
    "Region": ["East"] * 3 + ["West"] * 3
}

df = pd.DataFrame(data)

st.set_page_config(page_title="Animated EDA Dashboard", layout="wide")
st.title("📊 Animated EDA Dashboard")

# Sidebar filter
region = st.sidebar.selectbox(
    "Select Region",
    df["Region"].unique()
)

# Speed control
speed = st.slider("⏱ Animation Speed (seconds)", 0.5, 3.0, 1.0)


filtered_df = df[df["Region"] == region]

# KPIs
# c1, c2, c3 = st.columns(3)
# c1.metric("Total Sales", filtered_df["Sales"].sum())
# c2.metric("Total Profit", filtered_df["Profit"].sum())
# c3.metric("Avg Profit", round(filtered_df["Profit"].mean(), 2))



# KPI placeholders
k1, k2, k3 = st.columns(3)
sales_kpi = k1.empty()
profit_kpi = k2.empty()
cust_kpi = k3.empty()

chart_placeholder = st.empty()

# Animate KPIs
for i in range(len(df)):
    sales_kpi.metric(
        label="💰 Total Sales",
        value=df.loc[i, "Sales"],
        delta=df.loc[i, "Sales"] - df.loc[i-1, "Sales"] if i > 0 else None
    )

    profit_kpi.metric(
        label="📈 Profit",
        value=df.loc[i, "Profit"],
        delta=df.loc[i, "Profit"] - df.loc[i-1, "Profit"] if i > 0 else None
    )

    cust_kpi.metric(
        label="👥 Customers",
        value=df.loc[i, "Customers"],
        delta=df.loc[i, "Customers"] - df.loc[i-1, "Customers"] if i > 0 else None
    )

    # Line chart animation
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Month"][:i+1],
        y=df["Sales"][:i+1],
        mode="lines+markers"
    ))

    fig.update_layout(
        title="📈 Sales Growth Over Time",
        xaxis_title="Month",
        yaxis_title="Sales",
        height=400
    )

    chart_placeholder.plotly_chart(fig, use_container_width=True)

    time.sleep(speed)



# Animated line chart
st.subheader("📈 Animated Sales Trend")
fig = px.line(
    filtered_df,
    x="Month",
    y="Sales",
    animation_frame="Month",
    markers=True,
    range_y=[0, filtered_df["Sales"].max() + 500],
    title="Sales Growth Over Time"
)
st.plotly_chart(fig, use_container_width=True)

# Animated bar chart
st.subheader("📊 Animated Profit Bars")
fig = px.bar(
    filtered_df,
    x="Month",
    y="Profit",
    animation_frame="Month",
    range_y=[0, filtered_df["Profit"].max() + 200],
    title="Monthly Profit Animation"
)
st.plotly_chart(fig, use_container_width=True)

# Animated scatter
st.subheader("🔄 Sales vs Profit (Animated)")
fig = px.scatter(
    df,
    x="Sales",
    y="Profit",
    color="Region",
    size="Sales",
    animation_frame="Month",
    hover_name="Region",
    range_x=[0, 2500],
    range_y=[0, 700],
    title="Sales-Profit Relationship Over Time"
)
st.plotly_chart(fig, use_container_width=True)
