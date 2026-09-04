import streamlit as st # Force hot-reload
import pandas as pd
import time
import os

try:
    from src.ai_engine import process_dataframe
except ModuleNotFoundError:
    # Fallback in case the src folder wasn't preserved during GitHub upload
    from ai_engine import process_dataframe

st.set_page_config(page_title="Myntra AI Discovery Engine", page_icon="🛍️", layout="wide")

st.title("🛍️ Myntra AI Discovery Engine")
st.markdown("### Wishlist → Purchase Conversion Analyzer")
st.markdown("This tool aggregates user feedback across platforms and uses Gemini AI to discover *why* users hesitate to purchase wishlisted items.")

# --- SIDEBAR: DATA COLLECTION ---
st.sidebar.header("1. Data Collection")
source = st.sidebar.selectbox("Select Data Source", ["Synthetic Data (For Case Study)"])
count = st.sidebar.slider("Number of items to fetch", 10, 1500, 50)

if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None
if 'analyzed_data' not in st.session_state:
    st.session_state.analyzed_data = None

if st.sidebar.button("Fetch & Analyze Data"):
    with st.spinner(f"Fetching data from {source}..."):
        if source == "Play Store":
            df = fetch_play_store_reviews(count=count)
        elif source == "Reddit":
            df = fetch_reddit_discussions(limit=count)
        elif source == "YouTube":
            df = fetch_youtube_comments(max_results=count)
        elif source == "Synthetic Data (For Case Study)":
            import pandas as pd
            import random
            
            # Pre-analyzed synthetic data
            synthetic_data = [
                {"text": "I love this dress but I'm going to wait until the end of reason sale to buy it.", "intent": "Waiting for sale", "hesitation": "Price too high", "summary": "Waiting for sale", "is_wishlist_related": True},
                {"text": "Added to wishlist because I don't know if the size M will fit my shoulders.", "intent": "Comparing options", "hesitation": "Unsure about fit/size", "summary": "Uncertain about fit", "is_wishlist_related": True},
                {"text": "I have 50 things in my wishlist, just using it as a Pinterest board at this point.", "intent": "Just browsing", "hesitation": "None", "summary": "Using as moodboard", "is_wishlist_related": True},
                {"text": "Wishlisted this top, but the reviews say the color bleeds. Holding off for now.", "intent": "Comparing options", "hesitation": "Poor reviews", "summary": "Concerned about reviews", "is_wishlist_related": True},
                {"text": "Saved this for my brother's wedding, need to check with my sister if it matches the theme.", "intent": "Bookmarking for later", "hesitation": "Needs social validation", "summary": "Checking with sister", "is_wishlist_related": True},
                {"text": "I really want this jacket but 4000 rs is too steep. Wishlisted hoping for a price drop.", "intent": "Waiting for sale", "hesitation": "Price too high", "summary": "Hoping for price drop", "is_wishlist_related": True},
                {"text": "Wishlist is full of sneakers I want to buy, just waiting for my salary to credit.", "intent": "Bookmarking for later", "hesitation": "Price too high", "summary": "Waiting for salary", "is_wishlist_related": True},
                {"text": "I like the style but the neckline looks too deep in the pictures. Kept in wishlist while I look for alternatives.", "intent": "Comparing options", "hesitation": "Unsure about fit/size", "summary": "Neckline might be deep", "is_wishlist_related": True},
                {"text": "Saved it for later. I want to buy it but I'm not sure what jeans to pair it with.", "intent": "Bookmarking for later", "hesitation": "Needs social validation", "summary": "Unsure how to style", "is_wishlist_related": True}
            ]
            
            # Repeat to meet the count requested
            repeated = [random.choice(synthetic_data) for _ in range(count)]
            df = pd.DataFrame(repeated)
            df['source'] = 'Synthetic'
            
        if not df.empty:
            st.session_state.raw_data = df
            st.sidebar.success(f"Fetched {len(df)} items!")
            
            if source == "Synthetic Data (For Case Study)":
                st.session_state.analyzed_data = df
                st.sidebar.success("Synthetic Analysis Loaded Instantly!")
            else:
                with st.spinner("Running Gemini AI Analysis (extracting intent & hesitation)..."):
                    progress_bar = st.sidebar.progress(0)
                    status_text = st.sidebar.empty()
                    
                    def update_progress(current, total):
                        progress = int((current / total) * 100)
                        # Streamlit progress bar accepts values between 0 and 100
                        progress_bar.progress(progress)
                        status_text.text(f"Processing batch {current} of {total}...")
                    
                    st.session_state.analyzed_data = process_dataframe(df, progress_callback=update_progress)
                    
                    progress_bar.empty()
                    status_text.empty()
                st.sidebar.success("AI Analysis Complete!")
        else:
            st.sidebar.error("Failed to fetch data or no data found.")

# --- MAIN DASHBOARD ---
if st.session_state.analyzed_data is not None:
    df = st.session_state.analyzed_data
    
    tab1, tab2 = st.tabs(["📊 Dashboard Insights", "💬 Chat with Data"])
    
    with tab1:
        # 1. High-Level Metrics
        st.header("Opportunity Areas (Quantified)")
        
        col1, col2, col3 = st.columns(3)
        
        # Safely get the column, defaulting to False if it's missing for some reason
        is_related = df.get('is_wishlist_related', pd.Series([False]*len(df)))
        wishlist_related = df[is_related == True]
        
        col1.metric("Total Analyzed", len(df))
        col1.metric("Wishlist-Related Signals", len(wishlist_related))
        
        if not wishlist_related.empty:
            # Top Hesitations
            hesitations = wishlist_related['hesitation'].value_counts()
            col2.markdown("**Top Hesitations (Why they don't buy)**")
            st.bar_chart(hesitations)
            
            # Top Intents
            intents = wishlist_related['intent'].value_counts()
            col3.markdown("**Core User Intent**")
            st.bar_chart(intents)
        else:
            st.info("No explicitly wishlist-related signals found in this batch. Try fetching more data or a different source.")

        # 2. Deep Dive Data Explorer
        st.header("Deep Dive: Raw Verbatims")
        
        filter_hesitation = st.selectbox("Filter by Hesitation", ["All"] + list(df['hesitation'].unique()))
        
        display_df = df if filter_hesitation == "All" else df[df['hesitation'] == filter_hesitation]
        
        st.dataframe(
            display_df[['source', 'intent', 'hesitation', 'summary', 'text']], 
            use_container_width=True,
            hide_index=True
        )

    with tab2:
        st.header("💬 Ask the Discovery Engine")
        st.markdown("Ask complex questions about your data to complete your case study! (e.g. *'What information do users seek outside Myntra before purchasing?'*)")
        
        user_question = st.chat_input("Ask a question about the wishlist behaviors...")
        if user_question:
            st.chat_message("user").write(user_question)
            
            with st.spinner("Analyzing all insights..."):
                try:
                    from src.ai_engine import chat_with_data
                except ModuleNotFoundError:
                    from ai_engine import chat_with_data
                answer = chat_with_data(df, user_question)
                
            st.chat_message("assistant").write(answer)


else:
    st.info("👈 Use the sidebar to fetch data and run the AI analysis!")

