import os
from googleapiclient.discovery import build
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def fetch_youtube_comments(video_id='dQw4w9WgXcQ', max_results=100):
    """
    Fetches comments from a specific YouTube video.
    For Myntra, you would pass the video_id of a popular Myntra haul video.
    """
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("Warning: YOUTUBE_API_KEY not found in environment.")
        return pd.DataFrame()

    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        formatted_comments = []
        next_page_token = None
        
        while len(formatted_comments) < max_results:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, max_results - len(formatted_comments)),
                textFormat="plainText",
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']
                formatted_comments.append({
                    'source': 'YouTube',
                    'author': comment['authorDisplayName'],
                    'date': comment['publishedAt'],
                    'rating': None,
                    'text': comment['textDisplay'],
                    'upvotes': comment['likeCount']
                })
                
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
                
        df = pd.DataFrame(formatted_comments)
        return df
    except Exception as e:
        print(f"Error fetching YouTube comments: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Test with a dummy video ID
    df = fetch_youtube_comments(max_results=5)
    print(f"Fetched {len(df)} comments from YouTube:")
    print(df.head())
