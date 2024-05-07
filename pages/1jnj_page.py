# Import necessary libraries
import streamlit as st
from newsapi import NewsApiClient
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, '..')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from data_extraction import fetch_news_data, fetch_stock_data


# Cache expensive data fetching operations
@st.cache_data()
def load_data():
        jnj_stock_df = fetch_stock_data('JNJ')
        jnj_df = fetch_news_data('JNJ')
        return jnj_stock_df, jnj_df
    

# Streamlit app
def main():
    st.title('J&J News Sentiment Analysis')

    # Load data using caching
    jnj_stock_df, jnj_df = load_data()
    st.line_chart(jnj_stock_df[['Returns']])

    
    # Group by date and calculate mean compound score
    jnj_mean = jnj_df.groupby('Date')['compound'].mean()
    
    # Filter out dates with no articles
    jnj_mean = jnj_mean[jnj_mean != 0]
    
    if not jnj_mean.empty:
        # Display bar chart of mean compound scores
        st.bar_chart(jnj_mean)
        
        # Display article titles
        st.subheader('Article Titles:')
        st.table(jnj_df[['Time', 'title', 'sentiment_category']])
    else:
        st.write("No articles found for the selected date range.")

if __name__ == "__main__":
    main()