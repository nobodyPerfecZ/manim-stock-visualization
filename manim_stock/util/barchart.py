"""Utility functions for Barchart objects."""

from typing import List

import numpy as np
from manim import DOWN, UP, BarChart, VGroup, config

from manim_stock.util.const import AXES_FONT_SIZE


def create_barchart(
    bar_values: List[float],
    bar_names: List[str],
    y_range: List[float],
    bar_colors: List[str],
) -> BarChart:
    """
    Creates a BarChart object.

    Args:
        bar_values (List[float]):
            The values of the bars.

        bar_names (List[str]):
            The names of the bars.

        y_range (List[float]):
            The [y_min, y_max, y_step] of the y-axis.

        bar_colors (List[str]):
            The colors of the bars.

    Returns:
        BarChart:
            A BarChart object.
    """
    return BarChart(
        values=bar_values,
        bar_names=bar_names,
        y_range=y_range,
        y_length=round(config.frame_height) - 2,
        x_length=round(config.frame_width) - 2,
        bar_colors=bar_colors,
        tips=False,
        y_axis_config={
            "include_numbers": False,
            "font_size": AXES_FONT_SIZE,
        },
        x_axis_config={
            "include_numbers": False,
            "font_size": AXES_FONT_SIZE,
        },
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


def add_bar_names(ax: BarChart, bar_names: List[str]):
    """
    Add x-axis labels to an BarChart object.

    Args:
        ax (BarChart):
            The BarChart object.

        bar_names (List[str]):
            The x-axis labels of the bars.
    """
    val_range = np.arange(0.5, len(bar_names), 1)
    labels = VGroup()
    for i, (value, bar_name) in enumerate(zip(val_range, bar_names)):
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


def update_bar_names(ax: BarChart, bar_names: List[str]):
    """
    Remove old and add new x-axis labels to an BarChart object.

    Args:
        ax (BarChart):
            The BarChart object.

        bar_names (List[str]):
            The x-axis labels of the bars.
    """
    remove_bar_names(ax)
    add_bar_names(ax, bar_names)


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
    y_round: bool = False,
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

        y_round (bool):
            Whether to use non-decimal numbers for the y-axis labels.
    """
    y_tick_indices = ax.y_axis.get_tick_range().tolist()
    y_labels = np.linspace(
        start=y_min,
        stop=y_max,
        num=num_y_ticks + 1,
        endpoint=True,
        dtype=float,
    )[1:]
    if y_round:
        y_labels = y_labels.astype(np.int32)
    else:
        y_labels = np.round(y_labels, decimals=2)
    ax.y_axis.add_labels(
        {y_tick_idx: y_label for y_tick_idx, y_label in zip(y_tick_indices, y_labels)}
    )


def update_bar_values(
    ax: BarChart,
    y_min: float,
    y_max: float,
    num_y_ticks: int,
    y_round: bool = False,
):
    """
    Remove old and add new y-axis labels to an BarChart object.

    Args:
        ax (BarChart):
            The BarChart object.

        y_min (float):
            The minimum value of the y-axis.

        y_max (float):
            The maximum value of the y-axis.

        num_y_ticks (int):
            The number of y-axis ticks.

        y_round (bool):
            Whether to use non-decimal numbers for the y-axis
    """
    remove_bar_values(ax)
    add_bar_values(ax, y_min, y_max, num_y_ticks, y_round)
