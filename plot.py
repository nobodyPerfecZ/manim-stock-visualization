"""Example of visualizing the stock price of Apple, NVIDIA and Tesla."""

import argparse

from manim_stock.visualization import Barplot, GrowingBarplot, GrowingLineplot, Lineplot

parser = argparse.ArgumentParser(description="Visualize stock data.")
parser.add_argument(
    "-p",
    "--path",
    type=str,
    default="stock_data.csv",
    help="Path to the stock data.",
)
parser.add_argument(
    "-t",
    "--type",
    type=str,
    help="Type of the plot.",
    default="growing_line",
    choices=["line", "growing_line", "bar", "growing_bar"],
)
parser.add_argument(
    "-b",
    "--background_run_time",
    type=int,
    help="Number of seconds to create the initial plot.",
    default=5,
)
parser.add_argument(
    "-a",
    "--animation_run_time",
    type=int,
    help="Number of seconds from the initial plot to the final plot",
    default=50,
)
parser.add_argument(
    "-w",
    "--wait_run_time",
    type=int,
    help="Number of seconds after the final plot.",
    default=5,
)


if __name__ == "__main__":
    # Parse arguments
    args = parser.parse_args()

    # Create scene
    if args.type == "line":
        scene = Lineplot(
            path=args.path,
            background_run_time=args.background_run_time,
            animation_run_time=args.animation_run_time,
            wait_run_time=args.wait_run_time,
        )
    elif args.type == "growing_line":
        scene = GrowingLineplot(
            path=args.path,
            background_run_time=args.background_run_time,
            animation_run_time=args.animation_run_time,
            wait_run_time=args.wait_run_time,
        )
    elif args.type == "bar":
        scene = Barplot(
            path=args.path,
            background_run_time=args.background_run_time,
            animation_run_time=args.animation_run_time,
            wait_run_time=args.wait_run_time,
        )
    else:
        scene = GrowingBarplot(
            path=args.path,
            background_run_time=args.background_run_time,
            animation_run_time=args.animation_run_time,
            wait_run_time=args.wait_run_time,
        )

    # Render the scene
    scene.render()
