"""Visualization of stock prices over time for multiple ticker."""

import logging
from dataclasses import dataclass, replace

import numpy as np
from manim import (
    DEFAULT_FONT_SIZE,
    UR,
    WHITE,
    Axes,
    Create,
    DecimalNumber,
    Dot,
    FadeOut,
    ValueTracker,
    VGroup,
    Write,
    config,
)

from manim_stock.util import create_axes, create_title, update_x_labels, update_y_labels
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

    x_min: float
    x_max: float
    num_x_ticks: int
    y_min: float
    y_max: float
    num_y_ticks: int

    @property
    def x_tick(self) -> float:
        """The value between each tick on the x-axis."""
        return (self.x_max - self.x_min) / self.num_x_ticks

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

    def axes(self, x: np.ndarray, y: np.ndarray) -> Axes:
        """
        Returns an Axes object with the specified x-/y-labels.

        Args:
            x (np.ndarray):
                The x-values of the data points.

            y (np.ndarray):
                The y-values of the data points.

        Returns:
            Axes:
                An Axes object with the specified x-/y-labels.
        """
        ax = create_axes(
            x_range=[self.x_min, self.x_max, self.x_tick],
            y_range=[self.y_min, self.y_max, self.y_tick],
        )
        update_x_labels(ax, x, self.x_min, self.x_max, self.num_x_ticks)
        update_y_labels(ax, y, self.y_min, self.y_max, self.num_y_ticks)
        return ax

    def points(
        self, ax: Axes, x_indices: np.ndarray, y: np.ndarray
    ) -> list[tuple[float, float]]:
        """
        Returns the points on the graph corresponding to the x-/y-values.

        Args:
            ax (Axes):
                The Axes object to plot

            x_indices (np.ndarray):
                The x-values of the data points.

            y (np.ndarray):
                The y-values of the data points.

        Returns:
            list[tuple[float, float]]:
                The points on the graph corresponding to the x-/y-values.
        """
        return [ax.c2p(x_indices[i], y[i]) for i in range(len(x_indices))]


class Lineplot(StockVisualization):
    """
    Visualization of stock prices with line graphs for multiple tickers.

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

        background_run_time (int):
            The run time for the write animation of the background elements

        animation_run_time (int):
            The run time for the create animation of the graph

        wait_run_time (int):
            The run time for the fade out animation at the end

        camera_scale (float):
            The scale factor for the camera frame

        graph_colors(list[str]):
            The colors for all graphs

        num_ticks (int):
            The number of ticks on the x-/y-axis

        num_samples (int):
            The number of samples to draw from the entire data
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

        if colors is None:
            colors = [
                "#003f5c",
                "#58508d",
                "#bc5090",
                "#ff6361",
                "#ffa600",
            ][: len(self.df.columns) - 1]
        elif isinstance(colors, str):
            colors = [colors]

        assert (
            len(colors) >= len(self.df.columns) - 1
        ), "colors should have at least as many colors as tickers!"

        self.colors = colors

    def _create_line_graph_with_value_tracker(
        self,
        ax: Axes,
        x_tracker: ValueTracker,
        color: str,
        x: np.ndarray,
        y: np.ndarray,
    ):
        """Creates a line graph including its dot and value tracker."""
        f = ax.plot_line_graph(
            x_values=np.arange(len(x)),
            y_values=y,
            line_color=color,
            add_vertex_dots=False,
        )
        points = f.get_all_points()

        dot = Dot(points[0], color=WHITE)
        dot.add_updater(lambda mob: mob.move_to(points[int(x_tracker.get_value())]))

        return f, dot

    def construct(self):
        #  Scale the camera frame up by camera_frame_scale
        self.camera.frame.scale(self.camera_scale)

        # Create the initial state
        state = State(
            x_min=0,
            x_max=self.X_indices.max(),
            num_x_ticks=self.num_ticks,
            y_min=0,
            y_max=self.Y.max(),
            num_y_ticks=self.num_ticks,
        )

        # Create the axes
        ax = state.axes(self.X, self.Y)

        # Create the title
        title = create_title(self.title)

        # Create the x position tracker
        x_tracker = ValueTracker(0)

        # Plot the line graph
        graphs = [
            ax.plot_line_graph(
                x_values=self.X_indices,
                y_values=self.Y[:, j],
                line_color=self.colors[j],
                add_vertex_dots=False,
            )
            for j in range(len(self.df.columns) - 1)
        ]
        points = [graphs[j].get_all_points() for j in range(len(self.df.columns) - 1)]
        dots = [Dot(points[j][0], radius=0.02) for j in range(len(self.df.columns) - 1)]
        for j in range(len(self.df.columns) - 1):
            dots[j].add_updater(lambda mob: mob.move_to(points[j][int(x_tracker.get_value())]))
        animations = [Create(graphs[j]) for j in range(len(self.df.columns) - 1)]

        # Play the animation
        self.play(
            Write(VGroup(ax, title, *dots)),
            run_time=self.background_run_time,
        )
        self.play(
            *animations,
            x_tracker.animate.set_value(len(self.df) - 1),
            run_time=self.animation_run_time,
        )
        self.play(
            FadeOut(VGroup(*dots)),
            run_time=self.wait_run_time,
        )
