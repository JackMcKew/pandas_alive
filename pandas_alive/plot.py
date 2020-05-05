import pandas as pd
from pandas.core.base import PandasObject
import typing
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.animation import FuncAnimation
from .charts import BarChart, LineChart

# from .settings import OUTPUT_TYPE, OUTPUT_FILENAME
from . import config

# import config


def get_allowed_kinds():
    return ["barh", "line"]

def verify_filename(filename:str) -> str:
    if len(filename) <= 0:
            raise ValueError("Specify filename")

    if (
        isinstance(filename, str)
        and "." not in filename
        or len(filename.split(".")[1]) <= 0
    ):
        raise ValueError("`filename` must be provided & have an extension")

    return filename

def plot(
    input_df: pd.DataFrame,
    filename: str = None,
    x: str = None,
    y: str = None,
    kind: str = "barh",
    line_width: int = 3,
    use_index: bool = True,
    steps_per_period: int = 10,
    period_length: int = 500,
    figsize: typing.Tuple[float, float] = (6.5, 3.5),
    title: str = None,
    fig: plt.figure = None,
    enable_legend: bool = False,
    orientation: str = "h",
    sort: str = "desc",
    n_bars: int = None,
    label_bars: bool = None,
    cmap: typing.Union[str, matplotlib.colors.Colormap, typing.List[str]] = "dark24",
    bar_label_size: typing.Union[int, float] = 7,
    tick_label_size: typing.Union[int, float] = 7,
    period_label_size: typing.Union[int, float] = 16,
    x_period_label_location: typing.Union[int, float] = None,
    y_period_label_location: typing.Union[int, float] = None,
    append_period_to_title: bool = None,
    hide_period: bool = True,
    dpi: float = 144,
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
            x_period_label_location=x_period_label_location,
            y_period_label_location=y_period_label_location,
            append_period_to_title=append_period_to_title,
            dpi=dpi,
            hide_period=hide_period,
            fig=fig,
            kwargs=kwargs,
        )
        if filename:
            bcr.save(verify_filename(filename))
            # bcr.make_animation(config.OUTPUT_FILENAME)
        return bcr

    elif kind == "line":
        line_race = LineChart(
            df,
            line_width=line_width,
            enable_legend=enable_legend,
            use_index=True,
            steps_per_period=steps_per_period,
            period_length=period_length,
            figsize=figsize,
            cmap=cmap,
            tick_label_size=tick_label_size,
            period_label_size=period_label_size,
            x_period_label_location=x_period_label_location,
            y_period_label_location=y_period_label_location,
            append_period_to_title=append_period_to_title,
            dpi=dpi,
            hide_period=hide_period,
            title=title,
            fig=fig,
            kwargs=kwargs,
        )
        if filename:
            line_race.save(verify_filename(filename))
        return line_race


def animate_multiple_plots(
    filename: str,
    plots: typing.List[typing.Union[BarChart, LineChart]],
    title: str = None,
    title_fontsize: typing.Union[int, float] = 16,
):
    """ Plot multiple animated plots

    Args:
        plots (List[Union[_BarChartRace,_LineChartRace]]): List of plots to animate
    """

    # TODO Maybe add multichart class?

    def update_all_graphs(frame):
        for plot in plots:
            try:
                plot.anim_func(frame)
            except:
                raise UserWarning(
                    f"{type(plot)} {plot.title} error plotting on frame {frame}, ensure all plots share index"
                )

    # Current just number of columns for number of plots
    # TODO add option for number of rows/columns
    # TODO Use gridspec?
    fig, axes = plt.subplots(len(plots))

    # Used for overlapping titles, supplot not considered so move down by 10%
    # https://stackoverflow.com/questions/8248467/matplotlib-tight-layout-doesnt-take-into-account-figure-suptitle
    fig.tight_layout(rect=[0, 0, 1, 0.9])

    if title is not None:
        fig.suptitle(title)

    for num, plot in enumerate(plots):
        axes[num].set_title(plot.title)
        plot.ax = axes[num]

        plot.init_func()

    fps = 1000 / plots[0].period_length * plots[0].steps_per_period
    interval = plots[0].period_length / plots[0].steps_per_period
    anim = FuncAnimation(
        fig,
        update_all_graphs,
        min([max(plot.get_frames()) for plot in plots]),
        interval=interval,
    )

    extension = filename.split(".")[-1]
    if extension == "gif":
        anim.save(filename, fps=fps, writer="imagemagick")
    else:
        anim.save(filename, fps=fps)


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
