"""Utility functions for Manim objects."""

from manim_stock.util.axes import (
    add_x_labels_custom,
    add_x_labels_range,
    add_y_labels_custom,
    add_y_labels_range,
    create_axes,
    remove_x_labels,
    remove_y_labels,
)
from manim_stock.util.barchart import (
    add_bar_names,
    add_bar_values,
    create_barchart,
    remove_bar_names,
    remove_bar_values,
)
from manim_stock.util.const import (
    AXES_FONT_SIZE,
    DOT_RADIUS,
    GRAPH_STROKE_WIDTH,
    LABEL_FONT_SIZE,
)
from manim_stock.util.dot import create_dot
from manim_stock.util.finance import (
    download_stock_data,
    preprocess_portfolio_value,
    preprocess_stock_data,
)
from manim_stock.util.graph import create_graph
from manim_stock.util.tex import (
    create_label_name,
    create_label_value,
    create_tex,
    next_to_tex,
)
from manim_stock.util.title import create_title

__all__ = [
    "AXES_FONT_SIZE",
    "DOT_RADIUS",
    "GRAPH_STROKE_WIDTH",
    "LABEL_FONT_SIZE",
    "add_bar_names",
    "add_bar_values",
    "add_x_labels_custom",
    "add_x_labels_range",
    "add_y_labels_custom",
    "add_y_labels_range",
    "create_axes",
    "create_barchart",
    "create_dot",
    "create_graph",
    "create_label_name",
    "create_label_value",
    "create_tex",
    "create_title",
    "download_stock_data",
    "next_to_tex",
    "preprocess_portfolio_value",
    "preprocess_stock_data",
    "remove_bar_names",
    "remove_bar_values",
    "remove_x_labels",
    "remove_y_labels",
]

assert __all__ == sorted(__all__), f"__all__ needs to be sorted into {sorted(__all__)}!"
