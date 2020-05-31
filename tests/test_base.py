import pytest

import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ".")

import pandas_alive


# @pytest.fixture(scope="function")
def test_load_dataset():

    # Load default dataset:
    covid_df = pandas_alive.load_dataset()

    return covid_df
