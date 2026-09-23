# Airline Review Sentiment Analysis

An end-to-end text-analysis project that collects public airline reviews, classifies sentiment, and identifies recurring discussion topics.

## What it demonstrates

- Web scraping with `requests` and Beautiful Soup
- Text cleaning and stop-word removal
- Sentiment labels created with TextBlob polarity scores
- Topic modelling with Latent Dirichlet Allocation (LDA)
- CSV summaries and chart outputs for review

## Run locally

```bash
pip install -r requirements.txt
python review_scraper.py --pages 10
python analyse_reviews.py
```

The raw reviews are deliberately not committed. Running the scraper creates `data/ba_reviews.csv`; the analysis script writes its results to `output/`.
