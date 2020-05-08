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


```
import pandas as pd
import pandas_alive

elec_df = pd.read_csv("data/Aus_Elec_Gen_1980_2018.csv",index_col=0,parse_dates=[0],thousands=',')

elec_df.fillna(0).plot_animated('examples/example-electricity-generated-australia.gif',period_fmt="%Y",title='Australian Electricity Generation Sources 1980-2018')
```

    Generating BarChart, plotting ['  Black coal', '  Brown coal', '  Natural gas', '  Oil products', '  Other a', '  Biomass', '  Wind', '  Hydro', 'Large-scale solar PV', '  Small-scale solar PV', '  Geothermal']





    BarChart(df=                       Black coal    Brown coal    Natural gas  \
    index                                                            
    1989-01-01 00:00:00      87573.00     33594.000      14359.000   
    1989-02-06 12:36:00      87766.80     33839.400      14000.300   
    1989-03-15 01:12:00      87960.60     34084.800      13641.600   
    1989-04-20 13:48:00      88154.40     34330.200      13282.900   
    1989-05-27 02:24:00      88348.20     34575.600      12924.200   
    ...                           ...           ...            ...   
    2016-08-07 21:36:00     120264.48     39063.304      52487.534   
    2016-09-13 10:12:00     120596.51     38314.228      52825.498   
    2016-10-19 22:48:00     120928.54     37565.152      53163.462   
    2016-11-25 11:24:00     121260.57     36816.076      53501.426   
    2017-01-01 00:00:00     121592.60     36067.000      53839.390   
    
                           Oil products    Other a    Biomass       Wind  \
    index                                                                  
    1989-01-01 00:00:00        3552.000        0.0    750.000      0.000   
    1989-02-06 12:36:00        3536.400        0.0    751.900      0.000   
    1989-03-15 01:12:00        3520.800        0.0    753.800      0.000   
    1989-04-20 13:48:00        3505.200        0.0    755.700      0.000   
    1989-05-27 02:24:00        3489.600        0.0    757.600      0.000   
    ...                             ...        ...        ...        ...   
    2016-08-07 21:36:00        5266.596        0.0   3520.674  14032.448   
    2016-09-13 10:12:00        5265.597        0.0   3524.028  14271.691   
    2016-10-19 22:48:00        5264.598        0.0   3527.382  14510.934   
    2016-11-25 11:24:00        5263.599        0.0   3530.736  14750.177   
    2017-01-01 00:00:00        5262.600        0.0   3534.090  14989.420   
    
                             Hydro  Large-scale solar PV    Small-scale solar PV  \
    index                                                                          
    1989-01-01 00:00:00  14880.000                 0.000                    0.00   
    1989-02-06 12:36:00  15002.300                 0.000                    0.00   
    1989-03-15 01:12:00  15124.600                 0.000                    0.00   
    1989-04-20 13:48:00  15246.900                 0.000                    0.00   
    1989-05-27 02:24:00  15369.200                 0.000                    0.00   
    ...                        ...                   ...                     ...   
    2016-08-07 21:36:00  16017.248               873.508                 8313.12   
    2016-09-13 10:12:00  15972.641               907.026                 8465.43   
    2016-10-19 22:48:00  15928.034               940.544                 8617.74   
    2016-11-25 11:24:00  15883.427               974.062                 8770.05   
    2017-01-01 00:00:00  15838.820              1007.580                 8922.36   
    
                           Geothermal  
    index                              
    1989-01-01 00:00:00          0.00  
    1989-02-06 12:36:00          0.00  
    1989-03-15 01:12:00          0.00  
    1989-04-20 13:48:00          0.00  
    1989-05-27 02:24:00          0.00  
    ...                           ...  
    2016-08-07 21:36:00          0.20  
    2016-09-13 10:12:00          0.15  
    2016-10-19 22:48:00          0.10  
    2016-11-25 11:24:00          0.05  
    2017-01-01 00:00:00          0.00  
    
    [281 rows x 11 columns], interpolate_period=True, steps_per_period=10, period_length=500, period_fmt='%Y', figsize=array([7.45486111, 3.5       ]), title='Australian Electricity Generation Sources 1980-2018', fig=<Figure size 1072x504 with 1 Axes>, cmap='dark24', tick_label_size=7, period_label=True, dpi=144, kwargs={}, orientation='h', sort='desc', label_bars=True, bar_label_size=7, n_visible=11)



