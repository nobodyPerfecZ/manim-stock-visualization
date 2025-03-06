"""Utility functions for Dot objects."""

import numpy as np
from manim import Dot

from manim_stock.util.const import DOT_RADIUS


def create_dot(
    point: np.ndarray,
    radius: float = DOT_RADIUS,
    **kwargs,
) -> Dot:
    """
    Create a Dot object.

    Args:
        point (np.ndarray):
            The point where the dot will be located.

        radius (float):
            The size of the dot.

        **kwargs:
            Additional arguments to be passed to Dot().

    Returns:
        Dot:
            The Dot object.
    """
    return Dot(point=point, radius=radius, **kwargs)
