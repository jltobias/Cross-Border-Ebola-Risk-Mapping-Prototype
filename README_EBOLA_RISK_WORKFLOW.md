# Cross-Border Ebola Risk Mapping Notebook Scaffold

This scaffold adds a reproducible notebook workflow for ecological niche modeling,
spillover suitability, cross-border importation pressure, and South Sudan health
facility/catchment risk mapping along the DRC-South Sudan border corridor.

The workflow is designed to use local geospatial layers already stored in the
repository `GIS/` folder while also providing configuration placeholders for
external datasets such as WorldPop, Hansen Global Forest Change, Global Forest
Watch/WRI forest-loss drivers, GBIF bat occurrences, OSM roads/buildings/water,
ACLED conflict data, caves, mines, orchards, and other human-vector interface
layers.

## Important public-health framing

This repository is for preparedness analytics, surveillance planning, and
resource prioritization. It is not a diagnostic tool and should not be used to
stigmatize communities, facilities, occupational groups, displaced populations,
or wildlife habitats. Outputs should be reviewed with Ministry of Health,
surveillance, IPC, laboratory, community engagement, and data-governance teams
before operational use.

## What this scaffold adds

```text
configs/
  layer_catalog.yml             # local GIS and external data source manifest
  model_config.yml              # AOI, CRS, resolution, outputs, validation
  weights_baseline.yml          # deterministic weighted-overlay model weights
  scenarios.yml                 # stochastic and preparedness scenarios
  data_sensitivity.yml          # suggested sharing/handling classifications
notebooks/
  00_repository_orientation.ipynb
  01_data_inventory_gis_folder.ipynb
  02_area_of_interest_border_corridor.ipynb
  03_standardize_layers.ipynb
  04_feature_engineering_interface_layers.ipynb
  05_bat_reservoir_enm_elapid.ipynb
  06_importation_pressure_mobility_corridors.ipynb
  07_facility_catchment_vulnerability.ipynb
  08_deterministic_risk_index.ipynb
  09_stochastic_scenarios_uncertainty.ipynb
  10_validation_sensitivity_export.ipynb
notebooks_lite/
  00_jupyterlite_synthetic_risk_demo.ipynb
  01_jupyterlite_weight_sensitivity.ipynb
scripts/
  build_layer_catalog.py
  create_synthetic_demo_data.py
  run_synthetic_risk_demo.py
src/cberm/
  config.py, io.py, raster.py, vector.py, features.py, risk.py,
  enm.py, network.py, stochastic.py, plotting.py, validation.py
```

## Quick start

```bash
conda env create -f environment.yml
conda activate cberm-ebola-risk
pip install -e .
python scripts/build_layer_catalog.py --gis-root GIS --out data/interim/layer_inventory.csv
python scripts/create_synthetic_demo_data.py
python scripts/run_synthetic_risk_demo.py
jupyter lab
```

If you only want a browser/JupyterLite-friendly demonstration without GDAL,
rasterio, geopandas, or local files, open the notebooks in `notebooks_lite/`.
Those notebooks use synthetic tables and pure Python/pandas/numpy logic.

## Recommended modeling products

1. Spillover suitability surface: ecological and human-animal interface risk.
2. Importation pressure surface: outbreak pressure moving through corridors.
3. Facility/catchment vulnerability score: detection, isolation, referral, IPC.
4. Combined risk index: transparent deterministic weighted overlay.
5. Stochastic scenario ensemble: uncertainty intervals and scenario comparison.
6. Export package: GeoTIFFs, GeoPackages, facility tables, and method notes.

## Data governance notes

Do not commit sensitive line lists, personally identifiable records, precise
roost coordinates, exact vulnerable facility readiness gaps, or unreviewed case
locations to a public repository. Use synthetic data for public examples and keep
controlled datasets outside Git or in approved secure storage.

## Suggested sequence

1. Run `01_data_inventory_gis_folder.ipynb` to inventory current GIS holdings.
2. Complete `configs/layer_catalog.yml` for each local and external layer.
3. Build the AOI and corridor grid in `02_area_of_interest_border_corridor.ipynb`.
4. Standardize CRS/resolution/extent in `03_standardize_layers.ipynb`.
5. Build interface features in `04_feature_engineering_interface_layers.ipynb`.
6. Use `05_bat_reservoir_enm_elapid.ipynb` for ecological niche modeling.
7. Use `06_importation_pressure_mobility_corridors.ipynb` for network pressure.
8. Use `07_facility_catchment_vulnerability.ipynb` for preparedness metrics.
9. Use `08` and `09` to create deterministic and stochastic risk outputs.
10. Use `10` to validate, summarize uncertainty, and export deliverables.
