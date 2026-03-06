from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional, Tuple


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Failed to locate repo root (expected dirs: scripts/, src/).")


def _read_grid(csv_path: Path) -> Tuple[Tuple[int, ...], ...]:
    # Handle optional UTF-8 BOM via utf-8-sig.
    lines = csv_path.read_text(encoding="utf-8-sig").splitlines()
    grid = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        grid.append(tuple(int(x) for x in s.split(",")))
    if not grid:
        raise ValueError(f"Empty grid: {csv_path}")
    n_cols = len(grid[0])
    if any(len(r) != n_cols for r in grid):
        raise ValueError(f"Non-rectangular grid in {csv_path}")
    return tuple(grid)


def load_map(csv_path: Optional[Path] = None) -> Dict[int, Tuple[int, int]]:
    """Load SmartPalate channel -> (row, col) coordinate map (0-based).

    Rules:
    - Ignore -1 and 124.
    - For duplicates, keep the first coordinate encountered.
    - Missing channels are simply absent from the returned dict.
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
                continue
            if v not in channel_to_rc:
                channel_to_rc[v] = (r, c)

    return channel_to_rc

