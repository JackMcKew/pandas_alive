# Pandas_Alive

Animated plotting extension for Pandas with Matplotlib

**Pandas_Alive** is intended to provide a plotting backend for animated [matplotlib](https://matplotlib.org/) charts for [Pandas](https://pandas.pydata.org/) DataFrames, similar to the already [existing Visualization feature of Pandas](https://pandas.pydata.org/pandas-docs/stable/visualization.html).

With **Pandas_Alive**, creating stunning, animated visualisations is as easy as calling:

`df.plot_animated()`

![Example Bar Chart](examples/example-barh-chart.gif)

## Installation

Install with `pip install pandas_alive`

## Usage

As this package builds upon [`bar_chart_race`](https://github.com/dexplo/bar_chart_race), the example data set is sourced from there.

Must begin with a pandas DataFrame containing 'wide' data where:

- Every row represents a single period of time
- Each column holds the value for a particular category
- The index contains the time component (optional)

The data below is an example of properly formatted data. It shows total deaths from COVID-19 for the highest 20 countries by date.

![Example Data Table](https://raw.githubusercontent.com/dexplo/bar_chart_race/master/images/wide_data.png)
[Example Table](examples/example_dataset_table.md)

To produce the above visualisation:

- Check [Requirements](#requirements) first to ensure you have the tooling installed!
- Call `plot_animated()` on the DataFrame
    - Either specify a file name to write to with `df.plot_animated(filename='example.mp4')` or use `df.plot_animated().get_html5_video` to return a HTML5 video
- Done!


```
import pandas_alive

covid_df = pandas_alive.load_dataset()

covid_df.plot_animated(filename='examples/example-barh-chart.gif')
```

    Generating BarChart, plotting ['Belgium', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Indonesia', 'Iran', 'Ireland', 'Italy', 'Mexico', 'Netherlands', 'Portugal', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'USA', 'United Kingdom']





    BarChart(df=                     Belgium  Brazil  Canada   China   France  Germany  India  \
    date                                                                            
    2020-02-26 00:00:00      NaN     NaN     NaN  2717.0      2.0      NaN    NaN   
    2020-02-26 02:24:00      NaN     NaN     NaN  2719.9      2.0      NaN    NaN   
    2020-02-26 04:48:00      NaN     NaN     NaN  2722.8      2.0      NaN    NaN   
    2020-02-26 07:12:00      NaN     NaN     NaN  2725.7      2.0      NaN    NaN   
    2020-02-26 09:36:00      NaN     NaN     NaN  2728.6      2.0      NaN    NaN   
    ...                      ...     ...     ...     ...      ...      ...    ...   
    2020-04-21 14:24:00   6156.4  2840.0  2008.2  4636.0  21155.4   5180.6  666.6   
    2020-04-21 16:48:00   6182.8  2856.5  2024.9  4636.0  21209.8   5205.2  670.2   
    2020-04-21 19:12:00   6209.2  2873.0  2041.6  4636.0  21264.2   5229.8  673.8   
    2020-04-21 21:36:00   6235.6  2889.5  2058.3  4636.0  21318.6   5254.4  677.4   
    2020-04-22 00:00:00   6262.0  2906.0  2075.0  4636.0  21373.0   5279.0  681.0   
    
                         Indonesia    Iran  Ireland    Italy  Mexico  Netherlands  \
    date                                                                            
    2020-02-26 00:00:00        NaN    19.0      NaN     12.0     NaN          NaN   
    2020-02-26 02:24:00        NaN    19.7      NaN     12.5     NaN          NaN   
    2020-02-26 04:48:00        NaN    20.4      NaN     13.0     NaN          NaN   
    2020-02-26 07:12:00        NaN    21.1      NaN     13.5     NaN          NaN   
    2020-02-26 09:36:00        NaN    21.8      NaN     14.0     NaN          NaN   
    ...                        ...     ...      ...      ...     ...          ...   
    2020-04-21 14:24:00      627.4  5353.4    753.4  24910.2   799.0       4012.4   
    2020-04-21 16:48:00      629.3  5362.8    757.3  24953.9   813.5       4026.3   
    2020-04-21 19:12:00      631.2  5372.2    761.2  24997.6   828.0       4040.2   
    2020-04-21 21:36:00      633.1  5381.6    765.1  25041.3   842.5       4054.1   
    2020-04-22 00:00:00      635.0  5391.0    769.0  25085.0   857.0       4068.0   
    
                         Portugal    Spain  Sweden  Switzerland  Turkey      USA  \
    date                                                                           
    2020-02-26 00:00:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 02:24:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 04:48:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 07:12:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 09:36:00       NaN      NaN     NaN          NaN     NaN      NaN   
    ...                       ...      ...     ...          ...     ...      ...   
    2020-04-21 14:24:00     775.8  21543.0  1868.2       1496.6  2329.2  45755.6   
    2020-04-21 16:48:00     778.1  21586.5  1885.4       1499.7  2340.9  45973.7   
    2020-04-21 19:12:00     780.4  21630.0  1902.6       1502.8  2352.6  46191.8   
    2020-04-21 21:36:00     782.7  21673.5  1919.8       1505.9  2364.3  46409.9   
    2020-04-22 00:00:00     785.0  21717.0  1937.0       1509.0  2376.0  46628.0   
    
                         United Kingdom  
    date                                 
    2020-02-26 00:00:00             NaN  
    2020-02-26 02:24:00             NaN  
    2020-02-26 04:48:00             NaN  
    2020-02-26 07:12:00             NaN  
    2020-02-26 09:36:00             NaN  
    ...                             ...  
    2020-04-21 14:24:00         17841.8  
    2020-04-21 16:48:00         17919.1  
    2020-04-21 19:12:00         17996.4  
    2020-04-21 21:36:00         18073.7  
    2020-04-22 00:00:00         18151.0  
    
    [561 rows x 20 columns], interpolate_period=True, steps_per_period=10, period_length=500, period_fmt='%d/%m/%Y', figsize=array([7.18229167, 3.5       ]), title=None, fig=<Figure size 1034x504 with 1 Axes>, cmap='dark24', tick_label_size=7, period_label=True, dpi=144, kwargs={}, orientation='h', sort='desc', label_bars=True, bar_label_size=7, n_visible=20)



### Currently Supported Chart Types

`pandas_alive` current supports:

- [Horizontal Bar Charts](#horizontal-bar-charts)
- [Vertical Bar Charts](#vertical-bar-charts)
- [Line Charts](#line-charts)

#### Horizontal Bar Charts


```
import pandas_alive

covid_df = pandas_alive.load_dataset()

covid_df.plot_animated(filename='example-barh-chart.gif')
```

    Generating BarChart, plotting ['Belgium', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Indonesia', 'Iran', 'Ireland', 'Italy', 'Mexico', 'Netherlands', 'Portugal', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'USA', 'United Kingdom']





    BarChart(df=                     Belgium  Brazil  Canada   China   France  Germany  India  \
    date                                                                            
    2020-02-26 00:00:00      NaN     NaN     NaN  2717.0      2.0      NaN    NaN   
    2020-02-26 02:24:00      NaN     NaN     NaN  2719.9      2.0      NaN    NaN   
    2020-02-26 04:48:00      NaN     NaN     NaN  2722.8      2.0      NaN    NaN   
    2020-02-26 07:12:00      NaN     NaN     NaN  2725.7      2.0      NaN    NaN   
    2020-02-26 09:36:00      NaN     NaN     NaN  2728.6      2.0      NaN    NaN   
    ...                      ...     ...     ...     ...      ...      ...    ...   
    2020-04-21 14:24:00   6156.4  2840.0  2008.2  4636.0  21155.4   5180.6  666.6   
    2020-04-21 16:48:00   6182.8  2856.5  2024.9  4636.0  21209.8   5205.2  670.2   
    2020-04-21 19:12:00   6209.2  2873.0  2041.6  4636.0  21264.2   5229.8  673.8   
    2020-04-21 21:36:00   6235.6  2889.5  2058.3  4636.0  21318.6   5254.4  677.4   
    2020-04-22 00:00:00   6262.0  2906.0  2075.0  4636.0  21373.0   5279.0  681.0   
    
                         Indonesia    Iran  Ireland    Italy  Mexico  Netherlands  \
    date                                                                            
    2020-02-26 00:00:00        NaN    19.0      NaN     12.0     NaN          NaN   
    2020-02-26 02:24:00        NaN    19.7      NaN     12.5     NaN          NaN   
    2020-02-26 04:48:00        NaN    20.4      NaN     13.0     NaN          NaN   
    2020-02-26 07:12:00        NaN    21.1      NaN     13.5     NaN          NaN   
    2020-02-26 09:36:00        NaN    21.8      NaN     14.0     NaN          NaN   
    ...                        ...     ...      ...      ...     ...          ...   
    2020-04-21 14:24:00      627.4  5353.4    753.4  24910.2   799.0       4012.4   
    2020-04-21 16:48:00      629.3  5362.8    757.3  24953.9   813.5       4026.3   
    2020-04-21 19:12:00      631.2  5372.2    761.2  24997.6   828.0       4040.2   
    2020-04-21 21:36:00      633.1  5381.6    765.1  25041.3   842.5       4054.1   
    2020-04-22 00:00:00      635.0  5391.0    769.0  25085.0   857.0       4068.0   
    
                         Portugal    Spain  Sweden  Switzerland  Turkey      USA  \
    date                                                                           
    2020-02-26 00:00:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 02:24:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 04:48:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 07:12:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 09:36:00       NaN      NaN     NaN          NaN     NaN      NaN   
    ...                       ...      ...     ...          ...     ...      ...   
    2020-04-21 14:24:00     775.8  21543.0  1868.2       1496.6  2329.2  45755.6   
    2020-04-21 16:48:00     778.1  21586.5  1885.4       1499.7  2340.9  45973.7   
    2020-04-21 19:12:00     780.4  21630.0  1902.6       1502.8  2352.6  46191.8   
    2020-04-21 21:36:00     782.7  21673.5  1919.8       1505.9  2364.3  46409.9   
    2020-04-22 00:00:00     785.0  21717.0  1937.0       1509.0  2376.0  46628.0   
    
                         United Kingdom  
    date                                 
    2020-02-26 00:00:00             NaN  
    2020-02-26 02:24:00             NaN  
    2020-02-26 04:48:00             NaN  
    2020-02-26 07:12:00             NaN  
    2020-02-26 09:36:00             NaN  
    ...                             ...  
    2020-04-21 14:24:00         17841.8  
    2020-04-21 16:48:00         17919.1  
    2020-04-21 19:12:00         17996.4  
    2020-04-21 21:36:00         18073.7  
    2020-04-22 00:00:00         18151.0  
    
    [561 rows x 20 columns], interpolate_period=True, steps_per_period=10, period_length=500, period_fmt='%d/%m/%Y', figsize=array([7.18229167, 3.5       ]), title=None, fig=<Figure size 1034x504 with 1 Axes>, cmap='dark24', tick_label_size=7, period_label=True, dpi=144, kwargs={}, orientation='h', sort='desc', label_bars=True, bar_label_size=7, n_visible=20)



![Example Barh Chart](examples/example-barh-chart.gif)

#### Vertical Bar Charts


```
import pandas_alive

covid_df = pandas_alive.load_dataset()

covid_df.plot_animated(filename='examples/example-barv-chart.gif',orientation='v')
```

    Generating BarChart, plotting ['Belgium', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Indonesia', 'Iran', 'Ireland', 'Italy', 'Mexico', 'Netherlands', 'Portugal', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'USA', 'United Kingdom']





    BarChart(df=                     Belgium  Brazil  Canada   China   France  Germany  India  \
    date                                                                            
    2020-02-26 00:00:00      NaN     NaN     NaN  2717.0      2.0      NaN    NaN   
    2020-02-26 02:24:00      NaN     NaN     NaN  2719.9      2.0      NaN    NaN   
    2020-02-26 04:48:00      NaN     NaN     NaN  2722.8      2.0      NaN    NaN   
    2020-02-26 07:12:00      NaN     NaN     NaN  2725.7      2.0      NaN    NaN   
    2020-02-26 09:36:00      NaN     NaN     NaN  2728.6      2.0      NaN    NaN   
    ...                      ...     ...     ...     ...      ...      ...    ...   
    2020-04-21 14:24:00   6156.4  2840.0  2008.2  4636.0  21155.4   5180.6  666.6   
    2020-04-21 16:48:00   6182.8  2856.5  2024.9  4636.0  21209.8   5205.2  670.2   
    2020-04-21 19:12:00   6209.2  2873.0  2041.6  4636.0  21264.2   5229.8  673.8   
    2020-04-21 21:36:00   6235.6  2889.5  2058.3  4636.0  21318.6   5254.4  677.4   
    2020-04-22 00:00:00   6262.0  2906.0  2075.0  4636.0  21373.0   5279.0  681.0   
    
                         Indonesia    Iran  Ireland    Italy  Mexico  Netherlands  \
    date                                                                            
    2020-02-26 00:00:00        NaN    19.0      NaN     12.0     NaN          NaN   
    2020-02-26 02:24:00        NaN    19.7      NaN     12.5     NaN          NaN   
    2020-02-26 04:48:00        NaN    20.4      NaN     13.0     NaN          NaN   
    2020-02-26 07:12:00        NaN    21.1      NaN     13.5     NaN          NaN   
    2020-02-26 09:36:00        NaN    21.8      NaN     14.0     NaN          NaN   
    ...                        ...     ...      ...      ...     ...          ...   
    2020-04-21 14:24:00      627.4  5353.4    753.4  24910.2   799.0       4012.4   
    2020-04-21 16:48:00      629.3  5362.8    757.3  24953.9   813.5       4026.3   
    2020-04-21 19:12:00      631.2  5372.2    761.2  24997.6   828.0       4040.2   
    2020-04-21 21:36:00      633.1  5381.6    765.1  25041.3   842.5       4054.1   
    2020-04-22 00:00:00      635.0  5391.0    769.0  25085.0   857.0       4068.0   
    
                         Portugal    Spain  Sweden  Switzerland  Turkey      USA  \
    date                                                                           
    2020-02-26 00:00:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 02:24:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 04:48:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 07:12:00       NaN      NaN     NaN          NaN     NaN      NaN   
    2020-02-26 09:36:00       NaN      NaN     NaN          NaN     NaN      NaN   
    ...                       ...      ...     ...          ...     ...      ...   
    2020-04-21 14:24:00     775.8  21543.0  1868.2       1496.6  2329.2  45755.6   
    2020-04-21 16:48:00     778.1  21586.5  1885.4       1499.7  2340.9  45973.7   
    2020-04-21 19:12:00     780.4  21630.0  1902.6       1502.8  2352.6  46191.8   
    2020-04-21 21:36:00     782.7  21673.5  1919.8       1505.9  2364.3  46409.9   
    2020-04-22 00:00:00     785.0  21717.0  1937.0       1509.0  2376.0  46628.0   
    
                         United Kingdom  
    date                                 
    2020-02-26 00:00:00             NaN  
    2020-02-26 02:24:00             NaN  
    2020-02-26 04:48:00             NaN  
    2020-02-26 07:12:00             NaN  
    2020-02-26 09:36:00             NaN  
    ...                             ...  
    2020-04-21 14:24:00         17841.8  
    2020-04-21 16:48:00         17919.1  
    2020-04-21 19:12:00         17996.4  
    2020-04-21 21:36:00         18073.7  
    2020-04-22 00:00:00         18151.0  
    
    [561 rows x 20 columns], interpolate_period=True, steps_per_period=10, period_length=500, period_fmt='%d/%m/%Y', figsize=array([6.85416667, 3.84114583]), title=None, fig=<Figure size 986x552 with 1 Axes>, cmap='dark24', tick_label_size=7, period_label=True, dpi=144, kwargs={}, orientation='v', sort='desc', label_bars=True, bar_label_size=7, n_visible=20)



![Example Barv Chart](examples/example-barv-chart.gif)

#### Line Charts

With as many lines as data columns in the DataFrame.


```
import pandas_alive

covid_df = pandas_alive.load_dataset()

covid_df.diff().fillna(0).plot_animated(filename='examples/example-line-chart.gif',kind='line')
```

    Generating LineChart, plotting ['Belgium', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Indonesia', 'Iran', 'Ireland', 'Italy', 'Mexico', 'Netherlands', 'Portugal', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'USA', 'United Kingdom']





    LineChart(df=                     Belgium  Brazil  Canada  China  France  Germany  India  \
    date                                                                          
    2020-02-26 00:00:00      0.0     0.0     0.0    0.0     0.0      0.0    0.0   
    2020-02-26 02:24:00      0.0     0.0     0.0    2.9     0.0      0.0    0.0   
    2020-02-26 04:48:00      0.0     0.0     0.0    5.8     0.0      0.0    0.0   
    2020-02-26 07:12:00      0.0     0.0     0.0    8.7     0.0      0.0    0.0   
    2020-02-26 09:36:00      0.0     0.0     0.0   11.6     0.0      0.0    0.0   
    ...                      ...     ...     ...    ...     ...      ...    ...   
    2020-04-21 14:24:00    226.4   160.6   173.4    0.0   541.2    216.0   42.8   
    2020-04-21 16:48:00    235.8   161.7   171.8    0.0   541.9    223.5   41.1   
    2020-04-21 19:12:00    245.2   162.8   170.2    0.0   542.6    231.0   39.4   
    2020-04-21 21:36:00    254.6   163.9   168.6    0.0   543.3    238.5   37.7   
    2020-04-22 00:00:00    264.0   165.0   167.0    0.0   544.0    246.0   36.0   
    
                         Indonesia  Iran  Ireland  Italy  Mexico  Netherlands  \
    date                                                                        
    2020-02-26 00:00:00        0.0   0.0      0.0    0.0     0.0          0.0   
    2020-02-26 02:24:00        0.0   0.7      0.0    0.5     0.0          0.0   
    2020-02-26 04:48:00        0.0   1.4      0.0    1.0     0.0          0.0   
    2020-02-26 07:12:00        0.0   2.1      0.0    1.5     0.0          0.0   
    2020-02-26 09:36:00        0.0   2.8      0.0    2.0     0.0          0.0   
    ...                        ...   ...      ...    ...     ...          ...   
    2020-04-21 14:24:00       21.8  91.6     40.6  475.8    97.4        149.4   
    2020-04-21 16:48:00       21.1  92.2     40.2  466.1   109.3        146.8   
    2020-04-21 19:12:00       20.4  92.8     39.8  456.4   121.2        144.2   
    2020-04-21 21:36:00       19.7  93.4     39.4  446.7   133.1        141.6   
    2020-04-22 00:00:00       19.0  94.0     39.0  437.0   145.0        139.0   
    
                         Portugal  Spain  Sweden  Switzerland  Turkey     USA  \
    date                                                                        
    2020-02-26 00:00:00       0.0    0.0     0.0          0.0     0.0     0.0   
    2020-02-26 02:24:00       0.0    0.0     0.0          0.0     0.0     0.0   
    2020-02-26 04:48:00       0.0    0.0     0.0          0.0     0.0     0.0   
    2020-02-26 07:12:00       0.0    0.0     0.0          0.0     0.0     0.0   
    2020-02-26 09:36:00       0.0    0.0     0.0          0.0     0.0     0.0   
    ...                       ...    ...     ...          ...     ...     ...   
    2020-04-21 14:24:00      24.6  433.0   177.2         38.2   117.8  2248.6   
    2020-04-21 16:48:00      24.2  433.5   175.9         36.4   117.6  2231.7   
    2020-04-21 19:12:00      23.8  434.0   174.6         34.6   117.4  2214.8   
    2020-04-21 21:36:00      23.4  434.5   173.3         32.8   117.2  2197.9   
    2020-04-22 00:00:00      23.0  435.0   172.0         31.0   117.0  2181.0   
    
                         United Kingdom  
    date                                 
    2020-02-26 00:00:00             0.0  
    2020-02-26 02:24:00             0.0  
    2020-02-26 04:48:00             0.0  
    2020-02-26 07:12:00             0.0  
    2020-02-26 09:36:00             0.0  
    ...                             ...  
    2020-04-21 14:24:00           795.0  
    2020-04-21 16:48:00           789.5  
    2020-04-21 19:12:00           784.0  
    2020-04-21 21:36:00           778.5  
    2020-04-22 00:00:00           773.0  
    
    [561 rows x 20 columns], interpolate_period=True, steps_per_period=10, period_length=500, period_fmt='%d/%m/%Y', figsize=array([6.78819444, 3.5       ]), title=None, fig=<Figure size 976x504 with 1 Axes>, cmap='dark24', tick_label_size=7, period_label=True, dpi=144, kwargs={}, line_width=2)



![Example Line Chart](examples/example-line-chart.gif)

### Multiple Charts

`pandas_alive` supports multiple animated charts in a single visualisation.

- Create a list of all charts to include in animation
- Use `animate_multiple_plots` with a `filename` and the list of charts (this will use `matplotlib.subplots`)
- Done!


```
import pandas_alive

covid_df = pandas_alive.load_dataset()

animated_line_chart = covid_df.diff().fillna(0).plot_animated(kind='line',period_label=False)

animated_bar_chart = covid_df.plot_animated(kind='barh',n_visible=10)

pandas_alive.animate_multiple_plots('examples/example-bar-and-line-chart.gif',[animated_bar_chart,animated_line_chart])
```

![Example Bar & Line Chart](examples/example-bar-and-line-chart.gif)


```
import pandas_alive

urban_df = pandas_alive.load_dataset("urban_pop")

animated_line_chart = (
    urban_df.sum(axis=1)
    .pct_change()
    .dropna()
    .mul(100)
    .plot_animated(kind="line", title="Total % Change in Population",period_label=False)
)

animated_bar_chart = urban_df.plot_animated(kind='barh',n_visible=10,title='Top 10 Populous Countries')

pandas_alive.animate_multiple_plots('examples/example-bar-and-line-urban-chart.gif',[animated_bar_chart,animated_line_chart],title='Urban Population 1977 - 2018')
```

    Generating LineChart, plotting ['0']
    Generating BarChart, plotting ['United States', 'India', 'China', 'Ethiopia', 'Poland', 'Malaysia', 'Peru', 'Venezuela', 'Iraq', 'Saudi Arabia', 'Canada', 'Algeria', 'Ukraine', 'Vietnam', 'Thailand', 'Congo, Dem. Rep.', 'Spain', 'South Africa', 'Colombia', 'Argentina', 'Egypt', 'South Korea', 'Italy', 'Philippines', 'France', 'United Kingdom', 'Bangladesh', 'Iran', 'Turkey', 'Germany', 'Pakistan', 'Nigeria', 'Mexico', 'Russia', 'Japan', 'Indonesia', 'Brazil']


![Urban Population Bar & Line Chart](examples/example-bar-and-line-urban-chart.gif)

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
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- See more at <https://matplotlib.org/3.2.1/api/animation_api.html#writer-classes>

## Documentation

Documentation is provided at <https://jackmckew.github.io/pandas_alive/>

## Contributing

Pull requests are welcome! Please help to cover more and more chart types!
