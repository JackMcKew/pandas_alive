# TODO add check if interpolate period true, must be datetime index

import datetime
import typing

import attr
from matplotlib import ticker
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Colormap, to_rgba
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.units as munits
import numpy as np
import pandas as pd

# For conciseDateFormatter for all plots https://matplotlib.org/3.1.0/gallery/ticks_and_spines/date_concise_formatter.html
converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[datetime.date] = converter
munits.registry[datetime.datetime] = converter


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


@attr.s()
class _BaseChart:
    # Refactored BaseChart
    df: pd.DataFrame = attr.ib()
    interpolate_period: bool = attr.ib()
    steps_per_period: int = attr.ib()
    period_length: int = attr.ib()
    period_fmt: str = attr.ib()
    figsize: typing.Tuple[float, float] = attr.ib()
    title: str = attr.ib()
    fig: plt.Figure = attr.ib()
    cmap: typing.Union[str, Colormap, typing.List[str]] = attr.ib()
    # n_visible: int = attr.ib()
    tick_label_size: typing.Union[int, float] = attr.ib()
    period_label: typing.Union[
        bool, typing.Dict[str, typing.Union[int, float, str]]
    ] = attr.ib()
    period_summary_func: typing.Callable = attr.ib()
    fixed_max: bool = attr.ib()
    # append_period_to_title: bool = attr.ib()
    # x_period_annotation_location: typing.Union[int, float] = attr.ib()
    # y_period_annotation_location: typing.Union[int, float] = attr.ib()
    # period_annotation_size: typing.Union[int, float] = attr.ib()
    # show_period_annotation: bool = attr.ib()
    # enable_legend: bool = attr.ib()
    # period_annotation_formatter: str = attr.ib()
    dpi: float = attr.ib()
    kwargs = attr.ib()

    def __attrs_post_init__(self):
        if isinstance(self.df, pd.Series):
            self.df = pd.DataFrame(self.df)
        from matplotlib import rcParams

        rcParams.update({"figure.autolayout": True})

        if self.interpolate_period == True and not isinstance(
            self.df.index, pd.DatetimeIndex
        ):
            raise ValueError(
                f"If using interpolate_period, ensure the index is a DatetimeIndex (eg, use df.index = pd.to_datetime(df.index))"
            )
        # rcParams.update({'figure.autolayout': True})
        self.orig_df = self.df.copy()
        self.colors = self.get_colors(self.cmap)  # Get colors for plotting
        if not isinstance(self.df.columns,pd.MultiIndex):
            self.data_cols = self.get_data_cols(self.df)  # Get column names with valid data
            self.df = self.rename_data_columns(
                self.df
            )  # Force data column names to be string
        else:
            self.data_cols = self.df.columns.get_level_values(level=0).unique().tolist()

        # Careful to use self.df in later calculations (eg, df_rank), use orig_df if needed
        self.df = self.get_interpolated_df(
            self.df, self.steps_per_period, self.interpolate_period
        )
        if self.fig is None:
            self.fig, self.ax = self.create_figure()
            self.figsize = self.fig.get_size_inches()
        else:
            self.fig = plt.figure()
            self.ax = plt.axes()
        self.fig.set_tight_layout(False)
        if self.title:
            self.ax.set_title(self.title)

        print(f"Generating {self.__class__.__name__}, plotting {self.data_cols}")

    def validate_params(self):
        """ Validate figure is a matplotlib Figure instance

        Args:
            attribute ([type]): Unused as required by attrs decorator
            value (plt.figure): Figure instance for chart

        Raises:
            TypeError: Figure provided is not matplotlib figure
        """
        if self.fig is not None and not isinstance(self.fig, plt.Figure):
            raise TypeError("`fig` must be a matplotlib Figure instance")

    def get_period_label(
        self,
        period_label: typing.Union[
            bool, typing.Dict[str, typing.Union[int, float, str]]
        ],
    ) -> typing.Union[bool, typing.Dict[str, typing.Union[int, float, str]]]:
        """ Parameters for period annotation on charts, dict will be passed to kwargs in matplotlib.ax.text()

        Args:
            period_label (typing.Union[bool,typing.Dict[str,typing.Union[int,float,str]]]): If `True` or dict, use the index as the text label

        Raises:
            ValueError: `x` and `y` must be supplied as a minimum

        Returns:
            typing.Union[bool,typing.Dict[str,typing.Union[int,float,str]]]: Returns `True` or dict will be passed to kwargs in matplotlib.ax.text()
        """
        if not period_label:
            return False
        elif period_label is True:
            # Default to bottom right corner
            period_label = {"size": 12, "x": 0.9, "y": 0.1, "ha": "right"}
        else:
            if "x" not in period_label or "y" not in period_label:
                raise ValueError(
                    '`period_label` dictionary must have keys for "x" and "y"'
                )
        return period_label

    def get_colors(
        self, cmap: typing.Union[Colormap, str, typing.List[str]]
    ) -> typing.List[str]:
        """ Get colours for plotting data

        Args:
            cmap (typing.Union[colors.Colormap,str]): Provide string of colormap name, colormap instance, single color instance or list of colors as supported by https://matplotlib.org/2.0.2/api/colors_api.html

        Raises:
            ValueError: If no supported colors are found
            TypeError: Type of colors is not supported

        Returns:
            typing.List[str]: Returns list of RGB values for colors as strings
        """
        if isinstance(cmap, str):
            try:
                cmap = DARK24 if cmap == "dark24" else plt.cm.get_cmap(cmap)
            except ValueError:
                # Try setting a list of repeating colours if no cmap found (for single colours)
                cmap = [to_rgba(cmap)] * len(self.get_data_cols(self.df))
            except:
                raise ValueError(
                    "Provide a suitable color name or color map as per matplotlib"
                )
        if isinstance(cmap, Colormap):
            chart_colors = cmap(range(cmap.N)).tolist()
        elif isinstance(cmap, list):
            chart_colors = cmap
        elif hasattr(cmap, "tolist"):
            chart_colors = cmap.tolist()
        else:
            raise TypeError(
                "`cmap` must be a string name of a color, colormap, list of colors or a matplotlib colormap instance"
                "or a list of colors"
            )

        return chart_colors

    def set_x_y_limits(self, df: pd.DataFrame, i: int, ax):
        # TODO fix max for x and y?
        if self.fixed_max:
            xlim_start = self.df.index.min()
            # For avoiding UserWarning on first frame with identical start and end limits
            xlim_end = self.df.index.max() + pd.Timedelta(seconds=1)
        else:
            xlim_start = self.df.index[: i + 1].min()
            # For avoiding UserWarning on first frame with identical start and end limits
            xlim_end = self.df.index[: i + 1].max() + pd.Timedelta(seconds=1)
        ax.set_xlim(xlim_start, xlim_end)
        # self.ax.set_xlim(self.df.index[: i + 1].min(), self.df.index[: i + 1].max())
        if self.fixed_max:
            ax.set_ylim(
                self.df.min().min(skipna=True), self.df.max().max(skipna=True),
            )
        else:
            ax.set_ylim(
                self.df.iloc[: i + 1]
                .select_dtypes(include=[np.number])
                .min()
                .min(skipna=True),
                self.df.iloc[: i + 1]
                .select_dtypes(include=[np.number])
                .max()
                .max(skipna=True),
            )

    def rename_data_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        # data_cols = self.get_data_cols(df)
        df.columns = df.columns.astype(str)
        return df

    def get_data_cols(self, df: pd.DataFrame) -> typing.List[str]:
        """ Get list of columns containing plottable numeric data to plot

        Raises:
            Exception: If column name is missing or changed during calculation
            Exception: If no numeric data was found to be plotted

        Returns:
            typing.List[str]: List of column names containing numeric data
        """
        data_cols = []
        for i, col in enumerate(df.columns):
            if col not in df.columns:
                raise Exception(
                    "Could not find '%s' in the columns of the provided DataFrame/Series. Please provide for the <y> parameter either a column name of the DataFrame/Series or an array of the same length."
                    % col
                )
            if np.issubdtype(df[col].dtype, np.number):
                data_cols.append(col)
        if not data_cols:
            raise Exception("No numeric data columns found for plotting.")

        data_cols = [str(col) for col in data_cols]

        return data_cols

    def get_interpolated_df(
        self, df: pd.DataFrame, steps_per_period: int, interpolate_period: bool
    ) -> pd.DataFrame:
        """ Get interpolated dataframe to span total animation

        Args:
            df (pd.DataFrame): Input dataframe
            steps_per_period (int): The number of steps to go from one period to the next. Data will show linearly between each period
            interpolate_period (bool): Whether to interpolate the period, must be datetime index

        Returns:
            pd.DataFrame: Interpolated dataframe
        """

        # Period interpolated to match other charts for multiple plotting
        # https://stackoverflow.com/questions/52701330/pandas-reindex-and-interpolate-time-series-efficiently-reindex-drops-data

        interpolated_df = df.reset_index()
        interpolated_df.index = interpolated_df.index * steps_per_period
        new_index = range(interpolated_df.index[-1] + 1)
        interpolated_df = interpolated_df.reindex(new_index)
        if interpolate_period:
            if interpolated_df.iloc[:, 0].dtype.kind == "M":
                first, last = interpolated_df.iloc[[0, -1], 0]
                dr = pd.date_range(first, last, periods=len(interpolated_df.index))
                interpolated_df.iloc[:, 0] = dr
            else:
                interpolated_df.iloc[:, 0] = interpolated_df.iloc[:, 0].interpolate()
        else:
            interpolated_df.iloc[:, 0] = interpolated_df.iloc[:, 0].fillna(
                method="ffill"
            )

        interpolated_df = interpolated_df.set_index(interpolated_df.columns[0])

        if interpolate_period:
            interpolated_df = interpolated_df.interpolate(method="time")
        else:
            interpolated_df = interpolated_df.interpolate()

        return interpolated_df

    def init_func(self) -> None:
        """ Initializing method for animation, to be overridden by extended classes

        Raises:
            NotImplementedError: Method to be overridden has not been implemented
        """
        raise NotImplementedError("Initializing method not yet implemented")

    def anim_func(self, frame: int) -> None:
        """ Animation method, to be overridden by extended chart class

        Args:
            frame (int): Frame to be animated

        Raises:
            NotImplementedError: Animation method not yet implemented in extended chart class
        """
        raise NotImplementedError("Animation method not yet implemented")

    def get_frames(self) -> typing.Iterable:
        """ Method for determining how many frames to animate

        Returns:
            int: Number of frames to animate
        """
        return range(len(self.df.index))

    def make_animation(
        self, frames: typing.Union[typing.Iterable, int], init_func: typing.Callable
    ) -> FuncAnimation:
        """ Method for creating animation

        Args:
            frames (int): Number of frames to animate
            init_func (function): Initialization function for chart

        Returns:
            FuncAnimation: FuncAnimation instance for extending with save, etc
        """

        interval = self.period_length / self.steps_per_period
        return FuncAnimation(
            self.fig, self.anim_func, frames, init_func, interval=interval
        )

    def calculate_new_figsize(self, real_fig: plt.figure) -> typing.List[float]:
        """ Calculate figure size to allow for labels, etc

        Args:
            real_fig (plt.figure): Figure before calculation

        Returns:
            typing.List[float]: The dimensions [left, bottom, width, height] of the new axes. All quantities are in fractions of figure width and height.
        """
        import io

        fig = plt.Figure(figsize=self.figsize)

        ax = fig.add_subplot()

        max_val = self.df.values.max().max()
        ax.tick_params(labelrotation=0, axis="y", labelsize=self.tick_label_size)

        fig.canvas.print_figure(io.BytesIO())
        orig_pos = ax.get_position()
        ax.set_yticklabels(self.df.columns)
        ax.set_xticklabels([max_val] * len(ax.get_xticks()))

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

    def apply_style(self, ax):
        ax.grid(True, axis="x", color="white")
        ax.set_axisbelow(True)
        ax.tick_params(length=0, labelsize=self.tick_label_size, pad=2)
        ax.set_facecolor(".9")
        for spine in ax.spines.values():
            spine.set_visible(False)
        return ax

    def create_figure(self) -> typing.Tuple[plt.figure, plt.axes]:
        """ Create base figure with styling, can be overridden if styling unwanted

        Returns:
            typing.Tuple[plt.figure,plt.figure.axes]: Returns Figure instance and the axes initialized within
        """

        fig = plt.Figure(figsize=self.figsize, dpi=self.dpi)
        # limit = (0.2, self.n_bars + 0.8)
        rect = self.calculate_new_figsize(fig)
        ax = fig.add_axes(rect)

        ax = self.apply_style(ax)
        
        return fig, ax

    def show_period(self, i: int) -> None:
        if self.period_label:
            if self.period_fmt:
                idx_val = self.df.index[i]
                if self.df.index.dtype.kind == "M":  # Date time
                    s = idx_val.strftime(self.period_fmt)
                else:
                    s = self.period_fmt.format(x=idx_val)
            else:
                s = self.df.index.astype(str)[i]
            num_texts = len(self.ax.texts)
            if num_texts == 0:
                # first frame
                self.ax.text(
                    s=s,
                    transform=self.ax.transAxes,
                    **self.get_period_label(self.period_label),
                )
            else:
                self.ax.texts[0].set_text(s)

        if self.period_summary_func:
            values = self.df.iloc[i]
            text_dict = self.period_summary_func(values)
            if "x" not in text_dict or "y" not in text_dict or "s" not in text_dict:
                name = self.period_summary_func.__name__
                raise ValueError(
                    f"The dictionary returned from `{name}` must contain "
                    '"x", "y", and "s"'
                )
            if len(self.ax.texts) != 2:
                self.ax.text(transform=self.ax.transAxes, **text_dict)
            else:
                self.ax.texts[1].set_text(text_dict["s"])

    def save(self, filename: str) -> None:
        """ Save method for FuncAnimation

        Args:
            filename (str): File name with extension to save animation to, supported formats at https://matplotlib.org/3.1.1/api/animation_api.html
        """

        # Inspiration for design pattern https://github.com/altair-viz/altair/blob/c55707730935159e4e2d2c789a6dd2bc3f1ec0f2/altair/utils/save.py
        # https://altair-viz.github.io/user_guide/saving_charts.html

        anim = self.make_animation(self.get_frames(), self.init_func)
        self.fps = 1000 / self.period_length * self.steps_per_period

        extension = filename.split(".")[-1]
        try:
            if extension == "gif":
                anim.save(filename, fps=self.fps, dpi=self.dpi, writer="imagemagick")
            else:
                anim.save(filename, fps=self.fps, dpi=self.dpi)
        except:
            raise RuntimeError("Ensure that a matplotlib writer library is installed, see https://github.com/JackMcKew/pandas_alive/blob/master/README.md#requirements for more details")

    def get_html5_video(self):
        """ Convert the animation to an HTML5 <video> tag.

        This saves the animation as an h264 video, encoded in base64 directly into the HTML5 video tag. This respects the rc parameters for the writer as well as the bitrate. This also makes use of the interval to control the speed, and uses the repeat parameter to decide whether to loop.

        Returns:
            HTML5 <video> tag: Encoded h264 video
        """

        anim = self.make_animation(self.get_frames(), self.init_func)
        return anim.to_html5_video()

    # Possibly include image background method?
    # def show_image(
    #     self,
    #     ax,
    #     path_to_image: str,
    #     extent: typing.Tuple[float],
    #     zorder: int = 0,
    #     aspect: str = "equal",
    # ):
    #     image = plt.imread(path_to_image)

    #     ax.imshow(image, zorder=zorder, extent=extent, aspect=aspect)

    #     return ax
