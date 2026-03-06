#!/usr/bin/env python3
"""SmartPalate 16x16 grid -> channel coordinate map.

This repo includes `scripts/smartpalate_distribution.csv`, a 16x16 integer grid.
Cells contain:
- -1: no electrode at that location
- 0..123: channel index (EPG feature dimension)
- 124: appears in the file but is not a valid channel index for this repo; ignore

The file may contain duplicates (same channel index appears multiple times) and
missing indices. This module provides a deterministic mapping:
- ignore -1 and 124
- for duplicates, keep the first coordinate encountered
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class SmartPalateMap:
    grid: List[List[int]]  # row-major 2D list (values as in CSV)
    channel_to_rc: Dict[int, Tuple[int, int]]  # 0..123 -> (row, col), 0-based

    @property
    def n_rows(self) -> int:
        return len(self.grid)

    @property
    def n_cols(self) -> int:
        return len(self.grid[0]) if self.grid else 0


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Failed to locate repo root (expected dirs: scripts/, src/).")


def _read_grid(csv_path: Path) -> List[List[int]]:
    # Handle optional UTF-8 BOM via utf-8-sig.
    lines = csv_path.read_text(encoding="utf-8-sig").splitlines()
    grid: List[List[int]] = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        grid.append([int(x) for x in s.split(",")])
    if not grid:
        raise ValueError(f"Empty grid: {csv_path}")
    n_cols = len(grid[0])
    if any(len(r) != n_cols for r in grid):
        raise ValueError(f"Non-rectangular grid in {csv_path}")
    return grid


def load_map(csv_path: Optional[Path] = None) -> SmartPalateMap:
    """Load SmartPalate channel->(row,col) map.

    Args:
        csv_path: path to `smartpalate_distribution.csv`. If None, uses the repo default.

    Returns:
        SmartPalateMap with:
          - grid: 2D list of ints
          - channel_to_rc: dict of channel -> (row, col), 0-based
    """
    if csv_path is None:
        csv_path = _repo_root() / "scripts" / "smartpalate_distribution.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"smartpalate CSV not found: {csv_path}")

    grid = _read_grid(csv_path)
    channel_to_rc: Dict[int, Tuple[int, int]] = {}

    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v in (-1, 124):
                continue
            if not (0 <= v <= 123):
                # Unknown value; ignore rather than guessing.
                continue
            if v not in channel_to_rc:
                channel_to_rc[v] = (r, c)

    return SmartPalateMap(grid=grid, channel_to_rc=channel_to_rc)


def unmapped_channels(sp_map: SmartPalateMap, *, n_channels: int = 124) -> List[int]:
    """List channels in [0, n_channels) missing coordinates."""
    return [ch for ch in range(n_channels) if ch not in sp_map.channel_to_rc]


def duplicates_in_grid(sp_map: SmartPalateMap) -> Dict[int, int]:
    """Return {channel: count} for channels that appear multiple times in the grid."""
    counts: Dict[int, int] = {}
    for row in sp_map.grid:
        for v in row:
            if v in (-1, 124):
                continue
            if not (0 <= v <= 123):
                continue
            counts[v] = counts.get(v, 0) + 1
    return {k: v for k, v in counts.items() if v > 1}


if __name__ == "__main__":
    m = load_map()
    dups = duplicates_in_grid(m)
    missing = unmapped_channels(m)
    print(f"grid={m.n_rows}x{m.n_cols} mapped={len(m.channel_to_rc)} missing={len(missing)} dups={len(dups)}")
    if dups:
        top = sorted(dups.items(), key=lambda t: t[1], reverse=True)[:10]
        print("top duplicates:", top)
    if missing:
        print("missing:", missing)

