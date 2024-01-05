"""Download European river basin shapefiles from hydrosheds & write to file.  

Only writes shapefiles clipped to Welsh extent and retaining more than one row.
Destination folder is data/hydrosheds-eu/welsh-basins/."""
import subprocess
import os
from tempfile import TemporaryDirectory
from pathlib import Path

import geopandas as gpd
import pandas as pd
from pyprojroot import here

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


# boundary shapes saved to pickle in src/boundaries/download-ons.property
boundary = extent_from_lads()
# include all river levels
EU_BASINS_URL = "https://data.hydrosheds.org/file/HydroBASINS/customized_with_lakes/hybas_lake_eu_lev01-12_v1c.zip"

with TemporaryDirectory(dir=here("data/hydrosheds-eu/")) as tmp:
    # download the zip file (large, ~400M)
    dest_zip = os.path.join(tmp, "basins-lakes-eu-lev01-12.zip")
    # dest_zip = here("data/hydrosheds-eu/basins-lakes-eu-lev01-12.zip")
    subprocess.run(
        [
            "curl",
            EU_BASINS_URL,
            "-o",
            dest_zip
            ])
    # unzip the data to tmp folder
    subprocess.run(["unzip", dest_zip, "-d", tmp])
    # shapefile lint in archives, target .shp only
    shp = [f for f in os.listdir(tmp) if f.endswith(".shp")]
    shp = sorted([os.path.join(tmp, f) for f in shp])
    #read in each shapefile as gdf
    n_shp = len(shp)
    for i, f in enumerate(shp, start=1):
        print(f"Reading {i}/{n_shp} shapefiles")
        basin = gpd.read_file(f, crs=4326)
        # need to clip the shapefiles to the extent of Wales
        welsh_basins = gpd.overlay(
            boundary, basin, how="intersection", make_valid=True)
        # append to all_basins, only do this if the basin shapefile is at a
        # meaningful granularity. Many of the coarse shapefiles have basins
        # larger than the UK
        if len(welsh_basins) > 1:
            target_pth = os.path.join(
                here("data/hydrosheds-eu/welsh-basins/"),
                os.path.basename(f).replace(".shp", ".pkl")
                )
            print(f"Writing filtered shapefile to {target_pth}")
            welsh_basins.to_pickle(target_pth)
