import warnings

import matplotlib.pyplot as plt
import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup


warnings.filterwarnings("ignore", category=FutureWarning)

TESLA_REVENUE_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
GAMESTOP_REVENUE_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"


def get_stock_history(symbol):
    history = yf.Ticker(symbol).history(period="max")
    return history.reset_index()


def get_revenue_data(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for table in soup.find_all("table"):
        headers = [cell.get_text(strip=True) for cell in table.find_all("th")]
        if "Date" not in headers or "Revenue" not in headers:
            continue

        rows = []
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) == 2:
                rows.append([cell.get_text(strip=True) for cell in cells])

        revenue = pd.DataFrame(rows, columns=["Date", "Revenue"])
        revenue["Revenue"] = pd.to_numeric(
            revenue["Revenue"].str.replace(r"[$,]", "", regex=True), errors="coerce"
        )
        revenue["Date"] = pd.to_datetime(revenue["Date"], errors="coerce")
        return revenue.dropna().sort_values("Date")

    raise ValueError("A revenue table could not be found on the source page.")


def make_graph(stock_data, revenue_data, company):
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=False)

    axes[0].plot(stock_data["Date"], stock_data["Close"], color="tab:blue")
    axes[0].set_title(f"{company}: Historical Share Price")
    axes[0].set_ylabel("Price (USD)")

    axes[1].plot(revenue_data["Date"], revenue_data["Revenue"], color="tab:green")
    axes[1].set_title(f"{company}: Quarterly Revenue")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Revenue (USD millions)")

    fig.tight_layout()
    plt.show()


def main():
    tesla_data = get_stock_history("TSLA")
    gamestop_data = get_stock_history("GME")
    tesla_revenue = get_revenue_data(TESLA_REVENUE_URL)
    gamestop_revenue = get_revenue_data(GAMESTOP_REVENUE_URL)

    make_graph(tesla_data, tesla_revenue, "Tesla")
    make_graph(gamestop_data, gamestop_revenue, "GameStop")


if __name__ == "__main__":
    main()
