import praw
import os
import requests
from prawcore.exceptions import NotFound, Forbidden, ResponseException
from dotenv import load_dotenv
load_dotenv()

def get_reddit_instance():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )

def scrape_user_data(username, limit=50):
    reddit = get_reddit_instance()
    posts, comments = [], []

    # Try PRAW first
    try:
        user = reddit.redditor(username)
        for submission in user.submissions.new(limit=limit):
            posts.append({
                "text": f"Title: {submission.title}\nBody: {submission.selftext}",
                "url": f"https://www.reddit.com{submission.permalink}"
            })
        for comment in user.comments.new(limit=limit):
            comments.append({
                "text": f"Comment: {comment.body}",
                "url": f"https://www.reddit.com{comment.permalink}"
            })
        if posts or comments:
            return posts, comments
    except (NotFound, Forbidden, ResponseException) as e:
        print(f"PRAW failed: {e}")

    # Fallback to Pushshift for posts
    print("Trying Pushshift API...")
    try:
        # Posts
        ps_posts = requests.get(
            f"https://api.pushshift.io/reddit/submission/search/?author={username}&size={limit}"
        ).json().get("data", [])
        for p in ps_posts:
            posts.append({
                "text": f"Title: {p.get('title','')}\nBody: {p.get('selftext','')}",
                "url": f"https://www.reddit.com{p.get('permalink','')}"
            })
        # Comments
        ps_comments = requests.get(
            f"https://api.pushshift.io/reddit/comment/search/?author={username}&size={limit}"
        ).json().get("data", [])
        for c in ps_comments:
            comments.append({
                "text": f"Comment: {c.get('body','')}",
                "url": f"https://www.reddit.com{c.get('permalink','')}"
            })
    except Exception as e:
        print(f"Pushshift failed: {e}")

    if not posts and not comments:
        print(f"No posts or comments found for user '{username}'.")
    return posts, comments