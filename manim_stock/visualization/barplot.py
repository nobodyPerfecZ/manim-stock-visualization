"""Visualization of stock prices with barplots for multiple tickers."""

import logging
from dataclasses import dataclass, replace
from typing import Sequence

from manim import (
    DOWN,
    UP,
    BarChart,
    FadeOut,
    Mobject,
    ReplacementTransform,
    Tex,
    VGroup,
    Write,
    config,
)
from manim.typing import Vector2D

from manim_stock.util import (
    add_bar_values,
    create_barchart,
    create_label_name,
    create_label_value,
    remove_bar_names,
    remove_bar_values,
)
from manim_stock.visualization.plot import Plot

# Set logging level to WARNING
logging.getLogger("manim").setLevel(logging.WARNING)

# Disable caching to speed up the rendering process
config.disable_caching = True


@dataclass(frozen=True)
class State:
    """
    Dataclass to store the state of the visualization of Barplot.

    Attributes:
        time (int):
            The timestep of the visualization.

        y_min (float):
            The minimum value of the y-axis.

        y_max (float):
            The maximum value of the y-axis.

        num_y_ticks (int):
            The number of ticks of the y-axis.

        y_decimals (float):
            The number of decimal places to round to.
    """

    time: int
    y_min: float
    y_max: float
    num_y_ticks: int
    y_decimals: int

    @property
    def y_tick(self) -> float:
        """The value between each tick of the y-axis."""
        return (self.y_max - self.y_min) / self.num_y_ticks

    def replace(self, **kwargs) -> "State":
        """Returns a new state with the replaced attributes."""
        return replace(self, **kwargs)

    def barchart(
        self,
        bar_values: Sequence[float],
        bar_names: Sequence[str],
        bar_colors: Sequence[str],
        **kwargs,
    ) -> BarChart:
        """
        Returns an BarChart object with the specified x-/y-labels.

        Args:
            bar_values (Sequence[float]):
                The y-values of the bars.

            bar_names (Sequence[str]):
                The x-values of the bars.

            bar_colors (Sequence[str]):
                The colors of the bars.

            **kwargs:
                Additional arguments to pass to create_barchart().

        Returns:
            BarChart:
                An BarChart object with the specified x-/y-labels.
        """
        ax = create_barchart(
            bar_values=bar_values,
            bar_names=bar_names,
            y_range=[self.y_min, self.y_max, self.y_tick],
            bar_colors=bar_colors,
            **kwargs,
        )
        remove_bar_names(ax)
        remove_bar_values(ax)
        add_bar_values(
            ax,
            self.y_min,
            self.y_max,
            self.num_y_ticks,
            self.y_decimals,
        )
        return ax

    def bar_position(self, ax: BarChart, bar_idx: int) -> Vector2D:
        """
        Returns the position of the i-th bar.

        Args:
            ax (BarChart):
                The BarChart object.

            bar_idx (int):
                The i-th index.

        Returns:
            Vector2D:
                The position of the i-th bar.
        """
        return ax.x_axis.number_to_point(0.5 + 1 * bar_idx)

    def direction(self, value: float) -> Vector2D:
        """
        Returns the direction (UP/DOWN) of the bar.

        Args:
            value (float):
                The y-value of the bar.

        Returns:
            Vector2D:
                The direction of the bar.
        """
        return UP if value < 0 else DOWN

    def bar_name(
        self,
        name: str,
        mobject_or_point: Vector2D | Mobject,
        **kwargs,
    ) -> Tex:
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

    def bar_value(
        self,
        value: float,
        mobject_or_point: Vector2D | Mobject,
        **kwargs,
    ) -> Tex:
        """
        Create a Tex object with the specified value next to the mobject/point.

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


class Barplot(Plot):
    """Visualization of stock prices with barplots for multiple tickers."""

    def __init__(self, path: str, **kwargs):
        super().__init__(path=path, **kwargs)

    def _create_state(self) -> State:
        """Returns the initial state of the visualization."""
        return State(
            time=0,
            y_min=0,
            y_max=self.Y.max(),
            num_y_ticks=self.num_y_ticks,
            y_decimals=self.y_decimals,
        )

    def _update_state(self, state: State, time: int) -> State:
        """Updates the state of the visualization."""
        return state.replace(time=time)

    def _create_mobjects(self, state: State) -> Sequence[Mobject]:
        """Returns the mobjects for the current state."""
        ax = state.barchart(self.Y[state.time], self.names, self.colors)
        points = [state.bar_position(ax, j) for j in range(self.Y.shape[-1])]
        directions = [
            state.direction(self.Y[state.time, j]) for j in range(self.Y.shape[-1])
        ]
        bar_names = [
            state.bar_name(
                name=self.names[j],
                mobject_or_point=points[j],
                **{
                    "tex_config": {"color": self.colors[j]},
                    "next_to_config": {"direction": directions[j]},
                },
            )
            for j in range(self.Y.shape[-1])
        ]
        bar_values = [
            state.bar_value(
                value=self.Y[state.time, j],
                mobject_or_point=bar_names[j],
                **{
                    "tex_config": {"color": self.colors[j]},
                    "next_to_config": {"direction": directions[j]},
                },
            )
            for j in range(self.Y.shape[-1])
        ]
        return ax, bar_names, bar_values

    def construct(self):
        #  Scale the camera frame up by camera_frame_scale
        self.camera.frame.scale(self.camera_scale)

        # Create the initial state and mobjects
        state = self._create_state()
        ax, bar_names, bar_values = self._create_mobjects(state)

        # Display the initial mobjects
        self.play(
            Write(VGroup(ax, *bar_names, *bar_values)),
            run_time=self.background_run_time,
        )

        # Incrementally update the state and mobjects
        for i in range(1, len(self.df)):
            state = self._update_state(state, i)
            new_ax, new_bar_names, new_bar_values = self._create_mobjects(state)

            # Animate the transition from the old to the new mobjects
            self.play(
                ReplacementTransform(ax, new_ax),
                ReplacementTransform(VGroup(*bar_names), VGroup(*new_bar_names)),
                ReplacementTransform(VGroup(*bar_values), VGroup(*new_bar_values)),
                run_time=self.animation_run_time / len(self.df),
            )

            # Update references for next iteration
            ax = new_ax
            bar_names = new_bar_names
            bar_values = new_bar_values

        # Wait before finishing the animation
        self.play(
            FadeOut(VGroup(*bar_names, *bar_values)),
            run_time=self.wait_run_time,
        )
