import streamlit as st
import snscrape.modules.twitter as sntwitter
import json
import os
from datetime import datetime

TWEET_FILE = "tweets.jsonl"
SCREENSHOT_DIR = "screenshots"

# Load tweet data from file
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

# Check if a tweet still exists on Twitter
def is_tweet_deleted(tweet_id):
    try:
        items = list(sntwitter.TwitterTweetScraper(tweet_id).get_items())
        return len(items) == 0
    except:
        return True

# Streamlit Layout
st.set_page_config(page_title="Tweet Watcher", layout="centered")
st.title("📡 Tweet Watcher Dashboard")
st.markdown("Monitoring tweets from a specific user with screenshots. Updated every 5 minutes.")

# Load and filter tweets
tweets = load_tweets()
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

# Display each tweet
for tweet in filtered:
    st.markdown("---")
    st.markdown(f"**🕒 {tweet['date']}**")

    # Check for deleted tweet
    is_deleted = is_tweet_deleted(tweet["id"])
    if is_deleted:
        st.markdown("🟥 **This tweet appears to have been deleted.**")

    # Show stats and link
    st.markdown(f"**👍 {tweet.get('likes', 0)}** &nbsp;&nbsp; **🔁 {tweet.get('retweets', 0)}**", unsafe_allow_html=True)
    st.markdown(f"[View on Twitter]({tweet['url']})")
    st.markdown(tweet["content"])

    # Show screenshot
    screenshot_path = tweet.get("screenshot")
    if screenshot_path and os.path.exists(screenshot_path):
        st.image(screenshot_path, use_column_width=True)
