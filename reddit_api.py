import requests
import pandas as pd
import time

def fetch_reddit_discussions(subreddit='IndianFashionAddicts', search_query='Myntra', limit=50):
    """
    Fetches posts and their top comments from Reddit using the unauthenticated JSON endpoint.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) MyntraReviewsAggregator/1.0'}
    
    # Search for posts mentioning Myntra in the subreddit
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={search_query}&restrict_sr=1&limit={limit}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Reddit API returned status {response.status_code}")
            return pd.DataFrame()
            
        data = response.json()
        formatted_posts = []
        
        for child in data.get('data', {}).get('children', []):
            post = child['data']
            # Only include text posts with actual content
            if post.get('selftext'):
                formatted_posts.append({
                    'source': 'Reddit',
                    'author': post['author'],
                    'date': pd.to_datetime(post['created_utc'], unit='s').isoformat(),
                    'rating': None,
                    'text': f"Title: {post['title']}\n\n{post['selftext']}",
                    'upvotes': post['ups']
                })
                
        df = pd.DataFrame(formatted_posts)
        return df
    except Exception as e:
        print(f"Error fetching Reddit data: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = fetch_reddit_discussions(limit=5)
    print(f"Fetched {len(df)} posts from Reddit:")
    print(df.head())
