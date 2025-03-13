"""Visualization of stock prices over time for multiple ticker."""

import logging
from dataclasses import dataclass, replace
from typing import List, Tuple

import numpy as np
from manim import (
    RIGHT,
    UR,
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

from manim_stock.util import (
    create_axes,
    create_dot,
    create_tex,
    next_to_tex,
    update_x_labels,
    update_y_labels,
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
    ) -> List[Tuple[float, float]]:
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
            List[Tuple[float, float]]:
                The points on the graph corresponding to the x-/y-values.
        """
        return [ax.c2p(x_indices[i], y[i]) for i in range(len(x_indices))]

    def dots(self, points: List[Tuple[float, float]]) -> List[Dot]:
        """
        Returns a list of dots objects at the specified points.

        Args:
            points (List[Tuple[float, float]]):
                The points to place the dots.

        Returns:
            List[Dot]:
                The list of dots
        """
        return [create_dot(point) for point in points]


class Lineplot(StockVisualization):
    """Visualization of stock prices with line graphs for multiple tickers."""

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
            colors=colors,
            num_ticks=num_ticks,
            num_samples=num_samples,
            **kwargs,
        )

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
        ax = state.axes(self.X, np.max(self.Y, axis=-1))
        points = [
            state.points(ax, self.X_indices, self.Y[:, j])[:1]
            for j in range(self.Y.shape[-1])
        ]
        graphs = [
            VMobject(color=self.colors[j]).set_points_as_corners(points[j])
            for j in range(self.Y.shape[-1])
        ]
        dots = [state.dots(points[j]) for j in range(self.Y.shape[-1])]
        graph_names = [
            next_to_tex(
                tex=create_tex(self.names[j], color=self.colors[j]),
                mobject_or_point=state.points(ax, self.X_indices, self.Y[:, j])[0],
                direction=UR,
            )
            for j in range(self.Y.shape[-1])
        ]
        graph_values = [
            next_to_tex(
                tex=create_tex(np.round(self.Y[0, j], 2), color=self.colors[j]),
                mobject_or_point=state.points(ax, self.X_indices, self.Y[:, j])[0],
                direction=RIGHT,
            )
            for j in range(self.Y.shape[-1])
        ]

        self.play(
            Write(VGroup(ax, *graphs, *dots, *graph_names, *graph_values)),
            run_time=self.background_run_time,
        )

        for i in range(1, len(self.df)):
            new_points = [
                state.points(ax, self.X_indices, self.Y[:, j])[: i + 1]
                for j in range(self.Y.shape[-1])
            ]
            new_graphs = [
                VMobject(color=self.colors[j]).set_points_as_corners(new_points[j])
                for j in range(self.Y.shape[-1])
            ]
            new_dots = [state.dots(new_points[j]) for j in range(self.Y.shape[-1])]
            new_graph_names = [
                next_to_tex(
                    tex=create_tex(self.names[j], color=self.colors[j]),
                    mobject_or_point=state.points(ax, self.X_indices, self.Y[:, j])[i],
                    direction=UR,
                )
                for j in range(self.Y.shape[-1])
            ]
            new_graph_values = [
                next_to_tex(
                    tex=create_tex(np.round(self.Y[i, j], 2), color=self.colors[j]),
                    mobject_or_point=state.points(ax, self.X_indices, self.Y[:, j])[i],
                    direction=RIGHT,
                )
                for j in range(self.Y.shape[-1])
            ]
            self.play(
                Transform(VGroup(*graphs), VGroup(*new_graphs)),
                ReplacementTransform(VGroup(*dots), VGroup(*new_dots)),
                ReplacementTransform(VGroup(*graph_names), VGroup(*new_graph_names)),
                ReplacementTransform(VGroup(*graph_values), VGroup(*new_graph_values)),
                run_time=self.animation_run_time / len(self.df),
            )

            points = new_points
            dots = new_dots
            graph_names = new_graph_names
            graph_values = new_graph_values

        self.play(
            FadeOut(VGroup(*dots, *graph_names, *graph_values)),
            run_time=self.wait_run_time,
        )
