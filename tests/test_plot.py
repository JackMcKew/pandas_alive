import pytest

import pandas_alive


@pytest.fixture(scope="function")
def covid_df():

    # Load Covid Dataset:
    covid_df = pandas_alive.load_dataset()

    return covid_df


def test_barh(covid_df):

    animated_plot = covid_df.plot_animated()

    animated_plot.save("test.mp4")


def test_barv(covid_df):

    animated_plot = covid_df.plot_animated(orientation="v")

    animated_plot.save("test.mp4")


def test_line(covid_df):

    animated_plot = covid_df.diff().fillna(0).plot_animated(kind="line")

    animated_plot.save("test.mp4")


def test_multi(covid_df):

    animated_line_chart = covid_df.diff().fillna(0).plot_animated(kind="line")

    animated_bar_chart = covid_df.plot_animated(kind="barh")

    pandas_alive.animate_multiple_plots(
        "test.mp4", [animated_bar_chart, animated_line_chart]
    )
