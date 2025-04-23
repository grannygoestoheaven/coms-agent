from urllib.parse import urlparse, parse_qs
from transformers import pipeline
from nltk.corpus import stopwords
from spacy.lang.en.stop_words import STOP_WORDS

# Load the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

def preprocess_comments(comments):
    clean_comments = []
    for c in comments:
        c = c.lower()
        c = re.sub(r'[^\w\s]', '', c)
        c = re.sub(r'http\S+|www\S+', '', c)
        words = [word for word in c.split() if word not in STOP_WORDS]
        c = " ".join(words)
        c = re.sub(r'\s+', ' ', c).strip()
        clean_comments.append(c)
    return clean_comments

def analyze_sentiment(text):
    """Analyzes the sentiment of a given text."""
    try:
        result = sentiment_pipeline(text)[0]
        sentiment = result["label"]
        score = result["score"]
        return sentiment, score
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return "Neutral", 0.5 # Default to neutral on error

def categorize_comments_by_sentiment(comments):
    good_comments = []
    bad_comments = []
    neutral_critical_comments = []
    for comment in comments:
        sentiment, score = analyze_sentiment(comment)
        if sentiment == "POSITIVE":
            good_comments.append(comment)
        elif sentiment == "NEGATIVE":
            bad_comments.append(comment)
        else:
            # We'll consider 'NEUTRAL' as our 'Neutral/Critical' category for now.
            # More sophisticated logic could be added here to differentiate
            # true neutral from critical comments if needed.
            neutral_critical_comments.append(comment)
    return {"Good": good_comments, "Bad": bad_comments, "Neutral/Critical": neutral_critical_comments}

def summarize_comments(comments):
    text = " ".join(comments)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    try:
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Summarization error: {e}")
        return "No summary available."

# if __name__ == '__main__':
#     test_comments = [
#         "This video is amazing!",
#         "I really disliked this content.",
#         "It was okay, but I have some questions.",
#         "Absolutely fantastic and well-explained.",
#         "This is terrible and misleading.",
#         "Interesting points raised in the video."
#     ]
#     categorized = categorize_comments_by_sentiment(test_comments)
#     print("Categorized Comments:", categorized)
#     for category, comments in categorized.items():
#         if comments:
#             summary = summarize_comments(comments)
#             print(f"\nSummary for {category} comments:\n{summary}")
