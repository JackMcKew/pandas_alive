""" Create stunning, animated visualisations with matplotlib and pandas as easy as 'df.plot_animated()'.

Initialise Pandas_Alive functions as an accessor on Pandas DataFrames eg `df.plot_animated()`.
Registers plot_animated as an accessor for Pandas DataFrames and Series.

# POSSIBLE LINK PLOTTING.PY docs here

Must begin with a pandas DataFrame containing 'wide' data where:

- Every row represents a single period of time
- Each column holds the value for a particular category
- The index contains the time component (optional)

"""


# Register animated_plot accessor for Pandas DataFrames and Series:
import pandas as pd
from pandas.core.accessor import CachedAccessor
from .plotting import AnimatedAccessor, plot, animate_multiple_plots

from .base import load_dataset

version = "0.2.3"


plot_animated = CachedAccessor("plot_animated", AnimatedAccessor)
pd.DataFrame.plot_animated = plot_animated
pd.Series.plot_animated = plot

# Define plot_animated method for GeoPandas and Series:

try:
    import geopandas as gpd
    from .geoplotting import geoplot

    gpd.GeoDataFrame.plot_animated = geoplot
    gpd.GeoSeries.plot_animated = geoplot

except ImportError:
    pass
