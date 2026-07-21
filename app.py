import streamlit as st
from supabase import create_client

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI News Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# AI FUTURISTIC CSS
# =====================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background:
    linear-gradient(
        135deg,
        #ffffff,
        #f8fafc,
        #eef2ff
    );
    color:#111827;
}
/* Remove default padding */

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
}


/* Text */

h1,h2,h3,h4,h5,h6{
    color:#111827;
}

/* Header */

.hero-title{

    font-size:55px;
    font-weight:900;
    background:
    linear-gradient(
        90deg,
        #2563eb,
        #7c3aed,
        #db2777
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

}


.subtitle{

    font-size:20px;
    color:#475569;

}




/* Glass Cards */


.news-card{

    background:
    rgba(255,255,255,0.06);

    border-radius:20px;

    padding:20px;

    border:
    1px solid rgba(255,255,255,0.15);

    backdrop-filter:
    blur(10px);

    margin-bottom:20px;

}


/* Metrics */


div[data-testid="stMetric"]{

    background:#ffffff;

    border-radius:18px;

    padding:18px;

    border:
    1px solid #e5e7eb;

    box-shadow:
    0px 4px 15px rgba(0,0,0,0.08);

}


div[data-testid="stMetricLabel"]{

    color:#475569 !important;

}


div[data-testid="stMetricValue"]{

    color:#111827 !important;

}
/* Images */

img{

    border-radius:18px;

}


/* Sidebar */

section[data-testid="stSidebar"]{

    background:
    linear-gradient(
        180deg,
        #020617,
        #111827
    );

}


/* Buttons */

/* Buttons & Link Buttons */
.stButton button, .stLinkButton a {
    border-radius: 15px !important;
    background-color: #f1f5f9 !important; /* Soft light gray default background */
    color: #111827 !important;            /* Dark text color */
    border: 1px solid #e2e8f0 !important; /* Subtle border */
    text-decoration: none !important;
    transition: all 0.2s ease;
}

/* Hover effect for both button types */
.stButton button:hover, .stLinkButton a:hover {
    background-color: #e2e8f0 !important; /* Slightly darker gray on hover */
    color: #2563eb !important;            /* Blue accent text on hover */
    border-color: #cbd5e1 !important;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
}

/* Divider */

hr{

    border:
    1px solid rgba(255,255,255,0.15);

}
/* ================================
   WHITE THEME TEXT FIX
================================ */


/* All normal text */

body, p, span, label {

    color:#111827 !important;

}



/* Input labels */

.stTextInput label,
.stSelectbox label {

    color:#111827 !important;

    font-weight:600;

}



/* Search box */

div[data-baseweb="input"] {

    background:white !important;

    border-radius:12px;

}



div[data-baseweb="input"] input {

    color:#111827 !important;

}



/* Select box */

div[data-baseweb="select"] > div {

    background:white !important;

    color:#111827 !important;

    border-radius:12px;

}



div[data-baseweb="select"] span {

    color:#111827 !important;

}



/* Metric text */

div[data-testid="stMetricLabel"] {

    color:#374151 !important;

}



div[data-testid="stMetricValue"] {

    color:#111827 !important;

}



div[data-testid="stMetricDelta"] {

    color:#374151 !important;

}



/* Caption text */

.stCaption {

    color:#475569 !important;

}

/* =====================================================
   SIDEBAR TEXT & COMPONENT LIGHT FIX
   ===================================================== */

/* Force all text inside the sidebar container to be bright and legible */
section[data-testid="stSidebar"] *, 
section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebar"] label {
    color: #f8fafc !important; /* Crisp off-white */
}

/* Fix Streamlit Metrics inside the Sidebar so they match the dark theme */
section[data-testid="stSidebar"] div[data-testid="stMetric"] {
    background: #1e293b !important; /* Slate dark background for cards */
    border: 1px solid #334155 !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] div[data-testid="stMetricLabel"] {
    color: #94a3b8 !important; /* Soft gray for metric titles */
}

section[data-testid="stSidebar"] div[data-testid="stMetricValue"] {
    color: #ffffff !important; /* Bright white for metric numbers */
}

/* Fix Select box inside the Sidebar so it looks clean against dark */
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #ffffff !important;
}

/* =====================================================
   STREAMLIT NATIVE TOOLBAR & DEPLOY BUTTON FIX
   ===================================================== */

/* Fix the text color inside the footer/header developer menus */
footer, 
header, 
div[data-testid="stStatusWidget"] button, 
div[data-testid="stStatusWidget"] span,
.stAppDeployButton button,
.stAppDeployButton span {
    color: #ffffff !important; /* Force text to be bright white */
}

