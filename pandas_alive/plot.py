
import pandas as pd
from pandas.core.base import PandasObject
from .charts import _BarChartRace, bar_chart_race, line_chart_race
# from .settings import OUTPUT_TYPE, OUTPUT_FILENAME
from . import config
# import config

def get_allowed_kinds():
    return ["barh"]


def plot(input_df: pd.DataFrame, kind: str = "barh", **kwargs):

    df = input_df.copy()
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)

    allowed_kinds = get_allowed_kinds()

    if kind not in allowed_kinds:
        allowed_kinds = "', '".join(allowed_kinds)
        raise ValueError("Allowed plot kinds are '%s'." % allowed_kinds)

    if kind == "barh":
        if config.OUTPUT_TYPE == "file":
            bcr = bar_chart_race(
                df,
                config.OUTPUT_FILENAME
            )
            bcr.make_animation()
        elif config.OUTPUT_TYPE == "html":
            return bar_chart_race(
                df
            )
        else:
            raise NotImplementedError(f"{config.OUTPUT_TYPE} is not implemented yet")
        # raise NotImplementedError("Barh is not supported yet")


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
