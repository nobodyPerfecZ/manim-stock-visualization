"""Utility functions for Axes objects."""

from typing import List

import numpy as np
from manim import Axes, config

from manim_stock.util.const import AXES_FONT_SIZE


def create_axes(x_range: List[float], y_range: List[float]) -> Axes:
    """
    Creates an Axes object.

    Args:
        x_range (List[float]):
            The [x_min, x_max, x_step] of the x-axis.

        y_range (List[float]):
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
    X: np.ndarray,
    x_min: float,
    x_max: float,
    num_x_ticks: int,
):
    """
    Add x-axis labels to an Axes object.

    Args:
        ax (Axes):
            The Axes object.

        X (np.ndarray):
            The data points of the x-axis.

        x_min (float):
            The minimum value of the x-axis.

        x_max (float):
            The maximum value of the x-axis.

        num_x_ticks (int):
            The number of x-axis ticks.
    """
    x_tick_indices = ax.x_axis.get_tick_range().tolist()
    x_label_indices = np.linspace(
        start=x_min,
        stop=x_max,
        num=num_x_ticks + 1,
        endpoint=True,
        dtype=int,
    )[1:]
    x_labels = X[x_label_indices]
    ax.x_axis.add_labels(
        {
            x_tick_idx: int(x_label)
            for x_tick_idx, x_label in zip(x_tick_indices, x_labels)
        }
    )


def update_x_labels(
    ax: Axes,
    X: np.ndarray,
    x_min: float,
    x_max: float,
    num_x_ticks: int,
):
    """
    Remove old and add new x-axis labels to an Axes object.

    Args:
        ax (Axes):
            The Axes object.

        X (np.ndarray):
            The data points of the x-axis.

        x_min (float):
            The minimum value of the x-axis.

        x_max (float):
            The maximum value of the x-axis.

        num_x_ticks (int):
            The number of x-axis ticks.
    """
    remove_x_labels(ax)
    add_x_labels(ax, X, x_min, x_max, num_x_ticks)


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
    Y: np.ndarray,
    y_min: float,
    y_max: float,
    num_y_ticks: int,
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


def update_y_labels(
    ax: Axes,
    Y: np.ndarray,
    y_min: float,
    y_max: float,
    num_y_ticks: int,
):
    """
    Remove old and add new x-axis labels to an Axes object.

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
    """
    remove_y_labels(ax)
    add_y_labels(ax, Y, y_min, y_max, num_y_ticks)
