import snscrape.modules.twitter as sntwitter
import datetime
import json
import os

TARGET_USER = "kanyewest"  # Change this to the user you want to monitor
SAVE_PATH = "tweets.jsonl"
MAX_TWEETS = 20  # To avoid rate limits

# Load existing tweet IDs
existing_ids = set()
if os.path.exists(SAVE_PATH):
    with open(SAVE_PATH, "r") as f:
        for line in f:
            try:
                tweet = json.loads(line)
                existing_ids.add(tweet["id"])
            except:
                pass

# Fetch recent tweets
tweets = []
for tweet in sntwitter.TwitterUserScraper(TARGET_USER).get_items():
    if len(tweets) >= MAX_TWEETS:
        break
    if tweet.id in existing_ids:
        continue

    tweets.append({
        "id": tweet.id,
        "content": tweet.content,
        "date": tweet.date.isoformat(),
        "url": tweet.url
    })

# Save new tweets
if tweets:
    with open(SAVE_PATH, "a") as f:
        for t in tweets:
            f.write(json.dumps(t) + "\n")

print(f"Saved {len(tweets)} new tweets.")
