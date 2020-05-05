.. SphinxDemo documentation master file, created by
   sphinx-quickstart on Tue Feb  4 20:05:16 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pandas_Alive |version|
========================================

Animated plotting extension for Pandas with Matplotlib

Pandas_alive is intended to provide a plotting backend for animated matplotlib charts for Pandas DataFrames, similar to the already existing Visualization feature of Pandas.

With Pandas_alive, creating stunning, animated visualisations is as easy as calling:

``df.plot_animated()``

.. image:: ../../examples/example-barh-chart.gif
   :target: examples/example-barh-chart.gif
   :alt: Example Bar Chart

.. toctree::
   :caption: Getting Started
   :maxdepth: 3

   README <README>

.. rubric:: Modules

.. autosummary::
   :toctree: generated

   pandas_alive.plot
   pandas_alive.base
   pandas_alive.charts
   pandas_alive.__init__

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
