import streamlit as st
from supabase import create_client
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI News Hub",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

div[data-testid="stMetric"]{
    border-radius:12px;
    padding:10px;
    border:1px solid #ddd;
}

img{
    border-radius:12px;
}

hr{
    margin-top:25px;
    margin-bottom:25px;
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
# FETCH NEWS
# =====================================================

try:

    response = (
        supabase
        .table("NewsData")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    news = response.data or []

except Exception as e:

    st.error(f"Database Error: {e}")
    st.stop()

# =====================================================
# GET CATEGORIES
# =====================================================

categories = sorted(
    list(
        {
            (article.get("category") or "Unknown").title()
            for article in news
        }
    )
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📊 Dashboard")

st.sidebar.success("🟢 Connected")

st.sidebar.metric(
    "📰 Articles",
    len(news)
)

st.sidebar.metric(
    "📂 Categories",
    len(categories)
)

st.sidebar.markdown("---")

st.sidebar.subheader("Sort News")

sort_option = st.sidebar.selectbox(
    "",
    [
        "Newest",
        "Oldest",
        "A-Z",
        "Z-A"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info("🤖 Google Gemini")

st.sidebar.info("🗄️ Supabase")

st.sidebar.info("🌐 Streamlit")

# =====================================================
# SORT NEWS
# =====================================================

if sort_option == "A-Z":

    news = sorted(
        news,
        key=lambda x: (x.get("ai_title") or "").lower()
    )

elif sort_option == "Z-A":

    news = sorted(
        news,
        key=lambda x: (x.get("ai_title") or "").lower(),
        reverse=True
    )

elif sort_option == "Oldest":

    news = list(reversed(news))

# =====================================================
# HEADER
# =====================================================

st.title("📰 AI News Hub")

st.caption(
    "AI Powered News Summaries using Google Gemini"
)

st.markdown("---")

# =====================================================
# SEARCH
# =====================================================

search = st.text_input(
    "🔍 Search News",
    placeholder="Search by title..."
)

selected_category = st.selectbox(
    "📂 Select Category",
    ["All"] + categories
)

# =====================================================
# METRICS
# =====================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Articles",
        len(news)
    )

with c2:
    st.metric(
        "Categories",
        len(categories)
    )

with c3:
    st.metric(
        "Search",
        search if search else "None"
    )

st.markdown("---")




# =====================================================
# FILTER ARTICLES
# =====================================================

filtered_news = []

for article in news:

    title = article.get("ai_title") or article.get("title") or ""
    category = article.get("category") or "Unknown"

    # Search Filter
    if search:
        if search.lower() not in title.lower():
            continue

    # Category Filter
    if selected_category != "All":
        if category.title() != selected_category:
            continue

    filtered_news.append(article)

# =====================================================
# FEATURED NEWS
# =====================================================

if filtered_news:

    featured = filtered_news[0]

    st.markdown("## 🌟 Featured News")

    feature_left, feature_right = st.columns([1, 2])

    with feature_left:

        if featured.get("image_url"):
            st.image(
                featured["image_url"],
                width=300
            )

    with feature_right:

        st.subheader(
            featured.get("ai_title")
            or featured.get("title")
        )

        st.caption(
            f"📂 {(featured.get('category') or 'Unknown').title()} | "
            f"📰 {featured.get('source') or 'Unknown'}"
        )

        if featured.get("description"):
            st.write(featured["description"])

        if featured.get("ai_summary"):
            st.success(featured["ai_summary"])

        if featured.get("url"):
            st.link_button(
                "🔗 Read Featured Article",
                featured["url"]
            )

    st.markdown("---")

# =====================================================
# LATEST NEWS
# =====================================================

st.header("📰 Latest News")

for article in filtered_news[1:]:

    title = article.get("ai_title") or article.get("title") or ""
    category = article.get("category") or "Unknown"
    source = article.get("source") or "Unknown"

    with st.container():

        left, right = st.columns([1, 2])

        with left:

            if article.get("image_url"):
                st.image(
                    article["image_url"],
                    width=230
                )

        with right:

            st.subheader(title)

            st.caption(
                f"📂 {category.title()} | 📰 {source}"
            )

            if article.get("description"):
                st.write(article["description"])

            if article.get("ai_summary"):
                st.info(article["ai_summary"])

            if article.get("content"):
                with st.expander("📖 Read Original Article"):
                    st.write(article["content"])

            if article.get("url"):
                st.link_button(
                    "🔗 Read Full Article",
                    article["url"]
                )

        st.markdown("---")





# =====================================================
# EMPTY SEARCH RESULT
# =====================================================

if not filtered_news:

    st.warning(
        "🔍 No articles found.\n\nTry another keyword or category."
    )

# =====================================================
# SIDEBAR SUMMARY
# =====================================================

st.sidebar.markdown("---")

st.sidebar.subheader("📈 Statistics")

st.sidebar.metric(
    "Showing Articles",
    len(filtered_news)
)

if news:

    latest_category = (
        filtered_news[0].get("category", "Unknown").title()
        if filtered_news
        else "-"
    )

    st.sidebar.metric(
        "Top Category",
        latest_category
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:gray; font-size:14px;">
        ❤️ Built using <b>Streamlit</b>, <b>Supabase</b> and
        <b>Google Gemini AI</b><br><br>
        © 2026 AI News Hub
    </div>
    """,
    unsafe_allow_html=True
)