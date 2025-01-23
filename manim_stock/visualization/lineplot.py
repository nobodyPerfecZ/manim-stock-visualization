"""Visualization of stock prices over time for a single ticker."""

import logging

import numpy as np
from manim import (
    DEFAULT_FONT_SIZE,
    GREEN,
    RED,
    UR,
    WHITE,
    Axes,
    Create,
    DecimalNumber,
    Dot,
    FadeOut,
    Title,
    ValueTracker,
    VGroup,
    Write,
)

from manim_stock.util import download_stock_data, preprocess_stock_data
from manim_stock.visualization.stock import StockVisualization

# Set logging level to WARNING
logging.getLogger("manim").setLevel(logging.WARNING)


class Lineplot(StockVisualization):
    """
    Visualization of stock prices with line graphs for a single ticker.

    Attributes:
        tickers (str | list[str]):
            The ticker(s) of the stock(s) to visualize

        start (str):
            The start date in YYYY-MM-DD format

        end (str):
            The end date in YYYY-MM-DD format

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

        graph_run_time (int):
            The run time for the create animation of the graph

        wait_run_time (int):
            The run time for the fade out animation at the end

        camera_frame_scale (float):
            The scale factor for the camera frame

        num_ticks (int):
            The number of ticks on the x-/y-axis

        num_samples (int):
            The number of samples to draw from the entire data
    """

    def __init__(
        self,
        tickers: str | list[str],
        start: str,
        end: str,
        title: str = "Market Price",
        x_label: str = "Year",
        y_label: str = r"Price [\$]",
        title_font_size: int = DEFAULT_FONT_SIZE,
        x_label_font_size: int = DEFAULT_FONT_SIZE,
        y_label_font_size: int = DEFAULT_FONT_SIZE,
        background_run_time: int = 10,
        graph_run_time: int = 45,
        wait_run_time: int = 5,
        camera_frame_scale: float = 1.2,
        num_ticks: int = 5,
        num_samples: int = 1000,
        **kwargs,
    ):
        if isinstance(tickers, list):
            assert (
                len(tickers) == 1
            ), f"{self.__class__.__name__} only supports one ticker!"
        assert background_run_time > 0, "background_run_time should be greater than 0!"
        assert graph_run_time > 0, "graph_run_time should be greater than 0!"
        assert wait_run_time > 0, "wait_run_time should be greater than 0!"
        assert (
            camera_frame_scale > 0.0
        ), "camera_frame_scale should be greater than 0.0!"
        assert num_ticks > 0, "num_ticks should be greater than 0!"
        assert num_samples > 0, "num_samples should be greater than 0!"

        super().__init__(
            tickers=tickers,
            start=start,
            end=end,
            title=title,
            x_label=x_label,
            y_label=y_label,
            title_font_size=title_font_size,
            x_label_font_size=x_label_font_size,
            y_label_font_size=y_label_font_size,
            **kwargs,
        )

        self.background_run_time = background_run_time
        self.graph_run_time = graph_run_time
        self.wait_run_time = wait_run_time
        self.camera_frame_scale = camera_frame_scale
        self.num_ticks = num_ticks
        self.num_samples = num_samples

        self.load_data()
        self.preprocess_data()

    def load_data(self):
        self.df = download_stock_data(
            tickers=self.tickers,
            start=self.start,
            end=self.end,
        )

    def preprocess_data(self):
        self.df = preprocess_stock_data(df=self.df, column="High")
        sample_indices = np.linspace(
            0,
            len(self.df) - 1,
            num=min(self.num_samples, len(self.df)),
            endpoint=True,
            dtype=int,
        )
        self.date = self.df["X"].to_numpy()[sample_indices]
        self.stock_price = self.df["Y0"].to_numpy()[sample_indices]

    def construct(self):
        #  Scale the camera frame up by camera_frame_scale
        self.camera.frame.scale(self.camera_frame_scale)

        # Create the axes
        ax = Axes(
            x_range=(0, len(self.date), len(self.date) / self.num_ticks),
            y_range=(
                0,
                self.stock_price.max(),
                self.stock_price.max() / self.num_ticks,
            ),
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

        # Remove the x-axis labels
        ax.x_axis.remove(ax.x_axis.numbers)

        # Create the x-axis labels
        x_tick_indices = [10.0] + ax.x_axis.get_tick_range().tolist()
        x_label_indices = np.linspace(
            0, len(self.date) - 1, num=self.num_ticks + 1, endpoint=True, dtype=int
        )
        x_labels = self.date[x_label_indices]
        ax.x_axis.add_labels(
            {
                x_tick_idx: int(x_label)
                for x_tick_idx, x_label in zip(x_tick_indices, x_labels)
            }
        )

        # Remove the y-axis labels
        ax.y_axis.remove(ax.y_axis.numbers)

        # Create the y-axis labels
        y_tick_indices = [10.0] + ax.y_axis.get_tick_range().tolist()
        y_labels = np.linspace(
            0, self.stock_price.max(), num=self.num_ticks + 1, endpoint=True, dtype=int
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

        """
        # Create the x-/y-axis label
        # TODO: Fix issue with placing of x-axis/y-axis labels
        x_label = ax.get_x_axis_label(
            label=Tex(self.x_label, font_size=self.x_label_font_size),
            edge=UR,
            direction=UR,
        )
        y_label = ax.get_y_axis_label(
            label=Tex(self.y_label, font_size=self.y_label_font_size),
            edge=UL,
            direction=UL,
        )
        labels = VGroup(x_label, y_label)
        """

        # Plot the line graph
        f = ax.plot_line_graph(
            x_values=np.arange(len(self.date)),
            y_values=self.stock_price,
            line_color=GREEN if self.stock_price[-1] > self.stock_price[0] else RED,
            add_vertex_dots=False,
        )

        # Get all points from the graph
        points = f.get_all_points()

        # Create the X Position Tracker
        x = ValueTracker(0)

        # Create the Dot Tracker
        dot = Dot(color=WHITE)
        dot.add_updater(lambda mob: mob.move_to(points[int(x.get_value()), :]))

        # Create the Stock Value Tracker
        stock_value = DecimalNumber()
        stock_value.add_updater(
            lambda mob: mob.next_to(points[int(x.get_value()), :], UR).set_value(
                ax.p2c(points[int(x.get_value())])[1]
            )
        )

        # Play the animation
        self.play(
            Write(VGroup(ax, title, dot, stock_value)),
            run_time=self.background_run_time,
        )
        self.play(
            Create(f),
            x.animate.set_value(len(points) - 1),
            run_time=self.graph_run_time,
        )
        self.play(
            FadeOut(dot, stock_value),
            run_time=self.wait_run_time,
        )
