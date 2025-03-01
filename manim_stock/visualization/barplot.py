"""Visualization of stock prices with barplots for multiple tickers."""

import logging

import numpy as np
from manim import (
    DEFAULT_FONT_SIZE,
    UP,
    BarChart,
    DecimalNumber,
    FadeOut,
    Title,
    ValueTracker,
    VGroup,
    Write,
    config,
)

from manim_stock.visualization.stock import StockVisualization

# Set logging level to WARNING
logging.getLogger("manim").setLevel(logging.WARNING)


class Barplot(StockVisualization):
    """
    Visualization of stock prices with barplots for multiple tickers.

    Attributes:
        path (str):
            The path to the CSV file containing the stock data

        title (str):
            The title of the visualization

        x_label (str):
            The label of the x-axis

        y_label (str):
            The label of the y-axis

        title_font_size (int):
            The font size of the title

        x_label_font_size (int):
            The font size of the x-axis label

        y_label_font_size (int):
            The font size of the y-axis label

        background_run_time (int):
            The run time for the write animation of the background elements

        bar_run_time (int):
            The run time for the create animation of the bars

        wait_run_time (int):
            The run time for the fade out animation at the end

        camera_frame_scale (float):
            The scale factor for the camera frame

        bar_colors(list[str]):
            The colors for all bars

        bar_width (float):
            The width of the bars

        bar_fill_opacity (float):
            The fill opacity of the bars

        bar_stroke_width (float):
            The stroke width of the bars.

        num_ticks (int):
            The number of ticks on the x-/y-axis

        num_samples (int):
            The number of samples to draw from the entire data
    """

    def __init__(
        self,
        path: str,
        bar_names: str | list[str],
        title: str = "Market Price",
        x_label: str = "Stocks",
        y_label: str = r"Price [\$]",
        title_font_size: int = DEFAULT_FONT_SIZE,
        x_label_font_size: int = DEFAULT_FONT_SIZE,
        y_label_font_size: int = DEFAULT_FONT_SIZE,
        background_run_time: int = 10,
        bar_run_time: int = 45,
        wait_run_time: int = 5,
        camera_frame_scale: float = 1.2,
        bar_colors: list[str] | None = None,
        bar_width: float = 0.6,
        bar_fill_opacity: float = 0.7,
        bar_stroke_width: float = 3,
        num_ticks: int = 5,
        num_samples: int = 1000,
        **kwargs,
    ):
        super().__init__(
            path=path,
            title=title,
            x_label=x_label,
            y_label=y_label,
            title_font_size=title_font_size,
            x_label_font_size=x_label_font_size,
            y_label_font_size=y_label_font_size,
            num_ticks=num_ticks,
            num_samples=num_samples,
            **kwargs,
        )

        if isinstance(bar_names, str):
            bar_names = [bar_names]

        assert (
            len(bar_names) == len(self.df.columns) - 1
        ), "bar_names should have the same length as the number of tickers!"
        assert background_run_time > 0, "background_run_time should be greater than 0!"
        assert bar_run_time > 0, "bar_run_time should be greater than 0!"
        assert wait_run_time > 0, "wait_run_time should be greater than 0!"
        assert (
            camera_frame_scale > 0.0
        ), "camera_frame_scale should be greater than 0.0!"
        if bar_colors is None:
            bar_colors = [
                "#003f5c",
                "#58508d",
                "#bc5090",
                "#ff6361",
                "#ffa600",
            ][: len(self.df.columns) - 1]
        else:
            assert len(bar_colors) >= len(
                self.df.columns - 1
            ), "bar_colors should have at least as many colors as tickers!"
        assert 0.0 <= bar_width <= 1.0, "bar_width should be in range (0.0, 1.0)!"
        assert (
            0.0 <= bar_fill_opacity <= 1.0
        ), "bar_fill_opacity should be in range (0.0, 1.0)!"
        assert bar_stroke_width > 0.0, "bar_stroke_width should be greater than 0.0!"

        self.bar_names = bar_names
        self.background_run_time = background_run_time
        self.bar_run_time = bar_run_time
        self.wait_run_time = wait_run_time
        self.camera_frame_scale = camera_frame_scale
        self.bar_colors = bar_colors
        self.bar_width = bar_width
        self.bar_fill_opacity = bar_fill_opacity
        self.bar_stroke_width = bar_stroke_width

    def construct(self):
        #  Scale the camera frame up by camera_frame_scale
        self.camera.frame.scale(self.camera_frame_scale)

        x = ValueTracker(0)

        # Create the Bar Plot
        y_range = [0, self.Y.max(), self.Y.max() / self.num_ticks]
        ax = BarChart(
            values=self.Y[0],
            bar_names=self.bar_names,
            y_range=y_range,
            y_length=round(config.frame_height) - 2,
            x_length=round(config.frame_width) - 2,
            bar_colors=self.bar_colors,
            bar_width=self.bar_width,
            bar_fill_opacity=self.bar_fill_opacity,
            bar_stroke_width=self.bar_stroke_width,
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

        # Remove the y-axis numbers
        ax.y_axis.remove(ax.y_axis.numbers)

        # Create the y-axis labels
        y_tick_indices = [10.0] + ax.y_axis.get_tick_range().tolist()
        y_labels = np.linspace(
            0,
            self.Y.max(),
            num=self.num_ticks + 1,
            endpoint=True,
            dtype=int,
        )
        ax.y_axis.add_labels(
            {
                y_tick_idx: y_label
                for y_tick_idx, y_label in zip(y_tick_indices, y_labels)
            }
        )

        # Create the title
        title = Title(
            self.title,
            font_size=self.title_font_size,
            include_underline=False,
        )

        # Create the Bar Labels
        bar_labels = [
            DecimalNumber(value, font_size=DEFAULT_FONT_SIZE).next_to(bar, UP)
            for bar, value in zip(ax.bars, ax.values)
        ]

        # Update Bar Plots
        ax.add_updater(lambda mob: mob.change_bar_values(self.Y[int(x.get_value())]))

        # Update Bar Labels
        # TODO: Change Hacky workaround to add different update functions to each bar label
        if len(bar_labels) >= 1:
            bar_labels[0].add_updater(
                lambda mob: mob.next_to(ax.bars[0], UP).set_value(ax.values[0])
            )
        if len(bar_labels) >= 2:
            bar_labels[1].add_updater(
                lambda mob: mob.next_to(ax.bars[1], UP).set_value(ax.values[1])
            )
        if len(bar_labels) >= 3:
            bar_labels[2].add_updater(
                lambda mob: mob.next_to(ax.bars[2], UP).set_value(ax.values[2])
            )
        if len(bar_labels) >= 4:
            bar_labels[3].add_updater(
                lambda mob: mob.next_to(ax.bars[3], UP).set_value(ax.values[3])
            )
        if len(bar_labels) == 5:
            bar_labels[4].add_updater(
                lambda mob: mob.next_to(ax.bars[4], UP).set_value(ax.values[4])
            )

        # Play the animation
        self.play(
            Write(VGroup(ax, title, *bar_labels)),
            run_time=self.background_run_time,
        )
        self.play(
            x.animate.set_value(len(self.Y) - 1),
            run_time=self.bar_run_time,
        )
        self.play(FadeOut(*bar_labels), run_time=self.wait_run_time)
