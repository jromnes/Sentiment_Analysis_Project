import streamlit as st

def main():
    # Sets the streamlit-app page layout to wide mode
    st.set_page_config(layout="wide")

    st.title("Welcome to Our Sentiment Analysis Streamlit App!")
    st.markdown("Below are some useful videos to understand some of the techniques and libraries we used to build this app!")
    
    st.subheader("Introduction to Sentiment Analysis")
    st.markdown("This informational video breaks down the meaning of sentiment analysis, the form of analysis used in this project.")
    st.video("https://www.youtube.com/watch?v=NcnwPAeYqMo") #Insert Video of Sentiment Analysis     Explanation
    
    st.divider()
    
    st.subheader("NLTK Library & Vader Polarity Scores")
    st.markdown("This video is what was utilized as a resource for us to learn about NLTK Library!")
    st.video("https://youtu.be/o-zM8onpQZY?si=WOZh3hJjXGkhIiPJ&t=1347")

if __name__ == "__main__":
    main()
