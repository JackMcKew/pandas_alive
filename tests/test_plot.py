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


@pytest.mark.parametrize("orientation", ["h", "v"])
@pytest.mark.parametrize("sort", ["desc", "asc"])
@pytest.mark.parametrize("label_bars", [True, False])
@pytest.mark.parametrize("bar_label_size", [6, 7, 8])
@pytest.mark.parametrize("n_visible", [6, 7, 8])
@pytest.mark.parametrize("fixed_order", [True, False])
@pytest.mark.parametrize("perpendicular_bar_func", ["mean", "min", "median"])
def test_bar_chart_race(
    covid_df,
    orientation,
    sort,
    label_bars,
    bar_label_size,
    n_visible,
    fixed_order,
    perpendicular_bar_func,
):

    animated_plot = covid_df.plot_animated(
        kind="race",
        orientation=orientation,
        sort=sort,
        label_bars=label_bars,
        bar_label_size=bar_label_size,
        n_visible=n_visible,
        fixed_order=fixed_order,
        perpendicular_bar_func=perpendicular_bar_func,
    )


# def test_barh(covid_df):

#     animated_plot = covid_df.plot_animated()

#     assert True

# @pytest.mark.parametrize("orientation",["h","v"])
# def test_barv(covid_df,orientation):

#     animated_plot = covid_df.plot_animated(orientation=orientation)

#     assert True


# def test_line(covid_df):

#     animated_plot = covid_df.diff().fillna(0).plot_animated(kind="line")

#     assert True
