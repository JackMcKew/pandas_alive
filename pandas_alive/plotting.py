""" Plotting implementations for accessor to Pandas.DataFrame & multiple animated plots

This module contains functions for plotting functionality.


Example:
    ``df.plot_animated()``
"""

import pandas as pd
from pandas.core.base import PandasObject
import typing
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.animation import FuncAnimation
from .charts import BarChart, LineChart, ScatterChart


def get_allowed_kinds() -> typing.List[str]:
    """ Get list of implemented charts

    Returns:
        typing.List[str]: List of implemented chart types
    """
    return ["barh", "line","scatter"]


def verify_filename(filename: str) -> str:
    """ Check file name is accurate

    Args:
        filename (str): String for file name with extension

    Raises:
        ValueError: Provide filename with extensions
        ValueError: Specify a length > 0

    Returns:
        str: Verified file name
    """
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
    n_visible: int = None,
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
    label_bars: bool = True,
    cmap: typing.Union[str, matplotlib.colors.Colormap, typing.List[str]] = "dark24",
    bar_label_size: typing.Union[int, float] = 7,
    tick_label_size: typing.Union[int, float] = 7,
    period_annotation_size: typing.Union[int, float] = 16,
    x_period_annotation_location: typing.Union[int, float] = None,
    y_period_annotation_location: typing.Union[int, float] = None,
    append_period_to_title: bool = None,
    show_period_annotation: bool = True,
    period_annotation_formatter: str = "%d/%m/%Y",
    dpi: float = 144,
    point_size: typing.Union[int,float] = 2,
    **kwargs,
) -> typing.Union[BarChart,LineChart]:
    """ Create animated charts with matplotlib. Optionally the index can label the time period. This is very resource intensive, will take time to run and export.

    Args:
        input_df (pd.DataFrame): Input dataframe containing data to be plotted. Function will attempt to plot as many columns of data as possible.
        filename (str, optional): If None returns instance of chart to be used later with `.save()` or `.get_html5_video()`. Defaults to None.
        x (str, optional): Intended for future use, currently does nothing. Defaults to None.
        y (str, optional): Intended for future use, currently does nothing.. Defaults to None.
        kind (str, optional): Type of chart to use, see get_allowed_kinds for possible options. Defaults to "barh".
        n_visible (int, optional): Show top/bottom N values in bar chart, not implemented for line chart currently. Defaults to None.
        line_width (int, optional): Line width for Line charts, applies to all lines. Defaults to 3.
        use_index (bool, optional): Use index for time axis. Defaults to True.
        steps_per_period (int, optional): The number of steps to go from one time period to the next. Animation will interpolate between time periods. Defaults to 10.
        period_length (int, optional): Number of milliseconds to animate each period (row). Defaults to 500.
        figsize (typing.Tuple[float, float], optional): Matplotlib figure size in inches, will be overridden if fig supplied. Defaults to (6.5, 3.5).
        title (str, optional): Title of plot, will become subplot title if used in multiple. Defaults to None.
        fig (plt.figure, optional): For specifying figure outside of this function. Defaults to None.
        enable_legend (bool, optional): Show legend on line charts, will run off screen for two many lines. Defaults to False.
        orientation (str, optional): Orientation of bar chart, horizontal ('h') or vertical ('v'). Defaults to "h".
        sort (str, optional): Choose how to sort the bar chart. Use 'desc' to put the largest bars on top, and 'asc' for the largest bars on bottom. Defaults to "desc".
        label_bars (bool, optional): Whether to label the bars with their value to the right. Defaults to None.
        cmap (typing.Union[str, matplotlib.colors.Colormap, typing.List[str]], optional): Provide string of colormap name, colormap instance, single color instance or list of colors as supported by https://matplotlib.org/2.0.2/api/colors_api.html. Defaults to "dark24".
        bar_label_size (typing.Union[int, float], optional): Size in points of numeric labels just outside of bars. Defaults to 7.
        tick_label_size (typing.Union[int, float], optional): Size in points of tick labels. Defaults to 7.
        period_annotation_size (typing.Union[int, float], optional): Size in points of period annotation on chart. Defaults to 16.
        x_period_annotation_location (typing.Union[int, float], optional): Custom x location for period annotation. Must be supplied with custom y location. Defaults to None.
        y_period_annotation_location (typing.Union[int, float], optional): Custom y location for period annotation. Must be supplied with custom x location.. Defaults to None.
        append_period_to_title (bool, optional): Append period annotation to title, this disables period annotation on chart. Defaults to None.
        show_period_annotation (bool, optional): Show period annotation on chart. Useful to hide when plotting multiple charts. Defaults to True.
        dpi (float, optional): It is possible for some bars to be out of order momentarily during a transition since both height and location change linearly.. Defaults to 144.

    Raises:
        ValueError: If supplied kind is not supported

    Returns:
        typing.Union[BarChart,LineChart]: Returns Chart instance to be used with animate_multiple or .save()
    """
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
            n_visible=n_visible,
            # n_bars=n_bars,
            label_bars=label_bars,
            use_index=True,
            steps_per_period=steps_per_period,
            period_length=period_length,
            figsize=figsize,
            cmap=cmap,
            title=title,
            bar_label_size=bar_label_size,
            tick_label_size=tick_label_size,
            period_annotation_size=period_annotation_size,
            x_period_annotation_location=x_period_annotation_location,
            y_period_annotation_location=y_period_annotation_location,
            append_period_to_title=append_period_to_title,
            dpi=dpi,
            show_period_annotation=show_period_annotation,
            period_annotation_formatter=period_annotation_formatter,
            fig=fig,
            kwargs=kwargs,
        )
        if filename:
            bcr.save(verify_filename(filename))
        return bcr

    elif kind == "line":
        line_race = LineChart(
            df,
            line_width=line_width,
            enable_legend=enable_legend,
            use_index=True,
            n_visible=n_visible,
            steps_per_period=steps_per_period,
            period_length=period_length,
            figsize=figsize,
            cmap=cmap,
            tick_label_size=tick_label_size,
            period_annotation_size=period_annotation_size,
            x_period_annotation_location=x_period_annotation_location,
            y_period_annotation_location=y_period_annotation_location,
            append_period_to_title=append_period_to_title,
            dpi=dpi,
            show_period_annotation=show_period_annotation,
            period_annotation_formatter=period_annotation_formatter,
            title=title,
            fig=fig,
            kwargs=kwargs,
        )
        if filename:
            line_race.save(verify_filename(filename))
        return line_race
    elif kind == "scatter":
        animated_scatter = ScatterChart(
            df,
            use_index=True,
            n_visible=n_visible,
            steps_per_period=steps_per_period,
            period_length=period_length,
            figsize=figsize,
            cmap=cmap,
            tick_label_size=tick_label_size,
            period_annotation_size=period_annotation_size,
            x_period_annotation_location=x_period_annotation_location,
            y_period_annotation_location=y_period_annotation_location,
            append_period_to_title=append_period_to_title,
            dpi=dpi,
            show_period_annotation=show_period_annotation,
            period_annotation_formatter=period_annotation_formatter,
            title=title,
            fig=fig,
            size = point_size,
            kwargs=kwargs,
        )
        if filename:
            animated_scatter.save(verify_filename(filename))
        return animated_scatter


