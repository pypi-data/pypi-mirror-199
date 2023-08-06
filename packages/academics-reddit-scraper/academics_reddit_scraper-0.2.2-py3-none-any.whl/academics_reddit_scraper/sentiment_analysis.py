import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text: str) -> float:
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    return sentiment["compound"]