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


def test_scatter(covid_df):

    covid_df.plot_animated()
