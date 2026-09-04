from google_play_scraper import Sort, reviews
import pandas as pd

def fetch_play_store_reviews(app_id='com.myntra.android', count=100):
    """
    Fetches reviews for Myntra from the Google Play Store.
    """
    try:
        result, continuation_token = reviews(
            app_id,
            lang='en', # defaults to 'en'
            country='in', # defaults to 'us'
            sort=Sort.NEWEST, # defaults to Sort.NEWEST
            count=count # defaults to 100
        )
        
        # Transform the output to a standard format
        formatted_reviews = []
        for r in result:
            formatted_reviews.append({
                'source': 'Play Store',
                'author': r['userName'],
                'date': r['at'],
                'rating': r['score'],
                'text': r['content'],
                'upvotes': r['thumbsUpCount']
            })
            
        df = pd.DataFrame(formatted_reviews)
        return df
    except Exception as e:
        print(f"Error fetching Play Store reviews: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Quick test
    df = fetch_play_store_reviews(count=10)
    print(f"Fetched {len(df)} reviews from Play Store:")
    print(df.head())
