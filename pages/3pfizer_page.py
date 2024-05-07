# Import necessary libraries

import streamlit as st
from newsapi import NewsApiClient
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys
sys.path.insert(0, '..')
from data_extraction import fetch_news_data, fetch_stock_data
import matplotlib.pyplot as plt
import altair as alt

@st.cache_data()
def load_data():
    pfizer_df = fetch_news_data('Pfizer')
    pfe_df = fetch_stock_data('PFE')
    return pfizer_df, pfe_df

# Streamlit app
def main():
    st.title('Pfizer News Sentiment Analysis')

    pfizer_df, pfe_df = load_data()
    # Create two columns layout
    headlines_column, charts_column = st.columns([2, 3])

    with headlines_column:    
        st.header('Latest Pfizer News Headlines', divider='grey')

        # Get the most recent article
        most_recent_article = pfizer_df.iloc[0]
        second_article = pfizer_df.iloc[1]
        third_article = pfizer_df.iloc[2]
        fourth_article = pfizer_df.iloc[3]
        fifth_article = pfizer_df.iloc[4]

                
        st.image("Images/logo.png", caption='Latest News Image', use_column_width=True)
      

        # Making a subheader of the title with the article URL as a hyperlink
        title_with_link = f"[{most_recent_article['title']}]({most_recent_article['Article URL']})"
        second_title_with_link = f"[{second_article['title']}]({second_article['Article URL']})"
        third_title_with_link = f"[{third_article['title']}]({third_article['Article URL']})"
        fourth_title_with_link = f"[{fourth_article['title']}]({fourth_article['Article URL']})"
        fifth_title_with_link = f"[{fifth_article['title']}]({fifth_article['Article URL']})"
        st.subheader(title_with_link)
        st.subheader(second_title_with_link)
        st.subheader(third_title_with_link)
        st.subheader(fourth_title_with_link)
        st.subheader(fifth_title_with_link)

    st.divider()
    
    # Charts column
    with charts_column:
        st.header('Recent Pfizer Stock Returns')
        
        # Daily Returns of Pfizer PFE Stock Over the Last 30 Days
        returns_chart = alt.Chart(pfe_df.reset_index()).mark_line(color='lightgray').encode(
            x='Date:T',
            y='Returns:Q'
        ).properties(
            title='Daily Returns of Pfizer PFE Stock Over the Last 30 Days'
        ).interactive()
        st.altair_chart(returns_chart, use_container_width=True)
        
        
        # Mean Compound Scores by Source
        
        # Calculate the mean compound scores for each source
        mean_scores = pfizer_df.groupby('source')['compound'].mean().reset_index()
        # Plotting Mean Compound Scores by Source
        sources_chart = alt.Chart(mean_scores).mark_bar().encode(
            x=alt.X('source', axis=alt.Axis(title='Source')),
            y=alt.Y('compound:Q', axis=alt.Axis(title='Mean Compound Score')),
            color=alt.Color('compound', scale=alt.Scale(domain=[-1, 0, 1], range=['red', 'lightgray', 'green']), legend=None),
            tooltip=['source', 'compound']
        ).properties(
            title='Mean Compound Scores by Source'
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16,
            align='center'
        )

        
       # Mean Compound Polarity Scores by Date
    
        # Group by date and calculate mean compound score
        pfizer_mean = pfizer_df.groupby('Date')['compound'].mean()
        # Filter out dates with no articles
        pfizer_mean = pfizer_mean[pfizer_mean != 0]
        # Plotting Mean Compound Polarity Scores by Date
        mean_chart = alt.Chart(pfizer_mean.reset_index()).mark_bar().encode(
            x='Date:T',
            y='compound:Q',
            color=alt.Color('compound', scale=alt.Scale(domain=[-1, 0, 1], range=['red', 'lightgray', 'green']), legend=None)
        ).properties(
            width=600,
            height=400,
            title='Mean Compound Polarity Scores of the last 30 days of Pfizer-related News Articles by Date'
        )


        # Plotting Compound Polarity Scores of All Articles
        all_chart = alt.Chart(pfizer_df).mark_point().encode(
            x='title:N',
            y='compound:Q',
            tooltip=['title', 'compound'],
            color=alt.Color('compound', scale=alt.Scale(domain=[-1, 0, 1], range=['red', 'lightgray', 'green']), legend=None)
        ).properties(
            width=600,
            height=400,
            title='Compound Polarity Scores of All Articles'
        ).interactive()

        # Calculate value counts of sentiment category
        value_counts = pfizer_df['sentiment_category'].value_counts().reset_index()
        value_counts.columns = ['Sentiment', 'Count']

        # Create pie chart using Altair
        pie_chart = alt.Chart(value_counts).mark_arc().encode(
            color='Sentiment',
            tooltip=['Sentiment', 'Count']
        ).properties(
            title='Sentiment Category Distribution'
        ).mark_arc().encode(
            theta='Count:Q',
            color='Sentiment:N',
            tooltip=['Sentiment', 'Count']
        ).interactive()

        
        st.title('Pfizer News Analysis')

        # Dropdown for selecting different charts
        chart_option = st.selectbox("Select Chart", ["Mean Compound Polarity Scores by Source", "Mean Compound Polarity Scores by Date", "Compound Polarity Scores of All Articles", "Sentiment Categories Pie Chart"])

        # Display selected chart
        if chart_option == "Mean Compound Polarity Scores by Source":
            st.write("## Mean Compound Scores by Source")
            st.altair_chart(sources_chart, use_container_width=True)
        elif chart_option == "Mean Compound Polarity Scores by Date":
            st.write("## Mean Compound Scores by Date")
            st.altair_chart(mean_chart, use_container_width=True)
        elif chart_option == "Compound Polarity Scores of All Articles":
            st.write("## Compound Polarity Scores of All Articles")
            st.altair_chart(all_chart, use_container_width=True)
        elif chart_option == "Sentiment Categories Pie Chart":
            st.altair_chart(pie_chart, use_container_width=True)

if __name__ == "__main__":
    main()