/* Ensure the background of the Deploy button stays clear and visible */
.stAppDeployButton button {
    background-color: #1e293b !important; /* Dark slate button background */
    border: 1px solid #334155 !important;
}

.stAppDeployButton button:hover {
    background-color: #334155 !important; /* Slightly lighter on hover */
}
/* =====================================================
   FORCE BRIGHT SIDEBAR BUTTON OVERRIDE
   ===================================================== */

/* 1. Target the actual button container element globally in the header */
.stApp header button, 
.stAppDeployButton + button,
[data-testid="stSidebarCollapseButton"] button {
    background-color: #2563eb !important; /* Forces a solid vibrant blue background box */
    border: 1px solid #60a5fa !important;
    border-radius: 8px !important;
}

/* 2. Force the arrow vector art inside that button to turn pure white */
.stApp header button svg,
.stApp header button span,
[data-testid="stSidebarCollapseButton"] button svg,
[data-testid="stSidebarCollapseButton"] button span {
    color: #ffffff !important;
    fill: #ffffff !important;
}

/* 3. Give it a nice clean hover color change */
.stApp header button:hover,
[data-testid="stSidebarCollapseButton"] button:hover {
    background-color: #1d4ed8 !important; /* Darker blue on hover */
}
</style>

""",
unsafe_allow_html=True)



# =====================================================
# LOAD SECRETS
# =====================================================


SUPABASE_URL = st.secrets["SUPABASE_URL"]

SUPABASE_KEY = st.secrets["SUPABASE_KEY"]



# =====================================================
# SUPABASE CONNECTION
# =====================================================


try:

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )


except Exception as e:

    st.error(
        f"Supabase Connection Error: {e}"
    )

    st.stop()



# =====================================================
# FETCH NEWS DATA
# =====================================================


try:

    response = (

        supabase

        .table("NewsData")

        .select("*")

        .order(
            "created_at",
            desc=True
        )

        .execute()

    )


    news = response.data or []


except Exception as e:


    st.error(
        f"Database Error: {e}"
    )

    st.stop()



# =====================================================
# CATEGORY EXTRACTION
# =====================================================


categories = sorted(

    list(

        {

            (
                article.get("category")
                or
                "Unknown"

            ).title()

            for article in news

        }

    )

)



# =====================================================
# SIDEBAR DASHBOARD
# =====================================================


st.sidebar.markdown(
    """
    <h1 style="
    color:#38bdf8;
    ">
    🤖 AI Hub
    </h1>
    """,

    unsafe_allow_html=True
)


st.sidebar.success(
    "🟢 System Online"
)



st.sidebar.metric(
    "📰 Total Articles",
    len(news)
)


st.sidebar.metric(
    "📂 Categories",
    len(categories)
)



st.sidebar.divider()



st.sidebar.subheader(
    "⚙️ Sort Intelligence"
)



sort_option = st.sidebar.selectbox(

    "",

    [

        "Newest",

        "Oldest",

        "A-Z",

        "Z-A"

    ]

)



st.sidebar.divider()



st.sidebar.markdown(
    """
    ### 🔗 Connected Services

    🧠 Google Gemini AI

    <br>

    🗄️ Supabase Database

    <br>

    🌐 Streamlit Cloud

    """,

    unsafe_allow_html=True

)



# =====================================================
# SORTING LOGIC
# =====================================================


if sort_option == "A-Z":


    news = sorted(

        news,

        key=lambda x:

        (

            x.get("ai_title")

            or

            x.get("title")

            or ""

        ).lower()

    )



elif sort_option == "Z-A":


    news = sorted(

        news,

        key=lambda x:

        (

            x.get("ai_title")

            or

            x.get("title")

            or ""

        ).lower(),

        reverse=True

    )



elif sort_option == "Oldest":


    news = list(
        reversed(news)
    )



# =====================================================
# MAIN HEADER
# =====================================================


st.markdown(

"""
<div class="hero-title">

🤖 AI News Hub

</div>


<div class="subtitle">

Your intelligent news platform powered by AI summaries

</div>

