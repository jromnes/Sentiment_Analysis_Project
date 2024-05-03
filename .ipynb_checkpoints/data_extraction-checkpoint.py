# Import necessary libraries
import streamlit as st
from newsapi import NewsApiClient
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import yfinance as yf
from dotenv import load_dotenv
import os
from googletrans import Translator
from helper_functions import categorize_sentiment, translate_to_english

# Load environment variables
load_dotenv('keys.env')

# Retrieve NewsAPI key from environment variables
newsapi_key = os.getenv('NEWSAPI_KEY')

# Initialize NewsApiClient with API key
newsapi = NewsApiClient(api_key=newsapi_key)

# Function to fetch and preprocess news data
def fetch_news_data(query):
    parsed_data = []
    all_headlines = newsapi.get_everything(q=query)
    for article in all_headlines['articles']:
        if 'title' not in article or not article['title']:
            continue # Skips over articles with no title
        title = article['title']
        timestamp = article['publishedAt']
        source_name = article['source']['name'] if 'source' in article and 'name' in article['source'] else None
        image = article['urlToImage']
        url = article['url']
        parsed_data.append({'timestamp': timestamp, 'title': title, 'source': source_name, 'Image URL': image, 'Article URL': url}) # appending             parsed data into 'parsed_data'
    df = pd.DataFrame(parsed_data) # Creating a dataframe with the parsed data from newsapi
    df['timestamp'] = pd.to_datetime(df['timestamp']) # Changing timestamp format to datetime
    df['Date'] = df['timestamp'].dt.date #  Setting 'Date' column
    df['Time'] = df['timestamp'].dt.time # Setting 'Time' column
    df.set_index('Date', inplace=True) # Setting 'Date' as index
    df.sort_values(by='Date', inplace=True)
    df = df.iloc[3:] 
    # Apply translation to non-English titles
    df['title'] = df['title'].apply(lambda x: translate_to_english(x))
    # Initilizing the NLTK library SentimentIntensityAnalyzer 'polarity_scores' function to return the compound polarity score and add a 'compound'     column to the dataframe
    df['compound'] = df['title'].apply(lambda x: SentimentIntensityAnalyzer().polarity_scores(x)['compound'])
    # Apply categorization function to create a new column 'sentiment_category'
    df['sentiment_category'] = df['compound'].apply(categorize_sentiment)
    df = df[df['compound'] != 0]
    return df

# Function to Retrieve historical stock data from Yahoo Finance for the given symbol and calculate daily returns. Also returns a DataFrame containing historical stock data and daily returns.
def fetch_stock_data(symbol):

    # Retrieve historical data from Yahoo Finance
    stock = yf.Ticker(symbol)
    stock_df = stock.history(interval='1d',
        period="1mo",
        actions=False,
        auto_adjust=True)
    
    # Calculate daily returns
    stock_df['Returns'] = stock_df['Close'].pct_change()
    stock_df.dropna(inplace=True)
    
    # Drop unnecessary columns
    #stock_df.drop(columns=['High', 'Low', 'Open', 'Volume'], inplace=True)
    
    return stock_df

