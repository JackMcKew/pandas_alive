# Pandas_Alive

Animated plotting extension for Pandas with Matplotlib

[![Inline docs](http://inch-ci.org/github/dwyl/hapi-auth-jwt2.svg?branch=master)](https://jackmckew.github.io/pandas_alive/) [![PyPI download month](https://img.shields.io/pypi/dm/pandas_alive.svg)](https://pypi.python.org/pypi/pandas_alive/) [![PyPI version shields.io](https://img.shields.io/pypi/v/pandas_alive.svg)](https://pypi.python.org/pypi/pandas_alive/) [![PyPI license](https://img.shields.io/pypi/l/pandas_alive.svg)](https://pypi.python.org/pypi/pandas_alive/) [![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://www.buymeacoffee.com/jackmckew)

**Pandas_Alive** is intended to provide a plotting backend for animated [matplotlib](https://matplotlib.org/) charts for [Pandas](https://pandas.pydata.org/) DataFrames, similar to the already [existing Visualization feature of Pandas](https://pandas.pydata.org/pandas-docs/stable/visualization.html).

With **Pandas_Alive**, creating stunning, animated visualisations is as easy as calling:

`df.plot_animated()`

![Example Bar Chart](examples/example-barh-chart.gif)

## Table of Contents
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Installation](#installation)
- [Usage](#usage)
  - [Currently Supported Chart Types](#currently-supported-chart-types)
    - [Horizontal Bar Chart Races](#horizontal-bar-chart-races)
    - [Vertical Bar Chart Races](#vertical-bar-chart-races)
    - [Line Charts](#line-charts)
    - [Bar Charts](#bar-charts)
    - [Scatter Charts](#scatter-charts)
    - [Pie Charts](#pie-charts)
    - [Bubble Charts](#bubble-charts)
  - [Multiple Charts](#multiple-charts)
    - [Urban Population](#urban-population)
    - [Life Expectancy in G7 Countries](#life-expectancy-in-g7-countries)
  - [HTML 5 Videos](#html-5-videos)
  - [Progress Bars!](#progress-bars)
- [Future Features](#future-features)
- [Inspiration](#inspiration)
- [Requirements](#requirements)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Changelog](#changelog)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Installation

Install with `pip install pandas_alive`

## Usage

As this package builds upon [`bar_chart_race`](https://github.com/dexplo/bar_chart_race), the example data set is sourced from there.

Must begin with a pandas DataFrame containing 'wide' data where:

- Every row represents a single period of time
- Each column holds the value for a particular category
- The index contains the time component (optional)

The data below is an example of properly formatted data. It shows total deaths from COVID-19 for the highest 20 countries by date.

![Example Data Table](https://raw.githubusercontent.com/dexplo/bar_chart_race/master/docs/images/wide_data.png)

To produce the above visualisation:

- Check [Requirements](#requirements) first to ensure you have the tooling installed!
- Call `plot_animated()` on the DataFrame
    - Either specify a file name to write to with `df.plot_animated(filename='example.mp4')` or use `df.plot_animated().get_html5_video` to return a HTML5 video
- Done!

``` python
import pandas_alive

covid_df = pandas_alive.load_dataset()

covid_df.plot_animated(filename='examples/example-barh-chart.gif')
```

### Currently Supported Chart Types

#### Horizontal Bar Chart Races

``` python
import pandas as pd
import pandas_alive

elec_df = pd.read_csv("data/Aus_Elec_Gen_1980_2018.csv",index_col=0,parse_dates=[0],thousands=',')

elec_df.fillna(0).plot_animated('examples/example-electricity-generated-australia.gif',period_fmt="%Y",title='Australian Electricity Generation Sources 1980-2018')
```

![Electricity Example Line Chart](examples/example-electricity-generated-australia.gif)

``` python
import pandas_alive

covid_df = pandas_alive.load_dataset()

def current_total(values):
    total = values.sum()
    s = f'Total : {int(total)}'
    return {'x': .85, 'y': .2, 's': s, 'ha': 'right', 'size': 11}

covid_df.plot_animated(filename='examples/summary-func-example.gif',period_summary_func=current_total)
```

![Summary Func Example](examples/summary-func-example.gif)

``` python
import pandas as pd
import pandas_alive

elec_df = pd.read_csv("data/Aus_Elec_Gen_1980_2018.csv",index_col=0,parse_dates=[0],thousands=',')

elec_df.fillna(0).plot_animated('examples/fixed-example.gif',period_fmt="%Y",title='Australian Electricity Generation Sources 1980-2018',fixed_max=True,fixed_order=True)
```

![Fixed Example](examples/fixed-example.gif)

``` python
import pandas_alive

covid_df = pandas_alive.load_dataset()

covid_df.plot_animated(filename='examples/perpendicular-example.gif',perpendicular_bar_func='mean')
```

![Perpendicular Example](examples/perpendicular-example.gif)

#### Vertical Bar Chart Races

``` python
import pandas_alive

covid_df = pandas_alive.load_dataset()

covid_df.plot_animated(filename='examples/example-barv-chart.gif',orientation='v')
```

![Example Barv Chart](examples/example-barv-chart.gif)

#### Line Charts

With as many lines as data columns in the DataFrame.

``` python
import pandas_alive

covid_df = pandas_alive.load_dataset()

covid_df.diff().fillna(0).plot_animated(filename='examples/example-line-chart.gif',kind='line',period_label={'x':0.1,'y':0.9})
```

![Example Line Chart](examples/example-line-chart.gif)


#### Bar Charts

Similar to line charts with time as the x-axis

``` python
import pandas_alive

covid_df = pandas_alive.load_dataset()

covid_df.sum(axis=1).fillna(0).plot_animated(filename='examples/example-bar-chart.gif',kind='bar',period_label={'x':0.1,'y':0.9})
```

![Example Bar Chart](examples/example-bar-chart.gif)

#### Scatter Charts

``` python
import pandas as pd
import pandas_alive

max_temp_df = pd.read_csv(
    "data/Newcastle_Australia_Max_Temps.csv",
    parse_dates={"Timestamp": ["Year", "Month", "Day"]},
)
min_temp_df = pd.read_csv(
    "data/Newcastle_Australia_Min_Temps.csv",
    parse_dates={"Timestamp": ["Year", "Month", "Day"]},
)

merged_temp_df = pd.merge_asof(max_temp_df, min_temp_df, on="Timestamp")

merged_temp_df.index = pd.to_datetime(merged_temp_df["Timestamp"].dt.strftime('%Y/%m/%d'))

keep_columns = ["Minimum temperature (Degree C)", "Maximum temperature (Degree C)"]

merged_temp_df[keep_columns].resample("Y").mean().plot_animated(filename='examples/example-scatter-chart.gif',kind="scatter",title='Max & Min Temperature Newcastle, Australia')

```

![Example Scatter Chart](examples/example-scatter-chart.gif)

#### Pie Charts

``` python
import pandas_alive

covid_df = pandas_alive.load_dataset()

covid_df.plot_animated(filename='examples/example-pie-chart.gif',kind="pie",rotatelabels=True,period_label={'x':0,'y':0})
```

![Example Pie Chart](examples/example-pie-chart.gif)

#### Bubble Charts

Bubble charts are generated from a multi-indexed dataframes. Where the index is the time period (optional) and the axes are defined with `x_data_label` & `y_data_label` which should be passed a string in the level 0 column labels.

See an example multi-indexed dataframe at: <https://github.com/JackMcKew/pandas_alive/tree/master/data/multi.csv>

``` python
import pandas_alive

multi_index_df = pd.read_csv("data/multi.csv", header=[0, 1], index_col=0)

multi_index_df.index = pd.to_datetime(multi_index_df.index,dayfirst=True)

map_chart = multi_index_df.plot_animated(
    kind="bubble",
    filename="examples/example-bubble-chart.gif",
    x_data_label="Longitude",
    y_data_label="Latitude",
    size_data_label="Cases",
)
```

![Bubble Chart Example](examples/example-bubble-chart.gif)

### Multiple Charts

`pandas_alive` supports multiple animated charts in a single visualisation.

- Create a list of all charts to include in animation
- Use `animate_multiple_plots` with a `filename` and the list of charts (this will use `matplotlib.subplots`)
- Done!

``` python
import pandas_alive

covid_df = pandas_alive.load_dataset()

animated_line_chart = covid_df.diff().fillna(0).plot_animated(kind='line',period_label=False)

animated_bar_chart = covid_df.plot_animated(n_visible=10)

pandas_alive.animate_multiple_plots('examples/example-bar-and-line-chart.gif',[animated_bar_chart,animated_line_chart])
```

![Example Bar & Line Chart](examples/example-bar-and-line-chart.gif)

#### Urban Population

``` python
import pandas_alive

urban_df = pandas_alive.load_dataset("urban_pop")

animated_line_chart = (
    urban_df.sum(axis=1)
    .pct_change()
    .dropna()
    .mul(100)
    .plot_animated(kind="line", title="Total % Change in Population",period_label=False)
)

animated_bar_chart = urban_df.plot_animated(n_visible=10,title='Top 10 Populous Countries',period_fmt="%Y")

pandas_alive.animate_multiple_plots('examples/example-bar-and-line-urban-chart.gif',[animated_bar_chart,animated_line_chart],title='Urban Population 1977 - 2018',adjust_subplot_top=0.85)
```

![Urban Population Bar & Line Chart](examples/example-bar-and-line-urban-chart.gif)


#### Life Expectancy in G7 Countries

``` python
import pandas_alive
import pandas as pd

data_raw = pd.read_csv(
    "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Long%20run%20life%20expectancy%20-%20Gapminder%2C%20UN/Long%20run%20life%20expectancy%20-%20Gapminder%2C%20UN.csv"
)

list_G7 = [
    "Canada",
    "France",
    "Germany",
    "Italy",
    "Japan",
    "United Kingdom",
    "United States",
]

data_raw = data_raw.pivot(
    index="Year", columns="Entity", values="Life expectancy (Gapminder, UN)"
)

data = pd.DataFrame()
data["Year"] = data_raw.reset_index()["Year"]
for country in list_G7:
    data[country] = data_raw[country].values

data = data.fillna(method="pad")
data = data.fillna(0)
data = data.set_index("Year").loc[1900:].reset_index()

data["Year"] = pd.to_datetime(data.reset_index()["Year"].astype(str))

data = data.set_index("Year")

animated_bar_chart = data.plot_animated(
    period_fmt="%Y",perpendicular_bar_func="mean", period_length=200,fixed_max=True
)

animated_line_chart = data.plot_animated(
    kind="line", period_fmt="%Y", period_length=200,fixed_max=True
)

pandas_alive.animate_multiple_plots(
    "examples/life-expectancy.gif",
    plots=[animated_bar_chart, animated_line_chart],
    title="Life expectancy in G7 countries up to 2015",
    adjust_subplot_left=0.2,
)

```

![Life Expectancy Chart](examples/life-expectancy.gif)

### HTML 5 Videos

`Pandas_Alive` supports rendering HTML5 videos through the use of `df.plot_animated().get_html5_video()`. `.get_html5_video` saves the animation as an h264 video, encoded in base64 directly into the HTML5 video tag. This respects the rc parameters for the writer as well as the bitrate. This also makes use of the interval to control the speed, and uses the repeat parameter to decide whether to loop.

This is typically used in Jupyter notebooks.

``` python
import pandas_alive
from IPython.display import HTML

covid_df = pandas_alive.load_dataset()

animated_html = covid_df.plot_animated().get_html5_video()

HTML(animated_html)
```

### Progress Bars!

Generating animations can take some time, so enable progress bars by installing [tqdm](https://github.com/tqdm/tqdm) with `pip install tqdm` and using the keyword `enable_progress_bar=True`.

By default Pandas_Alive will create a `tqdm` progress bar for the number of frames to animate, and update the progres bar after each frame.

``` python
import pandas_alive

covid_df = pandas_alive.load_dataset()

covid_df.plot_animated(enable_progress_bar=True)
```

Example of TQDM in action:

![TQDM Example](https://raw.githubusercontent.com/tqdm/tqdm/master/images/tqdm.gif)

## Future Features

A list of future features that may/may not be developed is:

- Geographic charts (currently using OSM export image, potential [geopandas](https://geopandas.org/))
    - This is currently working at a proof of concept level, stay tuned!
- ~~Loading bar support (potential [tqdm](https://github.com/tqdm/tqdm) or [alive-progress](https://github.com/rsalmei/alive-progress))~~
- Potentially support writing to GIF in memory with <https://github.com/maxhumber/gif>

A chart that was built using a development branch of Pandas_Alive is:

[![NSW COVID19 Cases](examples/nsw-covid.gif)](https://www.youtube.com/watch?v=qyqiYrtpxRE)

## Inspiration

The inspiration for this project comes from:

- [bar_chart_race](https://github.com/dexplo/bar_chart_race) by [Ted Petrou](https://github.com/tdpetrou)
- [Pandas-Bokeh](https://github.com/PatrikHlobil/Pandas-Bokeh) by [Patrik Hlobil](https://github.com/PatrikHlobil)

## Requirements

If you get an error such as `TypeError: 'MovieWriterRegistry' object is not an iterator`, this signals there isn't a writer library installed on your machine.

This package utilises the [matplotlib.animation function](https://matplotlib.org/3.2.1/api/animation_api.html), thus requiring a writer library.

Ensure to have one of the supported tooling software installed prior to use!

- [ffmpeg](https://ffmpeg.org/)
- [ImageMagick](https://imagemagick.org/index.php)
- See more at <https://matplotlib.org/3.2.1/api/animation_api.html#writer-classes>

> Outputting to GIF file type is only supported by ImageMagick

> Pillow is not supported currently, please submit a PR if you can make Pillow work!

## Documentation

Documentation is provided at <https://jackmckew.github.io/pandas_alive/>

## Contributing

Pull requests are welcome! Please help to cover more and more chart types!

## [Changelog](CHANGELOG.md)
