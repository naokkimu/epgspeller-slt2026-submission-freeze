#!/usr/bin/env python3
"""Pairwise comparison of two raw NPZ datasets (data,label).

Computes:
- Per-channel mean contact vectors (124-dim)
- Pearson correlation between mean-contact patterns
- Mean contact rate ratio
- 16x16 proxy heatmap of channel-mean differences (A - B)

Writes:
- results/.../pairwise_comparison.csv (upsert)
- results/.../figures/channel_mean_diff_heatmap16x16_<A>_minus_<B>.png

Assumes audits have already produced per_channel_stats.csv; if missing, falls back
to scanning NPZs (slow for large datasets).
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (expected scripts/ and src/)")


def _read_csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: List[Dict[str, object]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def _upsert_by_keys(
    *,
    existing_rows: List[Dict[str, str]],
    new_rows: List[Dict[str, object]],
    key_fields: Sequence[str],
    out_fields: Sequence[str],
) -> List[Dict[str, object]]:
    def k_of(r: Dict[str, object]) -> Tuple[str, ...]:
        return tuple(str(r.get(k, "")) for k in key_fields)

    new_map: Dict[Tuple[str, ...], Dict[str, object]] = {k_of(r): r for r in new_rows}

    out: List[Dict[str, object]] = []
    for r in existing_rows:
        key = tuple(str(r.get(k, "")) for k in key_fields)
        if key in new_map:
            continue
        out.append({k: r.get(k, "") for k in out_fields})
    for key in sorted(new_map.keys()):
        out.append({k: new_map[key].get(k, "") for k in out_fields})
    return out


def _read_smartpalate_grid(csv_path: Path) -> List[List[int]]:
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


def _heatmap_grid_from_channel_values(grid: List[List[int]], ch_values: np.ndarray) -> np.ndarray:
    out = np.full((len(grid), len(grid[0])), np.nan, dtype=np.float64)
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v in (-1, 124):
                continue
            if 0 <= v < len(ch_values):
                out[r, c] = float(ch_values[v])
    return out


def _save_heatmap_diff(path: Path, *, diff_grid: np.ndarray, title: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    vmax = float(np.nanmax(np.abs(diff_grid))) if np.isfinite(diff_grid).any() else 1.0
    vmax = max(vmax, 1e-6)
    vmin = -vmax
    plt.figure(figsize=(6, 5))
    im = plt.imshow(diff_grid, cmap="coolwarm", vmin=vmin, vmax=vmax)
    plt.title(title)
    plt.axis("off")
    plt.colorbar(im, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def _pearson(a: np.ndarray, b: np.ndarray) -> float:
    if a.shape != b.shape or a.size == 0:
        return float("nan")
    aa = a.astype(np.float64) - float(np.mean(a))
    bb = b.astype(np.float64) - float(np.mean(b))
    den = float(np.sqrt(np.sum(aa * aa) * np.sum(bb * bb)))
    if den <= 0:
        return float("nan")
    return float(np.sum(aa * bb) / den)


def _channel_means_from_per_channel_stats(
    per_channel_csv: Path, *, dataset_id: str, view: str
) -> Optional[np.ndarray]:
    rows = _read_csv_rows(per_channel_csv)
    sel = [r for r in rows if (r.get("dataset_id") == dataset_id and r.get("view") == view)]
    if not sel:
        return None
    vals = np.full((124,), np.nan, dtype=np.float64)
    for r in sel:
        ch_s = (r.get("ch") or "").strip()
        v_s = (r.get("mean_contact") or "").strip()
        if not ch_s or not v_s:
            continue
        ch = int(ch_s)
        vals[ch] = float(v_s)
    if not np.isfinite(vals).all():
        return None
    return vals


def _channel_means_by_scanning_npz(npz_path: Path) -> np.ndarray:
    npz = np.load(npz_path, allow_pickle=True)
    if "data" not in npz:
        raise SystemExit(f"NPZ missing key 'data': {npz_path} (keys={list(npz.keys())})")
    data = npz["data"]
    ch_sum = np.zeros((124,), dtype=np.float64)
    total_frames = 0
    for x in data:
        if not isinstance(x, np.ndarray) or x.ndim != 2 or x.shape[1] != 124:
            raise SystemExit(f"Invalid sample shape in {npz_path}: {getattr(x,'shape',None)}")
        ch_sum += x.sum(axis=0)
        total_frames += int(x.shape[0])
    if total_frames <= 0:
        raise SystemExit(f"total_frames<=0 for {npz_path}")
    return ch_sum / float(total_frames)


def main() -> None:
    ap = argparse.ArgumentParser(description="Compare two raw NPZ datasets")
    ap.add_argument("--a_npz", type=Path, required=True)
    ap.add_argument("--b_npz", type=Path, required=True)
    ap.add_argument("--a_id", type=str, required=True)
    ap.add_argument("--b_id", type=str, required=True)
    ap.add_argument("--a_view", type=str, default="raw")
    ap.add_argument("--b_view", type=str, default="raw")
    ap.add_argument("--smartpalate_csv", type=Path, default=Path("scripts/smartpalate_distribution.csv"))
    ap.add_argument(
        "--out_dir", type=Path, default=Path("results/dataset_audit_silentspeller_2026-02-24")
    )
    args = ap.parse_args()

    repo_root = _find_repo_root()

    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    a_npz = args.a_npz if args.a_npz.is_absolute() else (repo_root / args.a_npz)
    b_npz = args.b_npz if args.b_npz.is_absolute() else (repo_root / args.b_npz)
    if not a_npz.exists():
        raise SystemExit(f"a_npz not found: {a_npz}")
    if not b_npz.exists():
        raise SystemExit(f"b_npz not found: {b_npz}")

    smartpalate_csv = args.smartpalate_csv
    if not smartpalate_csv.is_absolute():
        smartpalate_csv = repo_root / smartpalate_csv
    if not smartpalate_csv.exists():
        raise SystemExit(f"smartpalate_csv not found: {smartpalate_csv}")

    grid = _read_smartpalate_grid(smartpalate_csv)

    per_channel_csv = out_dir / "per_channel_stats.csv"
    a_means = _channel_means_from_per_channel_stats(per_channel_csv, dataset_id=args.a_id, view=args.a_view)
    b_means = _channel_means_from_per_channel_stats(per_channel_csv, dataset_id=args.b_id, view=args.b_view)
    if a_means is None:
        a_means = _channel_means_by_scanning_npz(a_npz)
    if b_means is None:
        b_means = _channel_means_by_scanning_npz(b_npz)

    corr = _pearson(a_means, b_means)
    mean_a = float(np.mean(a_means))
    mean_b = float(np.mean(b_means))
    ratio = (mean_a / mean_b) if mean_b != 0 else float("nan")

    out_row = {
        "snapshot_date": _dt.date.today().isoformat(),
        "dataset_a": args.a_id,
        "view_a": args.a_view,
        "dataset_b": args.b_id,
        "view_b": args.b_view,
        "mean_pattern_corr": f"{corr:.8f}" if math.isfinite(corr) else "nan",
        "mean_contact_a": f"{mean_a:.8f}",
        "mean_contact_b": f"{mean_b:.8f}",
        "mean_contact_ratio_a_over_b": f"{ratio:.8f}" if math.isfinite(ratio) else "nan",
    }

    out_csv = out_dir / "pairwise_comparison.csv"
    fields = [
        "snapshot_date",
        "dataset_a",
        "view_a",
        "dataset_b",
        "view_b",
        "mean_pattern_corr",
        "mean_contact_a",
        "mean_contact_b",
        "mean_contact_ratio_a_over_b",
    ]
    existing = _read_csv_rows(out_csv)
    up = _upsert_by_keys(
        existing_rows=existing,
        new_rows=[out_row],
        key_fields=["dataset_a", "view_a", "dataset_b", "view_b"],
        out_fields=fields,
    )
    _write_csv(out_csv, up, fields)

    diff = a_means - b_means
    diff_grid = _heatmap_grid_from_channel_values(grid, diff)
    fig_path = out_dir / "figures" / f"channel_mean_diff_heatmap16x16_{args.a_id}_minus_{args.b_id}.png"
    _save_heatmap_diff(
        fig_path,
        diff_grid=diff_grid,
        title=f"Channel mean contact diff (A-B): {args.a_id}({args.a_view}) - {args.b_id}({args.b_view})",
    )

    print(f"[OK] wrote {out_csv} and {fig_path}")


if __name__ == "__main__":
    main()

