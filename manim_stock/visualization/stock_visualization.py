from manim import *

# Geometry directions
UP_UP_RIGHT = np.array((1.0, 3.0, 0.0))
UP_RIGHT = np.array((1.0, 1.0, 0.0))


class StockPriceVisualization(MovingCameraScene):
    """Visualization of stock prices over time."""

    def construct(self):
        self.camera.frame.save_state()

        # Set the years (X) and stock prices (Y)
        years = np.arange(2000, 2100, step=1)
        min_years, max_years = years.min(), years.max()
        stock_prices = np.arange(100, 200, step=1)
        min_stock_price, max_stock_price = stock_prices.min(), stock_prices.max()

        # Set the plot
        ax = Axes(
            x_range=(min_years, max_years, 10),
            y_range=(min_stock_price, max_stock_price, 10),
            axis_config={
                "include_numbers": True,
                "decimal_number_config": {
                    "group_with_commas": False,
                    "num_decimal_places": 0,
                },
            },
        )
        ax.center()

        # Set the labels of the x-/y-axis
        labels = ax.get_axis_labels(
            x_label=Tex("Year").scale(1.0),
            y_label=Tex("Stock Price").scale(1.0),
        )

        # Plot the line graph
        f = ax.plot_line_graph(
            x_values=years,
            y_values=stock_prices,
            line_color=BLUE,
            add_vertex_dots=False,
        )

        # Get all points of the graph
        points = f.get_all_points()

        # Set up the dot pointer
        tracker = ValueTracker()

        dot = Dot()
        dot.add_updater(lambda d: d.move_to(points[int(tracker.get_value()), :]))

        stock_value = DecimalNumber()
        stock_value.add_updater(
            lambda d: d.next_to(points[int(tracker.get_value()), :], UP_UP_RIGHT)
        )
        stock_value.add_updater(
            lambda d: d.set_value(ax.p2c(points[int(tracker.get_value())])[1])
        )

        time_value = DecimalNumber()
        time_value.add_updater(
            lambda d: d.next_to(points[int(tracker.get_value()), :], UP_RIGHT)
        )
        time_value.add_updater(
            lambda d: d.set_value(ax.p2c(points[int(tracker.get_value())])[0])
        )

        def update_curve(mob):
            mob.move_to(dot.get_center())

        self.camera.frame.add_updater(update_curve)

        # Animate the axis/labels being drawn
        self.play(Write(VGroup(ax, labels)))

        # Add the graphs and dots
        self.add(dot, stock_value, time_value, tracker)

        self.play(self.camera.frame.animate.scale(0.5).move_to(dot))

        self.play(Create(f), tracker.animate.set_value(len(points) - 1))

        self.camera.frame.remove_updater(update_curve)

        self.play(Restore(self.camera.frame))

        self.wait()
