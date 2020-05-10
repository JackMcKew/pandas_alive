
Pandas_Alive
============

Animated plotting extension for Pandas with Matplotlib

**Pandas_Alive** is intended to provide a plotting backend for animated `matplotlib <https://matplotlib.org/>`_ charts for `Pandas <https://pandas.pydata.org/>`_ DataFrames, similar to the already `existing Visualization feature of Pandas <https://pandas.pydata.org/pandas-docs/stable/visualization.html>`_.

With **Pandas_Alive**\ , creating stunning, animated visualisations is as easy as calling:

``df.plot_animated()``


.. image:: ../../examples/example-barh-chart.gif
   :target: examples/example-barh-chart.gif
   :alt: Example Bar Chart


Installation
------------

Install with ``pip install pandas_alive``

Usage
-----

As this package builds upon `\ ``bar_chart_race`` <https://github.com/dexplo/bar_chart_race>`_\ , the example data set is sourced from there.

Must begin with a pandas DataFrame containing 'wide' data where:


* Every row represents a single period of time
* Each column holds the value for a particular category
* The index contains the time component (optional)

The data below is an example of properly formatted data. It shows total deaths from COVID-19 for the highest 20 countries by date.


.. image:: https://raw.githubusercontent.com/dexplo/bar_chart_race/master/images/wide_data.png
   :target: https://raw.githubusercontent.com/dexplo/bar_chart_race/master/images/wide_data.png
   :alt: Example Data Table

`Example Table <examples/example_dataset_table.md>`_

To produce the above visualisation:


* Check `Requirements <#requirements>`_ first to ensure you have the tooling installed!
* Call ``plot_animated()`` on the DataFrame

  * Either specify a file name to write to with ``df.plot_animated(filename='example.mp4')`` or use ``df.plot_animated().get_html5_video`` to return a HTML5 video

* Done!

.. code-block:: python

   import pandas_alive

   covid_df = pandas_alive.load_dataset()

   covid_df.plot_animated(filename='examples/example-barh-chart.gif')

Currently Supported Chart Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pandas_alive`` current supports:


* `Horizontal Bar Charts <#horizontal-bar-charts>`_
* `Vertical Bar Charts <#vertical-bar-charts>`_
* `Line Charts <#line-charts>`_
* `Scatter Charts <#scatter-charts>`_
* `Pie Charts <#pie-charts>`_

Horizontal Bar Charts
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas_alive

   covid_df = pandas_alive.load_dataset()

   covid_df.plot_animated(filename='example-barh-chart.gif')


.. image:: ../../examples/example-barh-chart.gif
   :target: examples/example-barh-chart.gif
   :alt: Example Barh Chart


.. code-block:: python

   import pandas as pd
   import pandas_alive

   elec_df = pd.read_csv("data/Aus_Elec_Gen_1980_2018.csv",index_col=0,parse_dates=[0],thousands=',')

   elec_df.fillna(0).plot_animated('examples/example-electricity-generated-australia.gif',period_fmt="%Y",title='Australian Electricity Generation Sources 1980-2018')


.. image:: ../../examples/example-electricity-generated-australia.gif
   :target: examples/example-electricity-generated-australia.gif
   :alt: Electricity Example Line Chart


.. code-block:: python

   import pandas_alive

   covid_df = pandas_alive.load_dataset()

   def current_total(values):
       total = values.sum()
       s = f'Total : {int(total)}'
       return {'x': .85, 'y': .2, 's': s, 'ha': 'right', 'size': 11}

   covid_df.plot_animated(filename='examples/summary-func-example.gif',period_summary_func=current_total)


.. image:: ../../examples/summary-func-example.gif
   :target: examples/summary-func-example.gif
   :alt: Summary Func Example


.. code-block:: python

   import pandas as pd
   import pandas_alive

   elec_df = pd.read_csv("data/Aus_Elec_Gen_1980_2018.csv",index_col=0,parse_dates=[0],thousands=',')

   elec_df.fillna(0).plot_animated('examples/fixed-example.gif',period_fmt="%Y",title='Australian Electricity Generation Sources 1980-2018',fixed_max=True,fixed_order=True)


.. image:: ../../examples/fixed-example.gif
   :target: examples/fixed-example.gif
   :alt: Fixed Example


