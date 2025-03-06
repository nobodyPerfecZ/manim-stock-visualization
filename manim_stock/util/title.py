from manim import Title

from manim_stock.util.const import AXES_FONT_SIZE


def create_title(
    title: str,
    font_size: float = AXES_FONT_SIZE,
    include_underline: bool = False,
    **kwargs,
) -> Title:
    """
    Creates a Title object.

    Args:
        title (str):
            The text to be displayed.

    Returns:
        Title:
            A Title object.
    """
    return Title(
        title,
        font_size=font_size,
        include_underline=include_underline,
        **kwargs,
    )
