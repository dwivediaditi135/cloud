import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
import pandas as pd
import os
import re
from collections import Counter

# ─── HELPER FUNCTIONS ───────────────────────────────────────────────────────

# Load API key
YOUTUBE_API_KEY = st.secrets["YOUTUBE"]["API_KEY"]

# Fetch YouTube trending video titles/descriptions for query
def fetch_youtube_trending(query, max_results=50):
    try:
        url = (
            f"https://www.googleapis.com/youtube/v3/search?"
            f"part=snippet&q={query}&type=video&maxResults={max_results}"
            f"&key={YOUTUBE_API_KEY}"
        )
        res = requests.get(url).json()
        if "error" in res:
            return f"API Error: {res['error']['message']}"

        text = ""
        for item in res.get("items", []):
            title = item["snippet"]["title"]
            desc = item["snippet"]["description"]
            text += f" {title} {desc}"
        return text.strip()

    except Exception as e:
        return f"Network Error: {e}"

# Clean and count words
def clean_and_count(text, min_word_length=3):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = [w for w in text.split() if len(w) >= min_word_length]
    freq = Counter(words)
    return freq

# Generate and display wordcloud
def generate_wordcloud(freq_dict):
    wc = WordCloud(
        width=800,
        height=400,
        background_color='white'
    ).generate_from_frequencies(freq_dict)

    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# ─── STREAMLIT UI ───────────────────────────────────────────────────────────

st.set_page_config(page_title="Enhanced WordCloud Dashboard", layout="wide")
st.title("🔥 Enhanced WordCloud Dashboard (YouTube Trends)")

tabs = st.tabs(["Topic 1", "Topic 2", "Topic 3"])

for i, tab in enumerate(tabs, start=1):
    with tab:
        st.header(f"📌 Analyze Topic {i}")

        query = st.text_input(
            f"Enter a trending keyword for Topic {i}",
            value=f"Trending Topic {i}"
        )

        max_videos = st.slider(
            f"How many videos to analyze for Topic {i}?",
            min_value=10, max_value=100, value=30
        )

        if st.button(f"Generate WordCloud {i}"):
            with st.spinner("Fetching & processing data..."):
                raw_text = fetch_youtube_trending(query, max_results=max_videos)

                if raw_text.startswith("API Error") or raw_text.startswith("Network Error"):
                    st.error(raw_text)
                elif len(raw_text) < 10:
                    st.warning("No text found for that topic.")
                else:
                    # get frequencies
                    freq = clean_and_count(raw_text)
                    if not freq:
                        st.warning("Not enough valid words found.")
                    else:
                        # show top frequencies
                        freq_df = (
                            pd.DataFrame(freq.items(), columns=["Word", "Count"])
                            .sort_values(by="Count", ascending=False)
                            .reset_index(drop=True)
                        )

                        st.subheader("📊 Word Frequency Table")
                        st.dataframe(freq_df.head(50), use_container_width=True)

                        st.subheader("☁️ WordCloud")
                        generate_wordcloud(dict(freq_df.head(200).values))
