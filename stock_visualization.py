from manim import *


class StockPriceVisualizationV3(Scene):
    def construct(self):
        # Set the years (X) and stock prices (Y)
        years = np.array([2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030])
        min_years, max_years = years.min(), years.max()
        stock_prices = np.array([100, 150, 125, 175, 150, 200, 175, 225, 200])
        min_stock_price, max_stock_price = stock_prices.min(), stock_prices.max()

        # Set up indicies
        indicies = np.arange(len(years))

        # Set the plot
        ax = Axes(
            x_range=(min_years, max_years, 2),
            y_range=(min_stock_price, max_stock_price, 50),
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

        # Set up the dot pointer
        t = ValueTracker(0)

        # declare the two functions but always update their upper end to the ValueTracker
        f = always_redraw(
            lambda: ax.plot_line_graph(
                x_values=years[: int(t.get_value()) + 1],
                y_values=stock_prices[: int(t.get_value()) + 1],
                line_color=BLUE,
                add_vertex_dots=False,
            )
        )

        f_dot = always_redraw(
            lambda: Dot(
                point=ax.c2p(
                    years[int(t.get_value())], stock_prices[int(t.get_value())], 0
                ),
                color=BLUE,
            )
        )

        # Animate the axis/labels being drawn
        self.play(Write(VGroup(ax, labels)))

        # Add the graphs and dots
        self.add(f, f_dot)

        # Animate the value tracker, updating the plots and tracing dots
        self.play(t.animate.set_value(len(indicies) - 1))

        # Fade out the dots
        self.play(FadeOut(f_dot))
        self.wait()


class StockPriceVisualizationV2(Scene):
    def construct(self):
        # Set the years (X) and stock prices (Y)
        years = np.array([2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030])
        min_years, max_years = years.min(), years.max()

        stock_prices = np.array([150, 175, 200, 225, 250, 275, 300, 325, 350])
        min_stock_price, max_stock_price = stock_prices.min(), stock_prices.max()

        # Set up indicies
        indicies = np.arange(len(years))

        # Set the plot
        axes = Axes(
            x_range=(min_years, max_years, 2),
            y_range=(min_stock_price, max_stock_price, 100),
            axis_config={"include_numbers": True},
        )
        axes.center()

        # Set the dot pointer / tracker
        t = ValueTracker(0)
        initial_point = np.array([min_years, min_stock_price, 0])
        dot = Dot(point=initial_point)
        dot.add_updater(
            lambda x: x.move_to(
                axes.c2p(years[int(t.get_value())], stock_prices[int(t.get_value())], 0)
            )
        )

        # Set the labels
        labels = axes.get_axis_labels(
            x_label=Tex("Year").scale(1.0),
            y_label=Tex("Stock Price").scale(1.0),
        )

        # Set the line plot
        line_graph = axes.plot_line_graph(
            x_values=years,
            y_values=stock_prices,
            line_color=GOLD_E,
            add_vertex_dots=False,
            # vertex_dot_style=dict(stroke_width=3, fill_color=PURPLE),
            # stroke_width=4,
        )

        # Add all components
        self.add(axes, line_graph, labels, dot)
        self.play(t.animate.set_value(len(indicies) - 1))
        self.wait()


class StockPriceVisualizationV1(Scene):
    def construct(self):
        # Set the plot
        axes = Axes(
            x_range=(2022, 2026, 1),
            y_range=(0, 300, 50),
            x_length=5,
            y_length=5,
            axis_config={"include_numbers": True},
        )
        axes.center()

        # Set the labels
        labels = axes.get_axis_labels(
            Tex("Year").scale(1.0), Tex("Stock Price").scale(1.0)
        )

        line_graph = axes.plot_line_graph(
            x_values=[2022, 2023, 2024, 2025, 2026],
            y_values=[150, 175, 200, 225, 250],
            line_color=GOLD_E,
            vertex_dot_style=dict(stroke_width=3, fill_color=PURPLE),
            stroke_width=4,
        )
        self.add(axes, line_graph, labels)