.. code-block:: python

   import pandas_alive

   covid_df = pandas_alive.load_dataset()

   covid_df.plot_animated(filename='examples/perpendicular-example.gif',perpendicular_bar_func='mean')


.. image:: ../../examples/perpendicular-example.gif
   :target: examples/perpendicular-example.gif
   :alt: Perpendicular Example


Vertical Bar Charts
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas_alive

   covid_df = pandas_alive.load_dataset()

   covid_df.plot_animated(filename='examples/example-barv-chart.gif',orientation='v')


.. image:: ../../examples/example-barv-chart.gif
   :target: examples/example-barv-chart.gif
   :alt: Example Barv Chart


Line Charts
~~~~~~~~~~~

With as many lines as data columns in the DataFrame.

.. code-block:: python

   import pandas_alive

   covid_df = pandas_alive.load_dataset()

   covid_df.diff().fillna(0).plot_animated(filename='examples/example-line-chart.gif',kind='line',period_label={'x':0.1,'y':0.9})


.. image:: ../../examples/example-line-chart.gif
   :target: examples/example-line-chart.gif
   :alt: Example Line Chart


Scatter Charts
~~~~~~~~~~~~~~

.. code-block:: python

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


.. image:: ../../examples/example-scatter-chart.gif
   :target: examples/example-scatter-chart.gif
   :alt: Example Scatter Chart


Pie Charts
~~~~~~~~~~

.. code-block:: python

   import pandas_alive

   covid_df = pandas_alive.load_dataset()

   covid_df.plot_animated(filename='examples/example-pie-chart.gif',kind="pie",rotatelabels=True)


.. image:: ../../examples/example-pie-chart.gif
   :target: examples/example-pie-chart.gif
   :alt: Example Pie Chart


Multiple Charts
^^^^^^^^^^^^^^^

``pandas_alive`` supports multiple animated charts in a single visualisation.


* Create a list of all charts to include in animation
* Use ``animate_multiple_plots`` with a ``filename`` and the list of charts (this will use ``matplotlib.subplots``\ )
* Done!

.. code-block:: python

   import pandas_alive

   covid_df = pandas_alive.load_dataset()

   animated_line_chart = covid_df.diff().fillna(0).plot_animated(kind='line',period_label=False)

   animated_bar_chart = covid_df.plot_animated(n_visible=10)

   pandas_alive.animate_multiple_plots('examples/example-bar-and-line-chart.gif',[animated_bar_chart,animated_line_chart])


.. image:: ../../examples/example-bar-and-line-chart.gif
   :target: examples/example-bar-and-line-chart.gif
   :alt: Example Bar & Line Chart


.. code-block:: python

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


.. image:: ../../examples/example-bar-and-line-urban-chart.gif
   :target: examples/example-bar-and-line-urban-chart.gif
   :alt: Urban Population Bar & Line Chart


.. code-block:: python

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


.. image:: ../../examples/life-expectancy.gif
   :target: examples/life-expectancy.gif
   :alt: Life Expectancy Chart


Inspiration
-----------

The inspiration for this project comes from:


* `bar_chart_race <https://github.com/dexplo/bar_chart_race>`_ by `Ted Petrou <https://github.com/tdpetrou>`_
* `Pandas-Bokeh <https://github.com/PatrikHlobil/Pandas-Bokeh>`_ by `Patrik Hlobil <https://github.com/PatrikHlobil>`_

Requirements
------------

If you get an error such as ``TypeError: 'MovieWriterRegistry' object is not an iterator``\ , this signals there isn't a writer library installed on your machine.

This package utilises the `matplotlib.animation function <https://matplotlib.org/3.2.1/api/animation_api.html>`_\ , thus requiring a writer library.

Ensure to have one of the supported tooling software installed prior to use!


* `ffmpeg <https://ffmpeg.org/>`_
* `ImageMagick <https://imagemagick.org/index.php>`_
* `Pillow <https://pillow.readthedocs.io/en/stable/>`_
* See more at https://matplotlib.org/3.2.1/api/animation_api.html#writer-classes

Documentation
-------------

Documentation is provided at https://jackmckew.github.io/pandas_alive/

Contributing
------------

Pull requests are welcome! Please help to cover more and more chart types!

`Changelog <CHANGELOG.md>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Changelog <CHANGELOG.md>`_

.. code-block:: python


