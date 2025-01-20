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
    """

    def __init__(
        self,
        tickers: str | list[str],
        start: str,
        end: str,
        title: str,
        x_label: str,
        y_label: str,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.tickers = tickers
        self.start = start
        self.end = end
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    @abstractmethod
    def load_data(self):
        """Load the stock data."""

    @abstractmethod
    def preprocess_data(self):
        """Preprocess the stock data."""

    @abstractmethod
    def construct(self):
        """Construct the scene."""
