import yfinance as yf
import pandas as pd


def download_stock_data(
    ticker: str,
    start: str = "1900-01-01",
    end: str = "2100-01-01",
    rounding: bool = True,
) -> pd.DataFrame:
    """
    Download stock data from Yahoo Finance.

    Args:
        ticker (str):
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
    return yf.download(tickers=ticker, start=start, end=end, rounding=rounding)


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
    return pd.DataFrame(
        {
            "X": df.index.to_numpy().astype("datetime64[D]").astype(str),
            "Y": df[column].to_numpy(),
        }
    )
