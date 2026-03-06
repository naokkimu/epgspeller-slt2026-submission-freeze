#!/usr/bin/env python3
"""Generate uc20260226 sweep matrices (deterministic, no execution).

Outputs (under sweeps/uc20260226/matrices/):
- uc_spatial2d_patchpool_k124.csv   (104 runs; derived from msx_spatial_k124 spatial2d rows)
- uc_p3_to4_vector.csv             (12 runs; P3 single-source to subj4=su, vector)
- uc_p3ms_to4_vector.csv           (12 runs; P3MS multi-source to subj4=su, vector)
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (expected scripts/ and src/)")


def _read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _write_rows(path: Path, rows: Sequence[Dict[str, str]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fieldnames))
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def _must_get(row: Dict[str, str], key: str) -> str:
    if key not in row:
        raise KeyError(f"Missing column {key!r}")
    return row[key]


def _clone_row(row: Dict[str, str]) -> Dict[str, str]:
    return {k: (v if v is not None else "") for k, v in row.items()}


def _make_patchpool_rows(msx_rows: Sequence[Dict[str, str]], *, tag: str) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for r in msx_rows:
        if (_must_get(r, "model_family") or "").strip() != "spatial2d_uni_gru":
            continue
        # msx already has enable_spatial_aug in {0,1}; keep it.
        rr = _clone_row(r)
        rr["model_family"] = "spatial2d_patchpool_uni_gru"
        rr["note"] = "uc:spatial2d_patchpool_k124"

        rid = (_must_get(rr, "run_id") or "").strip()
        if not rid:
            raise ValueError("Empty run_id in msx matrix")
        rid = rid.replace("spatial2d_uni_gru", "spatial2d_patchpool_uni_gru")
        rid = rid.replace("msx20260224", tag)
        if tag not in rid:
            # Hard fail to avoid accidental overwrite.
            raise ValueError(f"run_id tag replacement failed: rid={rid}")
        rr["run_id"] = rid
        out.append(rr)

    if len(out) != 104:
        raise SystemExit(f"Expected 104 patchpool rows, got {len(out)}. Check msx matrix contents.")
    return out


def _base_row_for_vector(msx_rows: Sequence[Dict[str, str]]) -> Dict[str, str]:
    # Use any msx row as template for shared hyperparameters.
    if not msx_rows:
        raise SystemExit("msx_rows is empty")
    return _clone_row(msx_rows[0])


def _make_to4_vector_rows(
    *,
    base: Dict[str, str],
    protocol: str,
    split_ids: Sequence[str],
    split_npz_paths: Sequence[str],
    dataset_pickle_paths: Sequence[str],
    tag: str,
    note: str,
) -> List[Dict[str, str]]:
    if not (len(split_ids) == len(split_npz_paths) == len(dataset_pickle_paths)):
        raise ValueError("split_ids/split_npz_paths/dataset_pickle_paths length mismatch")

    out: List[Dict[str, str]] = []
    for split_id, split_npz, pkl in zip(split_ids, split_npz_paths, dataset_pickle_paths):
        r = _clone_row(base)
        r["protocol"] = protocol
        r["split_id"] = split_id
        r["split_npz"] = split_npz
        r["dataset_pickle"] = pkl
        r["model_family"] = "uni_gru"
        r["enable_spatial_aug"] = "0"
        r["subset_method"] = ""
        r["selection_rank"] = ""
        r["note"] = note

        # Ensure baseline-aligned settings (do not inherit a spatial model run_id).
        # Keep these explicit to avoid silent drift.
        r["n_units"] = "512"
        r["n_layers"] = "5"
        r["stride_len"] = "4"
        r["kernel_len"] = "32"
        r["input_proj_dim"] = "64"
        r["specaug_on"] = "1"
        r["white_noise_sd"] = "0.8"
        r["constant_offset_sd"] = "0.2"
        r["gaussian_smooth_width"] = "2.0"
        r["frame_ms"] = "10.0"
        r["n_batch"] = "10000"
        r["train_seed"] = "0"
        r["electrode_regions"] = "all"
        r["n_components"] = "-1"
        r["downsample_factor"] = "1"

        r["run_id"] = (
            f"{protocol}_{split_id}_raw_ds1_el-all_uni_gru_u512_l5_s4_k32_proj64_spec1_noiseDefault_trainseed0_{tag}"
        )
        out.append(r)

    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate uc20260226 matrices.")
    ap.add_argument("--tag", type=str, default="uc20260226")
    ap.add_argument(
        "--msx_spatial_matrix",
        type=Path,
        default=Path("sweeps/msx20260224/matrices/msx_spatial_k124.csv"),
        help="Source msx matrix used as hyperparameter template.",
    )
    ap.add_argument(
        "--out_dir",
        type=Path,
        default=Path("sweeps/uc20260226/matrices"),
        help="Output directory for generated matrices.",
    )
    args = ap.parse_args()

    repo_root = _find_repo_root()
    msx_matrix = args.msx_spatial_matrix if args.msx_spatial_matrix.is_absolute() else (repo_root / args.msx_spatial_matrix)
    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)

    if not msx_matrix.is_file():
        raise SystemExit(f"msx_spatial_matrix not found: {msx_matrix}")

    msx_rows = _read_rows(msx_matrix)
    if not msx_rows:
        raise SystemExit(f"msx_spatial_matrix is empty: {msx_matrix}")

    fieldnames = list(msx_rows[0].keys())
    for k in ["run_id", "protocol", "split_id", "split_npz", "dataset_pickle", "model_family", "enable_spatial_aug"]:
        if k not in fieldnames:
            raise SystemExit(f"msx_spatial_matrix missing required column: {k}")

    # --- spatial2d_patchpool at full channels (K=124), 104 runs ---
    patchpool_rows = _make_patchpool_rows(msx_rows, tag=args.tag)
    out_patchpool = out_dir / "uc_spatial2d_patchpool_k124.csv"
    _write_rows(out_patchpool, patchpool_rows, fieldnames=fieldnames)
    print(f"[OK] wrote: {out_patchpool} rows={len(patchpool_rows)}")

    # --- to4 vector matrices (need new dataset pickles under data/uc20260226) ---
    base = _base_row_for_vector(msx_rows)

    # P3: subj{1,2,3} -> subj4, seed0..3
    p3_split_ids: List[str] = []
    p3_split_npz: List[str] = []
    p3_pkl: List[str] = []
    for src in [1, 2, 3]:
        for seed in [0, 1, 2, 3]:
            sid = f"subj{src}to4_seed{seed}"
            p3_split_ids.append(sid)
            p3_split_npz.append(f"raw_dataset/protocolSx_split_seed{seed}_subj{src}to4_ds1.npz")
            p3_pkl.append(f"data/{args.tag}/P3_{sid}_raw_ds1_el-all.pkl")

    p3_rows = _make_to4_vector_rows(
        base=base,
        protocol="P3",
        split_ids=p3_split_ids,
        split_npz_paths=p3_split_npz,
        dataset_pickle_paths=p3_pkl,
        tag=args.tag,
        note="uc:to4_vector",
    )
    if len(p3_rows) != 12:
        raise SystemExit(f"Expected 12 P3->4 rows, got {len(p3_rows)}")
    out_p3 = out_dir / "uc_p3_to4_vector.csv"
    _write_rows(out_p3, p3_rows, fieldnames=fieldnames)
    print(f"[OK] wrote: {out_p3} rows={len(p3_rows)}")

    # P3MS: subj{12,13,23} -> subj4, seed0..3
    p3ms_split_ids: List[str] = []
    p3ms_split_npz: List[str] = []
    p3ms_pkl: List[str] = []
    for pair in ["12", "13", "23"]:
        for seed in [0, 1, 2, 3]:
            sid = f"subj{pair}to4_seed{seed}"
            p3ms_split_ids.append(sid)
            p3ms_split_npz.append(f"raw_dataset/protocolSxms_split_seed{seed}_subj{pair}to4_ds1.npz")
            p3ms_pkl.append(f"data/{args.tag}/P3MS_{sid}_raw_ds1_el-all.pkl")

    p3ms_rows = _make_to4_vector_rows(
        base=base,
        protocol="P3MS",
        split_ids=p3ms_split_ids,
        split_npz_paths=p3ms_split_npz,
        dataset_pickle_paths=p3ms_pkl,
        tag=args.tag,
        note="uc:to4_vector",
    )
    if len(p3ms_rows) != 12:
        raise SystemExit(f"Expected 12 P3MS->4 rows, got {len(p3ms_rows)}")
    out_p3ms = out_dir / "uc_p3ms_to4_vector.csv"
    _write_rows(out_p3ms, p3ms_rows, fieldnames=fieldnames)
    print(f"[OK] wrote: {out_p3ms} rows={len(p3ms_rows)}")


if __name__ == "__main__":
    main()