![Electricity Example Line Chart](examples/example-electricity-generated-australia.gif)

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

covid_df.diff().fillna(0).plot_animated(filename='examples/example-line-chart.gif',kind='line',period_label={'x':0.1,'y':0.9})
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
    
    [561 rows x 20 columns], interpolate_period=True, steps_per_period=10, period_length=500, period_fmt='%d/%m/%Y', figsize=array([6.78819444, 3.5       ]), title=None, fig=<Figure size 976x504 with 1 Axes>, cmap='dark24', tick_label_size=7, period_label={'x': 0.1, 'y': 0.9}, dpi=144, kwargs={}, line_width=2)



![Example Line Chart](examples/example-line-chart.gif)


#### Scatter Charts


```
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

    Generating ScatterChart, plotting ['Minimum temperature (Degree C)', 'Maximum temperature (Degree C)']





    ScatterChart(df=                               Minimum temperature (Degree C)  \
    Timestamp                                                       
    1957-12-31 00:00:00.000000000                       14.502727   
    1958-02-05 12:36:34.285714285                       14.565650   
    1958-03-14 01:13:08.571428571                       14.628573   
    1958-04-19 13:49:42.857142856                       14.691496   
    1958-05-26 02:26:17.142857142                       14.754419   
    ...                                                       ...   
    2020-08-06 21:33:42.857142784                       17.474473   
    2020-09-12 10:10:17.142856960                       17.803689   
    2020-10-18 22:46:51.428571392                       18.132906   
    2020-11-24 11:23:25.714285568                       18.462122   
    2020-12-31 00:00:00.000000000                       18.791339   
    
                                   Maximum temperature (Degree C)  
    Timestamp                                                      
    1957-12-31 00:00:00.000000000                       21.561212  
    1958-02-05 12:36:34.285714285                       21.543603  
    1958-03-14 01:13:08.571428571                       21.525994  
    1958-04-19 13:49:42.857142856                       21.508386  
    1958-05-26 02:26:17.142857142                       21.490777  
    ...                                                       ...  
    2020-08-06 21:33:42.857142784                       24.253680  
    2020-09-12 10:10:17.142856960                       24.437879  
    2020-10-18 22:46:51.428571392                       24.622078  
    2020-11-24 11:23:25.714285568                       24.806277  
    2020-12-31 00:00:00.000000000                       24.990476  
    
    [631 rows x 2 columns], interpolate_period=True, steps_per_period=10, period_length=500, period_fmt='%d/%m/%Y', figsize=array([8.01388889, 3.5       ]), title='Max & Min Temperature Newcastle, Australia', fig=<Figure size 1154x504 with 1 Axes>, cmap='dark24', tick_label_size=7, period_label=True, dpi=144, kwargs={}, size=2)



![Example Scatter Chart](examples/example-scatter-chart.gif)

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

    Generating LineChart, plotting ['Belgium', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Indonesia', 'Iran', 'Ireland', 'Italy', 'Mexico', 'Netherlands', 'Portugal', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'USA', 'United Kingdom']
    Generating BarChart, plotting ['Belgium', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Indonesia', 'Iran', 'Ireland', 'Italy', 'Mexico', 'Netherlands', 'Portugal', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'USA', 'United Kingdom']



![svg](README_files/README_18_1.svg)


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

animated_bar_chart = urban_df.plot_animated(kind='barh',n_visible=10,title='Top 10 Populous Countries',period_fmt="%Y")

pandas_alive.animate_multiple_plots('examples/example-bar-and-line-urban-chart.gif',[animated_bar_chart,animated_line_chart],title='Urban Population 1977 - 2018',adjust_subplot_top=0.85)
```

    Generating LineChart, plotting ['0']
    Generating BarChart, plotting ['United States', 'India', 'China', 'Ethiopia', 'Poland', 'Malaysia', 'Peru', 'Venezuela', 'Iraq', 'Saudi Arabia', 'Canada', 'Algeria', 'Ukraine', 'Vietnam', 'Thailand', 'Congo, Dem. Rep.', 'Spain', 'South Africa', 'Colombia', 'Argentina', 'Egypt', 'South Korea', 'Italy', 'Philippines', 'France', 'United Kingdom', 'Bangladesh', 'Iran', 'Turkey', 'Germany', 'Pakistan', 'Nigeria', 'Mexico', 'Russia', 'Japan', 'Indonesia', 'Brazil']



![svg](README_files/README_20_1.svg)


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


```

```
