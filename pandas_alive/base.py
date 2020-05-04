from pandas_alive.charts import BarChart, BaseChart, LineChart
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from typing import List, Union


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


def animate_multiple_plots(
    filename: str,
    plots: List[Union[BarChart, LineChart]],
    title: str = None,
    title_fontsize: Union[int, float] = 16,
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


# def plot_animated_grid(children_plots: List):
#     # TODO Implement multiple animated plots
#     a = 0
