# manim-stock-visualization 📈

This repository contains code to visualize stock market prices with Manim Community Edition (manimCE).

## Download Data

`manim-stock-visualization` provides methods to easily download and preprocess stock data by using [yfinance](https://github.com/ranaroussi/yfinance).

Below is an example script to download and preprocess stock data for Apple, NVIDIA and Tesla:

```python
"""Example of downloading the stockprices of Apple, NVIDIA and Tesla."""

from manim_stock.util import download_stock_data, preprocess_stock_data

# Download stock data
df = download_stock_data(
    tickers=["AAPL", "NVDA", "TSLA"],
    start="1900-01-01",
    end="2100-01-01",
)

# Preprocess stock data
df = preprocess_stock_data(df, column="High")

# Safe stock data as CSV file
df.to_csv("stock_data.csv", index=False)
```

## Data Format

`manim-stock-visualization` operates with CSV files in a specific format.
The first column represents the x-values (e.g., years), while the other columns represents the y-values (e.g., stock price), with each column corresponding to a distinct graph/bar.

An example CSV file is displayed below:

```
Year,AAPL,NVDA,TSLA
2010,7.96,0.25,1.67
2010,7.76,0.24,2.03
2010,7.67,0.24,1.73
2010,7.55,0.24,1.54
2010,7.61,0.24,1.33
2010,7.79,0.25,1.11
2010,7.91,0.25,1.17
2010,7.82,0.24,1.19
2010,7.88,0.24,1.2
2010,7.72,0.25,1.24
2010,7.7,0.26,1.34
2010,7.73,0.25,1.43
2010,7.67,0.25,1.42
2010,7.52,0.24,1.48
2010,7.61,0.25,1.46
2010,7.98,0.25,1.39
2010,7.82,0.24,1.42
2010,7.84,0.24,1.44
2010,7.83,0.24,1.43
```

## Example Videos 💻

You can watch the full example videos [here](docs/examples).

### Line Plot

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

<p align="center"><img src="examples/docs/lineplot.gif" alt="Logo"></p>

### Growing Line Plot

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

<p align="center"><img src="examples/docs/growinglineplot.gif" alt="Logo"></p>

### Bar Plot

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

<p align="center"><img src="examples/docs/barplot.gif" alt="Logo"></p>

### Growing Bar Plot

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

<p align="center"><img src="examples/docs/growingbarplot.gif" alt="Logo"></p>

## Installation of manim-stock-visualization ⚙️
To use `manim-stock-visualization`, you need to install ``manimCE`` and ``LaTeX`` on your system.
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
