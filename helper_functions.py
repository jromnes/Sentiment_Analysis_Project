from googletrans import Translator


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
        
 # Function to translate non-English titles to English
def translate_to_english(text):
    translator = Translator()
    return translator.translate(text).text



