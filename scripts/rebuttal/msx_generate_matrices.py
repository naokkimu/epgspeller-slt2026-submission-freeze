#!/usr/bin/env python3
"""Generate msx20260224 matrices (additional experiments on top of ms20260224 baseline).

This script does not execute experiments. It produces stage-matrix-compatible CSVs
that can be converted to cmdlists via scripts/rebuttal/gc_make_cmdlists.py.

Outputs under sweeps/<tag>/matrices:
- msx_spatial_k124.csv                 (156)  : rowcol/spatial2d (aug0/aug1) on K=124 pickles
- msx_k64_uni_gru.csv                  (208)  : uni_gru on K=64 subsets (4 methods) for P1/P2/P3
- msx_spatial_k64_within_topk.csv      (156)  : rowcol/spatial2d (aug0/aug1) on K=64 within_topk subsets
- msx_p3ms.csv                         (48)   : P3MS (2SRC->1TGT) with 4 model variants
- msx_kshot_subj3.csv                  (32)   : subj3 k-shot (k=1/2) with 4 model variants
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


TAG_DEFAULT = "msx20260224"


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
    "enable_spatial_aug",
    "subset_method",
    "note",
]


def _read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def _sanitize_regions(regions: str) -> str:
    parts = [p for p in (regions or "").strip().split() if p]
    if not parts:
        return "all"
    return "-".join(parts)


def _repr_tag(n_components: int) -> str:
    return "raw" if int(n_components) == -1 else f"pca{int(n_components)}"


def _proj_tag(input_proj_dim: Optional[int]) -> str:
    return "projNone" if (input_proj_dim is None) else f"proj{int(input_proj_dim)}"


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


def _subset_pkl_path(dataset_pickle: str, *, tag: str, subset_method: str) -> str:
    # Replace data/<baseline_tag>/... with data/<tag>/... and append subset suffix.
    p = Path(dataset_pickle)
    parts = list(p.parts)
    if len(parts) < 2 or parts[0] != "data":
        raise ValueError(f"Unexpected dataset_pickle path (expected data/<tag>/...): {dataset_pickle}")
    # parts[1] is baseline tag directory
    parts[1] = tag
    stem = Path(parts[-1]).stem
    parts[-1] = f"{stem}_{subset_method}.pkl"
    return str(Path(*parts))


def _baseline_row_base(row: Dict[str, str]) -> Dict[str, str]:
    # Keep only expected stage matrix columns (and provide missing keys as '').
    return {k: (row.get(k, "") or "") for k in STAGE_MATRIX_COLUMNS}


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate msx matrices (spatial, K64, multi-source, k-shot).")
    ap.add_argument("--tag", type=str, default=TAG_DEFAULT)
    ap.add_argument(
        "--baseline_matrix",
        type=Path,
        default=Path("sweeps/ms20260224/matrices/ms_baseline.csv"),
    )
    args = ap.parse_args()

    tag = args.tag
    base_rows = _read_rows(args.baseline_matrix)
    if not base_rows:
        raise SystemExit(f"No rows in baseline_matrix: {args.baseline_matrix}")

    # --- 1) Spatial@K124 (P1/P2/P3 only; 52 rows) ---
    spatial_rows: List[Dict[str, str]] = []
    for r in base_rows:
        protocol = (r.get("protocol") or "").strip()
        if protocol not in {"P1", "P2", "P3"}:
            continue

        base = _baseline_row_base(r)
        # Always reuse baseline dataset pickle (K=124) and split_npz.
        base["note"] = "msx:spatial_k124"
        base["subset_method"] = ""

        # row/col
        rr = dict(base)
        rr["model_family"] = "rowcol_uni_gru"
        rr["enable_spatial_aug"] = "0"
        rr["run_id"] = _run_id(
            protocol=protocol,
            split_id=base["split_id"],
            n_components=int(base["n_components"] or "-1"),
            downsample_factor=int(base["downsample_factor"] or "1"),
            electrode_regions=base["electrode_regions"] or "all",
            model_family="rowcol_uni_gru",
            n_units=int(base["n_units"] or "512"),
            n_layers=int(base["n_layers"] or "5"),
            stride_len=int(base["stride_len"] or "4"),
            kernel_len=int(base["kernel_len"] or "32"),
            input_proj_dim=int(base["input_proj_dim"] or "64") if (base["input_proj_dim"] or "").strip() else None,
            specaug_on=int(base["specaug_on"] or "1"),
            noise_tag="noiseDefault",
            train_seed=int(base["train_seed"] or "0"),
            tag=tag,
            extra_tags=(),
        )
        spatial_rows.append(rr)

        # spatial2d aug0/aug1
        for aug, aug_tag in [(0, "spaug0"), (1, "spaug1")]:
            sr = dict(base)
            sr["model_family"] = "spatial2d_uni_gru"
            sr["enable_spatial_aug"] = str(int(aug))
            sr["run_id"] = _run_id(
                protocol=protocol,
                split_id=base["split_id"],
                n_components=int(base["n_components"] or "-1"),
                downsample_factor=int(base["downsample_factor"] or "1"),
                electrode_regions=base["electrode_regions"] or "all",
                model_family="spatial2d_uni_gru",
                n_units=int(base["n_units"] or "512"),
                n_layers=int(base["n_layers"] or "5"),
                stride_len=int(base["stride_len"] or "4"),
                kernel_len=int(base["kernel_len"] or "32"),
                input_proj_dim=int(base["input_proj_dim"] or "64") if (base["input_proj_dim"] or "").strip() else None,
                specaug_on=int(base["specaug_on"] or "1"),
                noise_tag="noiseDefault",
                train_seed=int(base["train_seed"] or "0"),
                tag=tag,
                extra_tags=(aug_tag,),
            )
            spatial_rows.append(sr)

    if len(spatial_rows) != 156:
        raise SystemExit(f"Bug: msx_spatial_k124 expected 156 rows but got {len(spatial_rows)}")

    # --- 2) K=64 uni_gru (4 methods) on P1/P2/P3 baseline splits ---
    k64_methods = [
        "within_topk64",
        "within_fps2k64",
        "transfer_subj1_topk64",
        "random64_seed20260224",
    ]

    k64_rows: List[Dict[str, str]] = []
    for r in base_rows:
        protocol = (r.get("protocol") or "").strip()
        if protocol not in {"P1", "P2", "P3"}:
            continue
        base = _baseline_row_base(r)
        base["note"] = "msx:k64_uni_gru"
        base["model_family"] = "uni_gru"
        base["enable_spatial_aug"] = ""

        for method in k64_methods:
            rr = dict(base)
            rr["subset_method"] = method
            rr["dataset_pickle"] = _subset_pkl_path(base["dataset_pickle"], tag=tag, subset_method=method)
            rr["run_id"] = _run_id(
                protocol=protocol,
                split_id=base["split_id"],
                n_components=int(base["n_components"] or "-1"),
                downsample_factor=int(base["downsample_factor"] or "1"),
                electrode_regions=base["electrode_regions"] or "all",
                model_family="uni_gru",
                n_units=int(base["n_units"] or "512"),
                n_layers=int(base["n_layers"] or "5"),
                stride_len=int(base["stride_len"] or "4"),
                kernel_len=int(base["kernel_len"] or "32"),
                input_proj_dim=int(base["input_proj_dim"] or "64") if (base["input_proj_dim"] or "").strip() else None,
                specaug_on=int(base["specaug_on"] or "1"),
                noise_tag="noiseDefault",
                train_seed=int(base["train_seed"] or "0"),
                tag=tag,
                extra_tags=("K64", method),
            )
            k64_rows.append(rr)

    if len(k64_rows) != 208:
        raise SystemExit(f"Bug: msx_k64_uni_gru expected 208 rows but got {len(k64_rows)}")

    # --- 3) Spatial@K64 within_topk (P1/P2/P3 only) ---
    spatial_k64_rows: List[Dict[str, str]] = []
    for r in base_rows:
        protocol = (r.get("protocol") or "").strip()
        if protocol not in {"P1", "P2", "P3"}:
            continue
        base = _baseline_row_base(r)
        base["note"] = "msx:spatial_k64_within_topk"
        base["subset_method"] = "within_topk64"
        base["dataset_pickle"] = _subset_pkl_path(base["dataset_pickle"], tag=tag, subset_method="within_topk64")

        # row/col
        rr = dict(base)
        rr["model_family"] = "rowcol_uni_gru"
        rr["enable_spatial_aug"] = "0"
        rr["run_id"] = _run_id(
            protocol=protocol,
            split_id=base["split_id"],
            n_components=int(base["n_components"] or "-1"),
            downsample_factor=int(base["downsample_factor"] or "1"),
            electrode_regions=base["electrode_regions"] or "all",
            model_family="rowcol_uni_gru",
            n_units=int(base["n_units"] or "512"),
            n_layers=int(base["n_layers"] or "5"),
            stride_len=int(base["stride_len"] or "4"),
            kernel_len=int(base["kernel_len"] or "32"),
            input_proj_dim=int(base["input_proj_dim"] or "64") if (base["input_proj_dim"] or "").strip() else None,
            specaug_on=int(base["specaug_on"] or "1"),
            noise_tag="noiseDefault",
            train_seed=int(base["train_seed"] or "0"),
            tag=tag,
            extra_tags=("K64", "within_topk64"),
        )
        spatial_k64_rows.append(rr)

        for aug, aug_tag in [(0, "spaug0"), (1, "spaug1")]:
            sr = dict(base)
            sr["model_family"] = "spatial2d_uni_gru"
            sr["enable_spatial_aug"] = str(int(aug))
            sr["run_id"] = _run_id(
                protocol=protocol,
                split_id=base["split_id"],
                n_components=int(base["n_components"] or "-1"),
                downsample_factor=int(base["downsample_factor"] or "1"),
                electrode_regions=base["electrode_regions"] or "all",
                model_family="spatial2d_uni_gru",
                n_units=int(base["n_units"] or "512"),
                n_layers=int(base["n_layers"] or "5"),
                stride_len=int(base["stride_len"] or "4"),
                kernel_len=int(base["kernel_len"] or "32"),
                input_proj_dim=int(base["input_proj_dim"] or "64") if (base["input_proj_dim"] or "").strip() else None,
                specaug_on=int(base["specaug_on"] or "1"),
                noise_tag="noiseDefault",
                train_seed=int(base["train_seed"] or "0"),
                tag=tag,
                extra_tags=("K64", "within_topk64", aug_tag),
            )
            spatial_k64_rows.append(sr)

    if len(spatial_k64_rows) != 156:
        raise SystemExit(
            f"Bug: msx_spatial_k64_within_topk expected 156 rows but got {len(spatial_k64_rows)}"
        )

    # --- 4) P3MS matrix (12 splits x 4 models) ---
    fixed = {
        "n_components": "-1",
        "downsample_factor": "1",
        "electrode_regions": "all",
        "apply_ts2vec": "0",
        "ts2vec_output_dims": "",
        "ts2vec_epochs": "",
        "ts2vec_hidden_dims": "",
        "ts2vec_depth": "",
        "ts2vec_batch_size": "",
        "n_units": "512",
        "n_layers": "5",
        "stride_len": "4",
        "kernel_len": "32",
        "input_proj_dim": "64",
        "tcn_layers": "4",
        "tcn_kernel_size": "3",
        "transformer_heads": "4",
        "transformer_layers": "2",
        "transformer_ff_mult": "4",
        "specaug_on": "1",
        "white_noise_sd": "0.8",
        "constant_offset_sd": "0.2",
        "gaussian_smooth_width": "2.0",
        "frame_ms": "10.0",
        "n_batch": "10000",
        "train_seed": "0",
        "selection_rank": "",
    }

    def _new_row(*, protocol: str, split_id: str, split_npz: str, dataset_pickle: str) -> Dict[str, str]:
        out = {k: "" for k in STAGE_MATRIX_COLUMNS}
        out.update(fixed)
        out["protocol"] = protocol
        out["split_id"] = split_id
        out["split_npz"] = split_npz
        out["dataset_pickle"] = dataset_pickle
        return out

    p3ms_rows: List[Dict[str, str]] = []
    p3ms_dirs = ["subj23to1", "subj13to2", "subj12to3"]
    for direction in p3ms_dirs:
        for seed in range(4):
            split_id = f"{direction}_seed{seed}"
            split_npz = f"raw_dataset/protocolSxms_split_seed{seed}_{direction}_ds1.npz"
            dataset_pickle = _dataset_pickle(
                protocol="P3MS",
                split_id=split_id,
                n_components=-1,
                downsample_factor=1,
                electrode_regions="all",
                tag=tag,
            )

            base = _new_row(protocol="P3MS", split_id=split_id, split_npz=split_npz, dataset_pickle=dataset_pickle)
            base["note"] = "msx:p3ms"
            base["subset_method"] = ""

            # 4 model variants
            # uni_gru
            rr = dict(base)
            rr["model_family"] = "uni_gru"
            rr["enable_spatial_aug"] = ""
            rr["run_id"] = _run_id(
                protocol="P3MS",
                split_id=split_id,
                n_components=-1,
                downsample_factor=1,
                electrode_regions="all",
                model_family="uni_gru",
                n_units=512,
                n_layers=5,
                stride_len=4,
                kernel_len=32,
                input_proj_dim=64,
                specaug_on=1,
                noise_tag="noiseDefault",
                train_seed=0,
                tag=tag,
                extra_tags=(),
            )
            p3ms_rows.append(rr)

            # rowcol
            rr = dict(base)
            rr["model_family"] = "rowcol_uni_gru"
            rr["enable_spatial_aug"] = "0"
            rr["run_id"] = _run_id(
                protocol="P3MS",
                split_id=split_id,
                n_components=-1,
                downsample_factor=1,
                electrode_regions="all",
                model_family="rowcol_uni_gru",
                n_units=512,
                n_layers=5,
                stride_len=4,
                kernel_len=32,
                input_proj_dim=64,
                specaug_on=1,
                noise_tag="noiseDefault",
                train_seed=0,
                tag=tag,
                extra_tags=(),
            )
            p3ms_rows.append(rr)

            for aug, aug_tag in [(0, "spaug0"), (1, "spaug1")]:
                rr = dict(base)
                rr["model_family"] = "spatial2d_uni_gru"
                rr["enable_spatial_aug"] = str(int(aug))
                rr["run_id"] = _run_id(
                    protocol="P3MS",
                    split_id=split_id,
                    n_components=-1,
                    downsample_factor=1,
                    electrode_regions="all",
                    model_family="spatial2d_uni_gru",
                    n_units=512,
                    n_layers=5,
                    stride_len=4,
                    kernel_len=32,
                    input_proj_dim=64,
                    specaug_on=1,
                    noise_tag="noiseDefault",
                    train_seed=0,
                    tag=tag,
                    extra_tags=(aug_tag,),
                )
                p3ms_rows.append(rr)

    if len(p3ms_rows) != 48:
        raise SystemExit(f"Bug: msx_p3ms expected 48 rows but got {len(p3ms_rows)}")

    # --- 5) k-shot matrix (8 splits x 4 models) ---
    kshot_rows: List[Dict[str, str]] = []
    for k in (1, 2):
        for seed in range(4):
            split_id = f"subj3_seed{seed}_k{k}"
            split_npz = f"raw_dataset/protocolSkshot_split_seed{seed}_subj3_k{k}_ds1.npz"
            dataset_pickle = _dataset_pickle(
                protocol="P2K",
                split_id=split_id,
                n_components=-1,
                downsample_factor=1,
                electrode_regions="all",
                tag=tag,
            )

            base = _new_row(protocol="P2K", split_id=split_id, split_npz=split_npz, dataset_pickle=dataset_pickle)
            base["note"] = "msx:kshot"
            base["subset_method"] = ""

            rr = dict(base)
            rr["model_family"] = "uni_gru"
            rr["enable_spatial_aug"] = ""
            rr["run_id"] = _run_id(
                protocol="P2K",
                split_id=split_id,
                n_components=-1,
                downsample_factor=1,
                electrode_regions="all",
                model_family="uni_gru",
                n_units=512,
                n_layers=5,
                stride_len=4,
                kernel_len=32,
                input_proj_dim=64,
                specaug_on=1,
                noise_tag="noiseDefault",
                train_seed=0,
                tag=tag,
                extra_tags=(),
            )
            kshot_rows.append(rr)

            rr = dict(base)
            rr["model_family"] = "rowcol_uni_gru"
            rr["enable_spatial_aug"] = "0"
            rr["run_id"] = _run_id(
                protocol="P2K",
                split_id=split_id,
                n_components=-1,
                downsample_factor=1,
                electrode_regions="all",
                model_family="rowcol_uni_gru",
                n_units=512,
                n_layers=5,
                stride_len=4,
                kernel_len=32,
                input_proj_dim=64,
                specaug_on=1,
                noise_tag="noiseDefault",
                train_seed=0,
                tag=tag,
                extra_tags=(),
            )
            kshot_rows.append(rr)

            for aug, aug_tag in [(0, "spaug0"), (1, "spaug1")]:
                rr = dict(base)
                rr["model_family"] = "spatial2d_uni_gru"
                rr["enable_spatial_aug"] = str(int(aug))
                rr["run_id"] = _run_id(
                    protocol="P2K",
                    split_id=split_id,
                    n_components=-1,
                    downsample_factor=1,
                    electrode_regions="all",
                    model_family="spatial2d_uni_gru",
                    n_units=512,
                    n_layers=5,
                    stride_len=4,
                    kernel_len=32,
                    input_proj_dim=64,
                    specaug_on=1,
                    noise_tag="noiseDefault",
                    train_seed=0,
                    tag=tag,
                    extra_tags=(aug_tag,),
                )
                kshot_rows.append(rr)

    if len(kshot_rows) != 32:
        raise SystemExit(f"Bug: msx_kshot_subj3 expected 32 rows but got {len(kshot_rows)}")

    # --- Write matrices ---
    out_dir = Path("sweeps") / tag / "matrices"
    _write_csv(out_dir / "msx_spatial_k124.csv", spatial_rows, STAGE_MATRIX_COLUMNS)
    _write_csv(out_dir / "msx_k64_uni_gru.csv", k64_rows, STAGE_MATRIX_COLUMNS)
    _write_csv(out_dir / "msx_spatial_k64_within_topk.csv", spatial_k64_rows, STAGE_MATRIX_COLUMNS)
    _write_csv(out_dir / "msx_p3ms.csv", p3ms_rows, STAGE_MATRIX_COLUMNS)
    _write_csv(out_dir / "msx_kshot_subj3.csv", kshot_rows, STAGE_MATRIX_COLUMNS)

    # Validate run_id uniqueness per file
    for name, rows in [
        ("msx_spatial_k124.csv", spatial_rows),
        ("msx_k64_uni_gru.csv", k64_rows),
        ("msx_spatial_k64_within_topk.csv", spatial_k64_rows),
        ("msx_p3ms.csv", p3ms_rows),
        ("msx_kshot_subj3.csv", kshot_rows),
    ]:
        run_ids = [r["run_id"] for r in rows]
        if len(run_ids) != len(set(run_ids)):
            raise SystemExit(f"Duplicate run_id detected in {name}")

    print(f"[OK] wrote matrices under: {out_dir}")


if __name__ == "__main__":
    main()

