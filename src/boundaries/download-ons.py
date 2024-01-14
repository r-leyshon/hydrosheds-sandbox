"""Download Welsh LA shapefiles from ONS open geo portal.

Writes to data/boundaries/.
"""
from pyprojroot import here
import requests
import geopandas as gpd

# ENDPOINT = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_May_2023_UK_BGC_V2/FeatureServer/0/query"
ENDPOINT = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Countries_December_2022_UK_BGC/FeatureServer/0/query?outFields=*&where=1%3D1"

PARAMS = {
    # "where": "LAD23CD like 'W%'", # get only welsh LADs
    "f": "geoJSON",
    "outSR": 4326,
    "outFields": "*" # don't get LAD23NM if you don't ask for this.
}
# handle response
resp = requests.get(ENDPOINT, params=PARAMS)
if resp.ok:
    content = resp.json()
else:
    raise requests.exceptions.HTTPError(f"{resp.status_code}: {resp.reason}")


gdf = gpd.GeoDataFrame.from_features(
            content["features"],
            crs=content["crs"]["properties"]["name"]
            # safest to get crs from response
            )
# drop unneeded columns
# gdf = gdf[["geometry", "LAD23CD", "LAD23NM", "LAD23NMW"]]
gdf = gdf[["geometry", "CTRY22CD", "CTRY22NM", "CTRY22NMW"]]
# write to pickle
# gdf.to_pickle(here("data/boundaries/Wales-LAD23.pkl"))
gdf.to_pickle(here("data/boundaries/uk-countries.pkl"))
