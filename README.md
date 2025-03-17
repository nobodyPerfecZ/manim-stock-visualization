<div align="middle">
    <h1>
        <p>
            <img src="docs/images/logo.png", alt="Logo", width="300" height="300" />
        </p>
        📈 💸 Manim Stock Visualization
        <br>
        <a href="https://github.com/psf/black">
            <img src="https://img.shields.io/badge/code%20style-black-000000.svg">
        </a>
        <a>
            <img src="https://img.shields.io/badge/python-3.10-blue">
        </a>
        <a>
            <img src="https://img.shields.io/badge/tests-passed-brightgreen">
        </a>
        <a>
            <img src="https://img.shields.io/badge/coverage-91%25-brightgreen">
        </a>
    </h1>
</div>

This repository contains code to visualize stock market prices with Manim Community Edition (manimCE).

## Download Data ⬇️

`manim-stock-visualization` provides methods to easily download and preprocess stock data by using [yfinance](https://github.com/ranaroussi/yfinance).

Below is an example script to download and preprocess stock data for Apple, NVIDIA and Tesla:

```python
"""Example of downloading the stockprices of Apple, NVIDIA and Tesla."""

from manim_stock.util import download_stock_data, preprocess_stock_data

# Download stock data
df = download_stock_data(
    tickers=["AAPL", "NVDA", "TSLA"],
    start="2015-01-01",
    end="2025-01-01",
)

# Preprocess stock data
df = preprocess_stock_data(df, column="High")

# (Optional:) Convert stock price to portfolio value given an initial cashflow
df = preprocess_portfolio_value(df, init_cash=100)

# Safe stock data as CSV file
df.to_csv("stock_data.csv", index=False)
```

## Data Format 📝

`manim-stock-visualization` operates with CSV files in a specific format.
The first column represents the x-values (e.g., years), while the other columns represents the y-values (e.g., stock price), with each column corresponding to a distinct graph/bar.

An example CSV file is displayed below:

```
Year,AAPL,NVDA,TSLA
2015,100.0,100.0,100.0
2015,97.49899152884228,97.95918367346938,96.9758064516129
2015,96.40984267849939,97.95918367346938,95.96774193548386
2015,97.09560306575231,95.91836734693878,96.23655913978494
2015,100.64542154094393,97.95918367346938,95.76612903225805
2015,101.61355385235983,97.95918367346938,94.08602150537634
2015,101.04881000403388,97.95918367346938,91.59946236559139
2015,101.21016538926986,100.0,93.01075268817203
2015,99.15288422751108,97.95918367346938,87.43279569892472
2015,98.74949576442114,97.95918367346938,87.70161290322581
```

## Example Videos 💻

You can watch the full example videos [here](docs/gifs).

### Change the Default Settings 🛠

You can customize the default settings, such as the output filename, resolution and aspect ratio, by modifying the configuration.
Below are some examples demonstrating how to override these defaults:

```python
from manim import config

# Filename
config.output_file = "new_file_name"

# Aspect ratio (16:9) (1920x1080) (e.g. YouTube)
config.frame_width = 16
config.frame_height = 9
config.pixel_width = 1920
config.pixel_height = 1080

# Aspect ratio (9:16) (1080x1920) (e.g. TikTok)
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
```

### Line Plot 📈

The line plot visualizes the stock market prices [\$] of Apple, NVIDIA and Tesla from 01.01.2010 to 01.01.2025.
Below is the script to create the animation and the resulting output:

```python
from manim_stock.visualization import Lineplot

# Create animation
scene = Lineplot(
    path="stock_data.csv",
    background_run_time=5,
    animation_run_time=10,
    wait_run_time=5,
)

# Render animation
scene.render()
```

<p align="center"><img src="docs/gifs/lineplot.gif" alt="lineplot"></p>

### Growing Line Plot 📈

The growing line plot visualizes the stock market prices [\$] of Apple, NVIDIA and Tesla from 01.01.2010 to 01.01.2025.
Below is the script to create the animation and the resulting output.

```python
from manim_stock.visualization import GrowingLineplot

# Create animation
scene = GrowingLineplot(
    path="stock_data.csv",
    background_run_time=5,
    animation_run_time=10,
    wait_run_time=5,
)

# Render animation
scene.render()
```

<p align="center"><img src="docs/gifs/growinglineplot.gif" alt="growinglineplot"></p>

### Bar Plot 📊

The bar plot visualizes the stock market prices [\$] of Apple, NVIDIA and Tesla from 01.01.2010 to 01.01.2025.
Below is the script to create the animation and the resulting output.

```python
from manim_stock.visualization import Barplot

# Create animation
scene = Barplot(
    path="stock_data.csv",
    background_run_time=5,
    animation_run_time=10,
    wait_run_time=5,
)

# Render animation
scene.render()
```

<p align="center"><img src="docs/gifs/barplot.gif" alt="barplot"></p>

### Growing Bar Plot 📊

The growing bar plot visualizes the stock market prices [\$] of Apple, NVIDIA and Tesla from 01.01.2010 to 01.01.2025.
Below is the script to create the animation and the resulting output.

```python
from manim_stock.visualization import GrowingBarplot

# Create animation
scene = GrowingBarplot(
    path="stock_data.csv",
    background_run_time=5,
    animation_run_time=10,
    wait_run_time=5,
)

# Render animation
scene.render()
```

<p align="center"><img src="docs/gifs/growingbarplot.gif" alt="growingbarplot"></p>

## Installation of manim-stock-visualization ⚙️

To use `manim-stock-visualization`, you need to install `manimCE` and `LaTeX` on your system.
Please follow the steps below to install manimCE.
For other systems, please visit the [manimCE installation guide](https://docs.manim.community/en/stable/installation/uv.html).

### Linux (Debian-based)

1. **Update your package list and install prerequisites:**

```bash
sudo apt update
sudo apt install build-essential python3-dev libcairo2-dev libpango1.0-dev
```

2. **Installing LaTeX:**

```bash
sudo apt install texlive-full
```

3. **Installing manimCE:**

```bash
pip install manim
```

4. **Installing manim-stock-visualization**:

```bash
pip install manim-stock-visualization
```

## Development 🔧

Contributions are welcome! Please fork the repository and submit a pull request. Make sure to follow the coding standards and write tests for any new features or bug fixes.
