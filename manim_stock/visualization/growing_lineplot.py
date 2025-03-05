"""Visualization of stock prices over time with growing axes for multiple ticker."""

import logging
from dataclasses import dataclass, replace

import numpy as np
from manim import (
    Axes,
    Dot,
    FadeOut,
    ReplacementTransform,
    Transform,
    VGroup,
    VMobject,
    Write,
    config,
)

from manim_stock.util import create_axes, update_x_labels, update_y_labels
from manim_stock.util.title import create_title
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


class GrowingLineplot(StockVisualization):
    """
    A class to visualize the growth of a line plot over time.

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

        colors(str | list[str] | None):
            The colors for all graphs

        num_ticks (int):
            The number of maximum ticks on the x-/y-axis

        num_samples (int):
            The number of samples to draw from the entire data
    """

    def __init__(
        self,
        path: str,
        title: str = "Market Price",
        x_label: str = "Year",
        y_label: str = r"Price [\$]",
        background_run_time: int = 10,
        animation_run_time: int = 45,
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
            ][: self.Y.shape[-1]]
        elif isinstance(colors, str):
            colors = [colors]
        assert (
            len(colors) >= self.Y.shape[-1]
        ), "colors should have at least as many colors as tickers!"

        self.colors = colors
        self.next_indicies = int(self.num_samples / self.num_ticks)

    def construct(self):
        #  Scale the camera frame up by camera_frame_scale
        self.camera.frame.scale(self.camera_scale)

        # Create the initial state of the visualization
        state = State(
            x_min=0,
            x_max=self.X_indices[3 * self.next_indicies],
            num_x_ticks=3,
            y_min=0,
            y_max=np.max(self.Y[3 * self.next_indicies]),
            num_y_ticks=3,
        )

        # Create the title
        title = create_title(self.title)

        # Create the axes, data points, graphs and dots
        ax = state.axes(self.X, np.max(self.Y, axis=-1))
        points = [
            state.points(ax, self.X_indices, self.Y[:, j])[:1]
            for j in range(len(self.df.columns) - 1)
        ]
        graphs = [
            VMobject(color=self.colors[j]).set_points_as_corners(points[j])
            for j in range(len(self.df.columns) - 1)
        ]
        dots = [
            Dot(point, radius=0.02)
            for j in range(len(self.df.columns) - 1)
            for point in points[j]
        ]

        # Animate the creation of the axes, title, graph and dots
        self.play(
            Write(VGroup(ax, title, *graphs, *dots)),
            run_time=self.background_run_time,
        )

        # Incrementally add data points and scale axis if needed
        for i in range(1, len(self.df)):
            # Scale y-axis
            if np.max(self.Y[i]) >= state.y_max:
                if state.num_y_ticks < self.num_ticks:
                    state = state.replace(num_y_ticks=state.num_y_ticks + 1)
                state = state.replace(
                    y_max=np.max(self.Y[: min(i + self.next_indicies, len(self.df)), :])
                )

            # Scale x-axis
            if self.X_indices[i] >= state.x_max:
                if state.num_x_ticks < self.num_ticks:
                    state = state.replace(num_x_ticks=state.num_x_ticks + 1)
                state = state.replace(
                    x_max=np.max(
                        self.X_indices[: min(i + self.next_indicies, len(self.df))]
                    )
                )

            # Create new axes, data points, graphs and dots
            new_ax = state.axes(self.X, np.max(self.Y, axis=-1))
            new_points = [
                state.points(new_ax, self.X_indices, self.Y[:, j])[: i + 1]
                for j in range(len(self.df.columns) - 1)
            ]
            new_graphs = [
                VMobject(color=self.colors[j]).set_points_as_corners(new_points[j])
                for j in range(len(self.df.columns) - 1)
            ]
            new_dots = [
                Dot(point, radius=0.02)
                for j in range(len(self.df.columns) - 1)
                for point in new_points[j]
            ]

            # Animate graph growth and axis scaling
            self.play(
                ReplacementTransform(ax, new_ax),
                Transform(VGroup(*graphs), VGroup(*new_graphs)),
                ReplacementTransform(VGroup(*dots), VGroup(*new_dots)),
                run_time=self.animation_run_time / len(self.df),
            )

            # Update references for next iteration
            ax = new_ax
            points = new_points
            dots = new_dots

        # Remove the dots from the graph before finishing the animation
        self.play(
            FadeOut(VGroup(*dots)),
            run_time=self.wait_run_time,
        )
