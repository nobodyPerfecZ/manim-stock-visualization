"""Utility functions for Axes objects."""

from typing import Sequence

import numpy as np
from manim import Axes, config

from manim_stock.util.const import AXES_FONT_SIZE


def create_axes(
    x_range: Sequence[float],
    y_range: Sequence[float],
    **kwargs,
) -> Axes:
    """
    Creates an Axes object.

    Args:
        x_range (Sequence[float]):
            The [x_min, x_max, x_step] of the x-axis.

        y_range (Sequence[float]):
            The [y_min, y_max, y_step] of the y-axis.

        **kwargs:
            Additional arguments to be passed to Axes().

    Returns:
        Axes:
            The Axes object.
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

    return Axes(
        x_range=x_range,
        y_range=y_range,
        **kwargs,
    )


def remove_x_labels(ax: Axes):
    """Remove the x-axis labels from an Axes object."""
    if hasattr(ax.x_axis, "labels"):
        ax.x_axis.remove(ax.x_axis.labels)
    if hasattr(ax.x_axis, "numbers"):
        ax.x_axis.remove(ax.x_axis.numbers)


def add_x_labels_range(
    ax: Axes,
    x_min: float,
    x_max: float,
    num_x_ticks: int,
    x_decimals: int,
):
    """
    Add x-axis labels to an Axes object using a range of values.

    Args:
        ax (Axes):
            The Axes object.

        x_min (float):
            The minimum value of the x-axis.

        x_max (float):
            The maximum value of the x-axis.

        num_x_ticks (int):
            The number of x-axis ticks.

        x_decimals (int):
            The number of decimal places to round to.
    """
    x_labels = np.linspace(x_min, x_max, num_x_ticks + 1, endpoint=True)[1:]

    if x_decimals:
        x_labels = np.round(x_labels, x_decimals)
    else:
        x_labels = np.fix(x_labels).astype(np.int32)

    ax.x_axis.add_labels(dict(zip(ax.x_axis.get_tick_range(), x_labels, strict=False)))


def add_x_labels_custom(
    ax: Axes,
    x_labels: np.ndarray,
    num_x_ticks: int,
    x_decimals: int,
):
    """
    Add custom x-axis labels to an Axes object.

    Args:
        ax (Axes):
            The Axes object.

        x_labels (np.ndarray):
            The custom x-axis labels.

        num_x_ticks (int):
            The number of x-axis ticks.

        x_decimals (int):
            The number of decimal places to round to.
    """
    x_label_indicies = np.linspace(
        0,
        len(x_labels) - 1,
        num_x_ticks + 1,
        endpoint=True,
        dtype=np.int32,
    )[1:]
    x_labels = x_labels[x_label_indicies]

    if x_decimals:
        x_labels = np.round(x_labels, x_decimals)
    else:
        x_labels = np.fix(x_labels).astype(np.int32)

    ax.x_axis.add_labels(dict(zip(ax.x_axis.get_tick_range(), x_labels, strict=False)))


def remove_y_labels(ax: Axes):
    """Remove the y-axis labels from an Axes object."""
    if hasattr(ax.y_axis, "labels"):
        ax.y_axis.remove(ax.y_axis.labels)
    if hasattr(ax.y_axis, "numbers"):
        ax.y_axis.remove(ax.y_axis.numbers)


def add_y_labels_range(
    ax: Axes,
    y_min: float,
    y_max: float,
    num_y_ticks: int,
    y_decimals: int,
):
    """
    Add y-axis labels to an Axes object using a range of values.

    Args:
        ax (Axes):
            The Axes object.

        y_min (float):
            The minimum value of the y-axis.

        y_max (float):
            The maximum value of the y-axis.

        num_y_ticks (int):
            The number of y-axis ticks.

        y_decimals (int):
            The number of decimal places to round to.
    """
    y_labels = np.linspace(y_min, y_max, num_y_ticks + 1, endpoint=True)[1:]

    if y_decimals:
        y_labels = np.round(y_labels, y_decimals)
    else:
        y_labels = np.fix(y_labels).astype(np.int32)

    ax.y_axis.add_labels(dict(zip(ax.y_axis.get_tick_range(), y_labels, strict=False)))


def add_y_labels_custom(
    ax: Axes,
    y_labels: np.ndarray,
    num_y_ticks: int,
    y_decimals: int,
):
    """
    Add custom y-axis labels to an Axes object.

    Args:
        ax (Axes):
            The Axes object.

        y_labels (np.ndarray):
            The custom y-axis labels.

        num_y_ticks (int):
            The number of y-axis ticks.

        y_decimals (int):
            The number of decimal places to round to.
    """
    y_labels = np.linspace(
        0,
        len(y_labels) - 1,
        num_y_ticks + 1,
        endpoint=True,
        dtype=np.int32,
    )[1:]

    if y_decimals:
        y_labels = np.round(y_labels, y_decimals)
    else:
        y_labels = np.fix(y_labels).astype(np.int32)

    ax.y_axis.add_labels(dict(zip(ax.y_axis.get_tick_range(), y_labels, strict=False)))
