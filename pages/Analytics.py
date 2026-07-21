
import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# WHITE THEME
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #ffffff;
    color: #1f2937;
}

/* Main headings */
h1, h2, h3 {
    color: #111827 !important;
}

/* Normal text */
p, label, div {
    color: #1f2937;
}

/* Metric labels */
div[data-testid="stMetricLabel"] {
    color: #4b5563 !important;
}

/* Metric values */
div[data-testid="stMetricValue"] {
    color: #111827 !important;
}

/* Horizontal lines */
hr {
    border-color: #e5e7eb !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# CONNECT TO SUPABASE
# =====================================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =====================================================
# FETCH DATA
# =====================================================

response = (
    supabase
    .table("NewsData")
    .select("*")
    .execute()
)

news = response.data or []

df = pd.DataFrame(news)


# =====================================================
# PAGE TITLE
# =====================================================

st.title("📊 News Analytics")

st.markdown("---")


# =====================================================
# HANDLE EMPTY DATA
# =====================================================

if df.empty:

    st.info(
        "No news data is available for analytics yet."
    )

    st.stop()


# =====================================================
# TOP METRICS
# =====================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "📰 Total Articles",
        len(df)
    )

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



# =====================================================
# ARTICLES BY CATEGORY
# =====================================================

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

fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(
        color="#111827"
    ),
    xaxis=dict(
        title=dict(
            text="Category",
            font=dict(color="#111827")
        ),
        tickfont=dict(
            color="#111827"
        ),
        gridcolor="#e5e7eb"
    ),
    yaxis=dict(
        title=dict(
            text="Articles",
            font=dict(color="#111827")
        ),
        tickfont=dict(
            color="#111827"
        ),
        gridcolor="#e5e7eb"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)




# =====================================================
# ARTICLES BY SOURCE
# =====================================================

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

fig2.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(
        color="#111827"
    ),
    legend=dict(
        font=dict(
            color="#111827"
        )
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

