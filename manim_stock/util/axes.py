"""Utility functions for Axes objects."""

from typing import Tuple

import numpy as np
from manim import Axes, config

from manim_stock.util.const import AXES_FONT_SIZE


def create_axes(
    x_range: Tuple[float, float, float],
    y_range: Tuple[float, float, float],
) -> Axes:
    """
    Creates an Axes object.

    Args:
        x_range (Tuple[float, float, float]):
            The [x_min, x_max, x_step] of the x-axis.

        y_range (Tuple[float, float, float]):
            The [y_min, y_max, y_step] of the y-axis.

    Returns:
        Axes:
            The axes object.
    """
    return Axes(
        x_range=x_range,
        y_range=y_range,
        y_length=round(config.frame_height) - 2,
        x_length=round(config.frame_width) - 2,
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


def remove_x_labels(ax: Axes):
    """
    Remove the x-axis labels from an Axes object.

    Args:
        ax (Axes):
            The Axes object.
    """
    if hasattr(ax.x_axis, "labels"):
        ax.x_axis.remove(ax.x_axis.labels)
    if hasattr(ax.x_axis, "numbers"):
        ax.x_axis.remove(ax.x_axis.numbers)


def add_x_labels(
    ax: Axes,
    x: np.ndarray,
    x_min: float,
    x_max: float,
    num_x_ticks: int,
    x_round: bool = False,
):
    """
    Add x-axis labels to an Axes object.

    Args:
        ax (Axes):
            The Axes object.

        x (np.ndarray):
            The data points of the x-axis.

        x_min (float):
            The minimum value of the x-axis.

        x_max (float):
            The maximum value of the x-axis.

        num_x_ticks (int):
            The number of x-axis ticks.

        x_round (bool):
            Whether to use non-decimal numbers for the x-axis labels.
    """
    x_tick_indices = ax.x_axis.get_tick_range().tolist()
    x_label_indices = np.linspace(
        start=x_min,
        stop=x_max,
        num=num_x_ticks + 1,
        endpoint=True,
        dtype=int,
    )[1:]
    x_labels = x[x_label_indices]
    if x_round:
        x_labels = x_labels.astype(np.int32)
    else:
        x_labels = np.round(x_labels, 2)
    ax.x_axis.add_labels(
        {
            x_tick_idx: int(x_label)
            for x_tick_idx, x_label in zip(x_tick_indices, x_labels)
        }
    )


def update_x_labels(
    ax: Axes,
    x: np.ndarray,
    x_min: float,
    x_max: float,
    num_x_ticks: int,
    x_round: bool = False,
):
    """
    Remove old and add new x-axis labels to an Axes object.

    Args:
        ax (Axes):
            The Axes object.

        x (np.ndarray):
            The data points of the x-axis.

        x_min (float):
            The minimum value of the x-axis.

        x_max (float):
            The maximum value of the x-axis.

        num_x_ticks (int):
            The number of x-axis ticks.

        round (bool):
            Whether to use non-decimal numbers for the x-axis labels.
    """
    remove_x_labels(ax)
    add_x_labels(ax, x, x_min, x_max, num_x_ticks, x_round)


def remove_y_labels(ax: Axes):
    """
    Remove the y-axis labels from an Axes object.

    Args:
        ax (Axes):
            The Axes object.
    """
    if hasattr(ax.y_axis, "labels"):
        ax.y_axis.remove(ax.y_axis.labels)
    if hasattr(ax.y_axis, "numbers"):
        ax.y_axis.remove(ax.y_axis.numbers)


def add_y_labels(
    ax: Axes,
    y: np.ndarray,
    y_min: float,
    y_max: float,
    num_y_ticks: int,
    y_round: bool = False,
):
    """
    Add y-axis labels to an Axes object.

    Args:
        ax (Axes):
            The Axes object.

        Y (np.ndarray):
            The data points of the y-axis.

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
        y_labels = np.round(y_labels, 2)
    ax.y_axis.add_labels(
        {y_tick_idx: y_label for y_tick_idx, y_label in zip(y_tick_indices, y_labels)}
    )


def update_y_labels(
    ax: Axes,
    y: np.ndarray,
    y_min: float,
    y_max: float,
    num_y_ticks: int,
    y_round: bool = False,
):
    """
    Remove old and add new x-axis labels to an Axes object.

    Args:
        ax (Axes):
            The Axes object.

        y (np.ndarray):
            The data points of the y-axis.

        y_min (float):
            The minimum value of the y-axis.

        y_max (float):
            The maximum value of the y-axis.

        num_y_ticks (int):
            The number of y-axis ticks.

        y_round (bool):
            Whether to use non-decimal numbers for the y-axis labels.
    """
    remove_y_labels(ax)
    add_y_labels(ax, y, y_min, y_max, num_y_ticks, y_round)
