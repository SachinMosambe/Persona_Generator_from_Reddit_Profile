from reddit_scraper import scrape_user_data
from urllib.parse import urlparse

def extract_username(url):
    """Extract username from Reddit URL"""
    path = urlparse(url).path
    parts = [p for p in path.split('/') if p]
    return parts[1] if len(parts) > 1 else None

def test_scraper():
    # Test with the specific user
    url = "https://www.reddit.com/user/Hungry-Move-6603/comments/"
    username = extract_username(url)
    print(f"\nExtracting data for username: {username}")
    
    posts, comments = scrape_user_data(username, limit=50)
    
    print(f"Found {len(posts)} posts and {len(comments)} comments")
    
    if posts:
        print("\nSample posts:")
        for i, post in enumerate(posts[:3], 1):  # Show first 3 posts
            print(f"\n{i}. {post['text'][:200]}...")
            print(f"URL: {post['url']}")
    
    if comments:
        print("\nSample comments:")
        for i, comment in enumerate(comments[:3], 1):  # Show first 3 comments
            print(f"\n{i}. {comment['text'][:200]}...")
            print(f"URL: {comment['url']}")

if __name__ == "__main__":
    test_scraper()