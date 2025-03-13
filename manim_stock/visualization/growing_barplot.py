"""Visualization of stock prices with barplots for multiple tickers."""

import logging
from dataclasses import dataclass, replace
from typing import List

import numpy as np
from manim import (
    DOWN,
    UP,
    BarChart,
    FadeOut,
    ReplacementTransform,
    VGroup,
    Write,
    config,
)

from manim_stock.util import (
    create_barchart,
    create_tex,
    next_to_tex,
    remove_bar_names,
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
        
        y_round (bool):
            Whether to use non-decimal numbers for the y-axis labels.
    """

    y_min: float
    y_max: float
    num_y_ticks: int
    y_round: bool

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
        self, bar_values: List[float], bar_names: List[str], bar_colors: List[str]
    ) -> BarChart:
        """
        Returns an BarChart object with the specified x-/y-labels.

        Args:
            bar_values (List[float]):
                The y-values of the bars.

            bar_names (List[str]):
                The x-values of the bars.

            bar_colors (List[str]):
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
        remove_bar_names(ax)
        update_bar_values(ax, self.y_min, self.y_max, self.num_y_ticks, self.y_round)
        return ax


class GrowingBarplot(StockVisualization):
    """Visualization of stock prices with barplots for multiple tickers."""

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
            x_round=x_round,
            y_round=y_round,
            **kwargs,
        )

        self.next_indicies = int(self.num_samples / self.num_ticks)

    def construct(self):
        #  Scale the camera frame up by camera_frame_scale
        self.camera.frame.scale(self.camera_scale)

        state = State(
            y_min=0,
            y_max=np.max(self.Y[3 * self.next_indicies]),
            num_y_ticks=3,
            y_round=self.y_round,
        )

        # Create the barchart
        ax = state.barchart(self.Y[0], self.names, self.colors)
        xs = np.arange(0.5, self.Y.shape[-1], 1)
        points = [ax.x_axis.number_to_point(xs[j]) for j in range(self.Y.shape[-1])]
        directions = [UP if self.Y[0, j] < 0 else DOWN for j in range(self.Y.shape[-1])]
        bar_names = [
            next_to_tex(
                tex=create_tex(self.names[j], color=self.colors[j]),
                mobject_or_point=points[j],
                direction=directions[j],
            )
            for j in range(self.Y.shape[-1])
        ]
        bar_values = [
            next_to_tex(
                tex=create_tex(np.round(self.Y[0, j], 2), color=self.colors[j]),
                mobject_or_point=bar_names[j],
                direction=directions[j],
            )
            for j in range(self.Y.shape[-1])
        ]

        self.play(
            Write(VGroup(ax, *bar_names, *bar_values)),
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
            new_xs = np.arange(0.5, self.Y.shape[-1], 1)
            new_points = [
                new_ax.x_axis.number_to_point(new_xs[j])
                for j in range(self.Y.shape[-1])
            ]
            new_directions = [
                UP if self.Y[i, j] < 0 else DOWN for j in range(self.Y.shape[-1])
            ]
            new_bar_names = [
                next_to_tex(
                    tex=create_tex(self.names[j], color=self.colors[j]),
                    mobject_or_point=new_points[j],
                    direction=new_directions[j],
                )
                for j in range(self.Y.shape[-1])
            ]
            new_bar_values = [
                next_to_tex(
                    tex=create_tex(np.round(self.Y[i, j], 2), color=self.colors[j]),
                    mobject_or_point=new_bar_names[j],
                    direction=new_directions[j],
                )
                for j in range(self.Y.shape[-1])
            ]

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
