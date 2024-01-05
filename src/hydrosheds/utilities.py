import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

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


def save_clipped_shp(
    url:str, out_dir:Path, boundary_gdf:gpd.GeoDataFrame=extent_from_lads()
    ) -> None:
    """Download Hydroshed shapefile to tmp, clip to extent & write to file.

    Expects crs EPSG:4326. Works with Basins & rivers.

    Parameters
    ----------
    url : str
        Hydrosheds url for shapefile. Expects zip archive.
    out_dir : Path
        Parent directory to write found shapefiles to.
    boundary_gdf : gpd.GeoDataFrame, optional
        The extent of interest to clip the shapefiles using intersection, by
        default extent_from_lads()

    Returns
    -------
    None
        Used for side effects.
    """
    with TemporaryDirectory() as tmp:
        # download the zip file, possibly large in case of basins ~400M
        dest_zip = os.path.join(tmp, "shapefile.zip")
        subprocess.run(["curl", url, "-o", dest_zip ])
        # unzip the data to tmp folder
        subprocess.run(["unzip", dest_zip, "-d", tmp])
        # shapefile lint in archives, target .shp only, works for cases where
        # shpfiles are in root of zip archive
        shp = [f for f in os.listdir(tmp) if f.endswith(".shp")] 
        shp_loc = tmp
        if len(shp) == 0:
            # shapefiles contained in a directory with pattern"*_shp"
            shp_parent = [d for d in os.listdir(tmp) if d.endswith("_shp")][0]
            shp_loc = os.path.join(tmp, shp_parent)
            shp = [f for f in os.listdir(shp_loc) if f.endswith(".shp")]

        # get full paths to all shape files
        shp = sorted([os.path.join(shp_loc, f) for f in shp])
        #read in each shapefile as gdf
        n_shp = len(shp)
        for i, f in enumerate(shp, start=1):
            print(f"Reading {i}/{n_shp} shapefiles")
            hydroshed_feature = gpd.read_file(f, crs=4326)
            # need to clip the shapefiles to the boundary_gdf extent
            clipped_feature = gpd.overlay(
                hydroshed_feature,
                boundary_gdf,
                how="intersection",
                make_valid=True)
            # If the coarser shapefiles are too large for the boundary extent, 
            # only 1 row will be returned. Sensible to remove gdfs with 1 row.
            if len(clipped_feature) > 1:
                target_pth = os.path.join(
                    out_dir,
                    os.path.basename(f).replace(".shp", ".pkl")
                    )
                print(f"Writing filtered shapefile to {target_pth}")
                clipped_feature.to_pickle(target_pth)
    return None
    