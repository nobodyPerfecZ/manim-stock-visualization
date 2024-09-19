import logging
import pandas as pd

from manim import *

# Set logging level to WARNING
logging.getLogger("manim").setLevel(logging.WARNING)

# Geometry directions
UP_UP_RIGHT = np.array((1.0, 3.0, 0.0))
UP_RIGHT = np.array((1.0, 1.0, 0.0))


class StockVisualization(MovingCameraScene):
    """Visualization of stock prices over time."""

    def __init__(
        self,
        df: pd.DataFrame,
        title: str,
        num_x_ticks: int = 10,
        num_y_ticks: int = 10,
        x_length: int = 10,
        y_length: int = 5,
        write_run_time: int = 5,
        zoom_in_run_time: int = 5,
        create_run_time: int = 45,
        zoom_out_run_time: int = 5,
        visualize_live_stock_price: bool = True,
        visualize_live_date: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Create the date array
        self.date = df["X"]

        # Create the indices array (used for the x-axis)
        self.indices = np.arange(0, len(df["X"]))
        self.min_indices, self.max_indices = (
            self.indices.min(),
            self.indices.max(),
        )

        # Create the stock price array
        self.stock_price = df["Y"].to_numpy()
        self.min_stock_price, self.max_stock_price = (
            self.stock_price.min(),
            self.stock_price.max(),
        )

        self.title = title
        self.num_x_ticks = num_x_ticks
        self.num_y_ticks = num_y_ticks
        self.x_length = x_length
        self.y_length = y_length

        self.write_run_time = write_run_time
        self.zoom_in_run_time = zoom_in_run_time
        self.create_run_time = create_run_time
        self.zoom_out_run_time = zoom_out_run_time

        self.visualize_live_stock_price = visualize_live_stock_price
        self.visualize_live_date = visualize_live_date

    def construct(self):
        # Save the initial state of the camera
        self.camera.frame.save_state()

        # Set the plot
        ax = Axes(
            x_range=(
                self.min_indices,
                self.max_indices,
                self.max_indices - self.min_indices / self.num_x_ticks,
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

        # Set the title of the line plot
        title = Title(self.title, include_underline=False, font_size=60)

        # Set the labels of the x-/y-axis
        labels = ax.get_axis_labels(
            x_label=Tex("Date"),
            y_label=Tex("Stock Price"),
        )

        # Plot the line graph
        f = ax.plot_line_graph(
            x_values=self.indices,
            y_values=self.stock_price,
            line_color=GREEN if self.stock_price[0] < self.stock_price[-1] else RED,
            add_vertex_dots=False,
        )

        # Get all points of the graph
        points = f.get_all_points()

        # Set the group
        group = Group()

        # Set the tracker
        tracker = ValueTracker()

        # Add tracker to the group
        group.add(tracker)

        # Set the dot
        dot = Dot()

        # Set the updaters for the position of the dot
        dot.add_updater(lambda mob: mob.move_to(points[int(tracker.get_value()), :]))

        # Add the dot to the group
        group.add(dot)

        if self.visualize_live_stock_price:
            # Set the stock value
            stock_value = DecimalNumber(unit="\$")

            # Set the updater for the position of the stock value
            stock_value.add_updater(
                lambda mob: mob.next_to(points[int(tracker.get_value()), :], UP_RIGHT)
            )

            # Set the updater for the value of the stock value
            stock_value.add_updater(
                lambda mob: mob.set_value(ax.p2c(points[int(tracker.get_value())])[1])
            )

            # Add the stock value to the group
            group.add(stock_value)

        if self.visualize_live_date:
            # Set the date value
            date_value = Tex(f"{self.date[0]}")

            # Get the position of the date value
            pos = UP_UP_RIGHT if self.visualize_live_stock_price else UP_RIGHT

            # Set the updater for the position of the date value
            date_value.add_updater(
                lambda mob: mob.next_to(points[int(tracker.get_value()), :], pos)
            )

            # Set the updater for the value of the date value
            def update_date_value(mob: Mobject):
                new_mob = mob.become(
                    Tex(
                        f"{self.date[int(ax.p2c(points[int(tracker.get_value())])[0])]}"
                    )
                )
                new_mob.add_updater(
                    lambda mob: mob.next_to(points[int(tracker.get_value()), :], pos)
                )

            date_value.add_updater(update_date_value)

            # Add the date value to the group
            group.add(date_value)

        # Animate the axis/labels being drawn
        self.play(Write(VGroup(ax, labels, title)), run_time=self.write_run_time)

        # Add the group to the scene
        self.add(group)

        # Zoom in to the dot
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(points[0]),
            run_time=self.zoom_in_run_time,
        )

        # Set the updater of the camera frame
        def update_camera(mob: Mobject):
            mob.move_to(dot.get_center())

        self.camera.frame.add_updater(update_camera)

        # Animate the drawing of the line graph
        self.play(
            Create(f),
            tracker.animate.set_value(len(points) - 1),
            run_time=self.create_run_time,
        )

        # Remove the updater of the camera frame
        self.camera.frame.remove_updater(update_camera)

        # Remove the group from the scene
        self.remove(group)

        # Zoom out to the full graph
        self.play(Restore(self.camera.frame), run_time=self.zoom_out_run_time)

        # Wait until the end
        self.wait()
