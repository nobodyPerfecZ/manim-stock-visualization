"""Utility functions for Tex objects."""

import numpy as np
from manim import RIGHT, UR, Mobject, Tex
from manim.typing import Vector2D

from manim_stock.util.const import LABEL_FONT_SIZE


def create_tex(text: str, **kwargs) -> Tex:
    """
    Creates a Tex object.

    Args:
        text (str):
            The text to display.

        **kwargs:
            Additional arguments to be passed to Tex().

    Returns:
        Tex:
            The Tex object.
    """
    if "font_size" not in kwargs:
        kwargs["font_size"] = LABEL_FONT_SIZE
    return Tex(text, **kwargs)


def next_to_tex(tex: Tex, **kwargs) -> Tex:
    """
    Moves the Tex object next to the mobject/point in the direction.

    Args:
        tex (Tex):
            The Tex object.

        **kwargs:
            Additional arguments to be passed to next_to().

    Returns:
        Tex:
            The moved Tex object.
    """
    return tex.next_to(**kwargs)


def create_label_name(name: str, mobject_or_point: Vector2D | Mobject, **kwargs) -> Tex:
    """
    Create a Tex object with the specified name next to the mobject/point.

    Args:
        name (str):
            The name to display.

        mobject_or_point (Vector2D | Mobject):
            The point/mobject where the name will be located.

        **kwargs:
            Additional arguments to pass to create_tex() and next_to_tex().

    Returns:
        Tex:
            The Tex object.
    """
    tex_config = {} if "tex_config" not in kwargs else kwargs["tex_config"]
    next_to_config = (
        {"direction": UR}
        if "next_to_config" not in kwargs
        else kwargs["next_to_config"]
    )

    return next_to_tex(
        tex=create_tex(name, **tex_config),
        mobject_or_point=mobject_or_point,
        **next_to_config,
    )


def create_label_value(
    value: float,
    mobject_or_point: Vector2D | Mobject,
    value_decimals: int,
    **kwargs,
) -> Tex:
    """
    Create a Tex object with the specified value next to the mobject/point.

    Args:
        value (float):
            The value to display.

        mobject_or_point (Vector2D | Mobject):
            The point/mobject where the value will be located.

        value_decimals (int):
            The number of decimal places to round to.

        **kwargs:
            Additional arguments to pass to create_tex() and next_to_tex().

    Returns:
        Tex:
            The Tex object.
    """
    tex_config = {} if "tex_config" not in kwargs else kwargs["tex_config"]
    next_to_config = (
        {"direction": RIGHT}
        if "next_to_config" not in kwargs
        else kwargs["next_to_config"]
    )

    if value_decimals:
        value = np.round(value, value_decimals)
    else:
        value = np.fix(value).astype(np.int32)

    return next_to_tex(
        tex=create_tex(value, **tex_config),
        mobject_or_point=mobject_or_point,
        **next_to_config,
    )
