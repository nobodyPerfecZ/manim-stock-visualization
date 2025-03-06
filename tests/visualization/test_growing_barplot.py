"""Tests for manim_stock/visualization/growing_barplot.py."""

from manim_stock.visualization.growing_barplot import GrowingBarplot


class TestBarplot:
    """Tests the Barplot class."""

    def test_render(self):
        """Tests the render() method."""
        scene = GrowingBarplot(
            path="examples/data/stock_data.csv",
            background_run_time=1,
            animation_run_time=1,
            wait_run_time=1,
            num_samples=10,
        )
        scene.render()
