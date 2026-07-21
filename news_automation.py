from dotenv import load_dotenv
import os
import requests
from google import genai
from supabase import create_client

# ==========================
# LOAD ENVIRONMENT VARIABLES
# ==========================

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ==========================
# CLIENTS
# ==========================

client = genai.Client(api_key=GEMINI_API_KEY)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==========================
# CATEGORIES
# ==========================

CATEGORIES = [
    "AI",
    "Technology",
    "Business",
    "Health",
    "Science",
    "Sports",
    "Entertainment",
    "General"
]

# ==========================
# GEMINI CATEGORY FUNCTION
# ==========================

def get_category(title, description):

    prompt = f"""
You are a news classifier.

Classify the following news into ONLY ONE category.

Categories:
- AI
- Technology
- Business
- Health
- Science
- Sports
- Entertainment
- General

Title:
{title}

Description:
{description}

Return ONLY the category name.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        category = response.text.strip()

        if category in CATEGORIES:
            return category

        return "General"

    except Exception as e:

        print("Category Error:", e)

        return "General"


# ==========================
# GEMINI AI TITLE + SUMMARY
# ==========================

def generate_ai_content(title, description):

    prompt = f"""
Title:
{title}

Description:
{description}

Generate:

1. AI Title
2. AI Summary (3 lines)

Return exactly:

AI Title:
AI Summary:
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        text = response.text

        lines = text.split("\n")

        ai_title = ""
        ai_summary = ""

        for line in lines:

            if line.startswith("AI Title:"):

                ai_title = line.replace(
                    "AI Title:",
                    ""
                ).strip()

            elif line.startswith("AI Summary:"):

                ai_summary = line.replace(
                    "AI Summary:",
                    ""
                ).strip()

            elif ai_summary:

                ai_summary += "\n" + line

        return ai_title, ai_summary

    except Exception as e:

        print("AI Generation Error:", e)

        return title, description


# ==========================
# FETCH NEWS
# ==========================

url = (
    "https://newsapi.org/v2/everything?"
    "q=(artificial intelligence OR technology OR business "
    "OR health OR science OR sports OR entertainment)&"
    "language=en&"
    "sortBy=publishedAt&"
    "pageSize=20&"
    f"apiKey={NEWS_API_KEY}"
)

try:

    response = requests.get(url, timeout=30)

    response.raise_for_status()

    data = response.json()

    articles = data.get("articles", [])

except Exception as e:

    print("News API Error:", e)

    articles = []


print(f"\nFound {len(articles)} articles\n")


# ==========================
# PROCESS ARTICLES
# ==========================

for article in articles:

    title = article.get("title") or ""

    description = article.get("description") or ""

    article_url = article.get("url")

    source_name = (
        article.get("source", {}).get("name")
        or "Unknown"
    )

    image_url = article.get("urlToImage")

    content = article.get("content")


    # Skip articles without URL

    if not article_url:

        continue


    # ==========================
    # DUPLICATE CHECK
    # ==========================

    try:

        existing = (
            supabase
            .table("NewsData")
            .select("id")
            .eq("url", article_url)
            .execute()
        )

        if existing.data:

            print("Already Exists:", title)

            continue

    except Exception as e:

        print("Duplicate Check Error:", e)

        continue


    # ==========================
    # CATEGORY
    # ==========================

    category = get_category(
        title,
        description
    )

    print("Category:", category)


    # ==========================
    # AI TITLE + SUMMARY
    # ==========================

    ai_title, ai_summary = generate_ai_content(
        title,
        description
    )


    # ==========================
    # INSERT INTO SUPABASE
    # ==========================

    try:

        supabase.table("NewsData").insert({

            "category": category,

            "title": title,

            "description": description,

            "source": source_name,

            "content": content,

            "ai_summary": ai_summary,

            "ai_title": ai_title,

            "url": article_url,

            "image_url": image_url

        }).execute()


        print("Inserted:", title)


    except Exception as e:

        print("Supabase Insert Error:", e)


print("\nAutomation completed successfully!")