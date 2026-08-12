from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Duolingo AI Impact Analysis",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analysis_with_ai_sentiment.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    if not DATA_PATH.exists():
        st.error(
            f"Dataset not found.\n\n"
            f"Expected:\n{DATA_PATH}"
        )
        st.stop()

    return pd.read_csv(DATA_PATH)


df = load_data()


# ============================================================
# VALIDATE DATA
# ============================================================

required_columns = [
    "reviewId",
    "content",
    "score",
    "thumbsUpCount",
    "review_length",
    "word_count",
    "rating_sentiment",
    "ai_sentiment",
    "ai_confidence"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        "Missing required columns:\n\n"
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("🦉 Duolingo AI Strategy Impact Analysis")

st.markdown(
    """
    ### Review Intelligence & Hidden Dissatisfaction Analysis

    Analyze Duolingo Google Play reviews using traditional star ratings
    and AI-based sentiment analysis to uncover hidden dissatisfaction,
    product pain points, and business opportunities.
    """
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.write(
    "Filters dynamically update the dashboard."
)


# Rating filter
rating_options = sorted(
    df["score"].dropna().unique().tolist()
)

selected_ratings = st.sidebar.multiselect(
    "Star Rating",
    options=rating_options,
    default=rating_options
)


# AI sentiment filter
sentiment_options = sorted(
    df["ai_sentiment"].dropna().unique().tolist()
)

selected_sentiments = st.sidebar.multiselect(
    "AI Sentiment",
    options=sentiment_options,
    default=sentiment_options
)


# Confidence filter
min_confidence = st.sidebar.slider(
    "Minimum AI Confidence",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.05
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    df["score"].isin(selected_ratings)
    &
    df["ai_sentiment"].isin(selected_sentiments)
    &
    (df["ai_confidence"] >= min_confidence)
].copy()


# ============================================================
# FILTER STATUS
# ============================================================

st.sidebar.divider()

st.sidebar.metric(
    "Filtered Reviews",
    f"{len(filtered_df):,}"
)

st.sidebar.metric(
    "Original Reviews",
    f"{len(df):,}"
)


if len(filtered_df) == 0:

    st.warning(
        "No reviews match the selected filters."
    )

    st.stop()


# ============================================================
# FILTERED METRICS
# ============================================================

total_reviews = len(filtered_df)

positive_ai = (
    filtered_df["ai_sentiment"] == "positive"
).sum()

negative_ai = (
    filtered_df["ai_sentiment"] == "negative"
).sum()

neutral_ai = (
    filtered_df["ai_sentiment"] == "neutral"
).sum()


ai_negative_rate = (
    negative_ai / total_reviews * 100
)


# Hidden negative:
# Positive rating + AI negative

hidden_negative = filtered_df[
    (filtered_df["ai_sentiment"] == "negative")
    &
    (filtered_df["score"].isin([4, 5]))
].copy()


visible_negative = filtered_df[
    (filtered_df["ai_sentiment"] == "negative")
    &
    (filtered_df["score"].isin([1, 2]))
].copy()


hidden_count = len(hidden_negative)

visible_count = len(visible_negative)

hidden_share = (
    hidden_count / negative_ai * 100
    if negative_ai > 0
    else 0
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

st.header("Executive Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Filtered Reviews",
    f"{total_reviews:,}"
)

col2.metric(
    "AI Positive",
    f"{positive_ai:,}",
    f"{positive_ai / total_reviews * 100:.2f}%"
)

col3.metric(
    "AI Negative",
    f"{negative_ai:,}",
    f"{ai_negative_rate:.2f}%"
)

col4.metric(
    "Hidden Negative",
    f"{hidden_count:,}"
)

col5.metric(
    "Hidden Share",
    f"{hidden_share:.2f}%"
)


st.divider()


# ============================================================
# 1. RATING DISTRIBUTION
# ============================================================

st.header("1. Rating Distribution")

rating_counts = (
    filtered_df["score"]
    .value_counts()
    .sort_index()
)


col1, col2 = st.columns([2, 1])


with col1:

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(
        rating_counts.index.astype(str),
        rating_counts.values
    )

    ax.set_xlabel("Star Rating")
    ax.set_ylabel("Number of Reviews")

    ax.set_title(
        "Distribution of Duolingo Review Ratings"
    )

    st.pyplot(fig)

    plt.close(fig)


with col2:

    rating_table = pd.DataFrame({
        "Star Rating": rating_counts.index,
        "Reviews": rating_counts.values
    })

    st.dataframe(
        rating_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 2. RATING VS AI SENTIMENT
# ============================================================

st.header(
    "2. Rating-Based vs AI-Based Sentiment"
)


rating_sentiment = (
    filtered_df["rating_sentiment"]
    .value_counts(normalize=True)
    .mul(100)
)


ai_sentiment = (
    filtered_df["ai_sentiment"]
    .value_counts(normalize=True)
    .mul(100)
)


sentiment_order = [
    "positive",
    "neutral",
    "negative"
]


comparison = pd.DataFrame({

    "Rating-Based (%)":
        rating_sentiment
        .reindex(sentiment_order)
        .fillna(0),

    "AI-Based (%)":
        ai_sentiment
        .reindex(sentiment_order)
        .fillna(0)
})


st.dataframe(
    comparison.round(2),
    use_container_width=True
)


fig, ax = plt.subplots(figsize=(8, 4))

x = range(len(sentiment_order))

width = 0.35


ax.bar(
    [i - width / 2 for i in x],
    comparison["Rating-Based (%)"],
    width,
    label="Rating-Based"
)


ax.bar(
    [i + width / 2 for i in x],
    comparison["AI-Based (%)"],
    width,
    label="AI-Based"
)


ax.set_xticks(list(x))

ax.set_xticklabels(
    [
        s.capitalize()
        for s in sentiment_order
    ]
)

ax.set_ylabel(
    "Percentage of Reviews"
)

ax.set_title(
    "Rating-Based vs AI-Based Sentiment"
)

ax.legend()

st.pyplot(fig)

plt.close(fig)


# ============================================================
# 3. AI NEGATIVE BY STAR RATING
# ============================================================

st.header(
    "3. AI-Detected Negative Sentiment by Star Rating"
)


negative_by_rating = (
    filtered_df.groupby("score")["ai_sentiment"]
    .apply(
        lambda x:
        (x == "negative").sum()
    )
)


total_by_rating = (
    filtered_df.groupby("score")
    .size()
)


negative_rate = (
    negative_by_rating
    / total_by_rating
    * 100
)


negative_table = pd.DataFrame({

    "Total Reviews":
        total_by_rating,

    "AI Negative Reviews":
        negative_by_rating,

    "AI Negative Rate (%)":
        negative_rate.round(2)
})


st.dataframe(
    negative_table,
    use_container_width=True
)


fig, ax = plt.subplots(figsize=(8, 4))


ax.bar(
    negative_table.index.astype(str),
    negative_table["AI Negative Rate (%)"]
)


ax.set_xlabel(
    "Star Rating"
)

ax.set_ylabel(
    "AI-Negative Reviews (%)"
)

ax.set_title(
    "AI-Detected Negative Sentiment by Star Rating"
)


st.pyplot(fig)

plt.close(fig)


# ============================================================
# 4. HIDDEN DISSATISFACTION
# ============================================================

st.header(
    "4. Hidden Dissatisfaction"
)


st.markdown(
    """
    Hidden dissatisfaction represents reviews where users give the
    app **4–5 stars**, but AI detects negative sentiment in the
    written review.
    """
)


c1, c2, c3 = st.columns(3)


c1.metric(
    "AI Negative Reviews",
    f"{negative_ai:,}"
)


c2.metric(
    "Visible Negative",
    f"{visible_count:,}"
)


c3.metric(
    "Hidden Negative",
    f"{hidden_count:,}",
    f"{hidden_share:.2f}%"
)


fig, ax = plt.subplots(figsize=(8, 4))


ax.bar(
    [
        "Visible Negative",
        "Hidden Negative"
    ],
    [
        visible_count,
        hidden_count
    ]
)


ax.set_ylabel(
    "Number of Reviews"
)

ax.set_title(
    "Visible vs Hidden Negative Experiences"
)


st.pyplot(fig)

plt.close(fig)


# ============================================================
# 5. HIDDEN COMPLAINTS BY STAR RATING
# ============================================================

st.header(
    "5. Hidden Complaints by Star Rating"
)


hidden_by_rating = (
    hidden_negative["score"]
    .value_counts()
    .sort_index()
)


if len(hidden_by_rating) > 0:

    hidden_rating_table = (
        hidden_by_rating
        .rename("Hidden Complaints")
        .to_frame()
    )

    st.dataframe(
        hidden_rating_table,
        use_container_width=True
    )


    fig, ax = plt.subplots(figsize=(8, 4))


    ax.bar(
        hidden_rating_table.index.astype(str),
        hidden_rating_table[
            "Hidden Complaints"
        ]
    )


    ax.set_xlabel(
        "Star Rating"
    )

    ax.set_ylabel(
        "Hidden Complaints"
    )

    ax.set_title(
        "Hidden Complaints by Star Rating"
    )


    st.pyplot(fig)

    plt.close(fig)

else:

    st.info(
        "No hidden complaints match the current filters."
    )


# ============================================================
# 6. DYNAMIC BUSINESS THEME ANALYSIS
# ============================================================

st.header(
    "6. Business Pain Points in Filtered Reviews"
)


theme_keywords = {

    "Energy System": [
        "energy",
        "hearts",
        "heart",
        "battery"
    ],

    "UI / Features": [
        "widget",
        "icon",
        "interface",
        "ui",
        "update",
        "feature",
        "option",
        "button"
    ],

    "Subscription / Pricing": [
        "subscription",
        "subscribe",
        "monthly plan",
        "yearly",
        "annual",
        "price",
        "pricing",
        "expensive",
        "cost",
        "pay",
        "paid"
    ],

    "Ads": [
        "ad",
        "ads",
        "advertisement",
        "advertisements"
    ],

    "Monetization / Gems": [
        "gem",
        "gems",
        "purchase",
        "purchases",
        "spending",
        "spend",
        "money"
    ],

    "Bugs / Crashes": [
        "bug",
        "bugs",
        "crash",
        "crashed",
        "crashes",
        "error",
        "glitch",
        "broken"
    ]
}


theme_results = []


for theme, keywords in theme_keywords.items():

    pattern = "|".join(
        pd.Series(keywords)
        .str.replace(
            r"([.^$*+?{}\[\]\\|()])",
            r"\\\1",
            regex=True
        )
    )

    mask = (
        filtered_df["content"]
        .fillna("")
        .str.lower()
        .str.contains(
            pattern,
            regex=True,
            na=False
        )
    )

    count = mask.sum()

    percentage = (
        count / len(filtered_df) * 100
    )

    theme_results.append({

        "Theme": theme,

        "Reviews": count,

        "% of Filtered Reviews":
            round(percentage, 2)
    })


dynamic_theme_summary = (
    pd.DataFrame(theme_results)
    .sort_values(
        "Reviews",
        ascending=False
    )
    .reset_index(drop=True)
)


st.dataframe(
    dynamic_theme_summary,
    use_container_width=True,
    hide_index=True
)


fig, ax = plt.subplots(figsize=(9, 5))


plot_data = (
    dynamic_theme_summary
    .sort_values("Reviews")
)


ax.barh(
    plot_data["Theme"],
    plot_data["Reviews"]
)


ax.set_xlabel(
    "Reviews"
)

ax.set_ylabel(
    "Business Theme"
)

ax.set_title(
    "Business Pain Points in Filtered Reviews"
)


st.pyplot(fig)

plt.close(fig)


# ============================================================
# 7. FINAL VALIDATED BUSINESS PRIORITY MATRIX
# ============================================================

st.header(
    "7. Final Validated Business Priority Matrix"
)


st.info(
    "This section is intentionally not affected by dashboard "
    "filters. These are the final validated findings from the "
    "complete 10,000-review analysis."
)


priority_matrix = pd.DataFrame({

    "Theme": [
        "Energy System",
        "UI / Features",
        "Subscription / Pricing",
        "Ads",
        "Monetization / Gems",
        "Bugs / Crashes"
    ],

    "Reviews": [
        15,
        13,
        11,
        9,
        8,
        7
    ],

    "Priority": [
        "Critical",
        "Critical",
        "High",
        "Medium",
        "Medium",
        "Lower"
    ],

    "AI Strategy": [

        "Optimize energy/heart mechanics using personalized practice and recovery options.",

        "Use AI-driven feedback analysis to identify frustrating features and prioritize UX improvements.",

        "Use churn-risk prediction and personalized offers to reduce subscription friction.",

        "Optimize ad frequency and timing based on predicted user frustration.",

        "Personalize rewards and monetization without disrupting the learning experience.",

        "Use automated issue detection and complaint clustering to prioritize recurring technical problems."
    ]
})


st.dataframe(
    priority_matrix,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 8. REVIEW EXPLORER
# ============================================================

st.header(
    "8. Review Explorer"
)


search_term = st.text_input(
    "Search review text",
    placeholder="Try: energy, subscription, ads, lessons..."
)


explorer_df = filtered_df.copy()


if search_term:

    explorer_df = explorer_df[
        explorer_df["content"]
        .fillna("")
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    ]


display_columns = [
    "score",
    "rating_sentiment",
    "ai_sentiment",
    "ai_confidence",
    "thumbsUpCount",
    "content"
]


explorer_df = (
    explorer_df[
        display_columns
    ]
    .sort_values(
        "ai_confidence",
        ascending=False
    )
    .head(100)
)


st.dataframe(
    explorer_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 9. HIGH-CONFIDENCE HIDDEN COMPLAINTS
# ============================================================

st.header(
    "9. High-Confidence Hidden Complaints"
)


high_confidence_hidden = filtered_df[
    (filtered_df["ai_sentiment"] == "negative")
    &
    (filtered_df["score"].isin([4, 5]))
    &
    (filtered_df["ai_confidence"] >= 0.80)
].copy()


high_confidence_hidden = (
    high_confidence_hidden[
        [
            "score",
            "ai_confidence",
            "thumbsUpCount",
            "content"
        ]
    ]
    .sort_values(
        "ai_confidence",
        ascending=False
    )
    .head(20)
)


if len(high_confidence_hidden) > 0:

    st.dataframe(
        high_confidence_hidden,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No high-confidence hidden complaints "
        "match the current filters."
    )


# ============================================================
# FINAL TAKEAWAY
# ============================================================

st.divider()

st.header(
    "🎯 Strategic Takeaway"
)


st.markdown(
    f"""
    The current filtered dataset contains **{total_reviews:,} reviews**.

    AI identifies **{negative_ai:,} negative reviews**
    ({ai_negative_rate:.2f}% of filtered reviews).

    Among these, **{hidden_count:,} reviews** represent hidden
    dissatisfaction where users gave 4–5 stars despite negative
    sentiment.

    The dashboard allows these patterns to be explored dynamically
    using star rating, AI sentiment and model confidence filters.
    """
)


st.divider()

st.caption(
    "Duolingo AI Strategy Impact Analysis • "
    "Google Play Reviews • "
    "AI Sentiment Intelligence"
)