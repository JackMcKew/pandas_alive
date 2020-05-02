from .plot import plot,AnimatedAccessor
from .base import load_dataset

# Register animated_plot accessor for Pandas DataFrames and Series:
import pandas as pd
from pandas.core.accessor import CachedAccessor

animated_plot = CachedAccessor("animated_plot", AnimatedAccessor)
pd.DataFrame.animated_plot = animated_plot
pd.Series.animated_plot = plot

