"""Utility functions for Dot objects."""

from manim import Dot
from manim.typing import Vector2D

from manim_stock.util.const import DOT_RADIUS


def create_dot(point: Vector2D, **kwargs) -> Dot:
    """
    Create a Dot object.

    Args:
        point (Vector2D):
            The point where the dot will be located.

        **kwargs:
            Additional arguments to be passed to Dot().

    Returns:
        Dot:
            The Dot object.
    """
    if "radius" not in kwargs:
        kwargs["radius"] = DOT_RADIUS
    return Dot(point=point, **kwargs)
