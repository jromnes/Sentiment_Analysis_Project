# Import necessary libraries
import streamlit as st
from newsapi import NewsApiClient
import sys
sys.path.insert(0, '..')
from data_extraction import fetch_news_data, fetch_stock_data
from helper_functions import categorize_sentiment

# st.set_page_config(layout="wide")
# Cache expensive data fetching operations
@st.cache_data()
def load_data():
        jnj_stock_df = fetch_stock_data('JNJ')
        jnj_df = fetch_news_data('JNJ')
        return jnj_stock_df, jnj_df
    

# Streamlit app
def main():
    st.image("Images/jnjLogo.svg", use_column_width=True)

    st.markdown("<h1 style='text-align: center;'>J&J News Sentiment Analysis</h1>", unsafe_allow_html=True)
    
    # Load data using caching
    jnj_stock_df, jnj_df = load_data()

    # Sentiment score 
    overall_score = round(jnj_df['compound'].mean(), 3)
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
    st.markdown(
         f"<h1 style='text-align: center;'>Overall Compound score for Johnson & Johnson: <span style='color:{color_scale[overall_sentiment]}'>{overall_score}</span></h1>", unsafe_allow_html=True)
    st.markdown(
         f"<h2 style='text-align: center;'>Overall Sentiment Category: <span style='color:{color_scale[overall_sentiment]}'>{overall_sentiment}</span></h2>", unsafe_allow_html=True)


    # JNJ Stock Returns Line Chart
    st.line_chart(jnj_stock_df[['Returns']])

    # Group by date and calculate mean compound score
    jnj_mean = jnj_df.groupby('Date')['compound'].mean()
    
    # Filter out dates with no articles
    jnj_mean = jnj_mean[jnj_mean != 0]
    
    if not jnj_mean.empty:

        # Display Bar Chart of Mean Compound Scores
        st.bar_chart(jnj_mean)
        
        # Display article titles
        st.subheader('Article Titles:')
        st.table(jnj_df[['Time', 'title', 'sentiment_category']])
    else:
        st.write("No articles found for the selected date range.")

if __name__ == "__main__":
    main()