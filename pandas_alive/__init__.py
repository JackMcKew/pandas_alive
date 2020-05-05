from .plot import plot, AnimatedAccessor, animate_multiple_plots
from .base import load_dataset

version = "0.1.6"

# Register animated_plot accessor for Pandas DataFrames and Series:
import pandas as pd
from pandas.core.accessor import CachedAccessor

plot_animated = CachedAccessor("plot_animated", AnimatedAccessor)
pd.DataFrame.plot_animated = plot_animated
pd.Series.plot_animated = plot
