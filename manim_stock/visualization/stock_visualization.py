import pandas as pd

from manim import *

# Geometry directions
UP_UP_RIGHT = np.array((1.0, 1.0, 0.0))


class StockVisualization(MovingCameraScene):
    """Visualization of stock prices over time."""

    def __init__(
        self,
        df: pd.DataFrame,
        num_x_ticks: int = 10,
        num_y_ticks: int = 10,
        x_length: int = 10,
        y_length: int = 5,
        write_run_time: int = 5,
        zoom_in_run_time: int = 5,
        create_run_time: int = 45,
        zoom_out_run_time: int = 5,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Create the date array
        self.date = np.arange(1, len(df["X"]) + 1)
        self.min_date, self.max_date = (
            self.date.min(),
            self.date.max(),
        )

        # Create the stock price array
        self.stock_price = df["Y"].to_numpy()
        self.min_stock_price, self.max_stock_price = (
            self.stock_price.min(),
            self.stock_price.max(),
        )

        self.num_x_ticks = num_x_ticks
        self.num_y_ticks = num_y_ticks
        self.x_length = x_length
        self.y_length = y_length

        self.write_run_time = write_run_time
        self.zoom_in_run_time = zoom_in_run_time
        self.create_run_time = create_run_time
        self.zoom_out_run_time = zoom_out_run_time

    def construct(self):
        self.camera.frame.save_state()

        # Set the plot
        ax = Axes(
            x_range=(
                self.min_date,
                self.max_date,
                self.max_date - self.min_date / self.num_x_ticks,
            ),
            y_range=(
                self.min_stock_price,
                self.max_stock_price,
                self.max_stock_price - self.min_stock_price / self.num_y_ticks,
            ),
            x_length=self.x_length,
            y_length=self.y_length,
            axis_config={
                "include_numbers": False,
                "decimal_number_config": {
                    "group_with_commas": False,
                    "num_decimal_places": 2,
                },
            },
        )
        ax.center()

        # Set the labels of the x-/y-axis
        labels = ax.get_axis_labels(
            x_label=Tex("Date").scale(1.0),
            y_label=Tex("Stock Price").scale(1.0),
        )

        # Plot the line graph
        f = ax.plot_line_graph(
            x_values=self.date,
            y_values=self.stock_price,
            line_color=GREEN if self.stock_price[0] < self.stock_price[-1] else RED,
            add_vertex_dots=False,
        )

        # Get all points of the graph
        points = f.get_all_points()

        # Set the tracker
        tracker = ValueTracker()

        # Set the dot
        dot = Dot()

        # Set the updaters for the position of the dot
        dot.add_updater(lambda d: d.move_to(points[int(tracker.get_value()), :]))

        # Set the stock value
        stock_value = DecimalNumber()

        # Set the updater for the position of the stock value
        stock_value.add_updater(
            lambda d: d.next_to(points[int(tracker.get_value()), :], UP_UP_RIGHT)
        )

        # Set the updater for the value of the stock value
        stock_value.add_updater(
            lambda d: d.set_value(ax.p2c(points[int(tracker.get_value())])[1])
        )

        # Set the updater of the camera frame
        def update_curve(mob: Mobject):
            mob.move_to(dot.get_center())

        self.camera.frame.add_updater(update_curve)

        # Animate the axis/labels being drawn
        self.play(Write(VGroup(ax, labels)), run_time=self.write_run_time)

        # Add the objects to the scene
        self.add(dot, stock_value, tracker)

        # Zoom in to the dot
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(dot),
            run_time=self.zoom_in_run_time,
        )

        # Animate the drawing of the line graph
        self.play(
            Create(f),
            tracker.animate.set_value(len(points) - 1),
            run_time=self.create_run_time,
        )

        # Remove the updater of the camera frame
        self.camera.frame.remove_updater(update_curve)

        # Zoom out to the full graph
        self.play(Restore(self.camera.frame), run_time=self.zoom_out_run_time)

        # Wait until the end
        self.wait()
