#setup praw to connect to reddit

import praw 
import os
from dotenv import load_dotenv
import datetime
import pandas as pd

#load environment variables from .env file
load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv("REDDIT_CLIENT_ID"),
    client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent = "script:data_analysis:v1.0 (by /u/anon)"
)

subreddit = reddit.subreddit("CryptoCurrency")

#filter data for the last 180 days
six_mths_ago = datetime.datetime.now() - datetime.timedelta(days=180)

search_terms = [
    'price', 'regulation', 'crash', 'market', 'DeFi', 'technology', 'trend', 'USD', 'rise', 'boom', 'value'
]

crypto_posts = []

for term in search_terms:
    for submission in subreddit.search(term, limit=1000):
        try:
            post_time = datetime.datetime.fromtimestamp(submission.created_utc)
            if post_time > six_mths_ago:
                crypto_posts.append({
                    "created": datetime.datetime.fromtimestamp(submission.created_utc),
                    "title": submission.title,
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                    'url': submission.url
                })
        except Exception as e:
            print(f"error processing submission {submission.id}: {e}")

crypto_df = pd.DataFrame(crypto_posts)
print(f'Total posts found: {len(crypto_posts)}')

crypto_df.to_csv('reddit_crypto_search.csv', index=False, encoding='utf-8', sep=',')