""",

unsafe_allow_html=True

)



st.write("")



# =====================================================
# SEARCH & CATEGORY FILTER
# =====================================================


search = st.text_input(

    "🔍 Search Intelligence",

    placeholder=
    "Search AI summarized news..."

)



selected_category = st.selectbox(

    "📂 Filter Category",

    [

        "All"

    ]

    +

    categories

)



# =====================================================
# FILTER ARTICLES
# =====================================================


filtered_news = []


for article in news:


    title = (

        article.get("ai_title")

        or

        article.get("title")

        or ""

    )


    category = (

        article.get("category")

        or

        "Unknown"

    )


    if search:


        if search.lower() not in title.lower():

            continue



    if selected_category != "All":


        if category.title() != selected_category:

            continue



    filtered_news.append(article)
# =====================================================
# DASHBOARD METRICS
# =====================================================


st.markdown("---")


m1, m2, m3 = st.columns(3)


with m1:

    st.metric(

        "📰 Total Intelligence",

        len(news)

    )


with m2:

    st.metric(

        "📂 Available Categories",

        len(categories)

    )


with m3:

    st.metric(

        "👁️ Current View",

        len(filtered_news)

    )



st.markdown("---")



# =====================================================
# FEATURED NEWS
# =====================================================


if filtered_news:


    featured = filtered_news[0]


    st.markdown(
        "## ⭐ Featured Intelligence"
    )


    left, right = st.columns(
        [1,2]
    )


    with left:


        if featured.get("image_url"):


            st.image(

                featured["image_url"],

                use_container_width=True

            )


        else:


            st.info(
                "📰 No Image Available"
            )



    with right:


        title = (

            featured.get("ai_title")

            or

            featured.get("title")

            or

            "Untitled"

        )


        st.subheader(title)



        st.caption(

            f"""
            📂 {(featured.get('category') or 'Unknown').title()}
            
            |
            
            📰 {featured.get('source') or 'Unknown'}
            """

        )



        if featured.get("description"):


            st.write(

                featured["description"]

            )



        if featured.get("ai_summary"):


            st.success(

                "🤖 AI Summary\n\n"

                +

                featured["ai_summary"]

            )



        if featured.get("url"):


            st.link_button(

                "🚀 Open Original Article",

                featured["url"]

            )



    st.markdown("---")



# =====================================================
# LATEST NEWS SECTION
# =====================================================


st.markdown(

"## 📰 Latest AI Intelligence"

)



articles = filtered_news[1:]



if articles:


    for article in articles:



        title = (

            article.get("ai_title")

            or

            article.get("title")

            or

            "Untitled"

        )


        category = (

            article.get("category")

            or

            "Unknown"

        )


        source = (

            article.get("source")

            or

            "Unknown"

        )



        with st.container():


            st.markdown(

            """

            <div class="news-card">

            """,

            unsafe_allow_html=True

            )



            col1, col2 = st.columns(

                [1,2]

            )



            with col1:


                if article.get("image_url"):


                    st.image(

                        article["image_url"],

                        use_container_width=True

                    )


                else:


                    st.info(

                        "📰 No Image"

                    )



            with col2:


                st.subheader(

                    title

                )


                st.caption(

                    f"📂 {category.title()}  |  📰 {source}"

                )



                if article.get("description"):


                    st.write(

                        article["description"]

                    )



                if article.get("ai_summary"):


                    st.info(

                        "🤖 "

                        +

                        article["ai_summary"]

                    )



                if article.get("content"):


                    with st.expander(

                        "📖 Read Full Content"

                    ):


                        st.write(

                            article["content"]

                        )



                if article.get("url"):


                    st.link_button(

                        "🔗 Read Article",

                        article["url"]

                    )



            st.markdown(

            "</div>",

            unsafe_allow_html=True

            )


            st.write("")



else:


    st.warning(

        """
        🔍 No articles found.

        Try changing search or category filter.
        """

    )



# =====================================================
# SIDEBAR ANALYTICS
# =====================================================


st.sidebar.divider()


st.sidebar.subheader(

    "📈 Live Analytics"

)



st.sidebar.metric(

    "Articles Displayed",

    len(filtered_news)

)



if filtered_news:


    top_category = (

        filtered_news[0]

        .get("category","Unknown")

        .title()

    )


else:


    top_category = "-"



st.sidebar.metric(

    "Trending Category",

    top_category

)



# =====================================================
# FOOTER
# =====================================================


st.markdown("---")



st.markdown(

"""

<div style="

text-align:center;

color:#94a3b8;

font-size:15px;

">


<h3 style="color:#38bdf8;">

🤖 AI News Hub

</h3>


Powered by


<b>

Google Gemini AI

</b>

&nbsp; | &nbsp;


<b>

Supabase

</b>

&nbsp; | &nbsp;


<b>

Streamlit

</b>



<br><br>


Built with ❤️ for AI powered journalism


<br>


© 2026 AI News Hub


</div>


""",

unsafe_allow_html=True

)