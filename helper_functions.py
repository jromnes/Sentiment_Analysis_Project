from googletrans import Translator
import logging

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



