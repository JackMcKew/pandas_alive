
# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.1.11] - 2020-05-09

- `period_summary_func` provided for charts to display overall period calculations on plot
- Bar chart functionality extended
    - `fixed_order` can be used to disable bars moving on bar chart
    - `fixed_max` set limits of axis on charts to be total maximum of dataframe rather than dynamic
    - `perpendicular_bar_func` Plot perpendicular black bar on plot to demonstrate different stats, eg, max, min, median, etc. Use with Series.agg()

## [0.1.10] - 2020-05-08

- Complete overhaul of backend with `_base_plot.py`, refactored all arguments
- README & Examples generated from README.ipynb, converted with `nbconvert`
- Docs generated only on release
- DataFrames interpolated to match animation length
- Scatter plot introduced

## [0.1.9] - 2020-05-06

- Fix bar label plotting
- Update docs to render cleanly

## [0.1.8] - 2020-05-05

### Changed

- Removed **kwargs from multiple_animated_plot() due to weird errors when passed to `anim.save()`

## [0.1.7] - 2020-05-05

- Rename pandas-alive to pandas_alive for consistency
- Adjust subplot arguments in multiple animated plot function for flexibility in avoiding cropping as per <https://stackoverflow.com/questions/10101700/moving-matplotlib-legend-outside-of-the-axis-makes-it-cutoff-by-the-figure-box>
- Tests included - no CI/CD for tests as no ffmpeg/imagemagick on github actions

## [0.1.6] - 2020-05-05

- Documentation included at <https://jackmckew.github.io/pandas_alive/>
- DPI functionality fixed

## [0.1.5] - 2020-05-05

- Smoother reindexing/interpolation for line charts

## [0.1.4] - 2020-05-05

- Styling now applied at the base plot level, ensuring consistent styling across plots
- Dates now formatted on axises with ConciseDateFormatter

## [0.1.3] - 2020-05-05

- `pandas_alive.output_file()` deprecated in favour of `df.plot_animated(filename='example.mp4')` and/or `df.plot_animated().save('example.mp4')`
- HTML5 video method implemented with `df.plot_animated().get_html5_video()`, returns a HTML5 video instance
- Amended bug with append_period_to_title for line charts

## [0.1.2] - 2020-05-04

- Fix title of subplots & plots
    - Implement functionality to append current time period to title [#1](https://github.com/JackMcKew/pandas_alive/issues/1)
- Custom placement of current period [#1](https://github.com/JackMcKew/pandas_alive/issues/1)
- Implement functionality to specify single colour for all bars [#2](https://github.com/JackMcKew/pandas_alive/issues/2)
- Organise root folder [#3](https://github.com/JackMcKew/pandas_alive/issues/3)
- Move to save design pattern similar to altair
