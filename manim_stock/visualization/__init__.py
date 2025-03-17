"""Visualization animations for stock prices."""

from manim_stock.visualization.barplot import Barplot
from manim_stock.visualization.growing_barplot import GrowingBarplot
from manim_stock.visualization.growing_lineplot import GrowingLineplot
from manim_stock.visualization.lineplot import Lineplot
from manim_stock.visualization.plot import Plot

__all__ = [
    "Barplot",
    "GrowingBarplot",
    "GrowingLineplot",
    "Lineplot",
    "Plot",
]

assert __all__ == sorted(__all__), f"__all__ needs to be sorted into {sorted(__all__)}!"
