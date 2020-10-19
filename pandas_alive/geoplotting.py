import typing

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Colormap

from .geocharts import MapChart
from pandas_alive.plotting import verify_filename


def geoplot(
    # Base constructor
    input_df: typing.Union[pd.DataFrame, gpd.GeoDataFrame],
    filename: str = None,
    kind: str = "race",
    interpolate_period: bool = True,
    steps_per_period: int = 5,
    period_length: int = 500,
    period_fmt: str = "%d/%m/%Y",
    figsize: typing.Tuple[float, float] = (6.5, 3.5),
    title: str = None,
    fig: plt.Figure = None,
    cmap: typing.Union[str, Colormap, typing.List[str]] = "viridis",
    tick_label_size: typing.Union[int, float] = 7,
    period_label: typing.Union[
        bool, typing.Dict[str, typing.Union[int, float, str]]
    ] = True,
    period_summary_func: typing.Callable = None,
    fixed_max: bool = False,
    dpi: float = 144,
    writer: str = None,
    enable_progress_bar: bool = False,
    # Geo Chart
    basemap_format: typing.Dict = None,
    enable_markersize: bool = False,
    scale_markersize: float = 1,
    **kwargs,
):
    """
    Animated plotting accessor for Geopandas GeoDataFrames


    Args:
        basemap_format (Dict, optional): If provided with a dictionary with keywords arguments as per https://contextily.readthedocs.io/en/latest/reference.html#contextily.add_basemap, this will add a basemap. Defaults to None.
            Ensure to have contextily installed: https://contextily.readthedocs.io/en/latest/index.html
        enable_markersize (bool, optional): Set to True if using Points, this will use the values being plotted as the size of the markers. Defaults to False.
        scale_markersize (float, optional): To be used with enable_markersize, this will scale the size of the markers by the number specified. Defaults to 1.

    Returns:
        MapChart: Returns an instance of the MapChart class for use in multiple plots or save.
    """
    df = input_df.copy()
    map_chart = MapChart(
        df,
        interpolate_period=interpolate_period,
        steps_per_period=steps_per_period,
        period_length=period_length,
        period_fmt=period_fmt,
        figsize=figsize,
        title=title,
        fig=fig,
        cmap=cmap,
        tick_label_size=tick_label_size,
        period_label=period_label,
        period_summary_func=period_summary_func,
        fixed_max=fixed_max,
        dpi=dpi,
        writer=writer,
        enable_progress_bar=enable_progress_bar,
        basemap_format=basemap_format,
        enable_markersize=enable_markersize,
        scale_markersize=scale_markersize,
        kwargs=kwargs,
    )
    if filename:
        map_chart.save(verify_filename(filename))
    return map_chart
