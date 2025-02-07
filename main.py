"""Example of visualizing the stock price of Apple, NVIDIA and Tesla."""

from manim_stock.util import download_stock_data, preprocess_stock_data
from manim_stock.visualization import Lineplot

if __name__ == "__main__":
    # Download stock data
    df = download_stock_data(
        tickers=["AAPL", "NVDA", "TSLA"],
        start="1900-01-01",
        end="2100-01-01",
    )
    df = preprocess_stock_data(df)
    df.to_csv("stock_data.csv", index=False)

    # Create scene
    scene = Lineplot(
        path="stock_data.csv",
        title="Market Prices",
        background_run_time=5,
        graph_run_time=10,
        wait_run_time=5,
    )

    # Render scene
    scene.render()
