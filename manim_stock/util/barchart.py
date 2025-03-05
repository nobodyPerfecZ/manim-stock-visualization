"""Utility functions for Barchart objects."""

import numpy as np
from manim import DOWN, UP, BarChart, VGroup, config

from manim_stock.util.const import DEFAULT_FONT_SIZE


def create_barchart(
    bar_values: list[float],
    bar_names: list[str],
    y_range: list[float],
    bar_colors: list[str],
) -> BarChart:
    """
    Creates a BarChart object.

    Args:
        bar_values (list[float]):
            The values of the bars.

        bar_names (list[str]):
            The names of the bars.

        y_range (list[float]):
            The [y_min, y_max, y_step] of the y-axis.

        bar_colors (list[str]):
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
            "font_size": DEFAULT_FONT_SIZE,
        },
        x_axis_config={
            "include_numbers": False,
            "font_size": DEFAULT_FONT_SIZE,
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


def add_bar_names(ax: BarChart, bar_names: list[str], bar_values: list[float]):
    """
    Add x-axis labels to an BarChart object.

    Args:
        ax (BarChart):
            The BarChart object.

        bar_names (list[str]):
            The x-axis labels of the bars.

        bar_values (list[float]):
            The values of the bars.
    """
    val_range = np.arange(0.5, len(bar_names), 1)
    labels = VGroup()
    for i, (value, bar_name, bar_value) in enumerate(
        zip(val_range, bar_names, bar_values)
    ):
        direction = UP if ax.values[i] < 0 else DOWN
        bar_name_label = ax.x_axis.label_constructor(bar_name)
        bar_value_label = ax.x_axis.label_constructor(np.round(bar_value, 2))

        bar_name_label.font_size = ax.x_axis.font_size
        bar_name_label.next_to(
            ax.x_axis.number_to_point(value),
            direction=direction,
            buff=ax.x_axis.line_to_number_buff,
        )

        bar_value_label.font_size = ax.x_axis.font_size
        bar_value_label.next_to(
            ax.x_axis.number_to_point(value),
            direction=3 * direction,
            buff=ax.x_axis.line_to_number_buff,
        )

        labels.add(bar_name_label, bar_value_label)
    ax.x_axis.labels = labels
    ax.x_axis.add(labels)


def update_bar_names(ax: BarChart, bar_names: list[str], bar_values: list[float]):
    """
    Remove old and add new x-axis labels to an BarChart object.

    Args:
        ax (BarChart):
            The BarChart object.

        bar_names (list[str]):
            The x-axis labels of the bars.

        bar_values (list[float]):
            The values of the bars.
    """
    remove_bar_names(ax)
    add_bar_names(ax, bar_names, bar_values)


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


def add_bar_values(ax: BarChart, y_min: float, y_max: float, num_y_ticks: int):
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
    """
    y_tick_indices = ax.y_axis.get_tick_range().tolist()
    y_labels = np.linspace(
        start=y_min,
        stop=y_max,
        num=num_y_ticks + 1,
        endpoint=True,
        dtype=float,
    )[1:]
    y_labels = np.round(y_labels, decimals=2)
    ax.y_axis.add_labels(
        {y_tick_idx: y_label for y_tick_idx, y_label in zip(y_tick_indices, y_labels)}
    )


def update_bar_values(ax: BarChart, y_min: float, y_max: float, num_y_ticks: int):
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
    """
    remove_bar_values(ax)
    add_bar_values(ax, y_min, y_max, num_y_ticks)
