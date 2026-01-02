import streamlit as st

try:
    import feedparser
    st.success("feedparser loaded successfully")
except ImportError:
    st.error("feedparser is not installed!")

import streamlit as st
import feedparser
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="Trending Topics Dashboard", layout="wide")

st.title("🔥 Trending Topics Analysis Dashboard")
st.markdown("**TF-IDF & Word Cloud Analysis using Free Public Feeds**")

# ---------------------------------
# FUNCTION: FETCH DATA
# ---------------------------------
def fetch_titles(url, source_name):
    feed = feedparser.parse(url)
    titles = [entry.title for entry in feed.entries]
    df = pd.DataFrame(titles, columns=["title"])
    st.write(f"Total {source_name} Records:", df.shape[0])
    return df

# ---------------------------------
# FUNCTION: TF-IDF + WORD CLOUD
# ---------------------------------
def tfidf_wordcloud(df, source_name):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["title"])

    scores = tfidf_matrix.sum(axis=0).A1
    words = vectorizer.get_feature_names_out()

    tfidf_df = pd.DataFrame({
        "Word": words,
        "TF-IDF Score": scores
    }).sort_values(by="TF-IDF Score", ascending=False)

    st.subheader("📊 TF-IDF Keyword Table")
    st.dataframe(tfidf_df.head(50))

    st.subheader("☁️ Word Cloud")
    tfidf_dict = dict(zip(tfidf_df["Word"], tfidf_df["TF-IDF Score"]))

    wc = WordCloud(width=900, height=400, background_color="white")
    wc.generate_from_frequencies(tfidf_dict)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# ---------------------------------
# TABS
# ---------------------------------
tab1, tab2, tab3 = st.tabs(["🐦 Twitter", "📘 Facebook", "👽 Reddit"])

# ---------------------------------
# TWITTER TAB (Simulated via Google News)
# ---------------------------------
with tab1:
    st.header("🐦 Twitter Trending Topics")
    st.info("Twitter trends simulated using Google News RSS (Free Source)")

    twitter_url = "https://news.google.com/rss/search?q=trending+on+twitter"
    df_twitter = fetch_titles(twitter_url, "Twitter")

    st.dataframe(df_twitter.head(20))
    tfidf_wordcloud(df_twitter, "Twitter")

# ---------------------------------
# FACEBOOK TAB (Simulated via Google News)
# ---------------------------------
with tab2:
    st.header("📘 Facebook Trending Topics")
    st.info("Facebook trends simulated using Google News RSS (Free Source)")

    facebook_url = "https://news.google.com/rss/search?q=trending+on+facebook"
    df_facebook = fetch_titles(facebook_url, "Facebook")

    st.dataframe(df_facebook.head(20))
    tfidf_wordcloud(df_facebook, "Facebook")

# ---------------------------------
# REDDIT TAB (REAL DATA)
# ---------------------------------
with tab3:
    st.header("👽 Reddit Trending Topics")
    st.success("Real Reddit data using public RSS feed")

    reddit_url = "https://www.reddit.com/r/popular/.rss"
    df_reddit = fetch_titles(reddit_url, "Reddit")

    st.dataframe(df_reddit.head(20))
    tfidf_wordcloud(df_reddit, "Reddit")

# ---------------------------------
# FOOTER
# ---------------------------------
st.markdown("---")
st.markdown("✅ **Free APIs | NLP | TF-IDF | Word Cloud | Streamlit**")
