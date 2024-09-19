from manim_stock.visualization import StockVisualization
from manim_stock.util import download_stock_data, preprocess_stock_data

if __name__ == "__main__":
    # Download and preprocess stock data
    df = download_stock_data(
        ticker="AAPL",
        start="2014-01-01",
        end="2024-01-01",
        rounding=True,
    )
    df = preprocess_stock_data(df)

    # Visualize stock data
    scene = StockVisualization(
        df,
        title="Apple",
        visualize_live_stock_price=True,
        visualize_live_date=True,
    )
    scene.render()
