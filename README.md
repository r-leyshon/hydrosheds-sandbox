# hydrosheds-sandbox
Experimenting with hydrosheds data

Working through [Milos makes maps](https://www.youtube.com/watch?v=HugGwjogPv0)
tutorial.
[Code here](https://github.com/milos-agathon/mapping-river-basins-with-r)

Code in the src folder used to produce below maps. Could be further generalised
to take a toml config with area of interest. However, on inspecting the data
with `geopandas.explore()`, the accuracy and coverage of the data were not
particularly great in the Welsh region.

<img src="/outputs/wales/welsh-rivers-by-basin.png" alt="Welsh rivers by river basins" width=400/>

<img src="/outputs/uk/uk-rivers-by-basin.png" alt="UK rivers by river basins" width=400/>
