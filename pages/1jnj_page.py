# Import necessary libraries
import streamlit as st
from newsapi import NewsApiClient
import altair as alt
import sys
sys.path.insert(0, '..')
from data_extraction import fetch_news_data, fetch_stock_data
from helper_functions import categorize_sentiment

# Cache expensive data fetching operations
@st.cache_data()
def load_data():
        jnj_stock_df = fetch_stock_data('JNJ')
        # Optimal query for J&J used
        jnj_df = fetch_news_data('Johnson AND Johnson AND JNJ')
        return jnj_stock_df, jnj_df
    

# Streamlit app
def main():
    # JNJ Logo
    st.image("Images/jnjLogo.svg", use_column_width=True)

    # Title, centered
    st.markdown("<h1 style='text-align: center;'>J&J News Sentiment Analysis</h1>", unsafe_allow_html=True)
    
    # Horizontal line
    st.markdown("""---""")

    # Text
    st.markdown(
         "##### Johnson & Johnson (J&J) researches, develops, manufactures, and sells pharmaceutical products and medical devices. They are also the 3rd largest Pharmaceutical Company in the world by market cap with a $357.92B market cap.")

    # Load data using caching
    jnj_stock_df, jnj_df = load_data()

    # Plot JNJ Returns
    st.subheader('JNJ Daily Returns:')
    st.line_chart(jnj_stock_df.Returns)

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

    # Plotting Compound Polarity Scores of All Articles
    all_chart = alt.Chart(jnj_df).mark_point().encode(
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

    col1, col2 = st.columns(2)

    with col1:
        # Mean Compound Scores by Source
            
        # Calculate the mean compound scores for each source
        mean_scores = jnj_df.groupby('source')['compound'].mean().reset_index()
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
        st.altair_chart(sources_chart, use_container_width=True)

    with col2:
        # Heatmap of sentiment by source
        sentiment_counts = jnj_df.groupby(['source', 'sentiment_category']).size().reset_index(name='count')
        heatmap_chart = alt.Chart(sentiment_counts).mark_rect().encode(
            x=alt.X('source:N', title='Source'),
            y=alt.Y('sentiment_category:N', title='Sentiment Category', sort=['Positive', 'Neutral', 'Negative']),
            color=alt.Color('count:Q', title='Article Count', scale=alt.Scale(scheme='reds'))
        ).properties(
            width=800,
            height=400,
            title='Sentiment Distribution by Source'
        )
        st.altair_chart(heatmap_chart, use_container_width=True)



    # Group by date and calculate mean compound score
    jnj_mean = jnj_df.groupby('Date')['compound'].mean()
    
    # Filter out dates with no articles
    jnj_mean = jnj_mean[jnj_mean != 0]
    
    if not jnj_mean.empty:

        # Display Bar Chart of Mean Compound Scores
        st.subheader('Mean Compound Scores Daily:')
        st.bar_chart(jnj_mean)
        
        with st.expander("Comphrensive 30-Day Article Table"):
            # Display article titles
            st.subheader('Select Articles within 30 Days:')
            st.table(jnj_df[['Time', 'source','title', 'sentiment_category']])
    else:
        st.write("No articles found for the selected date range.")

if __name__ == "__main__":
    main()