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

from .base import load_dataset
from .geoplotting import geoplot
from .plotting import AnimatedAccessor, animate_multiple_plots, plot

version = "0.1.14"


plot_animated = CachedAccessor("plot_animated", AnimatedAccessor)
pd.DataFrame.plot_animated = plot_animated
pd.Series.plot_animated = plot

# Define plot_animated method for GeoPandas and Series:
try:
    import geopandas as gpd
    import descartes

    gpd.GeoDataFrame.plot_animated = geoplot
    gpd.GeoSeries.plot_animated = geoplot

except ImportError:
    pass
