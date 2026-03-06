#!/usr/bin/env python3
"""Generate training matrices for EPG design sweeps (P1-only).

This creates CSV matrices consumable by `scripts/rebuttal/gc_make_cmdlists.py`.
It assumes subset pickles have already been created under data/ed20260217/.

Outputs (default):
- sweeps/ed20260217/matrices/ed_p1_kcurve.csv
- sweeps/ed20260217/matrices/ed_p1_k64_spec0.csv
- sweeps/ed20260217/matrices/ed_p1_projNone.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List


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


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate EPG design matrices (P1).")
    ap.add_argument("--subset_defs", type=Path, required=True)
    ap.add_argument("--data_dir", type=Path, default=Path("data/ed20260217"))
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
        "model_family": "uni_gru",
        "n_units": "512",
        "n_layers": "5",
        "stride_len": "4",
        "kernel_len": "32",
        "white_noise_sd": "0.8",
        "constant_offset_sd": "0.2",
        "gaussian_smooth_width": "2.0",
        "frame_ms": "10.0",
        "n_batch": "10000",
        "train_seed": "0",
    }

    # Main k-curve matrix: proj64 + spec1
    kcurve: List[Dict[str, str]] = []
    for s in seeds:
        split_id = f"seed{s}"
        for sub in subset_rows:
            subset_id = (sub.get("subset_id") or "").strip()
            method = (sub.get("method") or "").strip()
            k = (sub.get("K") or "").strip()
            rseed = (sub.get("random_seed") or "").strip()
            if not subset_id:
                continue
            pkl = args.data_dir / f"P1_seed{s}_raw_ds1_{subset_id}.pkl"
            run_id = (
                f"P1_seed{s}_raw_ds1_sub-{subset_id}_"
                f"uni_gru_u512_l5_s4_k32_proj64_spec1_noiseDefault_trainseed0_{args.tag}"
            )
            row = dict(fixed)
            row.update(
                {
                    "run_id": run_id,
                    "split_id": split_id,
                    "dataset_pickle": str(pkl),
                    "input_proj_dim": "64",
                    "specaug_on": "1",
                    "subset_id": subset_id,
                    "subset_method": method,
                    "subset_K": k,
                    "subset_random_seed": rseed,
                    "note": "ed:kcurve",
                }
            )
            kcurve.append(row)

    out_kcurve = args.out_dir / "ed_p1_kcurve.csv"
    _write_csv(out_kcurve, kcurve)
    print(f"Wrote {out_kcurve} ({len(kcurve)} rows)")

    # H7: specaug_off for K=64 topk
    spec0_rows = [r for r in subset_rows if (r.get("subset_id") or "").strip() == "topk_k64"]
    if not spec0_rows:
        raise SystemExit("subset_defs missing required subset_id: topk_k64")
    spec0: List[Dict[str, str]] = []
    for s in seeds:
        subset_id = "topk_k64"
        pkl = args.data_dir / f"P1_seed{s}_raw_ds1_{subset_id}.pkl"
        run_id = (
            f"P1_seed{s}_raw_ds1_sub-{subset_id}_"
            f"uni_gru_u512_l5_s4_k32_proj64_spec0_noiseDefault_trainseed0_{args.tag}"
        )
        row = dict(fixed)
        row.update(
            {
                "run_id": run_id,
                "split_id": f"seed{s}",
                "dataset_pickle": str(pkl),
                "input_proj_dim": "64",
                "specaug_on": "0",
                "subset_id": subset_id,
                "subset_method": "topk",
                "subset_K": "64",
                "subset_random_seed": "",
                "note": "ed:spec0",
            }
        )
        spec0.append(row)

    out_spec0 = args.out_dir / "ed_p1_k64_spec0.csv"
    _write_csv(out_spec0, spec0)
    print(f"Wrote {out_spec0} ({len(spec0)} rows)")

    # H8: projNone for K in {16,32,64} topk
    need = {"topk_k16", "topk_k32", "topk_k64"}
    have = {((r.get("subset_id") or "").strip()) for r in subset_rows}
    missing = sorted(list(need - have))
    if missing:
        raise SystemExit(f"subset_defs missing required subsets: {missing}")

    proj_none: List[Dict[str, str]] = []
    for s in seeds:
        for subset_id in ["topk_k16", "topk_k32", "topk_k64"]:
            k = subset_id.split("_k", 1)[1]
            pkl = args.data_dir / f"P1_seed{s}_raw_ds1_{subset_id}.pkl"
            run_id = (
                f"P1_seed{s}_raw_ds1_sub-{subset_id}_"
                f"uni_gru_u512_l5_s4_k32_projNone_spec1_noiseDefault_trainseed0_{args.tag}"
            )
            row = dict(fixed)
            row.update(
                {
                    "run_id": run_id,
                    "split_id": f"seed{s}",
                    "dataset_pickle": str(pkl),
                    "input_proj_dim": "",
                    "specaug_on": "1",
                    "subset_id": subset_id,
                    "subset_method": "topk",
                    "subset_K": k,
                    "subset_random_seed": "",
                    "note": "ed:projNone",
                }
            )
            proj_none.append(row)

    out_proj_none = args.out_dir / "ed_p1_projNone.csv"
    _write_csv(out_proj_none, proj_none)
    print(f"Wrote {out_proj_none} ({len(proj_none)} rows)")


if __name__ == "__main__":
    main()

