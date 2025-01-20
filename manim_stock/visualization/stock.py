"""Abstract class for stock visualization."""

import logging
from abc import ABC, abstractmethod

from manim import MovingCameraScene

# Set logging level to WARNING
logging.getLogger("manim").setLevel(logging.WARNING)


class StockVisualization(ABC, MovingCameraScene):
    """
    Abstract class for stock visualization.

    Attributes:
        tickers (str | list[str]):
            The ticker(s) of the stock(s) to visualize

        start (str):
            The start date in YYYY-MM-DD format

        end (str):
            The end date in YYYY-MM-DD format

        title (str):
            The title of the visualization

        x_label (str):
            The label of the x-axis

        y_label (str):
            The label of the y-axis
        
        title_font_size (int):
            The font size of the title
        
        x_label_font_size (int):
            The font size of the x-axis label
        
        y_label_font_size (int):
            The font size of the y-axis label
    """

    def __init__(
        self,
        tickers: str | list[str],
        start: str,
        end: str,
        title: str,
        x_label: str,
        y_label: str,
        title_font_size: int,
        x_label_font_size: int,
        y_label_font_size: int,
        **kwargs,
    ):
        assert title_font_size > 0, "title_font_size must be greater than 0!"
        assert x_label_font_size > 0, "x_label_font_size must be greater than 0!"
        assert y_label_font_size > 0, "y_label_font_size must be greater than 0!"

        super().__init__(**kwargs)

        self.tickers = tickers
        self.start = start
        self.end = end
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.title_font_size = title_font_size
        self.x_label_font_size = x_label_font_size
        self.y_label_font_size = y_label_font_size

    @abstractmethod
    def load_data(self):
        """Load the stock data."""

    @abstractmethod
    def preprocess_data(self):
        """Preprocess the stock data."""

    @abstractmethod
    def construct(self):
        """Construct the scene."""
