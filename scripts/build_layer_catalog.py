#!/usr/bin/env python
from __future__ import annotations

import argparse
from cberm.io import discover_gis_files, write_inventory_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory files under the GIS folder.")
    parser.add_argument("--gis-root", default="GIS")
    parser.add_argument("--out", default="data/interim/layer_inventory.csv")
    args = parser.parse_args()
    rows = discover_gis_files(args.gis_root)
    write_inventory_csv(rows, args.out)
    print(f"Wrote {len(rows)} records to {args.out}")


if __name__ == "__main__":
    main()
