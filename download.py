"""Example of downloading the stockprices of Apple, NVIDIA and Tesla."""

from manim_stock.util import download_stock_data, preprocess_stock_data

if __name__ == "__main__":
    # Download stock data
    df = download_stock_data(
        tickers=["AAPL", "NVDA", "TSLA"],
        start="1900-01-01",
        end="2100-01-01",
    )
    df = preprocess_stock_data(df)
    df.to_csv("stock_data.csv", index=False)
