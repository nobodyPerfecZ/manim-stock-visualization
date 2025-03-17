"""Utility functions for Graph objects."""

from manim import VMobject
from manim.typing import Vector2D_Array

from manim_stock.util.const import GRAPH_STROKE_WIDTH


def create_graph(points: Vector2D_Array, **kwargs) -> VMobject:
    """
    Create a Graph object.

    Args:
        points (Vector2D):
            The points that define the graph.

        **kwargs:
            Additional arguments to pass to the VMobject().

    Returns:
        VMobject:
            The Graph object.
    """
    if "stroke_width" not in kwargs:
        kwargs["stroke_width"] = GRAPH_STROKE_WIDTH

    return VMobject(**kwargs).set_points_as_corners(points)
