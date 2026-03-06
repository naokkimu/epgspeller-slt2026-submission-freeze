#!/usr/bin/env python3
"""Generate multi-subject baseline matrix (P1/P2/P3) for ms20260224.

This script does not execute experiments.
It produces a stage-matrix-compatible CSV that can be converted to cmdlists via
scripts/rebuttal/gc_make_cmdlists.py.

Row count (baseline only): 52
- P1: subj1..subj4 × seed0..3 = 16
- P2: subj1..subj3 × seed0..3 = 12
- P3: 6 directions (ordered pairs over subj1..subj3) × seed0..3 = 24
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Optional, Sequence


TAG_DEFAULT = "ms20260224"


STAGE_MATRIX_COLUMNS: List[str] = [
    "run_id",
    "protocol",
    "split_id",
    "split_npz",
    "dataset_pickle",
    "n_components",
    "downsample_factor",
    "electrode_regions",
    "apply_ts2vec",
    "ts2vec_output_dims",
    "ts2vec_epochs",
    "ts2vec_hidden_dims",
    "ts2vec_depth",
    "ts2vec_batch_size",
    "model_family",
    "n_units",
    "n_layers",
    "stride_len",
    "kernel_len",
    "input_proj_dim",
    "tcn_layers",
    "tcn_kernel_size",
    "transformer_heads",
    "transformer_layers",
    "transformer_ff_mult",
    "specaug_on",
    "white_noise_sd",
    "constant_offset_sd",
    "gaussian_smooth_width",
    "frame_ms",
    "n_batch",
    "train_seed",
    "selection_rank",
    "note",
]


def _sanitize_regions(regions: str) -> str:
    parts = [p for p in (regions or "").strip().split() if p]
    if not parts:
        return "all"
    return "-".join(parts)


def _repr_tag(n_components: int) -> str:
    return "raw" if int(n_components) == -1 else f"pca{int(n_components)}"


def _dataset_pickle(
    *,
    protocol: str,
    split_id: str,
    n_components: int,
    downsample_factor: int,
    electrode_regions: str,
    tag: str,
    apply_ts2vec: bool = False,
    ts2vec_output_dims: int = 320,
) -> str:
    rep = _repr_tag(n_components)
    ds = f"ds{int(downsample_factor)}"
    el = f"el-{_sanitize_regions(electrode_regions)}"
    suffix = f"_ts2vec{int(ts2vec_output_dims)}" if apply_ts2vec else ""
    return f"data/{tag}/{protocol}_{split_id}_{rep}_{ds}_{el}{suffix}.pkl"


def _proj_tag(input_proj_dim: Optional[int]) -> str:
    return "projNone" if (input_proj_dim is None) else f"proj{int(input_proj_dim)}"


def _run_id(
    *,
    protocol: str,
    split_id: str,
    n_components: int,
    downsample_factor: int,
    electrode_regions: str,
    model_family: str,
    n_units: int,
    n_layers: int,
    stride_len: int,
    kernel_len: int,
    input_proj_dim: Optional[int],
    specaug_on: int,
    noise_tag: str,
    train_seed: int,
    tag: str,
    extra_tags: Sequence[str] = (),
) -> str:
    rep = _repr_tag(n_components)
    ds = f"ds{int(downsample_factor)}"
    el = f"el-{_sanitize_regions(electrode_regions)}"
    proj = _proj_tag(input_proj_dim)
    base = [
        protocol,
        split_id,
        rep,
        ds,
        el,
        model_family,
        f"u{int(n_units)}",
        f"l{int(n_layers)}",
        f"s{int(stride_len)}",
        f"k{int(kernel_len)}",
        proj,
        f"spec{int(specaug_on)}",
        noise_tag,
        f"trainseed{int(train_seed)}",
        *list(extra_tags),
        tag,
    ]
    return "_".join(base)


def _write_csv(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            out = {k: r.get(k, "") for k in fieldnames}
            w.writerow(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate multi-subject baseline matrix CSV")
    ap.add_argument("--tag", type=str, default=TAG_DEFAULT)
    ap.add_argument(
        "--out_csv",
        type=Path,
        default=Path(f"sweeps/{TAG_DEFAULT}/matrices/ms_baseline.csv"),
    )
    args = ap.parse_args()

    tag = args.tag

    # Baseline (fixed center point; mirror gc_generate_matrices.py)
    n_components = -1
    downsample_factor = 1
    electrode_regions = "all"
    apply_ts2vec = False

    model_family = "uni_gru"
    n_units = 512
    n_layers = 5
    stride_len = 4
    kernel_len = 32
    input_proj_dim: Optional[int] = 64

    # Keep these filled to match stage matrices (train.py accepts them for all families).
    tcn_layers = 4
    tcn_kernel_size = 3
    transformer_heads = 4
    transformer_layers = 2
    transformer_ff_mult = 4

    specaug_on = 1
    noise_tag = "noiseDefault"
    white_noise_sd = 0.8
    constant_offset_sd = 0.2
    gaussian_smooth_width = 2.0

    frame_ms = 10.0
    n_batch = 10000
    train_seed = 0

    rows: List[Dict[str, str]] = []

    def add_row(*, protocol: str, split_id: str, split_npz: str, note: str) -> None:
        dataset_pickle = _dataset_pickle(
            protocol=protocol,
            split_id=split_id,
            n_components=n_components,
            downsample_factor=downsample_factor,
            electrode_regions=electrode_regions,
            tag=tag,
            apply_ts2vec=apply_ts2vec,
        )
        run_id = _run_id(
            protocol=protocol,
            split_id=split_id,
            n_components=n_components,
            downsample_factor=downsample_factor,
            electrode_regions=electrode_regions,
            model_family=model_family,
            n_units=n_units,
            n_layers=n_layers,
            stride_len=stride_len,
            kernel_len=kernel_len,
            input_proj_dim=input_proj_dim,
            specaug_on=specaug_on,
            noise_tag=noise_tag,
            train_seed=train_seed,
            tag=tag,
        )

        rows.append(
            {
                "run_id": run_id,
                "protocol": protocol,
                "split_id": split_id,
                "split_npz": split_npz,
                "dataset_pickle": dataset_pickle,
                "n_components": str(n_components),
                "downsample_factor": str(downsample_factor),
                "electrode_regions": electrode_regions,
                "apply_ts2vec": "1" if apply_ts2vec else "0",
                "ts2vec_output_dims": "",
                "ts2vec_epochs": "",
                "ts2vec_hidden_dims": "",
                "ts2vec_depth": "",
                "ts2vec_batch_size": "",
                "model_family": model_family,
                "n_units": str(n_units),
                "n_layers": str(n_layers),
                "stride_len": str(stride_len),
                "kernel_len": str(kernel_len),
                "input_proj_dim": str(input_proj_dim) if input_proj_dim is not None else "",
                "tcn_layers": str(tcn_layers),
                "tcn_kernel_size": str(tcn_kernel_size),
                "transformer_heads": str(transformer_heads),
                "transformer_layers": str(transformer_layers),
                "transformer_ff_mult": str(transformer_ff_mult),
                "specaug_on": str(specaug_on),
                "white_noise_sd": str(white_noise_sd),
                "constant_offset_sd": str(constant_offset_sd),
                "gaussian_smooth_width": str(gaussian_smooth_width),
                "frame_ms": str(frame_ms),
                "n_batch": str(n_batch),
                "train_seed": str(train_seed),
                "selection_rank": "",
                "note": note,
            }
        )

    # P1: subj1..subj4 × seed0..3
    for subj in range(1, 5):
        for seed in range(4):
            split_id = f"subj{subj}_seed{seed}"
            split_npz = f"raw_dataset/train_test_competition_split_seed{seed}_subj{subj}_ds1.npz"
            add_row(protocol="P1", split_id=split_id, split_npz=split_npz, note="baseline:multi_subj")

    # P2: subj1..subj3 × seed0..3
    for subj in range(1, 4):
        for seed in range(4):
            split_id = f"subj{subj}_seed{seed}"
            split_npz = f"raw_dataset/protocolS_split_seed{seed}_subj{subj}_ds1.npz"
            add_row(protocol="P2", split_id=split_id, split_npz=split_npz, note="baseline:multi_subj")

    # P3: 6 directions × seed0..3
    directions = [
        "subj1to2",
        "subj2to1",
        "subj1to3",
        "subj3to1",
        "subj2to3",
        "subj3to2",
    ]
    for direction in directions:
        for seed in range(4):
            split_id = f"{direction}_seed{seed}"
            split_npz = f"raw_dataset/protocolSx_split_seed{seed}_{direction}_ds1.npz"
            add_row(protocol="P3", split_id=split_id, split_npz=split_npz, note="baseline:multi_subj")

    if len(rows) != 52:
        raise SystemExit(f"Bug: expected 52 rows but got {len(rows)}")

    run_ids = [r["run_id"] for r in rows]
    if len(run_ids) != len(set(run_ids)):
        dupes = [rid for rid in sorted(set(run_ids)) if run_ids.count(rid) > 1][:10]
        raise SystemExit(f"Duplicate run_id detected (examples): {dupes}")

    _write_csv(args.out_csv, rows, STAGE_MATRIX_COLUMNS)
    print(f"[OK] wrote {args.out_csv} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
