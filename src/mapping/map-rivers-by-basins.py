import pathlib

import pandas as pd
import geopandas as gpd
from pyprojroot import here
from matplotlib import colormaps, pyplot as plt
import numpy as np

# define the directories
LVL="07"
basins_pkl = here(f"data/hydrosheds-eu/welsh-basins/hybas_lake_eu_lev{LVL}_v1c.pkl")
rivers_pkl = here("data/hydrosheds-eu/welsh-rivers/HydroRIVERS_v10_eu.pkl")

# 1. import the target pickles
basins = pd.read_pickle(basins_pkl)
rivers = pd.read_pickle(rivers_pkl)
basins = gpd.GeoDataFrame(basins, crs=4326)
rivers = gpd.GeoDataFrame(rivers, crs=4326)
# calculate total length in km
river_len = sum(rivers["LENGTH_KM"])

rivers_by_basin = gpd.overlay(rivers,basins, how="intersection", keep_geom_type=False)
# rivers_by_basin["ORD_FLOW"].unique()
# [array([7, 6, 5, 4])]
# Define conditions and values
conditions = [
    (rivers_by_basin["ORD_FLOW"] == 7),
    (rivers_by_basin["ORD_FLOW"] == 6),
    (rivers_by_basin["ORD_FLOW"] == 5),
    (rivers_by_basin["ORD_FLOW"] == 4),
]
values = [0.8, 0.6, 0.4, 0.2]
# equivalent to case_when
rivers_by_basin["width"] = np.select(conditions, values, default=0.0)

####### PLOT


def map_rivers(
    gdf:gpd.GeoDataFrame,
    color_on:str,
    palette:str,
    width_factor:int, 
    title:str,
    dims:tuple,
    plt_pth:pathlib.Path=None
    ) -> plt.axes:
    """Plot a map of rivers. Optionally write to file.

    If plt_pth is a pathlib.Path object, the map will be written, otherwise the
    map is shown.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        A geodataframe containing the river features overlayed by boundary ID.
    color_on : str
        The column to use for group colour.
    palette : str
        A valid palette key for matplotlib.colormap.
    width_factor : int
        The factor to multiply river width by for plotting purposes.
    title : str
        The text to show in the plot title.
    dims : tuple
        The dimensions of the plot output.
    plt_pth : pathlib.Path, optional
        If provided, the map will be writtent to disk, by default None

    Returns
    -------
    plt.axes
        A custom map with rivers coloured by basin.

    """
    fig, ax = plt.subplots(figsize=dims)
    fig.patch.set_facecolor("#232b2b")
    # plt.title(f"{title} in {palette.name}", color="white")
    plt.title(title, color="white")
    plt.tick_params(
        left=False, bottom=False, labelleft=False, labelbottom=False
        )
    ax.set_facecolor("#232b2b")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    m = gdf.plot(
        ax=ax,
        column=color_on,
        cmap=palette,
        linewidth=gdf["width"] * width_factor,
        alpha=gdf["width"],
        categorical=True,
        legend=False,
        )
    # Custom footnote
    footnote_text = "Data source: https://www.hydrosheds.org"
    ax.text(
        0.5,
        -0.05,
        footnote_text,
        color="white",
        fontsize=10,
        ha="center",
        va="center",
        transform=ax.transAxes,
    )
    if plt_pth:
        plt.savefig(
            plt_pth, dpi=600, bbox_inches="tight", pad_inches=0.3,
            )
    else:
        plt.show()

    return m

river_m = map_rivers(
    rivers_by_basin,
    color_on="HYBAS_ID",
    palette="Accent",
    width_factor=2.0,
    title="Welsh Rivers by Basin",
    dims=(7,7),
    # plt_pth=None,
    plt_pth=here("outputs/wales/welsh-rivers-by-basin.png")
    )


# comparing colormaps
# for pal in list(colormaps.keys()):
#     river_m = map_rivers(
#         gdf=rivers_by_basin,
#         color_on="HYBAS_ID",
#         palette=colormaps[pal],
#         width_factor=2.8,
#         title=f"Welsh Rivers",
#         dims=(7, 7)
#         )
# fave_pals = [
#     "GnBu",
#     "PuBu",
#     "Spectral",
#     "cool",
#     "Accent",
#     "Pastel1",
#     "Pastel2",
#     "Set2",
#     ]
# 
# for pal in list(fave_pals):
#     river_m = map_rivers(
#         gdf=rivers_by_basin,
#         color_on="HYBAS_ID",
#         palette=colormaps[pal],
#         width_factor=2.8,
#         title=f"Welsh Rivers",
#         dims=(7, 7),
#         )
