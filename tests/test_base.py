import os
import sys

import pandas_alive
import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ".")


# @pytest.fixture(scope="function")
def test_load_dataset():

    # Load default dataset:
    covid_df = pandas_alive.load_dataset()

    return covid_df
