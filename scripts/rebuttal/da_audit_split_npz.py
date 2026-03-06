#!/usr/bin/env python3
"""Audit a Protocol split NPZ (train/test/competition) for SilentSpeller experiments.

This script is evidence-first and fail-fast:
- Validates split schema and value constraints (0/1, finite, shape=(T,124)).
- Computes partition-, label-, sample-, and channel-level statistics.
- Runs protocol integrity checks:
  - P1 (word-holdout)
  - P2 (within-subject instance-holdout; 1 instance/word per partition)
  - P3 (cross-subject instance-holdout; 1 instance/word per partition)
  - P3MS (multi-source cross-subject; 2 train/comp instances per word, 1 test instance/word)
  - P2K (k-shot within-subject; k train/comp instances per word, 1 test instance/word)
- Produces reproducible CSVs and figures under a fixed output directory.

Outputs (under --out_dir):
- protocol_split_summary.csv
- protocol_split_label_counts.csv
- protocol_split_per_sample_stats.csv
- protocol_split_per_channel_stats.csv
- protocol_split_all_zero_samples.csv
- protocol_split_vocab_sets.json

Notes
- Labels are normalized to uppercase for counting (to match downstream decoders),
  while the original string is preserved in per-sample outputs.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import math
import re
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


def _canonicalize_label(x) -> Tuple[str, str]:
    raw = x
    if isinstance(x, (bytes, bytearray)):
        try:
            raw = x.decode("utf-8")
        except Exception:
            raw = str(x)
    raw_s = str(raw).strip()
    return raw_s, raw_s.upper()


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


def _json_occ_hist(counter: Counter) -> str:
    h = Counter(counter.values())
    # JSON keys must be strings for stability.
    payload = {str(k): int(v) for k, v in sorted(h.items(), key=lambda kv: int(kv[0]))}
    return json.dumps(payload, sort_keys=True)


def _load_partition(npz: np.lib.npyio.NpzFile, part: str) -> Tuple[np.ndarray, np.ndarray]:
    data_key = f"{part}_data"
    if data_key not in npz:
        raise KeyError(f"Split NPZ missing key {data_key}. Available keys: {list(npz.keys())}")

    if f"{part}_label" in npz:
        label_key = f"{part}_label"
    elif f"{part}_labels" in npz:
        label_key = f"{part}_labels"
    else:
        raise KeyError(
            f"Split NPZ missing key {part}_label/{part}_labels. Available keys: {list(npz.keys())}"
        )

    data = npz[data_key]
    labels = npz[label_key]
    if len(data) != len(labels):
        raise ValueError(f"len({data_key}) != len({label_key}): {len(data)} vs {len(labels)}")
    return data, labels


def _assert_all_counts_equal(
    label_counter: Counter,
    *,
    expected: int,
    context: str,
) -> None:
    bad = {lab: int(cnt) for lab, cnt in label_counter.items() if int(cnt) != int(expected)}
    if bad:
        examples = list(sorted(bad.items(), key=lambda kv: (-kv[1], kv[0])))[:10]
        raise SystemExit(
            f"{context}: expected every label to have count={expected}, "
            f"but found {len(bad)} violating labels. Examples: {examples}"
        )


def _parse_k_from_split_id(split_id: str) -> int:
    # Expected token somewhere in split_id, e.g. "..._k1..." or "..._k2..."
    m = re.search(r"(?:^|_)k(?P<k>[12])(?:_|$)", split_id)
    if not m:
        raise SystemExit(
            "P2K integrity failed: could not parse k from split_id. "
            f"Expected token like _k1_ or _k2_. split_id={split_id!r}"
        )
    return int(m.group("k"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit a protocol split NPZ (train/test/competition)")
    ap.add_argument("--split_npz", type=Path, required=True)
    ap.add_argument("--split_id", type=str, required=True)
    ap.add_argument("--protocol", type=str, required=True, choices=["P1", "P2", "P3", "P3MS", "P2K"])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--subject", type=str, default="")
    ap.add_argument("--smartpalate_csv", type=Path, default=Path("scripts/smartpalate_distribution.csv"))
    ap.add_argument(
        "--out_dir",
        type=Path,
        default=Path("results/dataset_audit_silentspeller_2026-02-24"),
    )
    ap.add_argument(
        "--fig_dir",
        type=Path,
        default=None,
        help="Figure output dir. Defaults to <out_dir>/figures/protocol_splits",
    )
    args = ap.parse_args()

    repo_root = _find_repo_root()

    split_npz = args.split_npz if args.split_npz.is_absolute() else (repo_root / args.split_npz)
    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)
    smartpalate_csv = (
        args.smartpalate_csv
        if args.smartpalate_csv.is_absolute()
        else (repo_root / args.smartpalate_csv)
    )
    fig_dir = args.fig_dir
    if fig_dir is None:
        fig_dir = out_dir / "figures" / "protocol_splits"
    if not fig_dir.is_absolute():
        fig_dir = repo_root / fig_dir

    if not split_npz.exists():
        raise SystemExit(f"split_npz not found: {split_npz}")
    if not smartpalate_csv.exists():
        raise SystemExit(f"smartpalate_csv not found: {smartpalate_csv}")

    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    grid = _read_smartpalate_grid(smartpalate_csv)
    mapped_n, missing_ch, dup_ch = _grid_channel_stats(grid)

    split = np.load(split_npz, allow_pickle=True)

    summary_path = out_dir / "protocol_split_summary.csv"
    label_counts_path = out_dir / "protocol_split_label_counts.csv"
    per_sample_path = out_dir / "protocol_split_per_sample_stats.csv"
    per_channel_path = out_dir / "protocol_split_per_channel_stats.csv"
    all_zero_path = out_dir / "protocol_split_all_zero_samples.csv"
    vocab_sets_path = out_dir / "protocol_split_vocab_sets.json"

    existing_summary = _read_csv_rows(summary_path)
    existing_label_counts = _read_csv_rows(label_counts_path)
    existing_per_sample = _read_csv_rows(per_sample_path)
    existing_per_channel = _read_csv_rows(per_channel_path)
    existing_all_zero = _read_csv_rows(all_zero_path)

    snapshot_date = _dt.date.today().isoformat()

    summary_rows_new: List[Dict[str, object]] = []
    label_counts_rows_new: List[Dict[str, object]] = []
    per_sample_rows_new: List[Dict[str, object]] = []
    per_channel_rows_new: List[Dict[str, object]] = []
    all_zero_rows_new: List[Dict[str, object]] = []

    vocab_by_part: Dict[str, List[str]] = {}

    for part in ["train", "test", "competition"]:
        data, labels_arr = _load_partition(split, part)

        label_raw_list: List[str] = []
        label_up_list: List[str] = []
        for x in labels_arr.tolist():
            raw_s, up_s = _canonicalize_label(x)
            label_raw_list.append(raw_s)
            label_up_list.append(up_s)

        lens: List[int] = []
        per_sample_mean_contact: List[float] = []

        ch_sum = np.zeros((124,), dtype=np.float64)
        total_frames = 0
        all_zero_n = 0
        all_one_n = 0

        label_counter: Counter = Counter()

        for idx in range(int(len(data))):
            x = data[idx]
            if not isinstance(x, np.ndarray):
                raise SystemExit(f"{part}_data[{idx}] is not ndarray: {type(x)}")
            if x.ndim != 2 or x.shape[1] != 124:
                raise SystemExit(
                    f"{part}_data[{idx}] has invalid shape {getattr(x,shape,None)}; expected (T,124)"
                )
            if not np.isfinite(x).all():
                raise SystemExit(f"{part}_data[{idx}] contains NaN/inf")
            if not (((x == 0.0) | (x == 1.0)).all()):
                bad = x[~((x == 0.0) | (x == 1.0))]
                ex = bad.ravel()[:10]
                raise SystemExit(f"{part}_data[{idx}] contains non-binary values (examples: {ex})")

            T = int(x.shape[0])
            if T <= 0:
                raise SystemExit(f"{part}_data[{idx}] has non-positive T={T}")

            raw_lab = label_raw_list[idx]
            up_lab = label_up_list[idx]

            lens.append(T)
            mc = float(x.mean())
            per_sample_mean_contact.append(mc)

            row_sum = x.sum(axis=1)
            allzero_frames = int(np.count_nonzero(row_sum == 0))
            allone_frames = int(np.count_nonzero(row_sum == 124))
            frames_allzero_ratio = float(allzero_frames / T)
            frames_allone_ratio = float(allone_frames / T)

            active_mean = float(row_sum.mean())
            active_std = float(row_sum.std())

            is_all_zero = int(float(row_sum.sum()) == 0.0)
            is_all_one = int(float(row_sum.sum()) == float(T * 124))

            if is_all_zero:
                all_zero_n += 1
                all_zero_rows_new.append(
                    {
                        "snapshot_date": snapshot_date,
                        "split_id": args.split_id,
                        "protocol": args.protocol,
                        "seed": args.seed,
                        "subject": args.subject,
                        "partition": part,
                        "idx": idx,
                        "label": up_lab,
                        "label_raw": raw_lab,
                        "T": T,
                        "all_zero_flag": 1,
                    }
                )
            if is_all_one:
                all_one_n += 1

            ch_sum += x.sum(axis=0)
            total_frames += T

            label_counter[up_lab] += 1

            per_sample_rows_new.append(
                {
                    "snapshot_date": snapshot_date,
                    "split_id": args.split_id,
                    "protocol": args.protocol,
                    "seed": args.seed,
                    "subject": args.subject,
                    "partition": part,
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

        if total_frames <= 0:
            raise SystemExit(f"No frames accumulated for split_id={args.split_id} partition={part}")

        vocab = sorted(label_counter.keys())
        vocab_by_part[part] = vocab

        # Label-count rows
        for lab, cnt in sorted(label_counter.items(), key=lambda kv: kv[0]):
            label_counts_rows_new.append(
                {
                    "snapshot_date": snapshot_date,
                    "split_id": args.split_id,
                    "protocol": args.protocol,
                    "seed": args.seed,
                    "subject": args.subject,
                    "partition": part,
                    "label": lab,
                    "count": int(cnt),
                }
            )

        ch_mean = ch_sum / float(total_frames)
        overall_mean_contact = float(ch_mean.mean())

        dead_channels = [int(i) for i, v in enumerate(ch_mean.tolist()) if float(v) == 0.0]

        order = np.argsort(-ch_mean)
        ranks = np.empty_like(order)
        ranks[order] = np.arange(len(order))

        for ch in range(124):
            per_channel_rows_new.append(
                {
                    "snapshot_date": snapshot_date,
                    "split_id": args.split_id,
                    "protocol": args.protocol,
                    "seed": args.seed,
                    "subject": args.subject,
                    "partition": part,
                    "ch": ch,
                    "mean_contact": f"{float(ch_mean[ch]):.8f}",
                    "rank_mean_contact": int(ranks[ch]),
                    "dead_flag": 1 if ch in dead_channels else 0,
                }
            )

        summary_rows_new.append(
            {
                "snapshot_date": snapshot_date,
                "split_id": args.split_id,
                "protocol": args.protocol,
                "seed": args.seed,
                "subject": args.subject,
                "partition": part,
                "n_samples": int(len(data)),
                "n_unique_labels": int(len(vocab)),
                "T_min": int(min(lens)) if lens else "",
                "T_median": f"{_percentile(lens, 50):.3f}" if lens else "",
                "T_mean": f"{statistics.mean(lens):.6f}" if lens else "",
                "T_max": int(max(lens)) if lens else "",
                "total_frames": int(total_frames),
                "overall_mean_contact": f"{overall_mean_contact:.8f}",
                "all_zero_samples": int(all_zero_n),
                "all_one_samples": int(all_one_n),
                "dead_channels": int(len(dead_channels)),
                "label_occurrence_hist_json": _json_occ_hist(label_counter),
                "smartpalate_mapped_channels": int(mapped_n),
                "smartpalate_missing_channels_n": int(len(missing_ch)),
                "smartpalate_duplicate_channels_n": int(len(dup_ch)),
            }
        )

        # Figures
        _save_hist(
            fig_dir / f"T_hist_{args.split_id}_{part}.png",
            values=lens,
            title=f"T histogram: {args.split_id} ({part})",
            xlabel="T (frames)",
        )
        _save_hist(
            fig_dir / f"contact_rate_hist_{args.split_id}_{part}.png",
            values=per_sample_mean_contact,
            title=f"Per-sample mean contact: {args.split_id} ({part})",
            xlabel="mean contact",
        )

        grid_values = _heatmap_grid_from_channel_values(grid, ch_mean)
        _save_heatmap(
            fig_dir / f"channel_mean_heatmap16x16_{args.split_id}_{part}.png",
            grid_values=grid_values,
            title=(
                f"Channel mean contact (16x16 proxy): {args.split_id} ({part})\n"
                f"mapped={mapped_n}/124, missing={len(missing_ch)}, dups={len(dup_ch)}"
            ),
        )

    # --- Protocol integrity checks (fail-fast) ---
    train_vocab = set(vocab_by_part.get("train", []))
    test_vocab = set(vocab_by_part.get("test", []))
    comp_vocab = set(vocab_by_part.get("competition", []))

    if args.protocol == "P1":
        if (train_vocab & test_vocab) or (train_vocab & comp_vocab) or (test_vocab & comp_vocab):
            raise SystemExit(
                "P1 integrity failed: train/test/competition vocab must be pairwise disjoint. "
                f"sizes: |train∩test|={len(train_vocab & test_vocab)}, "
                f"|train∩comp|={len(train_vocab & comp_vocab)}, "
                f"|test∩comp|={len(test_vocab & comp_vocab)}"
            )

    elif args.protocol in {"P2", "P3"}:
        if train_vocab & comp_vocab:
            raise SystemExit(
                f"{args.protocol} integrity failed: train and competition vocab must be disjoint. "
                f"|train∩comp|={len(train_vocab & comp_vocab)}"
            )
        union_vocab = train_vocab | comp_vocab
        if test_vocab != union_vocab:
            missing = sorted(list(union_vocab - test_vocab))[:10]
            extra = sorted(list(test_vocab - union_vocab))[:10]
            raise SystemExit(
                f"{args.protocol} integrity failed: expected test_vocab == (train_vocab ∪ competition_vocab). "
                f"missing_in_test(examples)={missing} extra_in_test(examples)={extra}"
            )
        # Expect 1 instance/word per partition (instance-holdout split).
        for part in ["train", "test", "competition"]:
            data, labels_arr = _load_partition(split, part)
            labels_up = [(_canonicalize_label(x)[1]) for x in labels_arr.tolist()]
            c = Counter(labels_up)
            _assert_all_counts_equal(c, expected=1, context=f"{args.protocol} integrity ({args.split_id}) partition={part}")
            if len(c) != len(labels_up):
                raise SystemExit(
                    f"{args.protocol} integrity ({args.split_id}) partition={part}: expected unique labels (no duplicates). "
                    f"len(labels)={len(labels_up)} unique={len(c)}"
                )

    elif args.protocol == "P3MS":
        if train_vocab & comp_vocab:
            raise SystemExit(
                "P3MS integrity failed: train and competition vocab must be disjoint. "
                f"|train∩comp|={len(train_vocab & comp_vocab)}"
            )
        union_vocab = train_vocab | comp_vocab
        if test_vocab != union_vocab:
            missing = sorted(list(union_vocab - test_vocab))[:10]
            extra = sorted(list(test_vocab - union_vocab))[:10]
            raise SystemExit(
                "P3MS integrity failed: expected test_vocab == (train_vocab ∪ competition_vocab). "
                f"missing_in_test(examples)={missing} extra_in_test(examples)={extra}"
            )

        expected_counts = {"train": 2, "competition": 2, "test": 1}
        for part, expected in expected_counts.items():
            data, labels_arr = _load_partition(split, part)
            labels_up = [(_canonicalize_label(x)[1]) for x in labels_arr.tolist()]
            c = Counter(labels_up)
            _assert_all_counts_equal(
                c, expected=expected, context=f"P3MS integrity ({args.split_id}) partition={part}"
            )

    elif args.protocol == "P2K":
        k = _parse_k_from_split_id(args.split_id)
        if train_vocab & comp_vocab:
            raise SystemExit(
                "P2K integrity failed: train and competition vocab must be disjoint. "
                f"|train∩comp|={len(train_vocab & comp_vocab)}"
            )
        union_vocab = train_vocab | comp_vocab
        if test_vocab != union_vocab:
            missing = sorted(list(union_vocab - test_vocab))[:10]
            extra = sorted(list(test_vocab - union_vocab))[:10]
            raise SystemExit(
                "P2K integrity failed: expected test_vocab == (train_vocab ∪ competition_vocab). "
                f"missing_in_test(examples)={missing} extra_in_test(examples)={extra}"
            )

        expected_counts = {"train": k, "competition": k, "test": 1}
        for part, expected in expected_counts.items():
            data, labels_arr = _load_partition(split, part)
            labels_up = [(_canonicalize_label(x)[1]) for x in labels_arr.tolist()]
            c = Counter(labels_up)
            _assert_all_counts_equal(
                c, expected=expected, context=f"P2K integrity ({args.split_id}) partition={part}"
            )

    # --- Write/Upsert outputs ---
    summary_fields = [
        "snapshot_date",
        "split_id",
        "protocol",
        "seed",
        "subject",
        "partition",
        "n_samples",
        "n_unique_labels",
        "T_min",
        "T_median",
        "T_mean",
        "T_max",
        "total_frames",
        "overall_mean_contact",
        "all_zero_samples",
        "all_one_samples",
        "dead_channels",
        "label_occurrence_hist_json",
        "smartpalate_mapped_channels",
        "smartpalate_missing_channels_n",
        "smartpalate_duplicate_channels_n",
    ]
    label_count_fields = [
        "snapshot_date",
        "split_id",
        "protocol",
        "seed",
        "subject",
        "partition",
        "label",
        "count",
    ]
    per_sample_fields = [
        "snapshot_date",
        "split_id",
        "protocol",
        "seed",
        "subject",
        "partition",
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
    per_channel_fields = [
        "snapshot_date",
        "split_id",
        "protocol",
        "seed",
        "subject",
        "partition",
        "ch",
        "mean_contact",
        "rank_mean_contact",
        "dead_flag",
    ]
    all_zero_fields = [
        "snapshot_date",
        "split_id",
        "protocol",
        "seed",
        "subject",
        "partition",
        "idx",
        "label",
        "label_raw",
        "T",
        "all_zero_flag",
    ]

    _write_csv(
        summary_path,
        _upsert_by_keys(
            existing_rows=existing_summary,
            new_rows=summary_rows_new,
            key_fields=["split_id", "partition"],
            out_fields=summary_fields,
        ),
        summary_fields,
    )

    _write_csv(
        label_counts_path,
        _upsert_by_keys(
            existing_rows=existing_label_counts,
            new_rows=label_counts_rows_new,
            key_fields=["split_id", "partition", "label"],
            out_fields=label_count_fields,
        ),
        label_count_fields,
    )

    _write_csv(
        per_sample_path,
        _upsert_by_keys(
            existing_rows=existing_per_sample,
            new_rows=per_sample_rows_new,
            key_fields=["split_id", "partition", "idx"],
            out_fields=per_sample_fields,
        ),
        per_sample_fields,
    )

    _write_csv(
        per_channel_path,
        _upsert_by_keys(
            existing_rows=existing_per_channel,
            new_rows=per_channel_rows_new,
            key_fields=["split_id", "partition", "ch"],
            out_fields=per_channel_fields,
        ),
        per_channel_fields,
    )

    _write_csv(
        all_zero_path,
        _upsert_by_keys(
            existing_rows=existing_all_zero,
            new_rows=all_zero_rows_new,
            key_fields=["split_id", "partition", "idx"],
            out_fields=all_zero_fields,
        ),
        all_zero_fields,
    )

    vocab_payload = {
        "snapshot_date": snapshot_date,
        "split_id": args.split_id,
        "protocol": args.protocol,
        "seed": args.seed,
        "subject": args.subject,
        "split_npz": str(split_npz),
        "vocab": {
            "train": sorted(vocab_by_part.get("train", [])),
            "test": sorted(vocab_by_part.get("test", [])),
            "competition": sorted(vocab_by_part.get("competition", [])),
        },
    }

    if vocab_sets_path.exists():
        existing = json.loads(vocab_sets_path.read_text(encoding="utf-8"))
        if not isinstance(existing, dict):
            existing = {}
    else:
        existing = {}
    existing[args.split_id] = vocab_payload
    vocab_sets_path.parent.mkdir(parents=True, exist_ok=True)
    vocab_sets_path.write_text(json.dumps(existing, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"[OK] split audit complete: split_id={args.split_id} protocol={args.protocol}")


if __name__ == "__main__":
    main()
