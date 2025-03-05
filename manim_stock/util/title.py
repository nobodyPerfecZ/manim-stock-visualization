from manim import Title

from manim_stock.util.const import DEFAULT_FONT_SIZE


def create_title(title: str) -> Title:
    """
    Creates a Title object.

    Args:
        title (str):
            The text to be displayed.

    Returns:
        Title:
            A Title object.
    """
    return Title(title, font_size=DEFAULT_FONT_SIZE, include_underline=False)
