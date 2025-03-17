"""Visualization of stock prices with lineplots for multiple ticker."""

import logging
from dataclasses import dataclass, replace
from typing import Sequence

import numpy as np
from manim import (
    Axes,
    Dot,
    FadeOut,
    Mobject,
    ReplacementTransform,
    Tex,
    VGroup,
    VMobject,
    Write,
    config,
)
from manim.typing import Vector2D, Vector2D_Array

from manim_stock.util import (
    add_x_labels_custom,
    add_y_labels_range,
    create_axes,
    create_dot,
    create_graph,
    create_label_name,
    create_label_value,
    remove_x_labels,
    remove_y_labels,
)
from manim_stock.visualization.plot import Plot

# Set logging level to WARNING
logging.getLogger("manim").setLevel(logging.WARNING)

# Disable caching to speed up the rendering process
config.disable_caching = True


@dataclass(frozen=True)
class State:
    """
    Dataclass to store the state of the visualization of Lineplot.

    Attributes:
        time (int):
            The timestep of the visualization.

        x_min (float):
            The minimum value of the x-axis.

        x_max (float):
            The maximum value of the x-axis.

        num_x_ticks (int):
            The number of ticks of the x-axis.

        x_decimals (int):
            The number of decimal places to round to.

        y_min (float):
            The minimum value of the y-axis.

        y_max (float):
            The maximum value of the y-axis.

        num_y_ticks (int):
            The number of ticks of the y-axis.

        y_decimals (int):
            The number of decimal places to round to.
    """

    time: int
    x_min: float
    x_max: float
    num_x_ticks: int
    x_decimals: int
    y_min: float
    y_max: float
    num_y_ticks: int
    y_decimals: int

    @property
    def x_tick(self) -> float:
        """The value between each tick of the x-axis."""
        return (self.x_max - self.x_min) / self.num_x_ticks

    @property
    def y_tick(self) -> float:
        """The value between each tick of the y-axis."""
        return (self.y_max - self.y_min) / self.num_y_ticks

    def replace(self, **kwargs) -> "State":
        """Returns a new state with the replaced attributes."""
        return replace(self, **kwargs)

    def axes(self, x_labels: np.ndarray, **kwargs) -> Axes:
        """
        Returns an Axes object with the specified x-/y-labels.

        Args:
            x_labels (np.ndarray):
                The custom x-labels to display.

            **kwargs:
                Additional arguments to pass to create_axes().

        Returns:
            Axes:
                An Axes object with the specified x-/y-labels.
        """
        ax = create_axes(
            x_range=[self.x_min, self.x_max, self.x_tick],
            y_range=[self.y_min, self.y_max, self.y_tick],
            **kwargs,
        )
        remove_x_labels(ax)
        remove_y_labels(ax)
        add_x_labels_custom(
            ax,
            x_labels,
            self.num_x_ticks,
            self.x_decimals,
        )
        add_y_labels_range(
            ax,
            self.y_min,
            self.y_max,
            self.num_y_ticks,
            self.y_decimals,
        )
        return ax

    def points(self, ax: Axes, x_indices: np.ndarray, y: np.ndarray) -> Vector2D_Array:
        """
        Returns the points of the graph.

        Args:
            ax (Axes):
                The Axes object.

            x_indices (np.ndarray):
                The indices of the x-values.

            y (np.ndarray):
                The y-values.

        Returns:
            Vector2D_Array:
                The points of the graph.
        """
        return [ax.c2p(x_indices[i], y[i]) for i in range(len(x_indices))]

    def dots(self, points: Vector2D_Array) -> Sequence[Dot]:
        """
        Returns the Dot objects at each point.

        Args:
            points (Vector2D_Array):
                The points.

        Returns:
            Sequence[Dot]:
                The Dot objects
        """
        return [create_dot(point) for point in points]

    def graph(self, points: Vector2D_Array, **kwargs) -> VMobject:
        """
        Create a Graph object.

        Args:
            points (Vector2D_Array):
                The points.

            **kwargs:
                Additional arguments to pass to create_graph().

        Returns:
            VMobject:
                The Graph object.
        """
        return create_graph(points=points, **kwargs)

    def graph_name(self, name: str, mobject_or_point: Vector2D, **kwargs) -> Tex:
        """
        Create a Tex object with the specified name next to the mobject/point.

        Args:
            name (str):
                The name to display.

            mobject_or_point (Vector2D | Mobject):
                The point/mobject where the name will be located.

            **kwargs:
                Additional arguments to pass to create_label_name().

        Returns:
            Tex:
                The Tex object.
        """
        return create_label_name(name=name, mobject_or_point=mobject_or_point, **kwargs)

    def graph_value(self, value: float, mobject_or_point: Vector2D, **kwargs) -> Tex:
        """
        Create a Tex object with the specified value next to the last point.

        Args:
            value (float):
                The value to display.

            mobject_or_point (Vector2D | Mobject):
                The point/mobject where the value will be located.

            **kwargs:
                Additional arguments to pass to create_label_value().

        Returns:
            Tex:
                The Tex object.
        """
        return create_label_value(
            value=value,
            mobject_or_point=mobject_or_point,
            value_decimals=self.y_decimals,
            **kwargs,
        )


