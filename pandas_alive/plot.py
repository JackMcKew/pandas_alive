import pandas as pd
from pandas.core.base import PandasObject

def plot(input_df,settings=None,**kwargs):
    print("Implement Plotting method")

##############################################################################
########### Class to add Animated plotting methods to Pandas DataFrame
##############################################################################
# Inspiration: https://github.com/PatrikHlobil/Pandas-Bokeh/blob/cb241ea570a0a2ea3d0c7055fbe79bbdd06cc712/pandas_bokeh/plot.py#L1759


class BasePlotMethods(PandasObject):
    def __init__(self, data):
        self._parent = data  # can be Series or DataFrame

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

class AnimatedAccessor(BasePlotMethods):
    
    def __call__(self, *args, **kwargs):
        return plot(self.df, *args, **kwargs)

    @property
    def df(self):

        return self._parent

    def barh(self, x: str = None, y:str=None, **kwds):
        """ Make an animated horizontal bar plot.

        Args:
            x (str, optional): label or position. Defaults to DataFrame.index. Column to be used on categories.
            y (str, optional): label or position. Defaults to All numeric columns in DataFrame. Column to be plotted from the DataFrame

        Returns:
            [type]: [description]
        """
        
        return self(kind="barh", x=x, y=y, **kwds)


def load_dataset(name: str='covid19') -> pd.DataFrame:
    """ Returns a pandas DataFrame suitable for immediate use in `pandas-alive`

    Args:
        name (str, optional): Name of dataset to load. Either 'covid19' or 'urban_pop'. Defaults to 'covid19'.

    Returns:
        pd.DataFrame: Loaded DataFrame
    """
    
    return pd.read_csv(f'https://raw.githubusercontent.com/JackMcKew/pandas-alive/master/data/{name}.csv', 
                       index_col='date', parse_dates=['date'])