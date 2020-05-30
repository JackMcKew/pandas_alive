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
import geopandas
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
        self.df = self.df.copy()

        # Convert all columns except geometry to datetime
        try:
            self.df = self.convert_data_cols_to_datetime(self.df)
            self.df = self.get_interpolated_geo_df(self.df)
        except:
            import warnings

            warnings.warn(
                "Pandas_Alive failed to convert columns to datetime, setting interpolate_period to False and retrying..."
            )
            self.interpolate_period = False
            self.df = self.get_interpolated_geo_df(self.df)

    def get_data_cols(self, gdf: geopandas.GeoDataFrame) -> typing.List:
        """
        Get data columns from GeoDataFrame (this excludes geometry)

        Args:
            gdf (geopandas.GeoDataFrame): Input GeoDataframe

        Returns:
            typing.List: List of columns except geometry
        """
        return gdf.loc[:, gdf.columns != "geometry"].columns.tolist()

    def convert_data_cols_to_datetime(
        self, gdf: geopandas.GeoDataFrame
    ) -> geopandas.GeoDataFrame:
        """
        Convert all data columns to datetime with `pd.to_datetime`

        Args:
            gdf (geopandas.GeoDataFrame): Input GeoDataFrame

        Returns:
            geopandas.GeoDataFrame: GeoDataFrame with data columns converted to `Timestamp`
        """
        converted_column_names = []
        for col in gdf.columns:
            if col != "geometry":
                col = pd.to_datetime(col)

            converted_column_names.append(col)
        gdf.columns = converted_column_names
        return gdf

    def get_interpolated_geo_df(
        self, gdf: geopandas.GeoDataFrame
    ) -> geopandas.GeoDataFrame:
        """
        Interpolates GeoDataFrame by splitting data from geometry, interpolating and joining back together

        Args:
            gdf (geopandas.GeoDataFrame): Input GeoDataFrame

        Returns:
            geopandas.GeoDataFrame: Interpolated GeoDataFrame
        """

        # Separate data from geometry
        temp_df = pd.DataFrame(gdf)
        temp_df = temp_df.drop("geometry", axis=1)
        temp_df = temp_df.T
        geometry_column = gdf.geometry

        # Interpolate data
        interpolated_df = super().get_interpolated_df(
            temp_df, self.steps_per_period, self.interpolate_period
        )

        # Rejoin data with geometry
        interpolated_df = interpolated_df.T
        interpolated_df["geometry"] = geometry_column

        return geopandas.GeoDataFrame(interpolated_df)

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
