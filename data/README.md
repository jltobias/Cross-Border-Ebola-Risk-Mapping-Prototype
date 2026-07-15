# Data directory

This folder is intentionally lightweight. Store sensitive or large data outside
Git unless the project has an approved private data-governance arrangement.

Recommended layout:

```text
data/raw/         # downloaded source data, not committed
data/interim/     # standardized rasters/vectors, not committed
data/processed/   # model-ready features, not committed
data/demo/         # synthetic examples safe to commit if desired
```

The notebooks expect the existing repository `GIS/` folder to contain project
layers. Use `scripts/build_layer_catalog.py` to inventory those files.
