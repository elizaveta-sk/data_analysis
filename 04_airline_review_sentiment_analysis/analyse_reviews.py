"""Create sentiment and topic summaries from scraped airline reviews."""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import nltk
import pandas as pd
import seaborn as sns
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from textblob import TextBlob

INPUT_PATH = Path("data/ba_reviews.csv")
OUTPUT_DIRECTORY = Path("output")


def clean_text(review: str, stop_words: set[str]) -> str:
    """Normalise one review and remove common English stop words."""
    review = re.sub(r"[^a-zA-Z\s]", " ", review.lower())
    words = [word for word in review.split() if word not in stop_words and len(word) > 2]
    return " ".join(words)


def label_sentiment(score: float) -> str:
    if score > 0.1:
        return "positive"
    if score < -0.1:
        return "negative"
    return "neutral"


def main() -> None:
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt", quiet=True)

    if not INPUT_PATH.exists():
        raise FileNotFoundError("Run review_scraper.py before analysing the reviews.")

    reviews = pd.read_csv(INPUT_PATH).dropna(subset=["review"])
    stop_words = set(stopwords.words("english"))
    reviews["clean_review"] = reviews["review"].astype(str).apply(
        lambda review: clean_text(review, stop_words)
    )
    reviews["polarity"] = reviews["clean_review"].apply(
        lambda review: TextBlob(review).sentiment.polarity
    )
    reviews["sentiment"] = reviews["polarity"].apply(label_sentiment)

    tokens = [review.split() for review in reviews["clean_review"] if review]
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(review) for review in tokens]
    topic_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=10, random_state=42)
    reviews = reviews.loc[reviews["clean_review"] != ""].copy()
    reviews["topic"] = [
        max(topic_model[document], key=lambda item: item[1])[0]
        for document in corpus
    ]

    OUTPUT_DIRECTORY.mkdir(exist_ok=True)
    reviews.to_csv(OUTPUT_DIRECTORY / "review_results.csv", index=False)
    reviews["sentiment"].value_counts().rename_axis("sentiment").to_csv(
        OUTPUT_DIRECTORY / "sentiment_summary.csv"
    )

    topic_summary = pd.crosstab(reviews["topic"], reviews["sentiment"])
    topic_summary.to_csv(OUTPUT_DIRECTORY / "topic_sentiment_counts.csv")

    ax = reviews["sentiment"].value_counts().plot.bar(color=["#2e7d32", "#757575", "#c62828"])
    ax.set(title="Review sentiment distribution", xlabel="Sentiment", ylabel="Number of reviews")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIRECTORY / "sentiment_distribution.png", dpi=160)
    plt.close()

    sns.heatmap(topic_summary, annot=True, fmt="d", cmap="YlGnBu")
    plt.title("Topic and sentiment counts")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIRECTORY / "topic_sentiment_heatmap.png", dpi=160)
    plt.close()

    print(f"Saved analysis files to {OUTPUT_DIRECTORY}")


if __name__ == "__main__":
    main()
