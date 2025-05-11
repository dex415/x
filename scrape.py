import snscrape.modules.twitter as sntwitter
import datetime
import json
import os
from playwright.sync_api import sync_playwright

TARGET_USER = "kanyewest"  # Change this to your user
SAVE_PATH = "tweets.jsonl"
SCREENSHOT_DIR = "screenshots"
MAX_TWEETS = 1000

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Load seen tweet IDs
seen_ids = set()
if os.path.exists(SAVE_PATH):
    with open(SAVE_PATH, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                seen_ids.add(data["id"])
            except:
                pass

# Fetch tweets
tweets_to_save = []
for tweet in sntwitter.TwitterUserScraper(TARGET_USER).get_items():
    if len(tweets_to_save) >= MAX_TWEETS:
        break
    if tweet.id in seen_ids:
        continue

tweet_data = {
    "id": tweet.id,
    "content": tweet.content,
    "date": tweet.date.isoformat(),
    "url": tweet.url,
    "screenshot": f"{SCREENSHOT_DIR}/{tweet.id}.png",
    "likes": tweet.likeCount,
    "retweets": tweet.retweetCount
}

    # Screenshot the tweet
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto(tweet.url, timeout=15000)
            page.wait_for_timeout(4000)  # Wait for tweet to load
            page.screenshot(path=tweet_data["screenshot"], full_page=True)
            print(f"Screenshot saved for {tweet.id}")
        except Exception as e:
            print(f"Error with {tweet.url}: {e}")
        browser.close()

    tweets_to_save.append(tweet_data)

# Save new tweets
if tweets_to_save:
    with open(SAVE_PATH, "a") as f:
        for t in tweets_to_save:
            f.write(json.dumps(t) + "\n")

print(f"Done. {len(tweets_to_save)} new tweets saved.")
