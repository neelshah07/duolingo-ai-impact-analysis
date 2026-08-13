# 🦉 Duolingo AI Strategy Impact Analysis

## User Sentiment, Hidden Dissatisfaction & Business Impact Analysis

An end-to-end Data Science and AI project analyzing **10,000 Duolingo Google Play reviews** to understand user sentiment, uncover dissatisfaction hidden behind positive ratings, identify product pain points, and translate review intelligence into actionable business strategies.

The project combines traditional **star-rating sentiment** with **AI-based text sentiment analysis** and an interactive **Streamlit dashboard**.

---

## 🎯 Business Problem

Star ratings provide a simple measure of customer satisfaction, but they do not always capture the complete user experience.

A user may give Duolingo a **4- or 5-star rating** while still mentioning:

- Frustration with the energy/heart system
- Unwanted advertisements
- Subscription or pricing concerns
- Feature and UI problems
- Monetization and gem-related issues
- Bugs or technical problems

This creates a potential gap between what a rating communicates and what the written review actually says.

### Core Question

> **Can AI-powered sentiment analysis uncover dissatisfaction that traditional star ratings fail to capture?**

---

# 🔬 Project Objectives

The project aims to:

1. Analyze Duolingo user reviews from Google Play.
2. Clean and preprocess review text.
3. Compare rating-based sentiment with AI-based sentiment.
4. Identify negative sentiment hidden inside positive ratings.
5. Investigate the themes behind hidden dissatisfaction.
6. Prioritize major business pain points.
7. Translate findings into AI-driven strategic recommendations.
8. Build an interactive dashboard for business exploration.

---

# 📊 Dataset

The project analyzes:

**10,000 Duolingo Google Play reviews**

### Important fields

| Field | Description |
|---|---|
| `reviewId` | Unique review identifier |
| `userName` | Reviewer name |
| `content` | Original review text |
| `score` | Star rating |
| `thumbsUpCount` | Review engagement |
| `reviewCreatedVersion` | App version associated with review |
| `at` | Review timestamp |
| `appVersion` | App version |
| `review_length` | Character length of review |
| `word_count` | Number of words |
| `clean_text` | Cleaned review text |
| `rating_sentiment` | Sentiment derived from rating |
| `ai_sentiment` | AI-generated sentiment |
| `ai_confidence` | AI prediction confidence |

---

# 🧠 Methodology

```text
Google Play Reviews
        │
        ▼
Data Collection
        │
        ▼
Text Cleaning & Preprocessing
        │
        ▼
Feature Engineering
        │
        ├───────────────┐
        ▼               ▼
Rating Sentiment    AI Sentiment
        │               │
        └───────┬───────┘
                ▼
       Sentiment Comparison
                │
                ▼
    Hidden Dissatisfaction
                │
                ▼
      Complaint Theme Analysis
                │
                ▼
       Business Prioritization
                │
                ▼
      AI Strategy Recommendations
                │
                ▼
       Interactive Dashboard
```
