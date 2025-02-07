"""Abstract class for stock visualization."""

import logging
import os
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from manim import MovingCameraScene

# Set logging level to WARNING
logging.getLogger("manim").setLevel(logging.WARNING)


class StockVisualization(ABC, MovingCameraScene):
    """
    Abstract class for stock visualization.

    Attributes:
        path (str):
            The path to the CSV file containing the stock data

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

        num_samples (int):
            The number of samples to use for the visualization
    """

    def __init__(
        self,
        path: str,
        title: str,
        x_label: str,
        y_label: str,
        title_font_size: int,
        x_label_font_size: int,
        y_label_font_size: int,
        num_ticks: int,
        num_samples: int,
        **kwargs,
    ):
        super().__init__(**kwargs)

        assert os.path.exists(path), "path does not exist!"
        assert path.endswith(".csv"), "file must be a CSV file!"
        assert title_font_size > 0, "title_font_size must be greater than 0!"
        assert x_label_font_size > 0, "x_label_font_size must be greater than 0!"
        assert y_label_font_size > 0, "y_label_font_size must be greater than 0!"
        assert num_ticks > 0, "num_ticks must be greater than 0!"
        assert num_samples > 0, "num_samples must be greater than 0!"

        self.path = path
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.title_font_size = title_font_size
        self.x_label_font_size = x_label_font_size
        self.y_label_font_size = y_label_font_size
        self.num_ticks = num_ticks
        self.num_samples = num_samples

        self.load_data()
        self.preprocess_data()

    def load_data(self):
        """Load the stock data."""
        self.df = pd.read_csv(self.path)

    def preprocess_data(self):
        """Preprocess the stock data."""
        sample_indices = np.linspace(
            0,
            len(self.df) - 1,
            num=min(self.num_samples, len(self.df)),
            endpoint=True,
            dtype=int,
        )
        self.df = self.df.iloc[sample_indices]
        self.X = self.df["X"].to_numpy()
        self.Y = self.df[[f"Y{i}" for i in range(len(self.df.columns) - 1)]].to_numpy()

    @abstractmethod
    def construct(self):
        """Construct the scene."""
