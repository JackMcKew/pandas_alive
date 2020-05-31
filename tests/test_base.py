import pytest

import pandas_alive


@pytest.fixture(scope="function")
def covid_df():

    # Load Iris Dataset:
    covid_df = pandas_alive.load_dataset()

    return covid_df
