"""Tests for manim_stock/util/finance.py."""

import itertools

import numpy as np

from manim_stock.util import (
    download_stock_data,
    preprocess_portfolio_value,
    preprocess_stock_data,
)


def test_download_stock_data_with_single_ticker():
    """Tests the download_stock_data() method for a single ticker."""
    df = download_stock_data(
        tickers="AAPL",
        start="2020-01-01",
        end="2024-01-01",
    )
    multi_index = list(itertools.product(*df.columns.levels))

    assert df.shape == (1006, 5)
    assert multi_index == [
        ("Close", "AAPL"),
        ("High", "AAPL"),
        ("Low", "AAPL"),
        ("Open", "AAPL"),
        ("Volume", "AAPL"),
    ]


def test_download_stock_data_with_multiple_tickers():
    """Tests the download_stock_data() method for multiple tickers."""
    df = download_stock_data(
        tickers=["AAPL", "NVDA"],
        start="2020-01-01",
        end="2024-01-01",
    )
    multi_index = list(itertools.product(*df.columns.levels))

    assert df.shape == (1006, 10)
    assert multi_index == [
        ("Close", "AAPL"),
        ("Close", "NVDA"),
        ("High", "AAPL"),
        ("High", "NVDA"),
        ("Low", "AAPL"),
        ("Low", "NVDA"),
        ("Open", "AAPL"),
        ("Open", "NVDA"),
        ("Volume", "AAPL"),
        ("Volume", "NVDA"),
    ]


def test_preprocess_stock_data_with_single_ticker():
    """Tests the preprocess_stock_data() method for a single ticker."""
    df = download_stock_data(
        tickers="AAPL",
        start="2020-01-01",
        end="2024-01-01",
    )
    df = preprocess_stock_data(df, column="High")
    index = list(df.columns)

    assert df.shape == (1006, 2)
    assert index == ["Year", "AAPL"]


def test_preprocess_stock_data_with_multiple_tickers():
    """Tests the preprocess_stock_data() method for multiple tickers."""
    df = download_stock_data(
        tickers=["AAPL", "NVDA"],
        start="2020-01-01",
        end="2024-01-01",
    )
    df = preprocess_stock_data(df, column="High")
    index = list(df.columns)

    assert df.shape == (1006, 3)
    assert index == ["Year", "AAPL", "NVDA"]


def test_preprocess_portfolio_value_with_single_ticker():
    """Tests the preprocess_portfolio_value() method for a single ticker."""
    df = download_stock_data(
        tickers=["AAPL"],
        start="2020-01-01",
        end="2024-01-01",
    )
    df = preprocess_stock_data(df, column="High")
    df = preprocess_portfolio_value(df, 10000)
    index = list(df.columns)

    assert df.shape == (1006, 2)
    assert index == ["Year", "AAPL"]
    np.allclose(df["AAPL"].iloc[0], 10000)
    np.allclose(df["AAPL"].iloc[-1], 26551.250343500964)


def test_preprocess_portfolio_value_with_multiple_ticker():
    """Tests the preprocess_portfolio_value() method for multiple tickers."""
    df = download_stock_data(
        tickers=["AAPL", "NVDA"],
        start="2020-01-01",
        end="2024-01-01",
    )
    df = preprocess_stock_data(df, column="High")
    df = preprocess_portfolio_value(df, 10000)
    index = list(df.columns)

    assert df.shape == (1006, 3)
    assert index == ["Year", "AAPL", "NVDA"]
    np.allclose(df["AAPL"].iloc[0], 10000)
    np.allclose(df["NVDA"].iloc[0], 10000)
    np.allclose(df["AAPL"].iloc[-1], 26551.250343500964)
    np.allclose(df["NVDA"].iloc[-1], 83718.59296482411)
