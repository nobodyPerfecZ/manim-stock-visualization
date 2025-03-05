"""Visualization of stock prices with barplots for multiple tickers."""

import logging
from dataclasses import dataclass, replace

import numpy as np
from manim import BarChart, ReplacementTransform, VGroup, Write, config

from manim_stock.util import (
    create_barchart,
    create_title,
    update_bar_names,
    update_bar_values,
)
from manim_stock.visualization.stock import StockVisualization

# Set logging level to WARNING
logging.getLogger("manim").setLevel(logging.WARNING)

# Disable caching to speed up the rendering process
config.disable_caching = True


@dataclass(frozen=True)
class State:
    """
    Dataclass to store the state of the visualization of GrowingLineplot.

    Attributes:
        x_min (float):
            The minimum value of the x-axis.

        x_max (float):
            The maximum value of the x-axis.

        num_x_ticks (int):
            The number of ticks on the x-axis.

        y_min (float):
            The minimum value of the y-axis.

        y_max (float):
            The maximum value of the y-axis.

        num_y_ticks (int):
            The number of ticks on the y-axis.
    """

    y_min: float
    y_max: float
    num_y_ticks: int

    @property
    def y_tick(self) -> float:
        """The value between each tick on the y-axis."""
        return (self.y_max - self.y_min) / self.num_y_ticks

    def replace(self, **kwargs) -> "State":
        """
        Returns a new instance of State with the attributes replaced.

        Args:
            **kwargs:
                The attributes to replace.

        Returns:
            State:
                A new instance of State with the attributes replaced.
        """
        return replace(self, **kwargs)

    def barchart(
        self, bar_values: list[float], bar_names: list[str], bar_colors: list[str]
    ) -> BarChart:
        """
        Returns an BarChart object with the specified x-/y-labels.

        Args:
            bar_values (list[float]):
                The y-values of the bars.

            bar_names (list[str]):
                The x-values of the bars.

            bar_colors: list[str]:
                The colors of the bars.

        Returns:
            BarChart:
                An BarChart object with the specified x-/y-labels.
        """
        ax = create_barchart(
            bar_values=bar_values,
            bar_names=bar_names,
            y_range=[self.y_min, self.y_max, self.y_tick],
            bar_colors=bar_colors,
        )
        update_bar_names(ax, bar_names, bar_values)
        update_bar_values(ax, self.y_min, self.y_max, self.num_y_ticks)
        return ax


class GrowingBarplot(StockVisualization):
    """
    Visualization of stock prices with barplots for multiple tickers.

    Attributes:
        path (str):
            The path to the CSV file containing the stock data

        names (str | list[str] | None):
            The names of the bars.

        title (str):
            The title of the visualization

        x_label (str):
            The label of the x-axis

        y_label (str):
            The label of the y-axis

        background_run_time (int):
            The run time for the write animation of the background elements

        animation_run_time (int):
            The run time for the create animation of the bars

        wait_run_time (int):
            The run time for the fade out animation at the end

        camera_scale (float):
            The scale factor for the camera frame

        colors(str | list[str] | None):
            The colors for all bars

        num_ticks (int):
            The number of ticks on the x-/y-axis

        num_samples (int):
            The number of samples to draw from the entire data
    """

    def __init__(
        self,
        path: str,
        names: str | list[str],
        title: str = "Market Price",
        x_label: str = "Stocks",
        y_label: str = r"Price [\$]",
        background_run_time: int = 5,
        animation_run_time: int = 50,
        wait_run_time: int = 5,
        camera_scale: float = 1.2,
        colors: str | list[str] | None = None,
        num_ticks: int = 6,
        num_samples: int = 100,
        **kwargs,
    ):
        super().__init__(
            path=path,
            title=title,
            x_label=x_label,
            y_label=y_label,
            background_run_time=background_run_time,
            animation_run_time=animation_run_time,
            wait_run_time=wait_run_time,
            camera_scale=camera_scale,
            num_ticks=num_ticks,
            num_samples=num_samples,
            **kwargs,
        )

        if isinstance(names, str):
            names = [names]
        if colors is None:
            colors = [
                "#003f5c",
                "#58508d",
                "#bc5090",
                "#ff6361",
                "#ffa600",
            ][: self.Y.shape[-1]]
        elif isinstance(colors, str):
            colors = [colors]

        assert (
            len(names) == self.Y.shape[-1]
        ), "names should have the same length as the number of tickers!"
        assert (
            len(colors) >= self.Y.shape[-1]
        ), "colors should have at least as many colors as tickers!"

        self.names = names
        self.colors = colors
        self.next_indicies = int(self.num_samples / self.num_ticks)

    def construct(self):
        #  Scale the camera frame up by camera_frame_scale
        self.camera.frame.scale(self.camera_scale)

        state = State(
            y_min=0,
            y_max=np.max(self.Y[3 * self.next_indicies]),
            num_y_ticks=3,
        )

        # Create the title
        title = create_title(self.title)

        # Create the barchart
        ax = state.barchart(self.Y[0], self.names, self.colors)

        self.play(
            Write(VGroup(ax, title)),
            run_time=self.background_run_time,
        )

        for i in range(1, len(self.df)):
            # Scale y-axis
            if np.max(self.Y[i]) >= state.y_max:
                if state.num_y_ticks < self.num_ticks:
                    state = state.replace(num_y_ticks=state.num_y_ticks + 1)
                state = state.replace(
                    y_max=np.max(self.Y[: min(i + self.next_indicies, len(self.df)), :])
                )

            new_ax = state.barchart(self.Y[i], self.names, self.colors)

            self.play(
                ReplacementTransform(ax, new_ax),
                run_time=self.animation_run_time / len(self.df),
            )

            # Update references for next iteration
            ax = new_ax

        self.wait(self.wait_run_time)
