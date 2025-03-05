"""Example of visualizing the stock price of Apple, NVIDIA and Tesla."""

from manim_stock.visualization import Barplot, GrowingLineplot, Lineplot, GrowingBarplot

if __name__ == "__main__":
    """
    # Create scene
    scene = GrowingLineplot(
        path="stock_data.csv",
        title="Market Prices",
        num_samples=100,
        background_run_time=5,
        animation_run_time=50,
        wait_run_time=5,
    )
    """ 
    """
    # Create scene
    scene = Lineplot(
        path="stock_data.csv",
        title="Market Prices",
        background_run_time=5,
        animation_run_time=50,
        wait_run_time=5,
    )
    """
    """
    # Create scene
    scene = Barplot(
        path="stock_data.csv",
        bar_names=["APPLE", "NVIDIA", "TESLA"],
        title="Market Prices",
        background_run_time=5,
        animation_run_time=50,
        wait_run_time=5,
        num_samples=100,
    )
    """

    # Create scene
    scene = GrowingBarplot(
        path="stock_data.csv",
        bar_names=["APPLE", "NVIDIA", "TESLA"],
        title="Market Prices",
        background_run_time=5,
        animation_run_time=50,
        wait_run_time=5,
        num_samples=100,
    )

    # Render scene
    scene.render()
