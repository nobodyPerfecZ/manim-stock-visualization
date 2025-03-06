"""Utility functions for Tex objects."""

import numpy as np
from manim import Mobject, Tex

from manim_stock.util.const import LABEL_FONT_SIZE


def create_tex(text: str, font_size: float = LABEL_FONT_SIZE, **kwargs) -> Tex:
    """
    Creates a Tex object.

    Args:
        text (str):
            The text to display.

        font_size (float):
            The font size of the text.

        **kwargs:
            Additional arguments to be passed to Tex().

    Returns:
        Tex:
            The Tex object.
    """
    return Tex(text, font_size=font_size, **kwargs)


def next_to_tex(
    tex: Tex,
    mobject_or_point: Mobject | np.ndarray,
    direction: np.ndarray,
) -> Tex:
    """
    Moves the Tex object next to the given mobject or point in the given direction.

    Args:
        tex (Tex):
            The Tex object.

        mobject_or_point (Mobject | np.ndarray):
            The Mobject or point to move the Tex object next to.

        direction (np.ndarray):
            The direction in which to move the Tex object

    Returns:
        Tex:
            The moved Tex object.
    """
    return tex.next_to(mobject_or_point, direction)
