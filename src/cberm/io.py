from __future__ import annotations

from pathlib import Path
from typing import Iterable
import csv

VECTOR_EXTENSIONS = {".shp", ".gpkg", ".geojson", ".json", ".kml"}
RASTER_EXTENSIONS = {".tif", ".tiff", ".img", ".vrt", ".nc"}
TABLE_EXTENSIONS = {".csv", ".tsv", ".xlsx", ".parquet", ".feather"}


def discover_gis_files(gis_root: str | Path = "GIS") -> list[dict[str, str]]:
    """Recursively inventory GIS files without opening them.

    This works in restricted environments and is safe for large datasets because it
    only records file metadata, not contents.
    """
    root = Path(gis_root)
    rows: list[dict[str, str]] = []
    if not root.exists():
        return rows
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in VECTOR_EXTENSIONS:
            kind = "vector"
        elif suffix in RASTER_EXTENSIONS:
            kind = "raster"
        elif suffix in TABLE_EXTENSIONS:
            kind = "table"
        else:
            kind = "other"
        rows.append(
            {
                "path": str(path),
                "relative_path": str(path.relative_to(root)),
                "name": path.name,
                "suffix": suffix,
                "kind": kind,
                "size_bytes": str(path.stat().st_size),
            }
        )
    return rows


def classify_layer_name(path: str) -> str:
    """Assign a rough thematic class from a filename/path string."""
    text = path.lower()
    rules = [
        ("health_facilities", ["health", "facility", "clinic", "hospital", "phcu", "phcc"]),
        ("admin_boundaries", ["admin", "boundary", "adm", "county", "state", "payam"]),
        ("ebola_cases", ["ebola", "case", "outbreak", "vbd", "evd"]),
        ("bat_roosts_occurrences", ["bat", "roost", "wildlife", "pterop", "eidolon", "hypsignathus"]),
        ("forests", ["forest", "treecover", "tree_cover"]),
        ("deforestation", ["deforest", "loss", "gfc", "hansen"]),
        ("mines_caves_karst", ["mine", "shaft", "cave", "karst"]),
        ("osm_transport_buildings_water", ["osm", "road", "building", "water", "river", "way"]),
        ("worldpop_population", ["worldpop", "population", "pop"]),
        ("conflict_events", ["conflict", "acled", "security", "violence"]),
        ("elevation_dem", ["elevation", "dem", "srtm", "aster", "alos"]),
        ("orchards_agriculture", ["orchard", "fruit", "crop", "agric"]),
    ]
    for label, tokens in rules:
        if any(token in text for token in tokens):
            return label
    return "unclassified"


def write_inventory_csv(rows: Iterable[dict[str, str]], out_path: str | Path) -> None:
    rows = list(rows)
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["path", "relative_path", "name", "suffix", "kind", "size_bytes", "theme"]
    with p.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row = dict(row)
            row["theme"] = classify_layer_name(row.get("relative_path", row.get("path", "")))
            writer.writerow({key: row.get(key, "") for key in fieldnames})
