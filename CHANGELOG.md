
# Change Log

All notable changes to this project will be documented in this file.

## 0.2.3 - 2020-10-18

- Fixed an ongoing problem with `animate_multiple_plots` when re-using a line or scatter chart. Corresponding subplots would show a static figure from a previous single animation.
- Fixed `fig=` for single animations not being passed properly as a custom figure.
- Several performance improvements to speed up loops in animations.
- Fixed a problem with line and scatter plots being chopped off near the vertical limit values.
- Added a `colorbar` with bubble plots when a `Pandas` df column is passed as a colour. Currently only for individual animations.
- Added options for bubble plots above to control the `colorbar` scale limits with `vmin` & `vmax`. If None, then they are automatically calculated.
- Added option `add_legend=` for line and scatter animations for single & multiple plots. Default is `True`.
- Added the option `enable_progress_bar=` to `animate_multiple_plots`. Default is `False`.
- Improved the ability to re-use figures & axes in a notebook for multiple plots. Occasionally, these used to carry over old frames into a new animation.
- Made `animate_multiple_plots` to create a `Figure()` instance instead of a `figure()` one. Note that `matplotlib` can take twice as long to generate animations with the latter instance type. Not clear why.
- Added a new folder `./examples/test_notebooks/` for future collaborators to add new notebooks.
- Removed the limitation for the interpolation (`interpolate_period=`) only to work with a `DateTime` index. It should now work with any numeric df index.

## 0.2.2 - 2020-06-04

- Additional error catching with warnings for modules not being installed
- Add both attrs and pillow as dependencies, so users can install with pip and have it `just work`

## 0.2.1 - 2020-06-02

- Custom figures now supported in `animate_multiple_plots`
- Writing to GIF in memory with `PIL` now supported, no external dependencies for gifs!

## [0.2.0]

- Changing version format MAJOR.MINOR.PATCH
- Introduces support for geospatial data with geopandas
    - Introduces support for basemap on geospatial datasets with contextily

## [2020.05.15]

- Officially changing to version format with YYYY.MM.VERSION
- Hotfix for anaconda environment throwing an error:
    - `ufunc 'isfinite' not supported for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe''`

## [0.1.14] - 2020-05-23

- Progress bars (thanks to [`tqdm`](https://github.com/tqdm/tqdm) can now be enabled with `df.plot_animated(enable_progress_bar=True)
- Writer can now be specified with `df.plot_animated(writer="imagemagick")`
    - Pillow is now explicitly unsupported, see relevant issue here <https://github.com/JackMcKew/pandas_alive/issues/5>

## [0.1.13] - 2020-05-21

- New chart type introduced: Bubble Charts, to be used with MultiIndexed DataFrames.
    - Bubble charts support x & y axis by data inside MultiIndex (`x_data_label` & `y_data_label`)
    - Bubble charts support size & color optionally by data inside DataFrame (`size_data_label` & `color_data_label`)
- New chart type introduced: Scatter Chart
- New chart type introduced: Bar Chart, create animated bar charts with time as the x-axis
- QOL improvements for warnings & errors
- Line charts now support filling underneath to mimic an area chart `df.plot_animated(kind="line",fill_under_line_color="red")`
- Line charts now support event labelling with perpendicular bars

    ``` python
    df.plot_animated(
                kind='line',
                label_events={
                    'Ruby Princess Disembark':datetime.strptime("19/03/2020", "%d/%m/%Y"),
                    'Lockdown':datetime.strptime("31/03/2020", "%d/%m/%Y")
                },
            )
    ```

## [0.1.12] - 2020-05-10

- `fixed_max` optional for all chart types
- `fixed_max` amended to work with multiple plots

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
