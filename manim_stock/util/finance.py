"""Utility functions for downloading and preprocessing stock data."""

import itertools
from typing import Sequence

import pandas as pd
import yfinance as yf


def download_stock_data(
    tickers: str | Sequence[str],
    start: str = "1900-01-01",
    end: str = "2100-01-01",
    **kwargs,
) -> pd.DataFrame:
    """
    Download stock data from Yahoo Finance.

    Args:
        ticker (str | Sequence[str]):
            The stock ticker to download.

        start (str):
            The start date in YYYY-MM-DD format.

        end (str):
            The end date in YYYY-MM-DD format.

        **kwargs:
            Additional arguments to be passed to yf.download().

    Returns:
        pd.DataFrame:
            The resulting DataFrame.
    """
    if "rounding" not in kwargs:
        kwargs["rounding"] = True
    if "progress" not in kwargs:
        kwargs["progress"] = False
    if "auto_adjust" not in kwargs:
        kwargs["auto_adjust"] = True

    return yf.download(tickers=tickers, start=start, end=end, **kwargs)


def preprocess_stock_data(df: pd.DataFrame, column: str = "High") -> pd.DataFrame:
    """
    Extract the specified column and index from the DataFrame.

    Args:
        df (pd.DataFrame):
            The DataFrame to preprocess.

    Returns:
        pd.DataFrame:
            The preprocessed DataFrame.
    """
    levels = [[column], list(df.columns.levels[1])]
    multi_index = list(itertools.product(*levels))

    data = {"Year": df.index.strftime("%Y").to_numpy(dtype=int)}
    for col, ticker in multi_index:
        data[ticker] = df[(col, ticker)].to_numpy(dtype=float)

    return pd.DataFrame(data).dropna(inplace=False)


def preprocess_portfolio_value(
    df: pd.DataFrame,
    init_cash: float = 1000,
) -> pd.DataFrame:
    """
    Convert DataFrame with stock prices into DataFrame with portfolio value.

    Args:
        df (pd.DataFrame):
            The DataFrame with stock prices

        init_cash (float):
            The initial cash to invest

    Returns:
        pd.DataFrame:
            The DataFrame with portfolio value
    """
    shares = init_cash / df[df.columns[1:]].iloc[0]
    df[df.columns[1:]] = shares * df[df.columns[1:]]
    return df
