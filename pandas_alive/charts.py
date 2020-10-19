""" Implementations of support chart types

This module contains functions for chart types.

"""

import datetime
import typing
from typing import Mapping

import attr
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.units as munits
import numpy as np
import pandas as pd
from matplotlib import colors, ticker, transforms
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Colormap

from ._base_chart import _BaseChart

# For conciseDateFormatter for all plots https://matplotlib.org/3.1.0/gallery/ticks_and_spines/date_concise_formatter.html
converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[datetime.date] = converter
munits.registry[datetime.datetime] = converter


@attr.s()
class BarChartRace(_BaseChart):
    """ BarChart implementation for bar chart races

    Args:
        BaseChart (BaseChart): Base class shared by all chart types

    Returns:
        BarChart: Instance of BarChart allowing for inclusion in subplot charts or animating with .save()
    """

    orientation: str = attr.ib()
    sort: str = attr.ib()
    label_bars: bool = attr.ib()
    bar_label_size: typing.Union[int, float] = attr.ib()
    n_visible: int = attr.ib()
    fixed_order: typing.Union[list, bool] = attr.ib()

    perpendicular_bar_func: typing.Callable = attr.ib()

    def __attrs_post_init__(self):
        """ Properties to be determined after initialization
        """
        self.n_visible = self.n_visible if self.n_visible else self.df.shape[1]

        if self.fixed_order is True:
            last_values = self.df.iloc[-1].sort_values(ascending=False)
            cols = last_values.iloc[: self.n_visible].index
            self.df = self.df[cols]
        elif isinstance(self.fixed_order, list):
            cols = self.fixed_order
            self.df = self.df[cols]

        super().__attrs_post_init__()

        if self.n_visible > 15:
            import warnings

            warnings.warn(
                "Plotting too many bars may result in undesirable output, use `n_visible=15` to limit number of bars"
            )

        self.validate_params()

        self.df_rank = self.calculate_ranks(self.orig_df)

        if self.fixed_order:

            n = self.df.shape[1] + 1
            m = self.df.shape[0]
            rank_row = np.arange(1, n)
            if (self.sort == "desc" and self.orientation == "h") or (
                self.sort == "asc" and self.orientation == "v"
            ):
                rank_row = rank_row[::-1]

            ranks_arr = np.repeat(rank_row.reshape(1, -1), m, axis=0)
            self.df_rank = pd.DataFrame(data=ranks_arr, columns=cols)

        self.orig_index = self.df.index.astype("str")

        self.bar_colors = self.get_colors(self.cmap)

        self.ax.tick_params(labelsize=self.tick_label_size)

    def validate_params(self):
        """ Validate parameters provided to chart instance

        Raises:
            ValueError: If sort value is not provided (either 'asc' or 'desc')
            ValueError: Orientation must be 'h' (horizontal) or 'v' (vertical)
        """
        super().validate_params()

        if self.sort not in ("asc", "desc"):
            raise ValueError('`sort` must be "asc" or "desc"')

        if self.orientation not in ("h", "v"):
            raise ValueError('`orientation` must be "h" or "v"')

    def get_colors(
        self, cmap: typing.Union[str, Colormap, typing.List[str]]
    ) -> np.array:
        """ Get array of colours from BaseChart.get_colors and shorten to number of bars

        Args:
            cmap (typing.Union[str, colors.Colormap, typing.List[str]]): Provide string of colormap name, colormap instance, single color instance or list of colors as supported by https://matplotlib.org/2.0.2/api/colors_api.html

        Returns:
            np.array: Numpy Array of colors as strings
        """
        bar_colors = super().get_colors(cmap)

        # bar_colors is now a list
        n = len(bar_colors)
        if self.df.shape[1] > n:
            bar_colors = bar_colors * (self.df.shape[1] // n + 1)
        return np.array(bar_colors[: self.df.shape[1]])

    def get_label_position(self) -> typing.Tuple[float, float]:
        """ Get label position for period annotation

        Returns:
            typing.Tuple[float,float]: x,y of label
        """
        if self.orientation == "h":
            x_label = 0.6
            y_label = 0.25 if self.sort == "desc" else 0.8
        else:
            x_label = 0.7 if self.sort == "desc" else 0.1
            y_label = 0.8
        return x_label, y_label

    def calculate_ranks(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Calculate expanded dataframe to match length of animation

        Returns:
            typing.Tuple[pd.DataFrame,pd.DataFrame]: df_values contains interpolated values, df_rank contains interpolated rank
        """

        df_rank = df.rank(axis=1, method="first", ascending=False).clip(
            upper=self.n_visible + 1
        )
        if (self.sort == "desc" and self.orientation == "h") or (
            self.sort == "asc" and self.orientation == "v"
        ):
            # This flips all rankings, eg if n_visible = 5 then score 1 in table becomes (6-1 = 5)
            df_rank = self.n_visible + 1 - df_rank

        df_rank = self.get_interpolated_df(
            df_rank, self.steps_per_period, self.interpolate_period
        )
        # new_index = range(df.index.max() + 1)
        # df_rank = df_rank.reindex(new_index).interpolate()
        return df_rank

    def create_figure(self) -> typing.Tuple[plt.figure, plt.axes]:
        """ Create Bar chart figure

        Returns:
            typing.Tuple[plt.figure,plt.axes]: Figure & axes instance
        """
        fig = plt.Figure(figsize=self.figsize, dpi=self.dpi)
        limit = (0.2, self.n_visible + 0.8)
        rect = self.calculate_new_figsize(fig)
        ax = fig.add_axes(rect)
        if self.orientation == "h":
            ax.set_ylim(limit)
            if self.fixed_max:
                ax.set_xlim(0, self.df.values.max().max() * 1.05 * 1.11)
            ax.grid(True, axis="x", color="white")
            ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
        else:
            ax.set_xlim(limit)
            if self.fixed_max:
                ax.set_ylim(0, self.df.values.max().max() * 1.05 * 1.11)
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

    def calculate_new_figsize(self, real_fig: plt.figure) -> typing.List[float]:
        """ Calculate figure size to allow for labels, etc

        Args:
            real_fig (plt.figure): Figure before calculation

        Returns:
            typing.List[float]: The dimensions [left, bottom, width, height] of the new axes. All quantities are in fractions of figure width and height.
        """
        import io

        # df_values = self.prepare_data()
        fig = plt.Figure(figsize=self.figsize)
        # if self.title:
        # fig.tight_layout(rect=[0, 0, 1, 0.9])  # To include title
        ax = fig.add_subplot()
        fake_cols = [chr(i + 70) for i in range(self.df.shape[1])]

        max_val = self.df.max().max()
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

    def plot_bars(self, i: int) -> None:
        """ Plot bars in bar chart race on axes

        Args:
            i (int): index of current frame in animation
        """
        bar_location = self.df_rank.iloc[i].values

        bar_location[np.isnan(bar_location)] = 0

        top_filt = (bar_location > 0) & (bar_location < self.n_visible + 1)
        bar_location = bar_location[top_filt]

        bar_length = self.df.iloc[i].values[top_filt]
        cols = self.df.columns[top_filt]
        colors = self.bar_colors[top_filt]

        if self.orientation == "h":
            self.ax.barh(
                bar_location,
                bar_length,
                ec="white",
                tick_label=cols,
                color=colors,
                # **self.kwargs,
            )
            if not self.fixed_max:
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
            if not self.fixed_max:
                self.ax.set_ylim(self.ax.get_ylim()[0], bar_length.max() * 1.16)

        super().show_period(i)

        if self.label_bars:
            for text in self.ax.texts[int(bool(self.period_label)) :]:
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

        if self.perpendicular_bar_func:
            if isinstance(self.perpendicular_bar_func, str):
                val = pd.Series(bar_length).agg(self.perpendicular_bar_func)
            else:
                values = self.df.iloc[i]
                ranks = self.df_rank.iloc[i]
                val = self.perpendicular_bar_func(values, ranks)

            if not self.ax.lines:
                if self.orientation == "h":
                    self.ax.axvline(val, lw=8, color=".5", zorder=0.5)
                else:
                    self.ax.axhline(val, lw=8, color=".5", zorder=0.5)
            else:
                line = self.ax.lines[0]
                if self.orientation == "h":
                    line.set_xdata([val] * 2)
                else:
                    line.set_ydata([val] * 2)

    def anim_func(self, i: int) -> None:
        """ Animation function, removes all bars and updates legend/period annotation.

        Args:
            i (int): Frame index for animation
        """
        if self.enable_progress_bar:
            self.update_progress_bar()
        for bar in self.ax.containers:
            bar.remove()
        self.plot_bars(i)
        self.show_period(i)

    def init_func(self):
        """ Initialization function for animation
        """
        self.plot_bars(0)


@attr.s
class ScatterChart(_BaseChart):
    """
    ScatterChart to be generate animated plot with `matplotlib.pyplot.axes.scatter`

    Accepts kwargs as detailed on https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.scatter.html

    Args:
        _BaseChart : BaseChart constructor that all charts share

    Raises:
        ValueError: Size label must be a column in DataFrame
    """

    size: typing.Union[int, str] = attr.ib()
    add_legend: bool = attr.ib()

    def __attrs_post_init__(self):
        """ Properties to be determined after initialization
        """
        super().__attrs_post_init__()
        self.colors = self.get_colors(self.cmap)
        self._points: typing.Dict = {}
        for name in self.data_cols:
            self._points[name] = {}
            self._points[name]["x"] = []
            self._points[name]["y"] = []
            self._points[name]["size"] = []
        if isinstance(self.size, str) and self.size not in self.data_cols:
            raise ValueError(
                f"Size provided as string: {self.size}, not present in dataframe columns"
            )

    def plot_point(self, i: int) -> None:
        """
        Plot points for scatter on chart


        Args:
            i (int): Frame to be plotted, will take slice of DataFrame at this index

        Raises:
            ValueError: Size label must be a column in DataFrame
        """
        if not self.fixed_max:
            super().set_x_y_limits(self.df, i, self.ax)
        # If fixed_max is true then run it once to improve performance
        elif i==0:
            super().set_x_y_limits(self.df, i, self.ax)
        j = 0
        for name, color in zip(self.data_cols, self.colors):
            self._points[name]["x"] = self.df[name].index[:i+1]
            self._points[name]["y"] = self.df[name].iloc[:i+1]
            if isinstance(self.size, str) and self.size in self.data_cols:
                self._points[name]["size"] = abs(self.df[self.size].iloc[:i+1])
            else:
                self._points[name]["size"] = np.full((i+1), self.size)
            if i==0:
                self.sc = self.ax.scatter(
                    self._points[name]["x"],
                    self._points[name]["y"],
                    s=self._points[name]["size"],
                    color=color,
                    label=name,
                    edgecolors='none',
                    **self.kwargs,
                )
                if self.add_legend:
                    handles, labels = self.ax.get_legend_handles_labels()
                    legend = self.ax.legend(handles[:], labels[:], fontsize="x-small")
                    for handle in legend.legendHandles:
                        handle.set_sizes([15])
            else:
                # update all points
                self.ax.collections[j].set_color(color)
                if isinstance(self.df.index, pd.DatetimeIndex):
                    # date_array = np.c_[mdates.date2num(self._points[name]["x"]), self._points[name]["y"]]
                    self.ax.collections[j].set_offsets(np.c_[mdates.date2num(self._points[name]["x"]), self._points[name]["y"]])
                else:
                    self.ax.collections[j].set_offsets(np.c_[self._points[name]["x"], self._points[name]["y"]])
                self.ax.collections[j].set_sizes(self._points[name]["size"])
            j += 1
            

    def anim_func(self, i: int) -> None:
        """ Animation function, plots all scatter points and updates legend/period annotation.

        Args:
            i (int): Index of frame of animation
        """
        if self.enable_progress_bar:
            self.update_progress_bar()
        if self.period_fmt:
            self.show_period(i)
        self.plot_point(i)

    def init_func(self) -> None:
        """ Initialization function for animation
        """
        self.ax.scatter([], [])


@attr.s
class LineChart(_BaseChart):
    """ Animated Line Chart implementation

    Args:
        BaseChart (BaseChart): Shared Base Chart class inherit to all charts

    Returns:
        LineChart: Animated Line Chart class for use with multiple plots or save
    """

    line_width: int = attr.ib()
    label_events: typing.Dict[str, str] = attr.ib()
    fill_under_line_color: str = attr.ib()
    add_legend: bool = attr.ib()

    def __attrs_post_init__(self):
        """ Properties to be determined after initialization
        """
        super().__attrs_post_init__()
        self.line_colors = self.get_colors(self.cmap)
        self._lines: typing.Dict = {}
        for name in self.data_cols:
            self._lines[name] = {}
            self._lines[name]["x"] = []
            self._lines[name]["y"] = []

    def plot_line(self, i: int) -> None:
        """ Function for plotting all lines in dataframe

        Args:
            i (int): Index of frame for animation
        """
        # TODO Somehow implement n visible lines?
        if not self.fixed_max:
            super().set_x_y_limits(self.df, i, self.ax)
        # If fixed_max is true then run it once to improve performance
        elif i==0:
            super().set_x_y_limits(self.df, i, self.ax)
        j = 0
        # fills = [""]
        for name, color in zip(self.data_cols, self.line_colors):
            self._lines[name]["x"] = self.df[name].index[:i+1]
            self._lines[name]["y"] = self.df[name].iloc[:i+1]
            if i==0:
                self.ax.plot(
                    self._lines[name]["x"],
                    self._lines[name]["y"],
                    self.line_width,
                    color=color,
                    label=name,
                    **self.kwargs,
                    )
                if self.add_legend:
                    handles, labels = self.ax.get_legend_handles_labels()
                    self.ax.legend(handles[::2], labels[::2], fontsize="x-small")
                # if self.fill_under_line_color:
                #     self.ax.fill_between(
                #         self._lines[name]["x"],
                #         self._lines[name]["y"],
                #         color=self.get_single_color(self.fill_under_line_color),
                #         alpha=0.5,
                #     )
                #     fills = self.ax.collections[-1]
            else:
                # update all lines
                self.ax.lines[j].set_color(color)
                self.ax.lines[j].set_data(self._lines[name]["x"], self._lines[name]["y"])
            j += 1
            if self.fill_under_line_color:
                # Fills need to be removed and re-generated, or else `matplotlib` 
                # adds a new one per frame, performance degrades and alpha doesn't show properly.
                if i == 0:
                    self.ax.fill_between(
                        self._lines[name]["x"],
                        self._lines[name]["y"],
                        color=self.get_single_color(self.fill_under_line_color),
                        alpha=0.5,
                    )
                    self.fills = self.ax.collections[-1]
                else:
                    self.fills.remove()
                    self.ax.fill_between(
                        self._lines[name]["x"],
                        self._lines[name]["y"],
                        color=self.get_single_color(self.fill_under_line_color),
                        alpha=0.5,
                    )
                    self.fills = self.ax.collections[-1]

        # Set label_events once, it improves loop performance by x 4.
        if self.label_events and i==0:
            # from datetime import datetime
            # import numpy as np

            for pos, (label, date) in enumerate(self.label_events.items()):
                event_index = (self.df.index <= date).sum()
                # if i >= event_index:
                event_start = self.df.index[event_index]
                trans = transforms.blended_transform_factory(
                    self.ax.transData, self.ax.transAxes
                )

                self.ax.axvline(event_start, lw=8, color=".5", zorder=0.5)
                self.ax.text(
                    event_start, 0.9 - (pos * 0.1), label, transform=trans, fontsize="x-small"
                )
        

    def anim_func(self, i: int) -> None:
        """ Animation function, updates all lines and legend/period annotation.

        Args:
            i (int): Index of frame of animation
        """
        if self.enable_progress_bar:
            self.update_progress_bar()
        if self.period_fmt:
            self.show_period(i)
        self.plot_line(i)

    def init_func(self) -> None:
        """ Initialization function for animation
        """
        self.ax.plot([], [])


@attr.s
class PieChart(_BaseChart):
    """ Animated Pie Chart implementation

    Args:
        BaseChart (BaseChart): Shared Base Chart class inherit to all charts

    Returns:
        PieChart: Animated Pie Chart class for use with multiple plots or save
    """

    def __attrs_post_init__(self):
        """ Properties to be determined after initialization
        """
        super().__attrs_post_init__()
        self.wedge_colors = self.get_colors(self.cmap)

        self.wedge_colors = dict(zip(self.data_cols, self.wedge_colors))

        self._wedges: typing.Dict = {}
        for name in self.data_cols:
            self._wedges[name] = {}
            self._wedges[name]["size"] = []

    def plot_wedge(self, i: int) -> None:
        """ Function for plotting all lines in dataframe

        Args:
            i (int): Index of frame for animation
        """

        for text in self.ax.texts[int(bool(self.period_fmt)) :]:
            text.remove()

        # super().set_x_y_limits(self.df, i)
        # print(self.df[self.data_cols].notnull())
        filt_nan = self.df[self.data_cols].iloc[i].notnull()

        # print(self.df[self.data_cols].iloc[i][filt_nan])

        wedges = self.df[self.data_cols].iloc[i][filt_nan]

        wedge_color_list = []
        for label in wedges.index:
            wedge_color_list.append(self.wedge_colors[label])

        self.ax.pie(
            wedges.values, labels=wedges.index, colors=wedge_color_list, **self.kwargs
        )

        # for name, color in zip(self.data_cols, self.wedge_colors):

        #     self._wedges[name]["size"].append(self.df[name].index[i])
        #     # self._lines[name]["y"].append(self.df[name].iloc[i])
        #     self.ax.pie(
        #         self._wedges[name]["size"],
        #         label=name,
        #         color=color,
        #         **self.kwargs,
        #     )

    def anim_func(self, i: int) -> None:
        """ Animation function, removes all wedges and updates legend/period annotation.

        Args:
            i (int): Index of frame of animation
        """
        if self.enable_progress_bar:
            self.update_progress_bar()
        for wedge in self.ax.patches:
            wedge.remove()
        if self.period_fmt:
            self.show_period(i)
        self.plot_wedge(i)

    def init_func(self) -> None:
        """ Initialization function for animation
        """
        self.ax.pie([])


@attr.s
class BarChart(_BaseChart):
    """ Animated Bar Chart implementation

    Args:
        BaseChart (BaseChart): Shared Base Chart class inherit to all charts

    Returns:
        BarChart: Animated Bar Chart class for use with multiple plots or save
    """

    def __attrs_post_init__(self):
        """ Properties to be determined after initialization
        """

        super().__attrs_post_init__()
        self.bar_colors = self.get_colors(self.cmap)

        self._bars: typing.Dict = {}
        for name in self.data_cols:
            self._bars[name] = {}
            self._bars[name]["x"] = []
            self._bars[name]["y"] = []

    def plot_bars(self, i: int) -> None:
        """ Function for plotting all lines in dataframe

        Args:
            i (int): Index of frame for animation
        """
        if not self.fixed_max:
            super().set_x_y_limits(self.df, i, self.ax)
            self.ax.set_ylim(self.df.iloc[: i + 1].values.min(), self.df.iloc[: i + 1].values.max() + 1e-6)
        # If fixed_max is true then run it once to improve performance
        elif i==0:
            super().set_x_y_limits(self.df, i, self.ax)
            # bars are flat at the bottom/top, so no need to apply a tolerance like 
            # with line/scatter charts.
            self.ax.set_ylim(self.df.values.min(), self.df.values.max())

        for name, color in zip(self.data_cols, self.bar_colors):
            self._bars[name]["x"].append(self.df[name].index[i])
            self._bars[name]["y"].append(self.df[name].iloc[i])
            self.ax.bar(
                self._bars[name]["x"],
                self._bars[name]["y"],
                # self.line_width,
                color=color,
                **self.kwargs,
            )

    def anim_func(self, i: int) -> None:
        """ Animation function, removes all bars and updates legend/period annotation.

        Args:
            i (int): Index of frame of animation
        """
        if self.enable_progress_bar:
            self.update_progress_bar()
        for bar in self.ax.containers:
            bar.remove()
        if self.period_fmt:
            self.show_period(i)
        self.plot_bars(i)

    def init_func(self) -> None:
        """ Initialization function for animation
        """
        self.ax.bar([], [])


@attr.s
class BubbleChart(_BaseChart):
    """
    Multivariate Bubble charts from MultiIndex

    Generate animated bubble charts with multivariate data (x,y at a minimum must be supplied)
    Optionally supply data for colour and/or size

    Args:
        _BaseChart ([type]): Base chart for all chart classes

    Raises:
        ValueError: [description]
    """

    x_data_label: str = attr.ib()
    y_data_label: str = attr.ib()
    size_data_label: typing.Union[int, float, str] = attr.ib()
    color_data_label: str = attr.ib()
    vmin: typing.Union[int, float] = attr.ib()
    vmax: typing.Union[int, float] = attr.ib()

    def __attrs_post_init__(self):
        """ Properties to be determined after initialization
        """
        super().__attrs_post_init__()
        self.colors = self.get_colors(self.cmap)
        # Typically bubble plots are fixed scales on X & Y. Having varying 
        # limits will look odd in most cases. So force to True.
        # self.fixed_max = True
        self._points: typing.Dict = {}
        self.column_keys = self.df.columns.get_level_values(level=0).unique().tolist()
        # self.data_cols = self.df.columns.get_level_values(level=1).unique().tolist()
        self.mapping = {"x": self.x_data_label, "y": self.y_data_label}
        if isinstance(self.size_data_label, str):
            self.mapping["size"] = self.size_data_label
        if (
            isinstance(self.color_data_label, str)
            and self.color_data_label in self.column_keys
        ):
            self.mapping["color"] = self.color_data_label
            # setting up colorbar axes & limits when `color` is a pd column
            self.color_bar = True
            if self.cmap == "dark24":  # TODO: register "dark24" as a Colormap
                self.cmap = "jet"
            if self.vmin is None:
                self.vmin = np.floor(self.df[self.mapping["color"]].values.min())
            if self.vmax is None:
                self.vmax = np.ceil(self.df[self.mapping["color"]].values.max())
        else:
            self.color_bar = False
        if self.x_data_label is None or self.y_data_label is None:
            raise ValueError("X Y labels must be provided at a minimum")
        if not (
            self.x_data_label in self.column_keys
            and self.y_data_label in self.column_keys
        ):
            raise ValueError(
                f"Provided keys must be in level 0 multi index, possible values: {self.column_keys}"
            )
        if self.fixed_max:
            # scale to allow canvas to attempt covering for bubble size when near min/max axes values
            ax_xscale = (self.df[self.mapping["x"]].values.max() - self.df[self.mapping["x"]].values.min())*0.05
            ax_yscale = (self.df[self.mapping["y"]].values.max() - self.df[self.mapping["y"]].values.min())*0.05
            BBox = (
                self.df[self.mapping["x"]].values.min() - ax_xscale,
                self.df[self.mapping["x"]].values.max() + ax_xscale,
                self.df[self.mapping["y"]].values.min() - ax_yscale,
                self.df[self.mapping["y"]].values.max() + ax_yscale,
            )
            self.ax.set_xlim(BBox[0], BBox[1])
            self.ax.set_ylim(BBox[2], BBox[3])
    
        
        # TODO Add geopandas for map plots
        # self.ax = self.show_image(
        #     self.ax,
        #     "C:\\Users\\jackm\\Documents\\GitHub\\pandas-alive\\data\\nsw_map.png",
        #     extent=BBox,
        #     zorder=0,
        #     aspect="equal",
        # )

    def plot_point(self, i: int) -> None:
        """
        Plot points from MultiIndexed DataFrame

        Optionally size & colour can be provided and if so, the string provided must be present in the level 0 column labels

        Args:
            i (int): Frame to plot, will slice DataFrame at this index
        """
        for output_key, column_key in self.mapping.items():
            self._points[output_key] = self.df[column_key].iloc[i]
        
        self.sc = self.ax.scatter(
            x=self._points["x"],
            y=self._points["y"],
            s=self._points["size"]
            if isinstance(self.size_data_label, str)
            else self.size_data_label,
            c=self._points["color"]
            if self.color_bar
            else self.color_data_label,
            cmap=self.cmap,
            alpha=0.8,
            **self.kwargs,
        )
        # setting up colorbar when color is a pd column and doesn't exist 
        # already from a previous animation run with the same custom figure.
        if i==0 and self.color_bar:
            self.cbar = self.fig.colorbar(self.sc)
            # this sets colorbar scales & settings to remain constant for all frames
            self.cbar.ax.tick_params(labelsize="small")
            self.cbar.set_label(label="Size & Colour = "+self.color_data_label, fontsize="x-small")
        if self.color_bar:
            # this is required for all iterations to update colour on bubbles
            self.sc.set_clim(self.vmin, self.vmax)


    def anim_func(self, i: int) -> None:
        """ Animation function, removes bubbles and updates legend/period annotation.

        Args:
            i (int): Index of frame of animation
        """
        if self.enable_progress_bar:
            self.update_progress_bar()
        for path in self.ax.collections:
            path.remove()
        if self.period_fmt:
            self.show_period(i)
        self.plot_point(i)

    def init_func(self) -> None:
        """ Initialization function for animation
        """
        self.ax.scatter([], [])
