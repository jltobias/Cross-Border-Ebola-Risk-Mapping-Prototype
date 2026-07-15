from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml


def find_repo_root(start: str | Path = ".") -> Path:
    """Find a likely repository root by walking upward from *start*."""
    current = Path(start).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "configs").exists() or (candidate / ".git").exists():
            return candidate
    return current


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file and return an empty dict for empty files."""
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_yaml(data: dict[str, Any], path: str | Path) -> None:
    """Write a YAML file with stable key order."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    gis_root: Path
    data_raw: Path
    data_interim: Path
    data_processed: Path
    outputs: Path

    @classmethod
    def from_config(cls, config_path: str | Path = "configs/model_config.yml") -> "ProjectPaths":
        root = find_repo_root(Path(config_path).parent)
        cfg = load_yaml(root / config_path)
        paths = cfg.get("paths", {})
        return cls(
            root=root,
            gis_root=root / paths.get("gis_root", "GIS"),
            data_raw=root / paths.get("data_raw", "data/raw"),
            data_interim=root / paths.get("data_interim", "data/interim"),
            data_processed=root / paths.get("data_processed", "data/processed"),
            outputs=root / paths.get("outputs", "outputs"),
        )

    def ensure(self) -> None:
        for path in [self.gis_root, self.data_raw, self.data_interim, self.data_processed, self.outputs]:
            path.mkdir(parents=True, exist_ok=True)
