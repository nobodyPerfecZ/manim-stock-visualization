"""Visualization of stock prices with barplots abd growing axes for multiple tickers."""

import logging

from manim import config

from manim_stock.visualization.barplot import Barplot, State

# Set logging level to WARNING
logging.getLogger("manim").setLevel(logging.WARNING)

# Disable caching to speed up the rendering process
config.disable_caching = True


class GrowingBarplot(Barplot):
    """
    Visualization of stock prices with barplots
    and growing axes for multiple tickers.
    """

    def __init__(self, path: str, **kwargs):
        super().__init__(path=path, **kwargs)
        self.next_y_indicies = int(self.num_samples / self.num_y_ticks)

    def _create_state(self) -> State:
        return State(
            time=0,
            y_min=0,
            y_max=self.Y[3 * self.next_y_indicies].max(),
            num_y_ticks=3,
            y_decimals=self.y_decimals,
        )

    def _update_state(self, state: State, time: int) -> State:
        state = state.replace(time=time)

        # Scale y-axis
        if self.Y[time].max() >= state.y_max:
            if state.num_y_ticks < self.num_y_ticks:
                state = state.replace(num_y_ticks=state.num_y_ticks + 1)
            state = state.replace(
                y_max=self.Y[: min(time + self.next_y_indicies, len(self.df)), :].max()
            )

        return state
