from __future__ import annotations

from pathlib import Path
import numpy as np


def require_rioxarray():
    try:
        import rioxarray as rxr  # type: ignore
        return rxr
    except Exception as exc:  # pragma: no cover
        raise ImportError("rioxarray/rasterio are required for raster operations. Install the conda environment.") from exc


def read_raster(path: str | Path, masked: bool = True):
    """Open a raster as a squeezed rioxarray DataArray."""
    rxr = require_rioxarray()
    return rxr.open_rasterio(path, masked=masked).squeeze()


def minmax_array(values, invert: bool = False):
    """Normalize numpy-like values to 0..1, preserving NaN."""
    arr = np.asarray(values, dtype=float)
    valid = np.isfinite(arr)
    out = np.zeros(arr.shape, dtype=float)
    if valid.any():
        lo = np.nanmin(arr[valid])
        hi = np.nanmax(arr[valid])
        if hi > lo:
            out[valid] = (arr[valid] - lo) / (hi - lo)
    if invert:
        out[valid] = 1.0 - out[valid]
    out[~valid] = np.nan
    return out


def reproject_match(source_path: str | Path, template, out_path: str | Path | None = None):
    """Reproject a raster to match a template DataArray."""
    arr = read_raster(source_path)
    matched = arr.rio.reproject_match(template)
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        matched.rio.to_raster(out_path)
    return matched
