import os
import sys

import pandas_alive
import pytest

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from PIL import Image

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "../..")


@pytest.fixture(scope="function")
def example_dataframe():
    test_data = [
        [np.random.randint(0, 10000), np.random.randint(0, 10000)],
        [np.random.randint(0, 10000), np.random.randint(0, 10000)],
    ]
    test_columns = ["A", "B"]
    index_start = datetime(
        np.random.randint(2000, 2020),
        np.random.randint(1, 12),
        np.random.randint(1, 28),
    )
    index_end = index_start + timedelta(days=np.random.randint(1, 364))
    test_index = [index_start, index_end]
    return pd.DataFrame(data=test_data, columns=test_columns, index=test_index)


@pytest.mark.parametrize("kind", ["race", "line", "scatter", "pie", "bar"])
def test_plot(example_dataframe, kind):
    animated_plot = example_dataframe.plot_animated(filename="test.gif", kind=kind)
    im = Image.open("test.gif")
    assert im.format == "GIF"


@pytest.mark.parametrize("orientation", ["h", "v"])
@pytest.mark.parametrize("sort", ["desc", "asc"])
@pytest.mark.parametrize("label_bars", [True, False])
@pytest.mark.parametrize("bar_label_size", [6, 7, 8])
@pytest.mark.parametrize("n_visible", [6, 7, 8])
@pytest.mark.parametrize("fixed_order", [True, False])
@pytest.mark.parametrize("perpendicular_bar_func", ["mean", "min", "median"])
def test_bar_chart_race(
    example_dataframe,
    orientation,
    sort,
    label_bars,
    bar_label_size,
    n_visible,
    fixed_order,
    perpendicular_bar_func,
):

    animated_plot = example_dataframe.plot_animated(
        filename="test.gif",
        kind="race",
        orientation=orientation,
        sort=sort,
        label_bars=label_bars,
        bar_label_size=bar_label_size,
        n_visible=n_visible,
        fixed_order=fixed_order,
        perpendicular_bar_func=perpendicular_bar_func,
    )
    im = Image.open("test.gif")
    assert im.format == "GIF"


@pytest.mark.parametrize("line_width", [1, 2])
@pytest.mark.parametrize("fill_under_line_color", ["blue", "red"])
def test_line_chart(example_dataframe, line_width, fill_under_line_color):

    animated_plot = example_dataframe.plot_animated(
        filename="test.gif",
        kind="race",
        line_width=line_width,
        fill_under_line_color=fill_under_line_color,
    )
    im = Image.open("test.gif")
    assert im.format == "GIF"
