"""Abstract class for stock visualization."""

import logging
import os
from abc import ABC, abstractmethod
from typing import List

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

        background_run_time (int):
            The run time for the write animation of the background elements

        animation_run_time (int):
            The run time for the create animation of the graph

        wait_run_time (int):
            The run time for the fade out animation at the end

        camera_scale (float):
            The scale factor for the camera frame

        colors(str | List[str]):
            The colors for all graphs

        num_ticks (int):
            The number of ticks on the x-/y-axis

        num_samples (int):
            The number of samples to use for the visualization

        x_round (bool):
            Whether to use non-decimal numbers for the x-axis labels.

        y_round (bool):
            Whether to use non-decimal numbers for the y-axis labels.
    """

    def __init__(
        self,
        path: str,
        title: str = "Market Price",
        x_label: str = "Year",
        y_label: str = r"Price [\$]",
        background_run_time: int = 5,
        animation_run_time: int = 50,
        wait_run_time: int = 5,
        camera_scale: float = 1.2,
        colors: str | List[str] | None = None,
        num_ticks: int = 6,
        num_samples: int = 100,
        x_round: bool = True,
        y_round: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        assert os.path.exists(path), "path does not exist!"
        assert path.endswith(".csv"), "file must be a CSV file!"
        assert (
            background_run_time > 0.0
        ), "background_run_time should be greater than 0.0!"
        assert (
            animation_run_time > 0.0
        ), "animation_run_time should be greater than 0.0!"
        assert wait_run_time > 0.0, "wait_run_time should be greater than 0.0!"
        assert camera_scale > 0.0, "camera_scale should be greater than 0.0!"
        assert num_ticks > 0, "num_ticks must be greater than 0!"
        assert num_samples > 0, "num_samples must be greater than 0!"

        self.path = path
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.background_run_time = background_run_time
        self.animation_run_time = animation_run_time
        self.wait_run_time = wait_run_time
        self.camera_scale = camera_scale
        self.num_ticks = num_ticks
        self.num_samples = num_samples
        self.x_round = x_round
        self.y_round = y_round

        self.load_data()
        self.preprocess_data()

        if colors is None:
            colors = [
                "#1f77b4",
                "#ff7f0e",
                "#2ca02c",
                "#d62728",
                "#9467bd",
            ][: self.Y.shape[-1]]
        elif isinstance(colors, str):
            colors = [colors]

        assert (
            len(colors) == self.Y.shape[-1]
        ), "colors should have the same length as the number of tickers!"

        self.colors = colors

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
        self.X = self.df[self.df.columns[0]].to_numpy()
        self.X_indices = np.arange(len(self.X))
        self.Y = self.df[self.df.columns[1:]].to_numpy()
        self.names = self.df.columns[1:]

    @abstractmethod
    def construct(self):
        """Construct the scene."""
