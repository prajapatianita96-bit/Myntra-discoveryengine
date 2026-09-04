import pandas as pd
import random

def fetch_reddit_discussions(limit=100):
    """
    Since the Reddit API recently completely blocked unauthenticated scraping (Error 403),
    we generate highly realistic mock PM data for the Wishlist Case Study.
    This simulates discussions from r/IndianFashionAddicts and r/TwoXIndia.
    """
    templates = [
        "I have had this gorgeous Zara dress in my wishlist for 3 months now. I just can't justify the price right now. Does anyone know when the next Myntra EORS sale is?",
        "Added 5 kurtas to my wishlist yesterday. The sizes were almost gone but I'm not sure if the fabric is actually cotton or that weird synthetic blend. Waiting for someone to post a review.",
        "My wishlist is full of Mango tops but honestly they are way too expensive. I'm just using the wishlist as a moodboard at this point lol.",
        "Anyone else just add things to their wishlist and forget about them? I have like 200 items in there. Sometimes I go back and see they are out of stock and feel a bit of FOMO.",
        "I really want these Nike sneakers. They are sitting in my wishlist but I'm waiting for my salary to drop next week before I hit buy.",
        "The Myntra wishlist feature is so buggy! I added a bunch of makeup to buy later, and half of it just disappeared.",
        "Saved a bunch of winter wear to my wishlist. The prices fluctuate so much though! I saw a jacket go from 2k to 4k in one day.",
        "Is it just me or does anyone else use the wishlist just to track price drops? I never buy immediately. I just wait for the notification.",
        "I love this H&M sweater but I'm holding off on buying it because I'm not sure about the fit. Wish they had better sizing charts.",
        "Added to wishlist because I don't need it right now, but it's too cute to pass up if it ever goes on a crazy 70% off sale.",
        "Found the perfect wedding guest outfit! It's in my wishlist. Just waiting to confirm if my cousin is actually having the wedding this year.",
        "Why do things in my wishlist always go out of stock right when I decide to finally buy them? So frustrating.",
        "I have a habit of wishlisting expensive watches just to motivate myself to work harder 😂",
        "Wishlisted a whole skincare routine on Myntra. Waiting to see if the reviews are actually legit or paid.",
        "My wishlist is basically a graveyard of clothes I thought I'd lose weight to fit into."
    ]
    
    posts = []
    for i in range(limit):
        text = random.choice(templates)
        posts.append({
            'source': 'Reddit (Simulated)',
            'text': text,
            'score': random.randint(10, 500),
            'url': f"https://reddit.com/r/IndianFashionAddicts/comments/mock_post_{i}"
        })
        
    return pd.DataFrame(posts)

