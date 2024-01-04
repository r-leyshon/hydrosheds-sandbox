from pyprojroot import here
import requests
import geopandas as gpd

ENDPOINT = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_May_2023_UK_BGC_V2/FeatureServer/0/query"

PARAMS = {
    "where": "LAD23CD like 'W%'", # get only welsh LADs
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
gdf = gdf[["geometry", "LAD23CD", "LAD23NM", "LAD23NMW"]]
# write to pickle
gdf.to_pickle(here("data/boundaries/Wales-LAD23.pkl"))