def animate_multiple_plots(
    filename: str,
    plots: typing.List[typing.Union[BarChart, LineChart]],
    title: str = None,
    title_fontsize: typing.Union[int, float] = 16,
    dpi: int = 144,
    adjust_subplot_left: float = 0.125,
    adjust_subplot_right: float = 0.9,
    adjust_subplot_bottom: float = 0.1,
    adjust_subplot_top: float = 0.9,
    adjust_subplot_wspace: float = 0.2,
    adjust_subplot_hspace: float = 0.2,
):
    """ Plot multiple animated subplots with plt.subplots()

    Args:
        filename (str): Output file name with extension to rite to
        plots (typing.List[typing.Union[BarChart, LineChart]]): List of chart instances
        title (str, optional): Overall title for plots (suptitle). Defaults to None.
        title_fontsize (typing.Union[int, float], optional): Font size for suptitle. Defaults to 16.
        dpi (int, optional): Custom DPI to increase resolution. Defaults to 144.
        adjust_subplot_left (float, optional): the left side of the subplots of the figure. Defaults to 0.125.
        adjust_subplot_right (float, optional): the right side of the subplots of the figure. Defaults to 0.9.
        adjust_subplot_bottom (float, optional): the bottom of the subplots of the figure. Defaults to 0.1.
        adjust_subplot_top (float, optional): the top of the subplots of the figure. Defaults to 0.9.
        adjust_subplot_wspace (float, optional): the amount of width reserved for space between subplots, expressed as a fraction of the average axis width. Defaults to 0.2.
        adjust_subplot_hspace (float, optional): the amount of height reserved for space between subplots, expressed as a fraction of the average axis height. Defaults to 0.2.

    Raises:
        UserWarning: If Error found when plotting, prompt user to ensure indexs of plots are same length
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
    # Defaults from https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.subplots_adjust.html
    fig.subplots_adjust(left=adjust_subplot_left,right=adjust_subplot_right,bottom=adjust_subplot_bottom,top=adjust_subplot_top,wspace=adjust_subplot_wspace,hspace=adjust_subplot_hspace)
    # plt.tight_layout()
    # fig = plt.figure()
    # spec = fig.add_gridspec()
    # fig.add_subplot(spec[0, 1])
    # Used for overlapping titles, supplot not considered so move down by 10%
    # https://stackoverflow.com/questions/8248467/matplotlib-tight-layout-doesnt-take-into-account-figure-suptitle
    # fig.tight_layout(rect=[0, 0, 1, 0.9])
    # fig.constrained_layout()
    # plt.rcParams["figure.constrained_layout.use"] = True
    # plt.subplots_adjust(top=0.85)
    # plt.subplots_adjust()
    # plt.rcParams.update({'figure.autolayout': True})

    if title is not None:
        fig.suptitle(title)

    for num, plot in enumerate(plots):
        # plot.ax = fig.add_subplot(spec[num:,0])[0]
        axes[num].grid(True, axis="x", color="white")
        axes[num].set_axisbelow(True)
        axes[num].tick_params(length=0, labelsize=plot.tick_label_size, pad=2)
        axes[num].set_facecolor(".9")
        for spine in axes[num].spines.values():
            spine.set_visible(False)
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
        anim.save(filename, fps=fps,dpi=dpi, writer="imagemagick")
    else:
        anim.save(filename, fps=fps,dpi=dpi)


##############################################################################
########### Class to add Animated plotting methods to Pandas DataFrame
##############################################################################
# Inspiration: https://github.com/PatrikHlobil/Pandas-Bokeh/blob/cb241ea570a0a2ea3d0c7055fbe79bbdd06cc712/pandas_bokeh/plot.py#L1759


class BasePlotMethods(PandasObject):
    """ For extending accessor to pandas DataFrame

    Args:
        PandasObject (PandasObject): Base Pandas Object
    """
    def __init__(self, data):
        self._parent = data  # can be Series or DataFrame

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class AnimatedAccessor(BasePlotMethods):
    """ For including accessor on df, to enable `df.plot_animated()`

    Args:
        BasePlotMethods ([type]): BasePlotMethods within pandas
    """
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
            BarChart: BarChart instance for use with multiple plots or .save()
        """

        return self(kind="barh", x=x, y=y, **kwds)
