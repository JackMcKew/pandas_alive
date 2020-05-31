""" Common functions shared apart from charts/plots

This module contains functions/classes for functionality outside of plotting.

Example:
    `df = pandas_alive.load_dataset()`

    Example dataset suitable for immediate use with pandas_alive. Either `covid19` or `urban_pop`. Defaults to `covid19`.
"""

import pandas as pd


def load_dataset(name: str = "covid19") -> pd.DataFrame:
    """ Returns a pandas DataFrame suitable for immediate use in `pandas_alive`


    Example:
        ``df = pandas_alive.load_dataset()``

    Args:
        name (str, optional): Name of dataset to load. Either 'covid19' or 'urban_pop'. Defaults to 'covid19'.

    Returns:
        pd.DataFrame: Loaded DataFrame
    """

    return pd.read_csv(
        f"https://raw.githubusercontent.com/JackMcKew/pandas_alive/master/data/{name}.csv",
        index_col=0,
        parse_dates=[0],
    )
