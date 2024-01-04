import requests
import geopandas as gpd
from pyprojroot import here
import subprocess
from  tempfile import TemporaryDirectory
import os
import glob
# include all river levels
EU_BASINS_URL = "https://data.hydrosheds.org/file/HydroBASINS/customized_with_lakes/hybas_lake_eu_lev01-12_v1c.zip"
# download the zip file (large, ~400M)
dest_zip = here("data/hydrosheds-eu/basins-lakes-eu-lev01-12.zip")
subprocess.run(
    [
        "curl",
        EU_BASINS_URL,
        "-o",
        dest_zip
        ])
# unzip the data to tmp folder
tmp_pth = here("data/hydrosheds-eu/")
with TemporaryDirectory(dir=tmp_pth) as tmp:
    subprocess.run(["unzip", dest_zip, "-d", tmp])
    shp = [f for f in os.listdir(tmp) if f.endswith(".shp")]
    shp = [os.path.join(tmp_pth, f) for f in shp]
    print(shp)
