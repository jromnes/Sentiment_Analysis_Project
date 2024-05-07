from googletrans import Translator
import logging
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

 # Define custom thresholds for sentiment categories
thresholds = {
    'Negative': (-1, -0.5),
    'Slightly Negative': (-0.5, -0.1),
    'Neutral': (-0.1, 0.1),
    'Slightly Positive': (0.1, 0.5),
    'Positive': (0.5, 1)
}
# Categorize compound scores into sentiment categories
def categorize_sentiment(compound):
    for sentiment, (lower, upper) in thresholds.items():
        if lower <= compound < upper:
            return sentiment
        


# Initialize logger
logger = logging.getLogger(__name__)

# Function to translate non-English titles to English
def translate_to_english(text):
    try:
        translator = Translator()
        translated_text = translator.translate(text).text
        return translated_text
    except Exception as e:
        logger.error("Error occurred during translation: %s", str(e))
        return text

# Function to perform topic modeling using LDA
def topic_modeling_lda(data, n_topics=5):
    # Vectorize text data using CountVectorizer
    count_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tf = count_vectorizer.fit_transform(data['title'])

    # Fit LDA model
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
    lda.fit(tf)

    # Get feature names
    feature_names = count_vectorizer.get_feature_names_out()

    # Display top words for each topic
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[:-6:-1]  # Get the top 5 words
        top_words = [feature_names[i] for i in top_words_idx]
        topics.append(f"Topic {topic_idx + 1}: {' | '.join(top_words)}")
    
    return topics



