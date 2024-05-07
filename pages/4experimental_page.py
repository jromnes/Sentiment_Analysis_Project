# Import necessary libraries
import streamlit as st
from newsapi import NewsApiClient
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import altair as alt
import sys
sys.path.insert(0, '..')
from data_extraction import fetch_news_data, fetch_stock_data
from helper_functions import categorize_sentiment, topic_modeling_lda



# Streamlit app
def main():
    st.markdown("<h1 style='text-align: center;'>Fetch Sentiment Analysis Data for the Stock/Company of Your Choosing!</h1>", unsafe_allow_html=True)
    
    # Text input
    user_input = st.text_input("Enter stock/company name here", "Type here...")
    news_df = fetch_news_data(user_input)
    overall_score = round(news_df['compound'].mean(), 3)

   # Categorize overall score into sentiment category
    overall_sentiment = categorize_sentiment(overall_score)
    # Define color scale for sentiment categories
    color_scale = {
        'Negative': 'red',
        'Slightly Negative': 'lightcoral',
        'Neutral': 'white',
        'Slightly Positive': 'lightgreen',
        'Positive': 'green'
    }
    # Display the input and overall sentiment
    st.write("You entered:", user_input)
    st.markdown(f"<h1 style='text-align: center;'>Overall Compound score for {user_input}: <span style='color:{color_scale[overall_sentiment]}'>{overall_score}</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Overall Sentiment Category: <span style='color:{color_scale[overall_sentiment]}'>{overall_sentiment}</span></h2>", unsafe_allow_html=True)
    # Perform topic modeling
    st.sidebar.header('Topic Modeling')
    n_topics = st.sidebar.slider("Select number of topics", min_value=3, max_value=10, value=5, step=1)
    topics = topic_modeling_lda(news_df, n_topics)
    st.sidebar.subheader("Top Words for Each Topic")
    for topic in topics:
        st.sidebar.write(topic)

    # Plotting Compound Polarity Scores of All Articles
    all_chart = alt.Chart(news_df).mark_point().encode(
        x='title:N',
        y='compound:Q',
        tooltip=['title', 'compound'],
        color=alt.Color('compound', scale=alt.Scale(domain=[-1, 0, 1], range=['red', 'lightgray', 'green']), legend=None)
    ).properties(
        width=600,
        height=400,
        title='Compound Polarity Scores of All Articles'
    ).interactive()
    
    st.altair_chart(all_chart, use_container_width=True)

if __name__ == "__main__":
    main()