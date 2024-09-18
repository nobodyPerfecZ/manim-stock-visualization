from manim_stock.visualization import StockVisualization
from manim_stock.util import download_stock_data, preprocess_stock_data

if __name__ == "__main__":
    # Download and preprocess stock data
    df = download_stock_data(
        tickers="AAPL",
        start="2014-01-01",
        end="2024-01-01",
        rounding=True,
    )
    df = preprocess_stock_data(df)

    scene = StockVisualization(df)
    scene.render()
