import geopandas as gpd
import pandas as pd
from pyprojroot import here
from pathlib import Path

def extent_from_lads(
    lad_pth: Path=here("data/boundaries/Wales-LAD23.pkl")
    ) -> gpd.GeoDataFrame:
    """Read in LAD shapefile & unary union to get extent.

    Parameters
    ----------
    lad_pth : Path, optional
        Path to the LAD shapefile, by default
        `here("data/boundaries/Wales-LAD23.pkl")`

    Returns
    -------
    gpd.GeoDataFrame
        Full extent of the LAD shapefiles.
    """
    boundaries = pd.read_pickle(lad_pth)
    boundaries = gpd.GeoDataFrame(boundaries, crs=4326)
    boundary = gpd.GeoDataFrame(
        {'id':[1],'geometry':[boundaries.unary_union]}, crs=4326)
    return boundary
    