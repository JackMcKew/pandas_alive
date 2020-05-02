import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import ticker, colors
from typing import Tuple, Union, List

DARK24 = [
    "#2E91E5",
    "#E15F99",
    "#1CA71C",
    "#FB0D0D",
    "#DA16FF",
    "#222A2A",
    "#B68100",
    "#750D86",
    "#EB663B",
    "#511CFB",
    "#00A08B",
    "#FB00D1",
    "#FC0080",
    "#B2828D",
    "#6C7C32",
    "#778AAE",
    "#862A16",
    "#A777F1",
    "#620042",
    "#1616A7",
    "#DA60CA",
    "#6C4516",
    "#0D2A63",
    "#AF0038",
]


class _BaseChart:
    def __init__(
        self,
        data: Union[pd.DataFrame, pd.Series],
        use_index: bool,
        steps_per_period: int,
        period_length: int,
        title: str,
        figsize: Tuple,
        dpi: int,
        tick_label_size: int,
        bar_label_size: int,
        period_label_size: int,
        fig: plt.Figure,
        kwargs,
    ) -> None:
        self.data = data,
        self.use_index = use_index
        self.steps_per_period = steps_per_period
        self.period_length = period_length
        self.orig_index = self.data.index
        self.title = title
        self.figsize = figsize
        self.dpi = dpi
        self.tick_label_size = tick_label_size
        self.bar_label_size = bar_label_size
        self.period_label_size = period_label_size
        self.fps = 1000 / self.period_length * steps_per_period
        self.fig = fig
        self.kwargs = kwargs
        
    def validate_params(self) -> None:
        if self.fig is not None and not isinstance(self.fig, plt.Figure):
            raise TypeError("`fig` must be a matplotlib Figure instance")

    def anim_func(self, frame):
        raise NotImplementedError("Animation function not yet implemented")

    def make_animation(self, frames, init_func) -> FuncAnimation:

        interval = self.period_length / self.steps_per_period
        return FuncAnimation(
            self.fig,
            self.anim_func,
            frames,
            init_func,
            interval=interval,
        )


class _LineChartRace(_BaseChart):
    def __init__(
        self,
        series: pd.Series,
        filename: str,
        line_width: int,
        use_index: bool,
        steps_per_period: int,
        period_length: int,
        title: str,
        figsize: Tuple,
        dpi: int,
        tick_label_size: int,
        bar_label_size: int,
        period_label_size: int,
        fig: plt.Figure,
        kwargs,
    ) -> None:
        super().__init__(
            series,
            use_index,
            steps_per_period,
            period_length,
            title,
            figsize,
            144,
            tick_label_size,
            bar_label_size,
            period_label_size,
            fig,
            kwargs,
        )
        self.series = series
        self.filename = filename
        self.line_width = line_width
        self.xdata = []
        self.ydata = []
        if self.fig is not None:
            self.fig, self.ax = fig, fig.axes[0]
            self.figsize = fig.get_size_inches()
            self.dpi = fig.dpi
        else:
            self.fig = plt.figure()
            self.ax = plt.axes()



    def plot_line(self, i):
        self.ax.set_xlim(self.series.index.min(),self.series.index.max())
        self.ax.set_ylim((self.series.min(),self.series.max()))
        self.xdata.append(self.series.index[i])
        self.ydata.append(self.series.iloc[i])
        self.ax.plot(self.xdata,self.ydata,self.line_width)
        # return self.line

    def anim_func(self, i):
        for line in self.ax.lines:
            line.remove()
        self.plot_line(i)

    def init_func(self) -> None:
        self.ax.plot([],[],self.line_width)

    def get_frames(self):
        return range(len(self.series))

    def make_animation(self):
        
            # self.line.set_data([],[])

        anim = super().make_animation(self.get_frames(), self.init_func)

        extension = self.filename.split(".")[-1]
        if extension == "gif":
            anim.save(self.filename, fps=self.fps, writer="imagemagick")
        else:
            anim.save(self.filename, fps=self.fps)


