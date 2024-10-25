import pandas as pd
import praw
import os
from dotenv import load_dotenv

reddit_posts = pd.read_csv('./reddit_crypto_search.csv', encoding='utf-16', sep='\t')

print(reddit_posts.columns)

load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv("REDDIT_CLIENT_ID"),
    client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent = "script:data_analysis:v1.0 (by /u/anon)"
)

# fetch top 5 comments
def fetch_top_comments(url):
    submission = reddit.submission(url=url)
    
    submission.comments.replace_more(limit=0)
    
    top_comments = sorted(submission.comments, key=lambda comment: comment.score, reverse=True)[:5]
    
    top_comments_list = [(comment.body, comment.score) for comment in top_comments]
    
    return top_comments_list

reddit_posts['top_5_comments'] = reddit_posts['url'].apply(fetch_top_comments)

# print(reddit_posts[['title', 'top_5_comments']].head())

# reddit_posts.to_csv('./comments_reddit.csv', encoding='utf-16', sep='\t', index=False)

