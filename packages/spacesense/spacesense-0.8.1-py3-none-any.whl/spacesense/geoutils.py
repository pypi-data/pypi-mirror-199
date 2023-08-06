import logging

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from shapely.geometry import Point

logger = logging.getLogger(__name__)


def measure_distance(ds: xr.Dataset, SCL_val: int, lon: float, lat: float, plot: bool = True) -> float:
    """
    Function to calculate the distance from a specified longitude and latitude to the scene classification specified. The scene classification is taken from the first index on the Sentinel-2 SCL
    band in the fused result. The function returns the distance in meters, and plots the distance in a circle around the specified location.

    To use this function, you must pass a Sentinel-2 dataset with the SCL band already fused. Please ensure that clouds are minimal or nonexistant,
    as that can impact the location of the scene classificaitons in the SCL band.

    Args:
        ds (xr.Dataset): Dataset to measure
        SCL_val (int): Sentinel SCL band number representing classification to measure distance to
        lon (float): Longitude of point of interest to measure from
        lat (float): Latitude of point of interest to measure from
        plot (bool): Plot figure of distance measure

    :rtype: float

    Returns:
        Minimum distance from point of interest to the specified classification
    """
    if "spatial_ref" in ds.coords:
        ds = ds.drop(["spatial_ref"])
    if "time" in ds.coords:
        ds = ds.drop(["time"])
    ds["mask_val"] = (ds["S2_SCL"][0] == SCL_val) * 1

    # Polygonize
    x, y, mask_val = ds.x.values, ds.y.values, ds["mask_val"].values
    x, y = np.meshgrid(x, y)
    x, y, mask_val = x.flatten(), y.flatten(), mask_val.flatten()

    df = pd.DataFrame.from_dict({"mask_val": mask_val, "x": x, "y": y})
    threshold = 0.5
    df = df[df["mask_val"] > threshold]
    vector = gpd.GeoDataFrame(geometry=gpd.GeoSeries.from_xy(df["x"], df["y"]), crs="EPSG:4326")
    vector = vector.to_crs("EPSG:3857")
    vector = vector.buffer(5, cap_style=3)
    loc = Point(lon, lat)
    gdf = gpd.GeoDataFrame({"location": [1], "geometry": [loc]}, crs="EPSG:4326")
    gdf = gdf.to_crs(3857)
    vector = vector.to_crs(3857)
    wat_dist = vector.distance(gdf["geometry"][0])
    min_dist = round(min(wat_dist), 2)
    logger.info(f"Minimal distance to nearest specified classification: {min_dist} [m]")

    # Plot
    if plot is True:
        fig, ax = plt.subplots(1, 1)
        circle1 = plt.Circle((gdf["geometry"].x, gdf["geometry"].y), min_dist, fill=False)
        ax.add_patch(circle1)
        vector.plot(ax=ax)
        gdf.plot(color="None", edgecolor="red", linewidth=2, zorder=1, ax=ax)
        plt.show()

    return min_dist
