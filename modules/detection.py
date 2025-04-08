import streamlit as st
from transformers import pipeline

# Try to import the transformers library
try:
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    sentiment_enabled = True
except Exception as e:
    sentiment_pipeline = None
    sentiment_enabled = False
    print("Sentiment model loading failed:", e)

# Example usage
def detect_sentiment(text):
    if sentiment_enabled and sentiment_pipeline:
        try:
            result = sentiment_pipeline(text)[0]
            return result["label"]
        except Exception as e:
            return "UNKNOWN"
    else:
        return "DISABLED"

# --- Gaalis Set ---
hindi_gaalis = [
    "Abe madarchod, teri maa ki chut mein Google Search ka history bhar dunga!",
    "Abe madarchod, teri behan ki chut mein neutron bomb daal ke usko vaporize kar dunga...",
    # ... Add more creative gaalis
]

# --- Disrespect Detection ---
def is_abusive_or_disrespectful(text):
    sentiment = detect_sentiment(text)
    return sentiment == "NEGATIVE"
