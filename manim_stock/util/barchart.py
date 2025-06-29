"""Utility functions for Barchart objects."""

from typing import Sequence

import numpy as np
from manim import DOWN, UP, BarChart, VGroup, config

from manim_stock.util.const import AXES_FONT_SIZE


def create_barchart(
    bar_values: Sequence[float],
    bar_names: Sequence[str],
    y_range: Sequence[float],
    bar_colors: Sequence[str],
    **kwargs,
) -> BarChart:
    """
    Creates a BarChart object.

    Args:
        bar_values (Sequence[float]):
            The values of the bars.

        bar_names (Sequence[str]):
            The names of the bars.

        y_range (Sequence[float]):
            The [y_min, y_max, y_step] of the y-axis.

        bar_colors (Sequence[str]):
            The colors of the bars.

        **kwargs:
            Additional arguments to be passed to BarChart().

    Returns:
        BarChart:
            A BarChart object.
    """
    if "x_length" not in kwargs:
        kwargs["x_length"] = round(config.frame_width) - 2
    if "y_length" not in kwargs:
        kwargs["y_length"] = round(config.frame_height) - 2
    if "tips" not in kwargs:
        kwargs["tips"] = False
    if "x_axis_config" not in kwargs:
        kwargs["x_axis_config"] = {
            "include_numbers": False,
            "font_size": AXES_FONT_SIZE,
        }
    if "y_axis_config" not in kwargs:
        kwargs["y_axis_config"] = {
            "include_numbers": False,
            "font_size": AXES_FONT_SIZE,
        }

    return BarChart(
        values=bar_values,
        bar_names=bar_names,
        y_range=y_range,
        bar_colors=bar_colors,
        **kwargs,
    )


def remove_bar_names(ax: BarChart):
    """
    Remove the x-axis labels from an BarChart object.

    Args:
        ax (BarChart):
            The BarChart object.
    """
    if hasattr(ax.x_axis, "labels"):
        ax.x_axis.remove(ax.x_axis.labels)
    if hasattr(ax.x_axis, "numbers"):
        ax.x_axis.remove(ax.x_axis.numbers)


def add_bar_names(ax: BarChart, bar_names: Sequence[str]):
    """
    Add x-axis labels to an BarChart object.

    Args:
        ax (BarChart):
            The BarChart object.

        bar_names (Sequence[str]):
            The x-axis labels of the bars.
    """
    val_range = np.arange(0.5, len(bar_names), 1)
    labels = VGroup()
    for i, (value, bar_name) in enumerate(zip(val_range, bar_names, strict=True)):
        direction = UP if ax.values[i] < 0 else DOWN
        bar_name_label = ax.x_axis.label_constructor(bar_name)

        bar_name_label.font_size = ax.x_axis.font_size
        bar_name_label.next_to(
            ax.x_axis.number_to_point(value),
            direction=direction,
            buff=ax.x_axis.line_to_number_buff,
        )

        labels.add(bar_name_label)
    ax.x_axis.labels = labels
    ax.x_axis.add(labels)


def remove_bar_values(ax: BarChart):
    """
    Remove the y-axis labels from a BarChart object.

    Args:
        ax (BarChart):
            The BarChart object.
    """
    if hasattr(ax.y_axis, "labels"):
        ax.y_axis.remove(ax.y_axis.labels)
    if hasattr(ax.y_axis, "numbers"):
        ax.y_axis.remove(ax.y_axis.numbers)


def add_bar_values(
    ax: BarChart,
    y_min: float,
    y_max: float,
    num_y_ticks: int,
    y_decimals: int,
):
    """
    Add new y-axis labels to a BarChart object.

    Args:
        ax (BarChart):
            The BarChart object.

        y_min (float):
            The minimum value of the y-axis.

        y_max (float):
            The maximum value of the y-axis.

        num_y_ticks (int):
            The number of y-axis ticks.

        y_decimals (int):
            The number of decimals of the y-axis labels.
    """
    y_labels = np.linspace(y_min, y_max, num_y_ticks + 1, endpoint=True)[1:]

    if y_decimals:
        y_labels = np.round(y_labels, decimals=y_decimals)
    else:
        y_labels = np.fix(y_labels).astype(np.int32)

    ax.y_axis.add_labels(dict(zip(ax.y_axis.get_tick_range(), y_labels, strict=True)))
