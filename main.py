"""Example of visualizing the stock price of Apple, NVIDIA and Tesla."""

from manim_stock.visualization.lineplot import Lineplot

if __name__ == "__main__":
    scene = Lineplot(
        tickers=["AAPL", "NVDA", "TSLA"],
        start="1900-01-01",
        end="2100-01-01",
        title="Market Prices",
        background_run_time=5,
        graph_run_time=10,
        wait_run_time=5,
    )

    scene.render()
