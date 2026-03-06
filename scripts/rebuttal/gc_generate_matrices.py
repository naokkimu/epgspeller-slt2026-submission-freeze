#!/usr/bin/env python3
"""Generate gap-closure sweep matrices for a fixed run tag.

Design goals:
- No orchestrator usage: generate transparent CSVs that can be converted into cmdlists.
- Avoid human error: all rows are programmatically generated.
- Keep compatibility with existing sweep tooling: columns follow stage matrices.

This script does not execute experiments.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


TAG_DEFAULT = "gc20260216"


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


@dataclass(frozen=True)
class Split:
    protocol: str
    split_id: str
    split_npz: str


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


def _float_tag(x: float) -> str:
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return s.replace(".", "p")


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


def _splits() -> List[Split]:
    out: List[Split] = []
    for seed in range(4):
        out.append(
            Split(
                protocol="P1",
                split_id=f"seed{seed}",
                split_npz=f"raw_dataset/train_test_competition_split_seed{seed}.npz",
            )
        )
    for subj in (1, 2):
        for seed in range(4):
            out.append(
                Split(
                    protocol="P2",
                    split_id=f"subj{subj}_seed{seed}",
                    split_npz=f"raw_dataset/protocolS_split_seed{seed}_subj{subj}_ds1.npz",
                )
            )
    for direction in ("subj1to2", "subj2to1"):
        for seed in range(4):
            out.append(
                Split(
                    protocol="P3",
                    split_id=f"{direction}_seed{seed}",
                    split_npz=f"raw_dataset/protocolSx_split_seed{seed}_{direction}_ds1.npz",
                )
            )
    if len(out) != 20:
        raise SystemExit(f"Bug: expected 20 splits but got {len(out)}")
    return out


def _base_row(*, split: Split, tag: str) -> Dict[str, str]:
    # Baseline (fixed center point)
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
    specaug_on = 1
    noise_tag = "noiseDefault"
    white_noise_sd = 0.8
    constant_offset_sd = 0.2
    gaussian_smooth_width = 2.0
    frame_ms = 10.0
    n_batch = 10000
    train_seed = 0

    dataset_pickle = _dataset_pickle(
        protocol=split.protocol,
        split_id=split.split_id,
        n_components=n_components,
        downsample_factor=downsample_factor,
        electrode_regions=electrode_regions,
        tag=tag,
        apply_ts2vec=apply_ts2vec,
    )
    run_id = _run_id(
        protocol=split.protocol,
        split_id=split.split_id,
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

    return {
        "run_id": run_id,
        "protocol": split.protocol,
        "split_id": split.split_id,
        "split_npz": split.split_npz,
        "dataset_pickle": dataset_pickle,
        "n_components": str(n_components),
        "downsample_factor": str(downsample_factor),
        "electrode_regions": electrode_regions,
        "apply_ts2vec": "0",
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
        "tcn_layers": "4",
        "tcn_kernel_size": "3",
        "transformer_heads": "4",
        "transformer_layers": "2",
        "transformer_ff_mult": "4",
        "specaug_on": str(specaug_on),
        "white_noise_sd": str(white_noise_sd),
        "constant_offset_sd": str(constant_offset_sd),
        "gaussian_smooth_width": str(gaussian_smooth_width),
        "frame_ms": str(frame_ms),
        "n_batch": str(n_batch),
        "train_seed": str(train_seed),
        "selection_rank": "",
        "note": "baseline",
    }


def _clone_row(base: Dict[str, str], **updates: str) -> Dict[str, str]:
    out = dict(base)
    out.update({k: str(v) for k, v in updates.items()})
    return out


def _rebuild_run_id_and_dataset(
    row: Dict[str, str],
    *,
    tag: str,
    noise_tag: str,
    extra_tags: Sequence[str] = (),
) -> Dict[str, str]:
    protocol = row["protocol"]
    split_id = row["split_id"]
    n_components = int(row["n_components"])
    ds = int(row["downsample_factor"])
    regions = row["electrode_regions"]
    apply_ts2vec = row.get("apply_ts2vec", "0").strip() in {"1", "true", "True"}
    ts2vec_output_dims = int(row.get("ts2vec_output_dims", "320") or "320")

    dataset_pickle = _dataset_pickle(
        protocol=protocol,
        split_id=split_id,
        n_components=n_components,
        downsample_factor=ds,
        electrode_regions=regions,
        tag=tag,
        apply_ts2vec=apply_ts2vec,
        ts2vec_output_dims=ts2vec_output_dims,
    )

    input_proj_dim = row.get("input_proj_dim", "").strip()
    proj_dim = int(input_proj_dim) if input_proj_dim else None

    run_id = _run_id(
        protocol=protocol,
        split_id=split_id,
        n_components=n_components,
        downsample_factor=ds,
        electrode_regions=regions,
        model_family=row["model_family"],
        n_units=int(row["n_units"]),
        n_layers=int(row["n_layers"]),
        stride_len=int(row["stride_len"]),
        kernel_len=int(row["kernel_len"]),
        input_proj_dim=proj_dim,
        specaug_on=int(row["specaug_on"]),
        noise_tag=noise_tag,
        train_seed=int(row["train_seed"]),
        tag=tag,
        extra_tags=extra_tags,
    )

    out = dict(row)
    out["run_id"] = run_id
    out["dataset_pickle"] = dataset_pickle
    return out


def _matrix_baseline(splits: List[Split], *, tag: str) -> List[Dict[str, str]]:
    rows = [_base_row(split=s, tag=tag) for s in splits]
    for r in rows:
        r["note"] = "baseline"
    return rows


def _matrix_axis_a(splits: List[Split], *, tag: str) -> List[Dict[str, str]]:
    levels = [
        "anterior",
        "middle",
        "posterior",
        "left",
        "right",
        "anterior middle",
        "middle posterior",
    ]
    rows: List[Dict[str, str]] = []
    for s in splits:
        base = _base_row(split=s, tag=tag)
        for lvl in levels:
            r = _clone_row(base, electrode_regions=lvl, note=f"axisA:{lvl}")
            rows.append(_rebuild_run_id_and_dataset(r, tag=tag, noise_tag="noiseDefault"))
    return rows


def _matrix_axis_c(splits: List[Split], *, tag: str) -> List[Dict[str, str]]:
    combos: List[Tuple[int, Optional[int]]] = []
    for n_components in (-1, 16, 32, 64):
        for proj in (None, 64):
            if n_components == -1 and proj == 64:
                # Baseline combo.
                continue
            combos.append((n_components, proj))

    rows: List[Dict[str, str]] = []
    for s in splits:
        base = _base_row(split=s, tag=tag)
        for n_components, proj in combos:
            note = f"axisC:{_repr_tag(n_components)}:{_proj_tag(proj)}"
            input_proj_dim = "" if proj is None else str(proj)
            r = _clone_row(
                base,
                n_components=str(n_components),
                input_proj_dim=input_proj_dim,
                note=note,
            )
            rows.append(_rebuild_run_id_and_dataset(r, tag=tag, noise_tag="noiseDefault"))
    return rows


def _matrix_axis_d(splits: List[Split], *, tag: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for s in splits:
        base = _base_row(split=s, tag=tag)
        for ds in (2, 4):
            r = _clone_row(base, downsample_factor=str(ds), note=f"axisD:ds{ds}")
            rows.append(_rebuild_run_id_and_dataset(r, tag=tag, noise_tag="noiseDefault"))
    return rows


def _matrix_axis_e(splits: List[Split], *, tag: str) -> List[Dict[str, str]]:
    combos: List[Tuple[int, int, int, int]] = []
    for n_units in (512, 1024):
        for n_layers in (3, 5):
            for stride_len in (2, 4):
                for kernel_len in (16, 32):
                    if (n_units, n_layers, stride_len, kernel_len) == (512, 5, 4, 32):
                        # Baseline combo.
                        continue
                    combos.append((n_units, n_layers, stride_len, kernel_len))

    rows: List[Dict[str, str]] = []
    for s in splits:
        base = _base_row(split=s, tag=tag)
        for n_units, n_layers, stride_len, kernel_len in combos:
            note = f"axisE:u{n_units}_l{n_layers}_s{stride_len}_k{kernel_len}"
            r = _clone_row(
                base,
                n_units=str(n_units),
                n_layers=str(n_layers),
                stride_len=str(stride_len),
                kernel_len=str(kernel_len),
                note=note,
            )
            rows.append(_rebuild_run_id_and_dataset(r, tag=tag, noise_tag="noiseDefault"))
    return rows


def _matrix_axis_f_spec(splits: List[Split], *, tag: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for s in splits:
        base = _base_row(split=s, tag=tag)
        r = _clone_row(base, specaug_on="0", note="axisF:spec0")
        rows.append(_rebuild_run_id_and_dataset(r, tag=tag, noise_tag="noiseDefault"))
    return rows


def _matrix_axis_f_noise(splits: List[Split], *, tag: str) -> List[Dict[str, str]]:
    variants = [
        ("wn0", {"white_noise_sd": "0.0"}),
        ("wn1p6", {"white_noise_sd": "1.6"}),
        ("co0", {"constant_offset_sd": "0.0"}),
        ("co0p4", {"constant_offset_sd": "0.4"}),
        ("gs0", {"gaussian_smooth_width": "0.0"}),
        ("gs4", {"gaussian_smooth_width": "4.0"}),
    ]

    rows: List[Dict[str, str]] = []
    for s in splits:
        base = _base_row(split=s, tag=tag)
        for tag_noise, upd in variants:
            note = f"axisF:{tag_noise}"
            r = _clone_row(base, note=note, **upd)
            rows.append(_rebuild_run_id_and_dataset(r, tag=tag, noise_tag=f"noise{tag_noise}"))
    return rows


def _matrix_family_compare(splits: List[Split], *, tag: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for s in splits:
        base = _base_row(split=s, tag=tag)

        # causal_tcn
        r_tcn = _clone_row(
            base,
            model_family="causal_tcn",
            n_units="512",
            n_layers="6",
            tcn_layers="6",
            tcn_kernel_size="3",
            note="family:causal_tcn",
        )
        rows.append(_rebuild_run_id_and_dataset(r_tcn, tag=tag, noise_tag="noiseDefault"))

        # mini_transformer
        r_tx = _clone_row(
            base,
            model_family="mini_transformer",
            n_units="384",
            n_layers="3",
            transformer_heads="4",
            transformer_layers="3",
            transformer_ff_mult="4",
            note="family:mini_transformer",
        )
        rows.append(_rebuild_run_id_and_dataset(r_tx, tag=tag, noise_tag="noiseDefault"))

    return rows


def _matrix_ts2vec_minimal(splits: List[Split], *, tag: str) -> List[Dict[str, str]]:
    keep_ids = {
        "P1:seed0",
        "P2:subj1_seed0",
        "P2:subj2_seed0",
        "P3:subj1to2_seed0",
        "P3:subj2to1_seed0",
    }

    rows: List[Dict[str, str]] = []
    for s in splits:
        if f"{s.protocol}:{s.split_id}" not in keep_ids:
            continue
        base = _base_row(split=s, tag=tag)
        r = _clone_row(
            base,
            apply_ts2vec="1",
            ts2vec_output_dims="320",
            ts2vec_epochs="100",
            ts2vec_hidden_dims="64",
            ts2vec_depth="10",
            ts2vec_batch_size="16",
            note="ts2vec:minimal",
        )
        # Run-id should encode ts2vec.
        rows.append(
            _rebuild_run_id_and_dataset(
                r,
                tag=tag,
                noise_tag="noiseDefault",
                extra_tags=("ts2vec320",),
            )
        )

    if len(rows) != 5:
        raise SystemExit(f"Bug: expected 5 ts2vec rows but got {len(rows)}")
    return rows


def _assert_counts(mats: Dict[str, List[Dict[str, str]]]) -> None:
    expected = {
        "splits": 20,
        "gc_baseline": 20,
        "axisA_regions": 140,
        "axisC_repr_proj": 140,
        "axisD_downsample": 40,
        "axisE_capacity": 300,
        "axisF_specaug": 20,
        "axisF_noise": 120,
        "family_compare": 40,
        "ts2vec_minimal": 5,
    }
    for k, exp in expected.items():
        got = len(mats.get(k, []))
        if got != exp:
            raise SystemExit(f"Count mismatch for {k}: expected {exp}, got {got}")

    # Basic uniqueness checks.
    all_run_ids: List[str] = []
    for k, rows in mats.items():
        if k == "splits":
            continue
        all_run_ids.extend([r["run_id"] for r in rows])
    if len(all_run_ids) != len(set(all_run_ids)):
        dupes = [rid for rid in sorted(set(all_run_ids)) if all_run_ids.count(rid) > 1][:10]
        raise SystemExit(f"Duplicate run_id detected (examples): {dupes}")


def main() -> None:
    p = argparse.ArgumentParser(description="Generate gap-closure matrices (gc20260216-style).")
    p.add_argument("--out_dir", type=Path, default=Path(f"sweeps/{TAG_DEFAULT}/matrices"))
    p.add_argument("--tag", type=str, default=TAG_DEFAULT)
    args = p.parse_args()

    splits = _splits()

    split_rows = [
        {"protocol": s.protocol, "split_id": s.split_id, "split_npz": s.split_npz}
        for s in splits
    ]
    _write_csv(args.out_dir / "splits.csv", split_rows, ["protocol", "split_id", "split_npz"])

    mats: Dict[str, List[Dict[str, str]]] = {
        "splits": split_rows,
        "gc_baseline": _matrix_baseline(splits, tag=args.tag),
        "axisA_regions": _matrix_axis_a(splits, tag=args.tag),
        "axisC_repr_proj": _matrix_axis_c(splits, tag=args.tag),
        "axisD_downsample": _matrix_axis_d(splits, tag=args.tag),
        "axisE_capacity": _matrix_axis_e(splits, tag=args.tag),
        "axisF_specaug": _matrix_axis_f_spec(splits, tag=args.tag),
        "axisF_noise": _matrix_axis_f_noise(splits, tag=args.tag),
        "family_compare": _matrix_family_compare(splits, tag=args.tag),
        "ts2vec_minimal": _matrix_ts2vec_minimal(splits, tag=args.tag),
    }

    _assert_counts(mats)

    # Write matrices.
    _write_csv(args.out_dir / "gc_baseline.csv", mats["gc_baseline"], STAGE_MATRIX_COLUMNS)
    _write_csv(args.out_dir / "axisA_regions.csv", mats["axisA_regions"], STAGE_MATRIX_COLUMNS)
    _write_csv(args.out_dir / "axisC_repr_proj.csv", mats["axisC_repr_proj"], STAGE_MATRIX_COLUMNS)
    _write_csv(args.out_dir / "axisD_downsample.csv", mats["axisD_downsample"], STAGE_MATRIX_COLUMNS)
    _write_csv(args.out_dir / "axisE_capacity.csv", mats["axisE_capacity"], STAGE_MATRIX_COLUMNS)
    _write_csv(args.out_dir / "axisF_specaug.csv", mats["axisF_specaug"], STAGE_MATRIX_COLUMNS)
    _write_csv(args.out_dir / "axisF_noise.csv", mats["axisF_noise"], STAGE_MATRIX_COLUMNS)
    _write_csv(args.out_dir / "family_compare.csv", mats["family_compare"], STAGE_MATRIX_COLUMNS)
    _write_csv(args.out_dir / "ts2vec_minimal.csv", mats["ts2vec_minimal"], STAGE_MATRIX_COLUMNS)

    print(f"Wrote matrices to {args.out_dir}")
    for name in [
        "gc_baseline",
        "axisA_regions",
        "axisC_repr_proj",
        "axisD_downsample",
        "axisE_capacity",
        "axisF_specaug",
        "axisF_noise",
        "family_compare",
        "ts2vec_minimal",
    ]:
        print(f"- {name}: {len(mats[name])} rows")


if __name__ == "__main__":
    main()
