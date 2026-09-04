from app_store_scraper import AppStore
import pandas as pd

def fetch_app_store_reviews(app_name='myntra-fashion-shopping-app', app_id=907394059, count=100):
    """
    Fetches reviews for Myntra from the Apple App Store.
    """
    try:
        myntra = AppStore(country='in', app_name=app_name, app_id=app_id)
        # Fetch reviews
        myntra.review(how_many=count)
        
        if not myntra.reviews:
            return pd.DataFrame()
            
        # Transform the output to a standard format
        formatted_reviews = []
        for r in myntra.reviews:
            formatted_reviews.append({
                'source': 'App Store',
                'author': r.get('userName', 'Unknown'),
                'date': r.get('date'),
                'rating': r.get('rating'),
                'text': r.get('review'),
                'upvotes': 0 # App store scraper doesn't easily expose upvotes
            })
            
        df = pd.DataFrame(formatted_reviews)
        return df
    except Exception as e:
        print(f"Error fetching App Store reviews: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Quick test
    df = fetch_app_store_reviews(count=10)
    print(f"Fetched {len(df)} reviews from App Store:")
    print(df.head())
