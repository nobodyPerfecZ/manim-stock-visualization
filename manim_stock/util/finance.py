"""Utility functions for downloading and preprocessing stock data."""

import itertools

import pandas as pd
import yfinance as yf


def download_stock_data(
    tickers: str | list[str],
    start: str = "1900-01-01",
    end: str = "2100-01-01",
    rounding: bool = True,
) -> pd.DataFrame:
    """
    Download stock data from Yahoo Finance.

    Args:
        ticker (str | list[str]):
            The stock ticker to download

        start (str):
            The start date in YYYY-MM-DD format

        end (str):
            The end date in YYYY-MM-DD format

        rounding (bool):
            Whether to round the stock prices to 2 decimal places

    Returns:
        pd.DataFrame:
            The stock data as a DataFrame
    """
    return yf.download(
        tickers=tickers, start=start, end=end, rounding=rounding, progress=False
    )


def preprocess_stock_data(df: pd.DataFrame, column: str = "High") -> pd.DataFrame:
    """
    Preprocess stock data by extracting the specified column and the index.

    Args:
        df (pd.DataFrame):
            The stock data as a DataFrame

    Returns:
        pd.DataFrame:
            The preprocessed stock data
    """
    levels = [[column], list(df.columns.levels[1])]
    multi_index = list(itertools.product(*levels))

    data = {"X": df.index.strftime("%Y").to_numpy(dtype=int)}
    for i, idx in enumerate(multi_index):
        data[f"Y{i}"] = df[idx].to_numpy(dtype=float)

    return pd.DataFrame(data).dropna(inplace=False)
