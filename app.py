import streamlit as st
import json
import os
from datetime import datetime

TWEET_FILE = "tweets.jsonl"
SCREENSHOT_DIR = "screenshots"

# Load tweet data
def load_tweets():
    tweets = []
    if os.path.exists(TWEET_FILE):
        with open(TWEET_FILE, "r") as f:
            for line in f:
                try:
                    tweet = json.loads(line)
                    tweets.append(tweet)
                except:
                    pass
    return sorted(tweets, key=lambda x: x["date"], reverse=True)

# App Layout
st.set_page_config(page_title="Tweet Watcher", layout="centered")
st.title("📡 Tweet Watcher Dashboard")
st.markdown("Monitoring tweets with screenshots. Updated every 5 mins.")

tweets = load_tweets()

# Search and Filter
search = st.text_input("🔍 Search tweets")
date_filter = st.date_input("📅 Filter by date (optional)", value=None)

filtered = []
for t in tweets:
    match = True
    if search and search.lower() not in t["content"].lower():
        match = False
    if date_filter:
        tweet_date = datetime.fromisoformat(t["date"]).date()
        if tweet_date != date_filter:
            match = False
    if match:
        filtered.append(t)

st.write(f"Showing {len(filtered)} result(s)")

for tweet in filtered:
    st.markdown(f"---")
    st.markdown(f"**🕒 {tweet['date']}**")
    
    # ✅ ADD THIS LINE BELOW:
    st.markdown(f"👍 {tweet.get('likes', 0)}  🔁 {tweet.get('retweets', 0)}")

    st.markdown(f"[View on Twitter]({tweet['url']})")
    st.markdown(tweet["content"])

    screenshot_path = tweet.get("screenshot")
    if screenshot_path and os.path.exists(screenshot_path):
        st.image(screenshot_path, use_column_width=True)
