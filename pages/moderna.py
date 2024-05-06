# Import necessary libraries
import streamlit as st
from newsapi import NewsApiClient
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys
sys.path.insert(0, '..')
from data_extraction import fetch_news_data
from data_extraction import fetch_stock_data
import matplotlib.pyplot as plt
import altair as alt
import os
from wordcloud import WordCloud
from matplotlib.colors import LinearSegmentedColormap


def main():
    st.title('Moderna News Sentiment Analysis')
    # Fetch and preprocess news and stock data
    moderna_df = fetch_news_data('Moderna')
    mrna_df = fetch_stock_data('MRNA')
 # Group by date and calculate mean compound score
    moderna_mean = moderna_df.groupby('Date')['compound'].mean()
    # Filter out dates with no articles
    moderna_mean = moderna_mean[moderna_mean != 0]
# Plotting Mean Compound Polarity Scores by Date
    mean_chart = alt.Chart(moderna_mean.reset_index()).mark_bar().encode(
        x='Date:T',
        y='compound:Q',
        color=alt.Color('compound', scale=alt.Scale(domain=[-1, 0, 1], range=['red', 'lightgray', 'green']), legend=None)
    ).properties(
        width=600,
        height=400,
        title='Mean Compound Polarity Scores of the last 30 days of Moderna-related News Articles by Date'
        )
    st.altair_chart(mean_chart, use_container_width=True)
    # Calculate word frequencies
    word_freq = moderna_df['title'].str.split(expand=True).stack().value_counts()
    # Normalize sentiment scores between 0 and 1
    max_score = moderna_df['compound'].max()
    min_score = moderna_df['compound'].min()
    moderna_df['normalized_compound'] = (moderna_df['compound'] - min_score) / (max_score - min_score)
    # Create a custom colormap for sentiment colors
    colors = [(0, 0, 1), (1, 1, 1), (1, 0, 0)]  # Blue, White, Red
    cmap_name = 'sentiment_cmap'
    sentiment_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, colormap=sentiment_cmap).generate_from_frequencies(word_freq)
    # Plot word cloud
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    
    st.title("Word Cloud of News Titles")
    st.image(wordcloud.to_array(), use_column_width=True)
    
if __name__ == "__main__":
    main()