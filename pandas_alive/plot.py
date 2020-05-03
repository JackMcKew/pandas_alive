import pandas as pd
from pandas.core.base import PandasObject
import typing
import matplotlib
from .charts import BarChart, LineChart

# from .settings import OUTPUT_TYPE, OUTPUT_FILENAME
from . import config

# import config


def get_allowed_kinds():
    return ["barh", "line"]


def plot(
    input_df: pd.DataFrame,
    x: str = None,
    y: str = None,
    kind: str = "barh",
    line_width:int = 3,
    write_to_file:bool=True,
    use_index: bool = True,
    steps_per_period: int = 10,
    period_length: int = 500,
    figsize: typing.Tuple[float, float] = (6.5, 3.5),
    title: str = None,
    fig: matplotlib.pyplot.figure = None,
    orientation: str = "h",
    sort: str = "desc",
    n_bars: int = None,
    label_bars: bool = None,
    cmap: typing.Union[str, matplotlib.colors.Colormap, typing.List[str]] = "dark24",
    bar_label_size: typing.Union[int, float] = 7,
    tick_label_size: typing.Union[int, float] = 7,
    period_label_size: typing.Union[int, float] = 16,
    **kwargs,
):
    df = input_df.copy()
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)

    allowed_kinds = get_allowed_kinds()

    if kind not in allowed_kinds:
        allowed_kinds = "', '".join(allowed_kinds)
        raise ValueError("Allowed plot kinds are '%s'." % allowed_kinds)

    if kind == "barh":
        if config.OUTPUT_TYPE == "file":
            bcr = BarChart(
                df,
                orientation=orientation,
                sort=sort,
                n_bars=n_bars,
                label_bars=label_bars,
                use_index=True,
                steps_per_period=steps_per_period,
                period_length=period_length,
                figsize=figsize,
                cmap=cmap,
                title=title,
                bar_label_size=bar_label_size,
                tick_label_size=tick_label_size,
                period_label_size=period_label_size,
                fig=fig,
                kwargs=kwargs
            )
            if write_to_file:
                bcr.make_animation(config.OUTPUT_FILENAME)
            return bcr
        elif config.OUTPUT_TYPE == "html":
            return bar_chart_race(df)
        else:
            raise NotImplementedError(f"{config.OUTPUT_TYPE} is not implemented yet")

    elif kind == "line":
        if config.OUTPUT_TYPE == "file":
            # line_race = 
            line_race = LineChart(
                df,
                line_width=line_width,
                use_index=True,
                steps_per_period=steps_per_period,
                period_length=period_length,
                figsize=figsize,
                cmap=cmap,
                title=title,
                fig=fig,
                kwargs=kwargs
            )
            if write_to_file:
                line_race.make_animation(config.OUTPUT_FILENAME)
            return line_race


##############################################################################
########### Class to add Animated plotting methods to Pandas DataFrame
##############################################################################
# Inspiration: https://github.com/PatrikHlobil/Pandas-Bokeh/blob/cb241ea570a0a2ea3d0c7055fbe79bbdd06cc712/pandas_bokeh/plot.py#L1759


class BasePlotMethods(PandasObject):
    def __init__(self, data):
        self._parent = data  # can be Series or DataFrame

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class AnimatedAccessor(BasePlotMethods):
    def __call__(self, *args, **kwargs):
        return plot(self.df, *args, **kwargs)

    @property
    def df(self):

        return self._parent

    def barh(self, x: str = None, y: str = None, **kwds):
        """ Make an animated horizontal bar plot.

        Args:
            x (str, optional): label or position. Defaults to DataFrame.index. Column to be used on categories.
            y (str, optional): label or position. Defaults to All numeric columns in DataFrame. Column to be plotted from the DataFrame

        Returns:
            [type]: [description]
        """

        return self(kind="barh", x=x, y=y, **kwds)
