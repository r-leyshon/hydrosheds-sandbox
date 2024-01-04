import requests
import geopandas as gpd
from pyprojroot import here
import subprocess
from  tempfile import TemporaryDirectory
import os
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
with TemporaryDirectory(dir=here("data/hydrosheds-eu/")) as tmp:
    subprocess.run(["unzip", dest_zip, "-d", tmp])
    print("\n".join(os.listdir(tmp)))
