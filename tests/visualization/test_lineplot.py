"""Tests for manim_stock/visualization/lineplot.py."""

from manim_stock.visualization.lineplot import Lineplot


class TestLineplot:
    """Tests the Lineplot class."""

    def test_render(self):
        """Tests the render() method."""
        scene = Lineplot(
            tickers=["AAPL", "NVDA", "TSLA"],
            start="1900-01-01",
            end="2100-01-01",
            background_run_time=1,
            graph_run_time=1,
            wait_run_time=1,
            num_samples=10,
        )
        scene.render()
