# Import necessary libraries
import streamlit as st
from newsapi import NewsApiClient
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

        # Mean Compound Scores by Source
        
        # Calculate the mean compound scores for each source
    mean_scores_by_source = news_df.groupby('source')['compound'].mean().reset_index()
        # Plotting Mean Compound Scores by Source
    sources_chart = alt.Chart(mean_scores_by_source).mark_bar().encode(
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
    mean_by_date = news_df.groupby('Date')['compound'].mean()
        # Filter out dates with no articles
    mean_by_date = mean_by_date[mean_by_date != 0]
        # Plotting Mean Compound Polarity Scores by Date
    mean_chart_by_date = alt.Chart(mean_by_date.reset_index()).mark_bar().encode(
        x='Date:T',
        y='compound:Q',
        color=alt.Color('compound', scale=alt.Scale(domain=[-1, 0, 1], range=['red', 'lightgray', 'green']), legend=None)
    ).properties(
        width=600,
        height=400,
        title='Mean Compound Polarity Scores of the last 30 days of News Articles by Date'
    )


        # Plotting Compound Polarity Scores of All Articles
    all_scores_chart = alt.Chart(news_df).mark_point().encode(
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
    value_counts = news_df['sentiment_category'].value_counts().reset_index()
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

 # Dropdown for selecting different charts
    chart_option = st.selectbox("Select Chart", ["Mean Compound Polarity Scores by Source", "Mean Compound Polarity Scores by Date", "Compound Polarity Scores of All Articles", "Sentiment Categories Pie Chart"])

     # Select dropdown options
    if chart_option == "Mean Compound Polarity Scores by Source":
        st.write("## Mean Compound Scores by Source")
        st.altair_chart(sources_chart, use_container_width=True)
    elif chart_option == "Mean Compound Polarity Scores by Date":
        st.write("## Mean Compound Scores by Date")
        st.altair_chart(mean_chart_by_date, use_container_width=True)
    elif chart_option == "Compound Polarity Scores of All Articles":
        st.write("## Compound Polarity Scores of All Articles")                
        st.altair_chart(all_scores_chart, use_container_width=True)
    elif chart_option == "Sentiment Categories Pie Chart":
         st.altair_chart(pie_chart, use_container_width=True)


if __name__ == "__main__":
    main()