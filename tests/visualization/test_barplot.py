"""Tests for manim_stock/visualization/barplot.py."""

from manim_stock.visualization.barplot import Barplot


class TestBarplot:
    """Tests the Barplot class."""

    def test_render(self):
        """Tests the render() method."""
        scene = Barplot(
            path="docs/data/stock_data.csv",
            background_run_time=1,
            animation_run_time=1,
            wait_run_time=1,
            num_samples=10,
        )
        scene.render()
