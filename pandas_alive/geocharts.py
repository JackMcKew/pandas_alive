""" Implementation of geoplots with Geopandas
"""

import datetime
import typing
from typing import Mapping

import attr
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.units as munits
import numpy as np
import pandas as pd
from matplotlib import colors, ticker, transforms
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Colormap

from ._base_chart import _BaseChart


@attr.s
class MapChart(_BaseChart):
    """
    Map chart using Geopandas

    Args:
        _BaseChart ([type]): Base chart for all chart classes

    Raises:
        ValueError: [description]
    """

    def __attrs_post_init__(self):
        """ Properties to be determined after initialization
        """
        # super().__attrs_post_init__()
        print(self.df)
        print(type(self.df))
        # self.colors = self.get_colors(self.cmap)
        # self._points: typing.Dict = {}
        # self.column_keys = self.df.columns.get_level_values(level=0).unique().tolist()
        # # self.data_cols = self.df.columns.get_level_values(level=1).unique().tolist()
        # self.mapping = {"x": self.x_data_label, "y": self.y_data_label}
        # if isinstance(self.size_data_label, str):
        #     self.mapping["size"] = self.size_data_label
        # if (
        #     isinstance(self.color_data_label, str)
        #     and self.color_data_label in self.column_keys
        # ):
        #     self.mapping["color"] = self.color_data_label
        # if self.x_data_label is None or self.y_data_label is None:
        #     raise ValueError("X Y labels must be provided at a minimum")
        # if not (
        #     self.x_data_label in self.column_keys
        #     and self.y_data_label in self.column_keys
        # ):
        #     raise ValueError(
        #         f"Provided keys must be in level 0 multi index, possible values: {self.column_keys}"
        #     )

    # def plot_point(self, i: int) -> None:
    #     """
    #     Plot points from MultiIndexed DataFrame

    #     Optionally size & colour can be provided and if so, the string provided must be present in the level 0 column labels

    #     Args:
    #         i (int): Frame to plot, will slice DataFrame at this index
    #     """
    #     if self.fixed_max:
    #         BBox = (
    #             self.df[self.mapping["x"]].values.min(),
    #             self.df[self.mapping["x"]].values.max(),
    #             self.df[self.mapping["y"]].values.min(),
    #             self.df[self.mapping["y"]].values.max(),
    #         )
    #         self.ax.set_xlim(BBox[0], BBox[1])
    #         self.ax.set_ylim(BBox[2], BBox[3])

    #     # TODO Add geopandas for map plots
    #     # self.ax = self.show_image(
    #     #     self.ax,
    #     #     "C:\\Users\\jackm\\Documents\\GitHub\\pandas-alive\\data\\nsw_map.png",
    #     #     extent=BBox,
    #     #     zorder=0,
    #     #     aspect="equal",
    #     # )

    #     for output_key, column_key in self.mapping.items():
    #         self._points[output_key] = self.df[column_key].iloc[i].values

    #     self.ax.scatter(
    #         self._points["x"],
    #         self._points["y"],
    #         s=self._points["size"]
    #         if isinstance(self.size_data_label, str)
    #         else self.size_data_label,
    #         c=self._points["color"]
    #         if isinstance(self.color_data_label, str)
    #         and self.color_data_label in self.data_cols
    #         else self.color_data_label,
    #         **self.kwargs,
    #     )

    # def anim_func(self, i: int) -> None:
    #     """ Animation function, removes all lines and updates legend/period annotation

    #     Args:
    #         i (int): Index of frame of animation
    #     """
    #     if self.enable_progress_bar:
    #         self.update_progress_bar()
    #     for path in self.ax.collections:
    #         path.remove()
    #     self.plot_point(i)
    #     if self.period_fmt:
    #         self.show_period(i)

    # def init_func(self) -> None:
    #     """ Initialization function for animation
    #     """
    #     self.ax.scatter([], [])
