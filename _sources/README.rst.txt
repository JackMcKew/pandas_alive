
Pandas-Alive
============

Animated plotting extension for Pandas with Matplotlib

**Pandas-Alive** is intended to provide a plotting backend for animated `matplotlib <https://matplotlib.org/>`_ charts for `Pandas <https://pandas.pydata.org/>`_ DataFrames, similar to the already `existing Visualization feature of Pandas <https://pandas.pydata.org/pandas-docs/stable/visualization.html>`_.

With **Pandas-Alive**\ , creating stunning, animated visualisations is as easy as calling:

.. code-block:: python

   df.plot_animated()


.. image:: ../../examples/example-barh-chart.gif
   :target: examples/example-barh-chart.gif
   :alt: Example Bar Chart


Installation
------------

Install with ``pip install pandas-alive``

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

   df = pandas_alive.load_dataset()

   df.plot_animated(filename='example-barh-chart.gif')

Currently Supported Chart Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pandas-alive`` current supports:


* `Horizontal Bar Charts <#horizontal-bar-charts>`_
* `Vertical Bar Charts <#vertical-bar-charts>`_
* `Line Charts <#line-charts>`_

Horizontal Bar Charts
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas_alive

   df = pandas_alive.load_dataset()

   df.plot_animated(filename='example-barh-chart.gif')


.. image:: ../../examples/example-barh-chart.gif
   :target: examples/example-barh-chart.gif
   :alt: Example Barh Chart


Vertical Bar Charts
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas_alive

   df = pandas_alive.load_dataset()

   df.plot_animated(filename='example-barv-chart.gif',orientation='v')


.. image:: ../../examples/example-barv-chart.gif
   :target: examples/example-barv-chart.gif
   :alt: Example Barv Chart


Line Charts
~~~~~~~~~~~

With as many lines as data columns in DataFrame.

.. code-block:: python

   import pandas_alive

   df = pandas_alive.load_dataset()

   df.diff().fillna(0).plot_animated(filename='example-line-chart.gif',kind='line')


.. image:: ../../examples/example-line-chart.gif
   :target: examples/example-line-chart.gif
   :alt: Example Line Chart


Multiple Charts
^^^^^^^^^^^^^^^

``pandas-alive`` supports multiple animated charts in a single visualisation.


* Create a list of all charts to include in animation
* Use ``animate_multiple_plots`` with a ``filename`` and the list of charts (this will use ``matplotlib.subplots``\ )
* Done!

.. code-block:: python

   import pandas_alive

   df = pandas_alive.load_dataset()

   animated_line_chart = df.diff().fillna(0).plot_animated(kind='line',period_length=200)

   animated_bar_chart = df.plot_animated(kind='barh',period_length=200,n_visible=10)

   pandas_alive.animate_multiple_plots('example-bar-and-line-chart.gif',[animated_bar_chart,animated_line_chart]


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
       .plot_animated(kind="line", title="Total % Change in Population",show_period_annotation=False)
   )

   animated_bar_chart = urban_df.plot_animated(kind='barh',n_visible=10,title='Top 10 Populous Countries')

   pandas_alive.animate_multiple_plots('examples/example-bar-and-line-urban-chart.gif',[animated_bar_chart,animated_line_chart],title='Urban Population 1977 - 2018')


.. image:: ../../examples/example-bar-and-line-urban-chart.gif
   :target: examples/example-bar-and-line-urban-chart.gif
   :alt: Urban Population Bar & Line Chart


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

Documentation is provided at https://jackmckew.github.io/pandas-alive/

Contributing
------------

Pull requests are welcome! Please help to cover more and more chart types!
