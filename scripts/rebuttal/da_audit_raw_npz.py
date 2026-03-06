#!/usr/bin/env python3
"""Audit a raw SilentSpeller-style NPZ dataset (keys: data,label).

This script is evidence-first and fail-fast:
- Validates schema and value constraints (0/1, finite, shape=(T,124)).
- Computes dataset-, label-, sample-, and channel-level statistics.
- Detects anomalies (all-zero/all-one samples, dead channels).
- Produces reproducible CSVs and figures under a fixed output directory.

Outputs (under --out_dir):
- dataset_summary.csv
- label_counts.csv
- per_sample_stats.csv
- per_channel_stats.csv
- all_zero_samples.csv
- figures/*.png

Notes
- Labels are normalized to uppercase for counting (to match downstream decoders),
  while the original string is preserved in per-sample outputs.
- Optional --exclude_indices_json allows computing an additional "excluded" view
  with those indices removed.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (expected scripts/ and src/)")


def _sha256(path: Path, *, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


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


def _grid_channel_stats(
    grid: List[List[int]], *, n_channels: int = 124
) -> Tuple[int, List[int], Dict[int, int]]:
    """Return (mapped_count, missing_channels, duplicates{ch:count})."""
    counts: Dict[int, int] = {}
    for row in grid:
        for v in row:
            if v in (-1, 124):
                continue
            if not (0 <= v < n_channels):
                continue
            counts[v] = counts.get(v, 0) + 1
    mapped = set(counts.keys())
    missing = [ch for ch in range(n_channels) if ch not in mapped]
    dups = {ch: c for ch, c in counts.items() if c > 1}
    return len(mapped), missing, dups


def _maybe_read_label_array(npz: np.lib.npyio.NpzFile) -> np.ndarray:
    if "label" in npz:
        return npz["label"]
    if "labels" in npz:
        return npz["labels"]
    raise KeyError(f"NPZ missing key 'label'/'labels'. Available keys: {list(npz.keys())}")


def _canonicalize_label(x) -> Tuple[str, str]:
    raw = x
    if isinstance(x, (bytes, bytearray)):
        try:
            raw = x.decode("utf-8")
        except Exception:
            raw = str(x)
    raw_s = str(raw).strip()
    return raw_s, raw_s.upper()


def _parse_exclude_indices(path: Path) -> List[int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        xs = payload
    elif isinstance(payload, dict):
        if "exclude_indices" not in payload:
            raise ValueError(f"exclude json must contain key 'exclude_indices': {path}")
        xs = payload["exclude_indices"]
    else:
        raise ValueError(f"exclude json must be a list or dict: {path}")
    out: List[int] = []
    for v in xs:
        if isinstance(v, bool):
            raise ValueError(f"exclude index must be int, got bool: {v}")
        out.append(int(v))
    out = sorted(set(out))
    if any(i < 0 for i in out):
        raise ValueError(f"exclude indices must be >=0: {out[:10]}")
    return out


def _percentile(xs: Sequence[float], q: float) -> float:
    if not xs:
        return float("nan")
    return float(np.percentile(np.array(xs, dtype=np.float64), q))


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
    """Replace rows whose key matches; otherwise keep, then append new."""

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


def _save_hist(path: Path, *, values: Sequence[float], title: str, xlabel: str, bins: int = 60) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7, 4))
    plt.hist(list(values), bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def _heatmap_grid_from_channel_values(grid: List[List[int]], ch_values: np.ndarray) -> np.ndarray:
    out = np.full((len(grid), len(grid[0])), np.nan, dtype=np.float64)
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v in (-1, 124):
                continue
            if 0 <= v < len(ch_values):
                out[r, c] = float(ch_values[v])
    return out


def _save_heatmap(
    path: Path,
    *,
    grid_values: np.ndarray,
    title: str,
    cmap: str = "viridis",
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 5))
    im = plt.imshow(grid_values, cmap=cmap, vmin=vmin, vmax=vmax)
    plt.title(title)
    plt.axis("off")
    plt.colorbar(im, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def _audit_dataset(
    *,
    npz_path: Path,
    dataset_id: str,
    out_dir: Path,
    smartpalate_csv: Path,
    exclude_indices: Optional[Sequence[int]],
) -> None:
    grid = _read_smartpalate_grid(smartpalate_csv)
    mapped_n, missing, dups = _grid_channel_stats(grid)

    npz = np.load(npz_path, allow_pickle=True)
    if "data" not in npz:
        raise SystemExit(f"NPZ missing key 'data': {npz_path} (keys={list(npz.keys())})")
    data = npz["data"]
    labels_raw_arr = _maybe_read_label_array(npz)
    if len(data) != len(labels_raw_arr):
        raise SystemExit(f"len(data) != len(label): {len(data)} vs {len(labels_raw_arr)} for {npz_path}")

    N = int(len(data))

    exclude_set = set(int(i) for i in (exclude_indices or []))
    if exclude_set:
        bad = [i for i in sorted(exclude_set) if i < 0 or i >= N][:10]
        if bad:
            raise SystemExit(f"exclude indices out of range for N={N}: {bad}")

    file_size = npz_path.stat().st_size
    file_sha = _sha256(npz_path)

    # Canonicalize labels once.
    label_raw_list: List[str] = []
    label_up_list: List[str] = []
    for x in labels_raw_arr:
        raw, up = _canonicalize_label(x)
        label_raw_list.append(raw)
        label_up_list.append(up)

    views: List[Tuple[str, List[int]]] = [("raw", list(range(N)))]
    if exclude_set:
        keep = [i for i in range(N) if i not in exclude_set]
        views.append(("excluded", keep))

    summary_path = out_dir / "dataset_summary.csv"
    label_counts_path = out_dir / "label_counts.csv"
    per_sample_path = out_dir / "per_sample_stats.csv"
    per_channel_path = out_dir / "per_channel_stats.csv"
    all_zero_path = out_dir / "all_zero_samples.csv"

    existing_summary = _read_csv_rows(summary_path)
    existing_label_counts = _read_csv_rows(label_counts_path)
    existing_per_sample = _read_csv_rows(per_sample_path)
    existing_per_channel = _read_csv_rows(per_channel_path)
    existing_all_zero = _read_csv_rows(all_zero_path)

    summary_rows_new: List[Dict[str, object]] = []
    label_counts_rows_new: List[Dict[str, object]] = []
    per_sample_rows_new: List[Dict[str, object]] = []
    per_channel_rows_new: List[Dict[str, object]] = []
    all_zero_rows_new: List[Dict[str, object]] = []

    label_counts_by_view: Dict[str, Counter] = {}
    all_zero_raw: List[Tuple[int, int, str, str]] = []  # (idx, T, label_raw, label_up)

    for view_name, idxs in views:
        lens: List[int] = []
        per_sample_mean_contact: List[float] = []

        ch_sum = np.zeros((124,), dtype=np.float64)
        total_frames = 0
        all_zero_n = 0
        all_one_n = 0

        label_counter: Counter = Counter()

        for idx in idxs:
            x = data[idx]
            if not isinstance(x, np.ndarray):
                raise SystemExit(f"data[{idx}] is not ndarray: {type(x)}")
            if x.ndim != 2 or x.shape[1] != 124:
                raise SystemExit(f"data[{idx}] has invalid shape {getattr(x,'shape',None)}; expected (T,124)")
            if not np.isfinite(x).all():
                raise SystemExit(f"data[{idx}] contains NaN/inf")
            if not (((x == 0.0) | (x == 1.0)).all()):
                bad = x[~((x == 0.0) | (x == 1.0))]
                ex = bad.ravel()[:10]
                raise SystemExit(f"data[{idx}] contains non-binary values (examples: {ex})")

            T = int(x.shape[0])
            if T <= 0:
                raise SystemExit(f"data[{idx}] has non-positive T={T}")

            raw_lab = label_raw_list[idx]
            up_lab = label_up_list[idx]

            lens.append(T)
            mc = float(x.mean())
            per_sample_mean_contact.append(mc)

            row_sum = x.sum(axis=1)  # (T,)
            allzero_frames = int(np.count_nonzero(row_sum == 0))
            allone_frames = int(np.count_nonzero(row_sum == 124))
            frames_allzero_ratio = float(allzero_frames / T)
            frames_allone_ratio = float(allone_frames / T)

            active_mean = float(row_sum.mean())
            active_std = float(row_sum.std())

            if float(row_sum.sum()) == 0.0:
                all_zero_n += 1
                if view_name == "raw":
                    all_zero_raw.append((idx, T, raw_lab, up_lab))
            if float(row_sum.sum()) == float(T * 124):
                all_one_n += 1

            ch_sum += x.sum(axis=0)
            total_frames += T

            label_counter[up_lab] += 1

            per_sample_rows_new.append(
                {
                    "dataset_id": dataset_id,
                    "view": view_name,
                    "idx": idx,
                    "label": up_lab,
                    "label_raw": raw_lab,
                    "T": T,
                    "mean_contact": f"{mc:.8f}",
                    "frames_allzero_ratio": f"{frames_allzero_ratio:.6f}",
                    "frames_allone_ratio": f"{frames_allone_ratio:.6f}",
                    "active_ch_mean": f"{active_mean:.6f}",
                    "active_ch_std": f"{active_std:.6f}",
                }
            )

        label_counts_by_view[view_name] = label_counter

        if total_frames <= 0:
            raise SystemExit(f"No frames accumulated for view={view_name} ({npz_path})")

        ch_mean = ch_sum / float(total_frames)
        overall_mean_contact = float(ch_mean.mean())

        dead_channels = [int(i) for i, v in enumerate(ch_mean.tolist()) if float(v) == 0.0]

        order = sorted(range(124), key=lambda i: (-float(ch_mean[i]), i))
        rank = {ch: r + 1 for r, ch in enumerate(order)}
        for ch in range(124):
            v = float(ch_mean[ch])
            per_channel_rows_new.append(
                {
                    "dataset_id": dataset_id,
                    "view": view_name,
                    "ch": ch,
                    "mean_contact": f"{v:.8f}",
                    "rank_mean_contact": rank[ch],
                    "dead_flag": int(v == 0.0),
                }
            )

        for lab, cnt in sorted(label_counter.items(), key=lambda kv: (-kv[1], kv[0])):
            label_counts_rows_new.append(
                {"dataset_id": dataset_id, "view": view_name, "label": lab, "count": int(cnt)}
            )

        occ_hist = Counter(label_counter.values())
        occ_hist_json = json.dumps({int(k): int(v) for k, v in sorted(occ_hist.items())}, sort_keys=True)

        summary_rows_new.append(
            {
                "snapshot_date": _dt.date.today().isoformat(),
                "dataset_id": dataset_id,
                "view": view_name,
                "npz_path": str(npz_path),
                "file_size_bytes": int(file_size),
                "sha256": file_sha,
                "n_samples": int(len(idxs)),
                "n_unique_labels": int(len(label_counter)),
                "label_occurrence_hist_json": occ_hist_json,
                "T_min": int(min(lens)) if lens else "",
                "T_p10": f"{_percentile(lens, 10):.3f}" if lens else "",
                "T_median": f"{_percentile(lens, 50):.3f}" if lens else "",
                "T_mean": f"{(sum(lens) / len(lens)):.6f}" if lens else "",
                "T_p90": f"{_percentile(lens, 90):.3f}" if lens else "",
                "T_max": int(max(lens)) if lens else "",
                "total_frames": int(total_frames),
                "overall_mean_contact": f"{overall_mean_contact:.8f}",
                "per_sample_mean_contact_p10": f"{_percentile(per_sample_mean_contact, 10):.8f}",
                "per_sample_mean_contact_median": f"{_percentile(per_sample_mean_contact, 50):.8f}",
                "per_sample_mean_contact_mean": f"{(sum(per_sample_mean_contact) / len(per_sample_mean_contact)):.8f}",
                "per_sample_mean_contact_p90": f"{_percentile(per_sample_mean_contact, 90):.8f}",
                "all_zero_samples": int(all_zero_n),
                "all_one_samples": int(all_one_n),
                "dead_channels": int(len(dead_channels)),
                "smartpalate_mapped_channels": int(mapped_n),
                "smartpalate_missing_channels": int(len(missing)),
                "smartpalate_duplicate_channels": int(len(dups)),
                "exclude_indices_n": int(len(exclude_set)),
            }
        )

        figs_dir = out_dir / "figures"
        _save_hist(
            figs_dir / f"T_hist_{dataset_id}_{view_name}.png",
            values=lens,
            title=f"T histogram: {dataset_id} ({view_name})",
            xlabel="T (frames)",
        )
        _save_hist(
            figs_dir / f"contact_rate_hist_{dataset_id}_{view_name}.png",
            values=per_sample_mean_contact,
            title=f"Per-sample mean contact: {dataset_id} ({view_name})",
            xlabel="mean_contact",
        )
        grid_vals = _heatmap_grid_from_channel_values(grid, ch_mean)
        _save_heatmap(
            figs_dir / f"channel_mean_heatmap16x16_{dataset_id}_{view_name}.png",
            grid_values=grid_vals,
            title=(
                f"Channel mean contact (16x16 proxy): {dataset_id} ({view_name})\n"
                f"mapped={mapped_n} missing={len(missing)} dups={len(dups)}"
            ),
            cmap="viridis",
        )

    raw_counts = label_counts_by_view.get("raw", Counter())
    excl_counts = label_counts_by_view.get("excluded", raw_counts)
    for idx, T, raw_lab, up_lab in all_zero_raw:
        before = int(raw_counts.get(up_lab, 0))
        after = int(excl_counts.get(up_lab, 0))
        all_zero_rows_new.append(
            {
                "dataset_id": dataset_id,
                "idx": idx,
                "label": up_lab,
                "label_raw": raw_lab,
                "T": T,
                "word_count_before": before,
                "word_count_after_excl": after,
                "excluded_flag": int(idx in exclude_set),
            }
        )

    summary_fields = [
        "snapshot_date",
        "dataset_id",
        "view",
        "npz_path",
        "file_size_bytes",
        "sha256",
        "n_samples",
        "n_unique_labels",
        "label_occurrence_hist_json",
        "T_min",
        "T_p10",
        "T_median",
        "T_mean",
        "T_p90",
        "T_max",
        "total_frames",
        "overall_mean_contact",
        "per_sample_mean_contact_p10",
        "per_sample_mean_contact_median",
        "per_sample_mean_contact_mean",
        "per_sample_mean_contact_p90",
        "all_zero_samples",
        "all_one_samples",
        "dead_channels",
        "smartpalate_mapped_channels",
        "smartpalate_missing_channels",
        "smartpalate_duplicate_channels",
        "exclude_indices_n",
    ]
    label_count_fields = ["dataset_id", "view", "label", "count"]
    per_sample_fields = [
        "dataset_id",
        "view",
        "idx",
        "label",
        "label_raw",
        "T",
        "mean_contact",
        "frames_allzero_ratio",
        "frames_allone_ratio",
        "active_ch_mean",
        "active_ch_std",
    ]
    per_channel_fields = ["dataset_id", "view", "ch", "mean_contact", "rank_mean_contact", "dead_flag"]
    all_zero_fields = [
        "dataset_id",
        "idx",
        "label",
        "label_raw",
        "T",
        "word_count_before",
        "word_count_after_excl",
        "excluded_flag",
    ]

    _write_csv(
        summary_path,
        _upsert_by_keys(
            existing_rows=existing_summary,
            new_rows=summary_rows_new,
            key_fields=["dataset_id", "view"],
            out_fields=summary_fields,
        ),
        summary_fields,
    )
    _write_csv(
        label_counts_path,
        _upsert_by_keys(
            existing_rows=existing_label_counts,
            new_rows=label_counts_rows_new,
            key_fields=["dataset_id", "view", "label"],
            out_fields=label_count_fields,
        ),
        label_count_fields,
    )
    _write_csv(
        per_sample_path,
        _upsert_by_keys(
            existing_rows=existing_per_sample,
            new_rows=per_sample_rows_new,
            key_fields=["dataset_id", "view", "idx"],
            out_fields=per_sample_fields,
        ),
        per_sample_fields,
    )
    _write_csv(
        per_channel_path,
        _upsert_by_keys(
            existing_rows=existing_per_channel,
            new_rows=per_channel_rows_new,
            key_fields=["dataset_id", "view", "ch"],
            out_fields=per_channel_fields,
        ),
        per_channel_fields,
    )
    _write_csv(
        all_zero_path,
        _upsert_by_keys(
            existing_rows=existing_all_zero,
            new_rows=all_zero_rows_new,
            key_fields=["dataset_id", "idx"],
            out_fields=all_zero_fields,
        ),
        all_zero_fields,
    )

    print(f"[OK] audited {dataset_id} ({npz_path.name}) -> {out_dir}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit raw NPZ dataset (data,label)")
    ap.add_argument("--npz", type=Path, required=True)
    ap.add_argument("--dataset_id", type=str, required=True)
    ap.add_argument("--smartpalate_csv", type=Path, default=Path("scripts/smartpalate_distribution.csv"))
    ap.add_argument(
        "--out_dir", type=Path, default=Path("results/dataset_audit_silentspeller_2026-02-24")
    )
    ap.add_argument("--exclude_indices_json", type=Path, default=None)
    args = ap.parse_args()

    repo_root = _find_repo_root()

    npz_path = args.npz if args.npz.is_absolute() else (repo_root / args.npz)
    if not npz_path.exists():
        raise SystemExit(f"npz not found: {npz_path}")

    smartpalate_csv = args.smartpalate_csv
    if not smartpalate_csv.is_absolute():
        smartpalate_csv = repo_root / smartpalate_csv
    if not smartpalate_csv.exists():
        raise SystemExit(f"smartpalate_csv not found: {smartpalate_csv}")

    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    exclude_indices: Optional[List[int]] = None
    if args.exclude_indices_json is not None:
        p = args.exclude_indices_json
        if not p.is_absolute():
            p = repo_root / p
        if not p.exists():
            raise SystemExit(f"exclude_indices_json not found: {p}")
        exclude_indices = _parse_exclude_indices(p)

    _audit_dataset(
        npz_path=npz_path,
        dataset_id=args.dataset_id,
        out_dir=out_dir,
        smartpalate_csv=smartpalate_csv,
        exclude_indices=exclude_indices,
    )


if __name__ == "__main__":
    main()

