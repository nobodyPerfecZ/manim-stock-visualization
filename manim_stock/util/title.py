"""Utility functions for Title objects."""

from manim import Title

from manim_stock.util.const import AXES_FONT_SIZE


def create_title(title: str, **kwargs) -> Title:
    """
    Create a Title object.

    Args:
        title (str):
            The text to be displayed.

        **kwargs:
            Additional arguments to be passed to Title().

    Returns:
        Title:
            The Title object.
    """
    if "font_size" not in kwargs:
        kwargs["font_size"] = AXES_FONT_SIZE
    if "include_underline" not in kwargs:
        kwargs["include_underline"] = False
    return Title(title, **kwargs)
