# Stock and Revenue Analysis

This project compares historical share prices with reported revenue for Tesla and GameStop. It retrieves market data with Yahoo Finance, collects quarterly revenue data from the course-source web pages, cleans both datasets, and displays paired charts for each company.

## Techniques used

- Data retrieval with `yfinance` and `requests`
- HTML table extraction with Beautiful Soup
- Data cleaning with pandas
- Time-series visualisation with Matplotlib

## Run the project

```bash
pip install yfinance pandas requests beautifulsoup4 matplotlib
python stock_revenue_analysis.py
```

The script opens one chart for Tesla and one for GameStop. Each chart shows the historical closing share price above the quarterly revenue trend.
