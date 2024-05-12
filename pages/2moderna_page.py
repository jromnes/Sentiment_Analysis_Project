# Import necessary libraries
import streamlit as st
from newsapi import NewsApiClient
import sys
sys.path.insert(0, '..')
from data_extraction import fetch_news_data, fetch_stock_data
import altair as alt
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib.colors import LinearSegmentedColormap
from helper_functions import categorize_sentiment
# Cache expensive data fetching operations
@st.cache_data()
def load_data():
    moderna_df = fetch_news_data('Moderna')
    mrna_df = fetch_stock_data('MRNA')
    return moderna_df, mrna_df
def main():
    st.title('**Moderna News Sentiment Analysis**')
 # Load data using caching
    moderna_df, mrna_df = load_data()
 # Returns over time
    st.header('**Recent Pfizer Stock Returns**')
    # Daily Returns from Moderna (MRNA) over last 30 Days
    returns_chart = alt.Chart(mrna_df.reset_index()).mark_line(color='lightgray').encode(
        x='Date:T',
        y='Returns:Q'
    ).properties(
        title='Daily Returns of Moderna Stock Over the Last 30 Days'
    ).interactive()
    st.altair_chart(returns_chart, use_container_width=True)
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
# Overall sentiment score
    overall_score = round(moderna_df['compound'].mean(), 3)
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
    st.markdown(f"<h1 style='text-align: center;'>Overall Compound score : <span style='color:{color_scale[overall_sentiment]}'>{overall_score}</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Overall Sentiment Category: <span style='color:{color_scale[overall_sentiment]}'>{overall_sentiment}</span></h2>", unsafe_allow_html=True)
    # Plot word cloud
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    st.title("Word Cloud of News Titles")
    st.image(wordcloud.to_array(), use_column_width=True)
# Pie chart expressing sentiment values
    sentiment_counts = moderna_df['compound'].apply(categorize_sentiment).value_counts()
    labels = sentiment_counts.index.tolist()
    sizes = sentiment_counts.values.tolist()
    colors = [color_scale[sentiment] for sentiment in labels]
# Plotting the pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, shadow=False)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# Title and Legend
    ax.set_title('Pie Chart Distribution of Sentiment Categories')
    ax.legend(labels, loc='lower left')
# Display the pie chart
    st.pyplot(fig)
if __name__ == "__main__":
    main()