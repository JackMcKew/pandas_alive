import pytest

import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ".")


import pandas_alive


@pytest.fixture(scope="function")
def covid_df():

    # Load Covid Dataset:
    covid_df = pandas_alive.load_dataset()

    return covid_df


def test_barh(covid_df):

    animated_plot = covid_df.plot_animated(n_visible=5)


def test_barv(covid_df):

    animated_plot = covid_df.plot_animated(orientation="v", n_visible=5)


def test_line(covid_df):

    animated_plot = covid_df.diff().fillna(0).plot_animated(kind="line")
