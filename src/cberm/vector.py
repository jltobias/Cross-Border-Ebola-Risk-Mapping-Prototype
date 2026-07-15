from __future__ import annotations

from pathlib import Path


def require_geopandas():
    try:
        import geopandas as gpd  # type: ignore
        return gpd
    except Exception as exc:  # pragma: no cover
        raise ImportError("geopandas is required for this operation. Install the conda environment.") from exc


def read_vector(path: str | Path, target_crs: str | None = None):
    """Read a vector dataset and optionally reproject it."""
    gpd = require_geopandas()
    gdf = gpd.read_file(path)
    if target_crs and gdf.crs:
        gdf = gdf.to_crs(target_crs)
    return gdf


def buffer_features(gdf, distance_m: float):
    """Return a buffered copy of projected geometries."""
    out = gdf.copy()
    out["geometry"] = out.geometry.buffer(distance_m)
    return out


def dissolve_to_aoi(gdf, by: str | None = None):
    """Dissolve polygons to one AOI or by a named field."""
    if by and by in gdf.columns:
        return gdf.dissolve(by=by).reset_index()
    tmp = gdf.copy()
    tmp["_aoi"] = 1
    return tmp.dissolve(by="_aoi").reset_index(drop=True)
