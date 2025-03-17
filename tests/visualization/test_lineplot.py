"""Tests for manim_stock/visualization/lineplot.py."""

from manim_stock.visualization.lineplot import Lineplot


class TestLineplot:
    """Tests the Lineplot class."""

    def test_render(self):
        """Tests the render() method."""
        scene = Lineplot(
            path="docs/data/stock_data.csv",
            background_run_time=1,
            animation_run_time=1,
            wait_run_time=1,
            num_samples=10,
        )
        scene.render()
