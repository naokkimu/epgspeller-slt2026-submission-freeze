#!/usr/bin/env python3
"""Generate training matrices for spatial front-end experiments (EPG design).

Outputs (default):
- sweeps/ed20260217/matrices/ed_p1_spatial2d_compare.csv
- sweeps/ed20260217/matrices/ed_p1_rowcol_compare.csv
- sweeps/ed20260217/matrices/ed_p1_spatial2d_aug.csv

These matrices are consumable by `scripts/rebuttal/gc_make_cmdlists.py`.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Set, Tuple


FIELDNAMES = [
    "run_id",
    "protocol",
    "split_id",
    "dataset_pickle",
    "n_components",
    "downsample_factor",
    "electrode_regions",
    "model_family",
    "n_units",
    "n_layers",
    "stride_len",
    "kernel_len",
    "input_proj_dim",
    "specaug_on",
    "enable_spatial_aug",
    "white_noise_sd",
    "constant_offset_sd",
    "gaussian_smooth_width",
    "frame_ms",
    "n_batch",
    "train_seed",
    "subset_id",
    "subset_method",
    "subset_K",
    "subset_random_seed",
    "note",
]


def _read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDNAMES})


def _ensure_have(subset_rows: List[Dict[str, str]], need: Set[str]) -> None:
    have = {((r.get("subset_id") or "").strip()) for r in subset_rows}
    missing = sorted(list(need - have))
    if missing:
        raise SystemExit(f"subset_defs missing required subset_id(s): {missing}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate spatial-front-end matrices (P1).")
    ap.add_argument("--subset_defs", type=Path, required=True)
    ap.add_argument("--subset_pkl_dir", type=Path, default=Path("data/ed20260217"))
    ap.add_argument("--baseline_pkl_dir", type=Path, default=Path("data/gc20260216"))
    ap.add_argument("--out_dir", type=Path, default=Path("sweeps/ed20260217/matrices"))
    ap.add_argument("--seeds", type=str, default="0,1,2,3")
    ap.add_argument("--tag", type=str, default="ed20260217")
    args = ap.parse_args()

    subset_rows = _read_rows(args.subset_defs)
    if not subset_rows:
        raise SystemExit(f"No subset rows in {args.subset_defs}")

    seeds = [int(x.strip()) for x in args.seeds.split(",") if x.strip()]
    if not seeds:
        raise SystemExit("--seeds must be non-empty (e.g., 0,1,2,3)")

    fixed = {
        "protocol": "P1",
        "n_components": "-1",
        "downsample_factor": "1",
        "electrode_regions": "all",
        "n_units": "512",
        "n_layers": "5",
        "stride_len": "4",
        "kernel_len": "32",
        "input_proj_dim": "64",
        "specaug_on": "1",
        "white_noise_sd": "0.8",
        "constant_offset_sd": "0.2",
        "gaussian_smooth_width": "2.0",
        "frame_ms": "10.0",
        "n_batch": "10000",
        "train_seed": "0",
    }

    # --- H11: spatial2d compare (K=32/64/96, topk/fps2k) + baseline124 ---
    need_h11 = {"topk_k32", "topk_k64", "topk_k96", "fps2k_k32", "fps2k_k64", "fps2k_k96"}
    _ensure_have(subset_rows, need_h11)

    spatial2d_rows: List[Dict[str, str]] = []
    for s in seeds:
        split_id = f"seed{s}"
        for subset_id, method, k in [
            ("topk_k32", "topk", "32"),
            ("fps2k_k32", "fps2k", "32"),
            ("topk_k64", "topk", "64"),
            ("fps2k_k64", "fps2k", "64"),
            ("topk_k96", "topk", "96"),
            ("fps2k_k96", "fps2k", "96"),
        ]:
            pkl = args.subset_pkl_dir / f"P1_seed{s}_raw_ds1_{subset_id}.pkl"
            run_id = (
                f"P1_seed{s}_raw_ds1_sub-{subset_id}_"
                f"spatial2d_uni_gru_u512_l5_s4_k32_proj64_spec1_spaug0_noiseDefault_trainseed0_{args.tag}"
            )
            row = dict(fixed)
            row.update(
                {
                    "run_id": run_id,
                    "split_id": split_id,
                    "dataset_pickle": str(pkl),
                    "model_family": "spatial2d_uni_gru",
                    "enable_spatial_aug": "0",
                    "subset_id": subset_id,
                    "subset_method": method,
                    "subset_K": k,
                    "subset_random_seed": "",
                    "note": "ed:spatial2d_compare",
                }
            )
            spatial2d_rows.append(row)

        # baseline124
        pkl_all = args.baseline_pkl_dir / f"P1_seed{s}_raw_ds1_el-all.pkl"
        run_id_all = (
            f"P1_seed{s}_raw_ds1_sub-el-all_"
            f"spatial2d_uni_gru_u512_l5_s4_k32_proj64_spec1_spaug0_noiseDefault_trainseed0_{args.tag}"
        )
        row_all = dict(fixed)
        row_all.update(
            {
                "run_id": run_id_all,
                "split_id": split_id,
                "dataset_pickle": str(pkl_all),
                "model_family": "spatial2d_uni_gru",
                "enable_spatial_aug": "0",
                "subset_id": "el-all",
                "subset_method": "all",
                "subset_K": "124",
                "subset_random_seed": "",
                "note": "ed:spatial2d_compare_baseline124",
            }
        )
        spatial2d_rows.append(row_all)

    out_spatial2d = args.out_dir / "ed_p1_spatial2d_compare.csv"
    _write_csv(out_spatial2d, spatial2d_rows)
    print(f"Wrote {out_spatial2d} ({len(spatial2d_rows)} rows)")

    # --- H13: row/col compare (K=32/64, topk/fps2k) + baseline124 ---
    need_h13 = {"topk_k32", "topk_k64", "fps2k_k32", "fps2k_k64"}
    _ensure_have(subset_rows, need_h13)

    rowcol_rows: List[Dict[str, str]] = []
    for s in seeds:
        split_id = f"seed{s}"
        for subset_id, method, k in [
            ("topk_k32", "topk", "32"),
            ("fps2k_k32", "fps2k", "32"),
            ("topk_k64", "topk", "64"),
            ("fps2k_k64", "fps2k", "64"),
        ]:
            pkl = args.subset_pkl_dir / f"P1_seed{s}_raw_ds1_{subset_id}.pkl"
            run_id = (
                f"P1_seed{s}_raw_ds1_sub-{subset_id}_"
                f"rowcol_uni_gru_u512_l5_s4_k32_proj64_spec1_noiseDefault_trainseed0_{args.tag}"
            )
            row = dict(fixed)
            row.update(
                {
                    "run_id": run_id,
                    "split_id": split_id,
                    "dataset_pickle": str(pkl),
                    "model_family": "rowcol_uni_gru",
                    "enable_spatial_aug": "0",
                    "subset_id": subset_id,
                    "subset_method": method,
                    "subset_K": k,
                    "subset_random_seed": "",
                    "note": "ed:rowcol_compare",
                }
            )
            rowcol_rows.append(row)

        # baseline124
        pkl_all = args.baseline_pkl_dir / f"P1_seed{s}_raw_ds1_el-all.pkl"
        run_id_all = (
            f"P1_seed{s}_raw_ds1_sub-el-all_"
            f"rowcol_uni_gru_u512_l5_s4_k32_proj64_spec1_noiseDefault_trainseed0_{args.tag}"
        )
        row_all = dict(fixed)
        row_all.update(
            {
                "run_id": run_id_all,
                "split_id": split_id,
                "dataset_pickle": str(pkl_all),
                "model_family": "rowcol_uni_gru",
                "enable_spatial_aug": "0",
                "subset_id": "el-all",
                "subset_method": "all",
                "subset_K": "124",
                "subset_random_seed": "",
                "note": "ed:rowcol_compare_baseline124",
            }
        )
        rowcol_rows.append(row_all)

    out_rowcol = args.out_dir / "ed_p1_rowcol_compare.csv"
    _write_csv(out_rowcol, rowcol_rows)
    print(f"Wrote {out_rowcol} ({len(rowcol_rows)} rows)")

    # --- H12: spatial2d + spatial aug (K=64 topk only; aug=1) ---
    need_h12 = {"topk_k64"}
    _ensure_have(subset_rows, need_h12)

    spatial2d_aug_rows: List[Dict[str, str]] = []
    for s in seeds:
        split_id = f"seed{s}"
        subset_id = "topk_k64"
        pkl = args.subset_pkl_dir / f"P1_seed{s}_raw_ds1_{subset_id}.pkl"
        run_id = (
            f"P1_seed{s}_raw_ds1_sub-{subset_id}_"
            f"spatial2d_uni_gru_u512_l5_s4_k32_proj64_spec1_spaug1_noiseDefault_trainseed0_{args.tag}"
        )
        row = dict(fixed)
        row.update(
            {
                "run_id": run_id,
                "split_id": split_id,
                "dataset_pickle": str(pkl),
                "model_family": "spatial2d_uni_gru",
                "enable_spatial_aug": "1",
                "subset_id": subset_id,
                "subset_method": "topk",
                "subset_K": "64",
                "subset_random_seed": "",
                "note": "ed:spatial2d_aug",
            }
        )
        spatial2d_aug_rows.append(row)

    out_spatial2d_aug = args.out_dir / "ed_p1_spatial2d_aug.csv"
    _write_csv(out_spatial2d_aug, spatial2d_aug_rows)
    print(f"Wrote {out_spatial2d_aug} ({len(spatial2d_aug_rows)} rows)")


if __name__ == "__main__":
    main()

