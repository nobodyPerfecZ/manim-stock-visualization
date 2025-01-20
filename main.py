"""Example of visualizing the stock price of Apple using Manim Stock."""

from manim_stock.visualization.single_stock_price import SingleStockPriceVisualization

if __name__ == "__main__":
    scene = SingleStockPriceVisualization(
        tickers="AAPL",
        start="1900-01-01",
        end="2100-01-01",
        title="Apple",
        background_run_time=10,
        graph_run_time=45,
        wait_run_time=5,
    )
    scene.render()
