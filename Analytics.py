import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

# Connect to Supabase
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# Fetch data
response = (
    supabase
    .table("NewsData")
    .select("*")
    .execute()
)

news = response.data

df = pd.DataFrame(news)

st.title("📊 News Analytics")

st.markdown("---")

# Top Metrics
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("📰 Total Articles", len(df))

with c2:
    st.metric(
        "📂 Categories",
        df["category"].nunique()
    )

with c3:
    st.metric(
        "📰 Sources",
        df["source"].nunique()
    )

st.markdown("---")

# Articles by Category
st.subheader("📂 Articles by Category")

category_count = (
    df["category"]
    .value_counts()
    .reset_index()
)

category_count.columns = [
    "Category",
    "Articles"
]

fig = px.bar(
    category_count,
    x="Category",
    y="Articles",
    text="Articles"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Articles by Source
st.subheader("📰 Articles by Source")

source_count = (
    df["source"]
    .value_counts()
    .head(10)
    .reset_index()
)

source_count.columns = [
    "Source",
    "Articles"
]

fig2 = px.pie(
    source_count,
    names="Source",
    values="Articles"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)