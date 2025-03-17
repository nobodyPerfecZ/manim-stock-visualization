"""Example of downloading the stockprices of Apple, NVIDIA and Tesla."""

from manim_stock.util import (
    download_stock_data,
    preprocess_portfolio_value,
    preprocess_stock_data,
)

if __name__ == "__main__":
    # Download stock data
    df = download_stock_data(
        tickers=["AAPL", "NVDA", "TSLA"],
        start="1900-01-01",
        end="2100-01-01",
    )

    # Preprocess stock data
    df = preprocess_stock_data(df, column="High")

    # (Optional:) Convert stock price to portfolio value given an initial cashflow
    df = preprocess_portfolio_value(df, init_cash=10000)

    # Safe stock data as CSV file
    df.to_csv("stock_data.csv", index=False)