class Lineplot(Plot):
    """Visualization of stock prices with lineplots for multiple tickers."""

    def __init__(self, path: str, **kwargs):
        super().__init__(path=path, **kwargs)

    def _create_state(self) -> State:
        return State(
            time=0,
            x_min=0,
            x_max=self.X_indices.max(),
            num_x_ticks=3,
            x_decimals=self.x_decimals,
            y_min=0,
            y_max=self.Y.max(),
            num_y_ticks=3,
            y_decimals=self.y_decimals,
        )

    def _update_state(self, state: State, time: int) -> State:
        """Returns the initial state of the visualization."""
        return state.replace(time=time)

    def _create_mobjects(self, state: State) -> Sequence[Mobject]:
        """Returns the mobjects for the current state."""
        ax = state.axes(self.X[: state.x_max])
        points = [
            state.points(ax, self.X_indices, self.Y[:, j])[: state.time + 1]
            for j in range(self.Y.shape[-1])
        ]
        graphs = [
            state.graph(points=points[j], color=self.colors[j])
            for j in range(self.Y.shape[-1])
        ]
        graph_names = [
            state.graph_name(
                name=self.names[j],
                mobject_or_point=points[j][-1],
                **{"tex_config": {"color": self.colors[j]}},
            )
            for j in range(self.Y.shape[-1])
        ]
        graph_values = [
            state.graph_value(
                value=self.Y[state.time, j],
                mobject_or_point=points[j][-1],
                **{"tex_config": {"color": self.colors[j]}},
            )
            for j in range(self.Y.shape[-1])
        ]
        return ax, graphs, graph_names, graph_values

    def construct(self):
        #  Scale the camera frame up by camera_frame_scale
        self.camera.frame.scale(self.camera_scale)

        # Create the initial state and mobjects
        state = self._create_state()
        ax, graphs, graph_names, graph_values = self._create_mobjects(state)

        # Display the initial mobjects
        self.play(
            Write(VGroup(ax, *graphs, *graph_names, *graph_values)),
            run_time=self.background_run_time,
        )

        # Incrementally update the state and mobjects
        for i in range(1, len(self.df)):
            state = self._update_state(state, i)
            new_ax, new_graphs, new_graph_names, new_graph_values = (
                self._create_mobjects(state)
            )

            # Animate the transition from the old to the new mobjects
            self.play(
                ReplacementTransform(ax, new_ax),
                ReplacementTransform(VGroup(*graphs), VGroup(*new_graphs)),
                ReplacementTransform(VGroup(*graph_names), VGroup(*new_graph_names)),
                ReplacementTransform(VGroup(*graph_values), VGroup(*new_graph_values)),
                run_time=self.animation_run_time / len(self.df),
            )

            # Update references for next iteration
            ax = new_ax
            graphs = new_graphs
            graph_names = new_graph_names
            graph_values = new_graph_values

        # Wait before finishing the animation
        self.play(
            FadeOut(VGroup(*graph_names, *graph_values)),
            run_time=self.wait_run_time,
        )
