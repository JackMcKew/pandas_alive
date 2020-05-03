import pandas as pd
from typing import List

OUTPUT_TYPE: str = "file"
OUTPUT_FILENAME: str = ""


def load_dataset(name: str = "covid19") -> pd.DataFrame:
    """ Returns a pandas DataFrame suitable for immediate use in `pandas-alive`

    Args:
        name (str, optional): Name of dataset to load. Either 'covid19' or 'urban_pop'. Defaults to 'covid19'.

    Returns:
        pd.DataFrame: Loaded DataFrame
    """

    return pd.read_csv(
        f"https://raw.githubusercontent.com/JackMcKew/pandas-alive/master/data/{name}.csv",
        index_col="date",
        parse_dates=["date"],
    )


def plot_animated_grid(children_plots: List):
    # TODO Implement multiple animated plots
    a = 0

def output_file(filename: str) -> None:

    if len(filename) <= 0:
        raise ValueError("Specify filename")

    if (
        isinstance(filename, str)
        and "." not in filename
        or len(filename.split(".")[1]) <= 0
    ):
        raise ValueError("`filename` must have an extension")

    global OUTPUT_TYPE
    global OUTPUT_FILENAME
    OUTPUT_TYPE = "file"
    OUTPUT_FILENAME = filename


def output_html():

    global OUTPUT_TYPE
    OUTPUT_TYPE = "html"
