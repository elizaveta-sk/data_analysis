"""Collect recent British Airways reviews for the accompanying analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.airlinequality.com/airline-reviews/british-airways"
OUTPUT_PATH = Path("data/ba_reviews.csv")


def collect_reviews(page_count: int) -> list[str]:
    """Return review text from the requested number of result pages."""
    reviews: list[str] = []
    headers = {"User-Agent": "Mozilla/5.0 (portfolio coursework project)"}

    for page in range(1, page_count + 1):
        response = requests.get(
            f"{BASE_URL}/page/{page}/?sortby=post_date%3ADesc&pagesize=100",
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        reviews.extend(
            element.get_text(" ", strip=True)
            for element in soup.select("div.text_content")
        )
        print(f"Page {page}: {len(reviews)} reviews collected")

    return reviews


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect public airline-review text.")
    parser.add_argument("--pages", type=int, default=10, help="Number of result pages to collect.")
    args = parser.parse_args()

    reviews = collect_reviews(args.pages)
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    pd.DataFrame({"review": reviews}).to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(reviews)} reviews to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
