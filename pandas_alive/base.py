from pandas_alive.charts import BarChart, LineChart
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


def animate_multiple_plots(filename: str, plots: List[Union[BarChart,LineChart]]):
    """ Plot multiple animated plots

    Args:
        plots (List[Union[_BarChartRace,_LineChartRace]]): List of plots to animate
    """

    def update_all_graphs(frame):
        for plot in plots:
            try:
                plot.anim_func(frame)
            except:
                pass

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



# def plot_animated_grid(children_plots: List):
#     # TODO Implement multiple animated plots
#     a = 0
