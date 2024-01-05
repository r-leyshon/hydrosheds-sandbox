"""Download rivers & river basin shapefiles from hydrosheds, clip & write.  

Only writes shapefiles clipped to boundary extent and retaining more than one
row."""
import os

from pyprojroot import here

os.chdir(here("src/hydrosheds/"))
from utilities import save_clipped_shp

# boundary shapes saved to pickle in src/boundaries/download-ons.property
# boundary = extent_from_lads()
# include all river levels
EU_BASINS_URL = "https://data.hydrosheds.org/file/HydroBASINS/customized_with_lakes/hybas_lake_eu_lev01-12_v1c.zip"
EU_RIVERS_URL = "https://data.hydrosheds.org/file/HydroRIVERS/HydroRIVERS_v10_eu_shp.zip"
basins_out = here("data/hydrosheds-eu/welsh-basins/")
rivers_out = here("data/hydrosheds-eu/welsh-rivers/")
# write out clipped basins
save_clipped_shp(url=EU_BASINS_URL, out_dir=basins_out)
# write out clipped rivers
save_clipped_shp(url=EU_RIVERS_URL, out_dir=rivers_out)
