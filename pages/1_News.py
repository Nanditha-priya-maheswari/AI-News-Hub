import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="News | AI News Hub",
    page_icon="📰",
    layout="wide"
)


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
# CATEGORIES
# =====================================================

categories = sorted(
    {
        (article.get("category") or "Unknown").title()
        for article in news
    }
)


# =====================================================
# TITLE
# =====================================================

st.title("📰 Latest AI News")

st.caption(
    "AI generated summaries powered by Google Gemini"
)

st.markdown("---")


# =====================================================
# SEARCH & FILTER
# =====================================================

search = st.text_input(
    "🔍 Search News",
    placeholder="Search by title..."
)


selected_category = st.selectbox(
    "📂 Category",
    ["All"] + categories
)


# =====================================================
# FILTER NEWS
# =====================================================

filtered_news = []

for article in news:

    title = (
        article.get("ai_title")
        or article.get("title")
        or ""
    )

    category = (
        article.get("category")
        or "Unknown"
    )


    if search:

        if search.lower() not in title.lower():
            continue


    if selected_category != "All":

        if category.title() != selected_category:
            continue


    filtered_news.append(article)



# =====================================================
# DISPLAY NEWS
# =====================================================

if filtered_news:


    for article in filtered_news:


        title = (
            article.get("ai_title")
            or article.get("title")
            or ""
        )

        category = (
            article.get("category")
            or "Unknown"
        )

        source = (
            article.get("source")
            or "Unknown"
        )


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

                    st.write(
                        article["description"]
                    )


                if article.get("ai_summary"):

                    st.info(
                        article["ai_summary"]
                    )


                if article.get("url"):

                    st.link_button(
                        "🔗 Read Full Article",
                        article["url"]
                    )


            st.markdown("---")


else:

    st.warning(
        "No news found for your search."
    )