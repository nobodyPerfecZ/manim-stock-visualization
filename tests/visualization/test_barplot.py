"""Tests for manim_stock/visualization/barplot.py."""

from manim_stock.visualization.barplot import Barplot


class TestBarplot:
    """Tests the Barplot class."""

    def test_render(self):
        """Tests the render() method."""
        scene = Barplot(
            tickers=["AAPL", "NVDA", "TSLA", "AMZN", "GOOGL"],
            start="1900-01-01",
            end="2100-01-01",
            background_run_time=1,
            graph_run_time=1,
            wait_run_time=1,
            num_samples=10,
        )
        scene.render()
