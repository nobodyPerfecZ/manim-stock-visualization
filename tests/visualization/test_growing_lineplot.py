"""Tests for manim_stock/visualization/growing_lineplot.py."""

from manim_stock.visualization.growing_lineplot import GrowingLineplot


class TestGrowingLineplot:
    """Tests the GrowingLineplot class."""

    def test_render(self):
        """Tests the render() method."""
        scene = GrowingLineplot(
            path="examples/data/stock_data.csv",
            background_run_time=1,
            animation_run_time=1,
            wait_run_time=1,
            num_samples=10,
        )
        scene.render()