class _BarChartRace(_BaseChart):
    def __init__(
        self,
        df,
        filename,
        orientation,
        sort,
        n_bars,
        label_bars,
        use_index,
        steps_per_period,
        period_length,
        figsize,
        cmap,
        title,
        bar_label_size,
        tick_label_size,
        period_label_size,
        fig,
        kwargs,
    ):
        super().__init__(
            df,
            use_index,
            steps_per_period,
            period_length,
            title,
            figsize,
            144,
            tick_label_size,
            bar_label_size,
            period_label_size,
            fig,
            kwargs,
        )
        self.df = df
        self.filename = filename
        self.orientation = orientation
        self.sort = sort
        self.n_bars = n_bars or df.shape[1]
        self.label_bars = label_bars
        self.use_index = use_index
        self.steps_per_period = steps_per_period
        self.period_length = period_length
        self.orig_index = self.df.index.astype("str")
        self.title = title
        self.figsize = figsize
        self.dpi = 144
        self.tick_label_size = tick_label_size
        self.bar_label_size = bar_label_size
        self.period_label_size = period_label_size
        self.fps = 1000 / self.period_length * steps_per_period
        self.fig = fig
        self.kwargs = kwargs
        self.validate_params()
        self.html = self.filename is None
        self.bar_colors = self.get_colors(cmap)
        self.x_label, self.y_label = self.get_label_position()
        self.df_values, self.df_rank = self.prepare_data()
        if self.fig is not None:
            self.fig, self.ax = fig, fig.axes[0]
            self.figsize = fig.get_size_inches()
            self.dpi = fig.dpi
        else:
            self.fig, self.ax = self.create_figure()

    def validate_params(self):
        super().validate_params()
        
        if self.sort not in ("asc", "desc"):
            raise ValueError('`sort` must be "asc" or "desc"')

        if self.orientation not in ("h", "v"):
            raise ValueError('`orientation` must be "h" or "v"')

        if isinstance(self.filename, str):
            if "." not in self.filename:
                raise ValueError("`filename` must have an extension")
            if len(self.filename.split(".")[1]) <= 0:
                raise ValueError("`filename` must have an extension")
        elif self.filename is not None:
            raise TypeError("`filename` must be None or a string")

    def get_colors(self, cmap):
        if isinstance(cmap, str):
            cmap = DARK24 if cmap == "dark24" else plt.cm.get_cmap(cmap)
        if isinstance(cmap, colors.Colormap):
            bar_colors = cmap(range(cmap.N)).tolist()
        elif isinstance(cmap, list):
            bar_colors = cmap
        elif hasattr(cmap, "tolist"):
            bar_colors = cmap.tolist()
        else:
            raise TypeError(
                "`cmap` must be a string name of a colormap, a matplotlib colormap instance"
                "or a list of colors"
            )

        # bar_colors is now a list
        n = len(bar_colors)
        if self.df.shape[1] > n:
            bar_colors = bar_colors * (self.df.shape[1] // n + 1)
        return np.array(bar_colors[: self.df.shape[1]])

    def get_label_position(self):
        if self.orientation == "h":
            x_label = 0.6
            y_label = 0.25 if self.sort == "desc" else 0.8
        else:
            x_label = 0.7 if self.sort == "desc" else 0.1
            y_label = 0.8
        return x_label, y_label

    def prepare_data(self):
        df_values = self.df.reset_index(drop=True)
        df_values.index = df_values.index * self.steps_per_period
        df_rank = df_values.rank(axis=1, method="first", ascending=False).clip(
            upper=self.n_bars + 1
        )
        if (self.sort == "desc" and self.orientation == "h") or (
            self.sort == "asc" and self.orientation == "v"
        ):
            df_rank = self.n_bars + 1 - df_rank
        new_index = range(df_values.index.max() + 1)
        df_values = df_values.reindex(new_index).interpolate()
        df_rank = df_rank.reindex(new_index).interpolate()
        return df_values, df_rank

    def create_figure(self):
        fig = plt.Figure(figsize=self.figsize, dpi=self.dpi)
        limit = (0.2, self.n_bars + 0.8)
        rect = self.calculate_new_figsize(fig)
        ax = fig.add_axes(rect)
        if self.orientation == "h":
            ax.set_ylim(limit)
            ax.grid(True, axis="x", color="white")
            ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
        else:
            ax.set_xlim(limit)
            ax.grid(True, axis="y", color="white")
            ax.set_xticklabels(ax.get_xticklabels(), ha="right", rotation=30)
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

        ax.set_axisbelow(True)
        ax.tick_params(length=0, labelsize=self.tick_label_size, pad=2)
        ax.set_facecolor(".9")
        ax.set_title(self.title)
        for spine in ax.spines.values():
            spine.set_visible(False)
        return fig, ax

    def calculate_new_figsize(self, real_fig):
        import io

        fig = plt.Figure(tight_layout=True, figsize=self.figsize)
        ax = fig.add_subplot()
        fake_cols = [chr(i + 70) for i in range(self.df.shape[1])]
        max_val = self.df_values.max().max()
        if self.orientation == "h":
            ax.barh(fake_cols, [1] * self.df.shape[1])
            ax.tick_params(labelrotation=0, axis="y", labelsize=self.tick_label_size)
            ax.set_title(self.title)
            fig.canvas.print_figure(io.BytesIO())
            orig_pos = ax.get_position()
            ax.set_yticklabels(self.df.columns)
            ax.set_xticklabels([max_val] * len(ax.get_xticks()))
        else:
            ax.bar(fake_cols, [1] * self.df.shape[1])
            ax.tick_params(labelrotation=30, axis="x", labelsize=self.tick_label_size)
            ax.set_title(self.title)
            fig.canvas.print_figure(io.BytesIO())
            orig_pos = ax.get_position()
            ax.set_xticklabels(self.df.columns, ha="right")
            ax.set_yticklabels([max_val] * len(ax.get_yticks()))

        fig.canvas.print_figure(io.BytesIO(), format="png")
        new_pos = ax.get_position()

        coordx, prev_coordx = new_pos.x0, orig_pos.x0
        coordy, prev_coordy = new_pos.y0, orig_pos.y0
        old_w, old_h = self.figsize

        # if coordx > prev_coordx or coordy > prev_coordy:
        prev_w_inches = prev_coordx * old_w
        total_w_inches = coordx * old_w
        extra_w_inches = total_w_inches - prev_w_inches
        new_w_inches = extra_w_inches + old_w

        prev_h_inches = prev_coordy * old_h
        total_h_inches = coordy * old_h
        extra_h_inches = total_h_inches - prev_h_inches
        new_h_inches = extra_h_inches + old_h

        real_fig.set_size_inches(new_w_inches, new_h_inches)
        left = total_w_inches / new_w_inches
        bottom = total_h_inches / new_h_inches
        width = orig_pos.x1 - left
        height = orig_pos.y1 - bottom
        return [left, bottom, width, height]

    def plot_bars(self, i):
        bar_location = self.df_rank.iloc[i].values
        top_filt = (bar_location > 0) & (bar_location < self.n_bars + 1)
        bar_location = bar_location[top_filt]
        bar_length = self.df_values.iloc[i].values[top_filt]
        cols = self.df.columns[top_filt]
        colors = self.bar_colors[top_filt]
        if self.orientation == "h":
            self.ax.barh(
                bar_location,
                bar_length,
                ec="white",
                tick_label=cols,
                color=colors,
                **self.kwargs,
            )
            self.ax.set_xlim(self.ax.get_xlim()[0], bar_length.max() * 1.1)
        else:
            self.ax.bar(
                bar_location,
                bar_length,
                ec="white",
                tick_label=cols,
                color=colors,
                **self.kwargs,
            )
            self.ax.set_ylim(self.ax.get_ylim()[0], bar_length.max() * 1.16)

        if self.use_index:
            val = self.orig_index[i // self.steps_per_period]
            num_texts = len(self.ax.texts)
            if num_texts == 0:
                self.ax.text(
                    self.x_label,
                    self.y_label,
                    val,
                    transform=self.ax.transAxes,
                    fontsize=self.period_label_size,
                )
            else:
                self.ax.texts[0].set_text(val)

        if self.label_bars:
            for text in self.ax.texts[int(self.use_index) :]:
                text.remove()
            if self.orientation == "h":
                zipped = zip(bar_length, bar_location)
            else:
                zipped = zip(bar_location, bar_length)

            for x1, y1 in zipped:
                xtext, ytext = self.ax.transLimits.transform((x1, y1))
                if self.orientation == "h":
                    xtext += 0.01
                    text = f"{x1:,.0f}"
                    rotation = 0
                    ha = "left"
                    va = "center"
                else:
                    ytext += 0.015
                    text = f"{y1:,.0f}"
                    rotation = 90
                    ha = "center"
                    va = "bottom"
                xtext, ytext = self.ax.transLimits.inverted().transform((xtext, ytext))
                self.ax.text(
                    xtext,
                    ytext,
                    text,
                    ha=ha,
                    rotation=rotation,
                    fontsize=self.bar_label_size,
                    va=va,
                )

    def anim_func(self, i):
        for bar in self.ax.containers:
            bar.remove()
        self.plot_bars(i)

    def init_func(self):
        self.plot_bars(0)

    def get_frames(self):
        return range(len(self.df_values))

    def make_animation(self):
        
        anim = super().make_animation(self.get_frames(), self.init_func)

        if self.html:
            return anim.to_html5_video()

        extension = self.filename.split(".")[-1]
        if extension == "gif":
            anim.save(self.filename, fps=self.fps, writer="imagemagick")
        else:
            anim.save(self.filename, fps=self.fps)


def line_chart_race(
    series,
    filename,
    line_width,
    use_index,
    steps_per_period,
    period_length,
    title,
    figsize,
    tick_label_size,
    bar_label_size,
    period_label_size,
    fig,
    **kwargs,
):
    return _LineChartRace(
        series,
        filename,
        line_width,
        use_index,
        steps_per_period,
        period_length,
        title,
        figsize,
        144,
        tick_label_size,
        bar_label_size,
        period_label_size,
        fig,
        kwargs,
    )


def bar_chart_race(
    df,
    filename=None,
    orientation="h",
    sort="desc",
    n_bars=None,
    label_bars=True,
    use_index=True,
    steps_per_period=10,
    period_length=500,
    figsize=(6.5, 3.5),
    cmap="dark24",
    title=None,
    bar_label_size=7,
    tick_label_size=7,
    period_label_size=16,
    fig=None,
    **kwargs,
):
    """
    Create an animated bar chart race using matplotlib. Data must be in 'wide' format where each
    row represents a single time period and each column represents a distinct category. 
    Optionally, the index can label the time period.

    Bar height and location change linearly from one time period to the next.

    This is resource intensive - Start with just a few rows of data

    Parameters
    ----------
    df : pandas DataFrame
        Must be 'wide' where each row represents a single period of time. Each column contains
        the values of the bars for that category. Optionally, use the index to label each time period.

    filename : `None` or str, default None
        If `None` return animation as HTML5.
        If a string, save animation to that filename location. Use .mp4 or .gif extensions

    orientation : 'h' or 'v', default 'h'
        Bar orientation - horizontal or vertical

    sort : 'desc' or 'asc', default 'desc'
        Choose how to sort the bars. Use 'desc' to put largest bars on top and 'asc' to place largest
        bars on bottom.

    n_bars : int, default None
        Choose the maximum number of bars to display on the graph. By default, use all bars. 
        New bars entering the race will appear from the bottom or top.
    
    label_bars : bool, default `True`
        Whether to label the bars with their value on their right

    use_index : bool, default `True`
        Whether to use the index as the text in the plot

    steps_per_period : int, default 10
        The number of steps to go from one time period to the next. 
        The bar will grow linearly between each period.

    period_length : int, default 500
        Number of milliseconds to animate each period (row). Default is 500ms (half of a second)

    figsize : two-item tuple of numbers, default (6.5, 3.5)
        matplotlib figure size in inches. Will be overridden if own figure supplied to `fig`

    cmap : str, matplotlib colormap instance, or list of colors, default 'dark24'
        Colors to be used for the bars. Colors will repeat if there are more bars
        than colors.

    title : str, default None
        Title of plot

    bar_label_size : int, float, default 7
        Size in points of numeric labels just outside of the bars

    tick_label_size : int, float, default 7
        Size in points of tick labels

    period_label_size : int, float, default 16
        Size in points of label plotted with the axes that labels the period.

    fig : matplotlib Figure, default None
        For greater control over the aesthetics, supply your own figure with a single axes.

    **kwargs : key, value pairs
        Other keyword arguments passed to the matplotlib barh/bar function.


    Returns
    -------
    Either HTML5 video or creates an mp4/gif file of the animation and returns `None`

    Notes
    -----
    Default DPI of 144

    It is possible for some bars to be out of order momentarily during a transition since
    both height and location change linearly.

    Examples
    --------
    Use the `load_data` function to get an example dataset to create an animation.

    df = bcr.load_data('covid19')
    bcr.bar_chart_race(
        df=df,
        filename='covid19_horiz_desc.mp4',
        orientation='h',
        sort='desc',
        label_bars=True,
        use_index=True,
        steps_per_period=10,
        period_length=500,
        cmap='dark24',
        title='COVID-19 Deaths by Country',
        bar_label_size=7,
        tick_label_size=7,
        period_label_size=16,
        fig=None)
    """
    return _BarChartRace(
        df,
        filename,
        orientation,
        sort,
        n_bars,
        label_bars,
        use_index,
        steps_per_period,
        period_length,
        figsize,
        cmap,
        title,
        bar_label_size,
        tick_label_size,
        period_label_size,
        fig,
        kwargs,
    )

    # return bcr.make_animation()


def load_dataset(name="covid19"):
    """
    Return a pandas DataFrame suitable for immediate use in `bar_chart_race`

    Parameters
    ----------
    name : str, default 'covid19'
        Name of dataset to load. Either 'covid19' or 'urban_pop'

    Returns
    -------
    pandas DataFrame
    """
    return pd.read_csv(
        f"https://raw.githubusercontent.com/dexplo/bar_chart_race/master/data/{name}.csv",
        index_col="date",
        parse_dates=["date"],
    )

def animate_multiple_plots(filename: str,plots: List[Union[_BarChartRace,_LineChartRace]]):
    """ Plot multiple animated plots

    Args:
        plots (List[Union[_BarChartRace,_LineChartRace]]): List of plots to animate
    """

    def update_all_graphs(frame):
        for plot in plots:
            plot.anim_func(frame)

    fig, axes = plt.subplots(len(plots))
    for num, plot in enumerate(plots):
        plot.ax = axes[num]
        
        plot.init_func()

    interval = plots[0].period_length / plots[0].steps_per_period
    anim = FuncAnimation(
            fig,
            update_all_graphs,
            min([max(plot.get_frames()) for plot in plots]),
            # plots[0].get_frames(),
            # init_func,
            interval=interval,
        )

    extension = filename.split(".")[-1]
    if extension == "gif":
        anim.save(filename, fps=plots[0].fps, writer="imagemagick")
    else:
        anim.save(filename, fps=plots[0].fps)
