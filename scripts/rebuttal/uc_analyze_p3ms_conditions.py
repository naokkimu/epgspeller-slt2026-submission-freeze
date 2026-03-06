#!/usr/bin/env python3
"""Analyze P3MS condition dependence (uc20260226).

Goal
- Quantify when P3MS (multi-source) improves over the mean of its two corresponding
  single-source P3 directions, using evidence-only metrics CSVs.
- Attach simple dataset similarity measures computed from raw NPZ (channel-mean contact patterns).

Inputs (default, repo-root relative)
- sweeps/msx20260224/results/msx_all_metrics.csv (frozen; 652 rows; missing=0)
- sweeps/uc20260226/results/uc_to4_metrics.csv   (24 rows; missing=0; P3/P3MS to subj4)
- raw/silentspeller_dataset/{p1_2328_old,thad_2328_old,john_2328,su_1167_old}_dataset.npz
- results/dataset_audit_silentspeller_2026-02-24/exclusions/john_2328_exclude_indices.json

Outputs (default)
- results/uc20260226/p3ms_conditions.csv
- docs/report/figures/uc20260226/p3ms_delta_vs_similarity.png
- docs/report/p3ms_conditions_2026-02-26.md
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (expected scripts/ and src/)")


def _read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fieldnames))
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _require_columns(rows: Sequence[Mapping[str, str]], keys: Sequence[str], *, context: str) -> None:
    if not rows:
        raise SystemExit(f"{context}: empty rows")
    missing = [k for k in keys if k not in rows[0]]
    if missing:
        raise SystemExit(f"{context}: missing columns: {missing}")


def _to_float(v: str, *, context: str) -> float:
    s = (v or "").strip()
    if s == "":
        raise ValueError(f"Missing float for {context}")
    return float(s)


def _variant_id(row: Mapping[str, str]) -> str:
    mf = (row.get("model_family") or "").strip()
    if not mf:
        raise ValueError("Missing model_family")
    if mf in {"spatial2d_uni_gru", "spatial2d_patchpool_uni_gru"}:
        aug = (row.get("enable_spatial_aug") or "").strip() or "0"
        subset_method = (row.get("subset_method") or "").strip()
        base = f"{mf}_aug{aug}"
        return f"{base}_{subset_method}" if subset_method else base
    subset_method = (row.get("subset_method") or "").strip()
    return f"{mf}_{subset_method}" if subset_method else mf


def _parse_split_id(protocol: str, split_id: str) -> Tuple[str, int, Tuple[int, ...], int]:
    """Return (group_id, seed, src_tuple, tgt)."""
    s = (split_id or "").strip()

    def _must_int(x: str) -> int:
        return int(x)

    if protocol == "P3":
        # subj{src}to{tgt}_seed{seed}
        if not s.startswith("subj") or "to" not in s or "_seed" not in s:
            raise ValueError(f"Unexpected split_id for P3: {s}")
        core, seed_part = s.split("_seed", 1)
        seed = _must_int(seed_part)
        src_tgt = core.replace("subj", "")
        src_s, tgt_s = src_tgt.split("to", 1)
        src, tgt = _must_int(src_s), _must_int(tgt_s)
        return f"subj{src}to{tgt}", seed, (src,), tgt

    if protocol == "P3MS":
        # subj{srca}{srcb}to{tgt}_seed{seed}
        if not s.startswith("subj") or "to" not in s or "_seed" not in s:
            raise ValueError(f"Unexpected split_id for P3MS: {s}")
        core, seed_part = s.split("_seed", 1)
        seed = _must_int(seed_part)
        srcs_tgt = core.replace("subj", "")
        srcs_s, tgt_s = srcs_tgt.split("to", 1)
        if len(srcs_s) != 2:
            raise ValueError(f"Unexpected multi-source prefix in split_id: {s}")
        src_a, src_b = _must_int(srcs_s[0]), _must_int(srcs_s[1])
        tgt = _must_int(tgt_s)
        return f"subj{src_a}{src_b}to{tgt}", seed, (src_a, src_b), tgt

    raise ValueError(f"Unsupported protocol for split_id parsing: {protocol}")


def _pearson(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=np.float64).reshape(-1)
    b = np.asarray(b, dtype=np.float64).reshape(-1)
    if a.shape != b.shape:
        raise ValueError(f"shape mismatch: {a.shape} vs {b.shape}")
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        return float("nan")
    sa = float(np.std(a))
    sb = float(np.std(b))
    if sa == 0.0 or sb == 0.0:
        return float("nan")
    c = float(np.corrcoef(a, b)[0, 1])
    return c


def _parse_exclude_indices(path: Path) -> List[int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        xs = payload
    elif isinstance(payload, dict):
        xs = payload.get("exclude_indices")
        if xs is None:
            raise ValueError(f"exclude json missing key 'exclude_indices': {path}")
    else:
        raise ValueError(f"exclude json must be list/dict: {path}")
    out: List[int] = []
    for v in xs:
        if isinstance(v, bool):
            raise ValueError(f"exclude index must be int, got bool: {v}")
        out.append(int(v))
    out = sorted(set(out))
    if any(i < 0 for i in out):
        raise ValueError(f"exclude indices must be >=0: {out[:10]}")
    return out


def _channel_means_from_npz(npz_path: Path, *, exclude_indices: Optional[Sequence[int]] = None) -> Tuple[np.ndarray, float, int]:
    if not npz_path.exists():
        raise SystemExit(f"raw npz not found: {npz_path}")
    exclude = set(int(i) for i in (exclude_indices or []))

    npz = np.load(npz_path, allow_pickle=True)
    if "data" not in npz:
        raise SystemExit(f"NPZ missing key 'data': {npz_path} keys={list(npz.keys())}")
    data = npz["data"]
    if len(data) == 0:
        raise SystemExit(f"Empty data array: {npz_path}")

    sum_ch = np.zeros((124,), dtype=np.float64)
    total_frames = 0
    kept = 0
    for i in range(len(data)):
        if i in exclude:
            continue
        x = data[i]
        if x.shape[1] != 124:
            raise SystemExit(f"Unexpected channel dim in {npz_path} idx={i}: shape={x.shape}")
        if not np.isfinite(x).all():
            raise SystemExit(f"Non-finite in {npz_path} idx={i}")
        total_frames += int(x.shape[0])
        sum_ch += np.sum(x, axis=0, dtype=np.float64)
        kept += 1

    if total_frames <= 0 or kept <= 0:
        raise SystemExit(f"No kept frames after exclusions for {npz_path}")

    ch_mean = sum_ch / float(total_frames)
    overall_mean_contact = float(np.mean(ch_mean))
    return ch_mean, overall_mean_contact, int(total_frames)


def _save_scatter(path: Path, *, xs: Sequence[float], ys: Sequence[float], labels: Sequence[str], title: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7, 4.5))
    plt.axhline(0.0, color="k", linewidth=1, alpha=0.4)
    plt.scatter(xs, ys, s=60)
    for x, y, lab in zip(xs, ys, labels):
        plt.text(float(x), float(y), str(lab), fontsize=9, ha="left", va="bottom")
    plt.title(title)
    plt.xlabel("mean(src-target channel-mean corr)")
    plt.ylabel("delta_cer = cer(P3MS) - mean(cer(P3 srcA->tgt), cer(P3 srcB->tgt))")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def main() -> None:
    ap = argparse.ArgumentParser(description="Analyze P3MS condition dependence (uc20260226).")
    ap.add_argument(
        "--msx_metrics_csv",
        type=Path,
        default=Path("sweeps/msx20260224/results/msx_all_metrics.csv"),
        help="Frozen msx aggregated metrics CSV (652 rows, missing=0).",
    )
    ap.add_argument(
        "--uc_to4_metrics_csv",
        type=Path,
        default=Path("sweeps/uc20260226/results/uc_to4_metrics.csv"),
        help="Aggregated metrics for P3/P3MS to participant4 (24 rows, missing=0).",
    )
    ap.add_argument("--subj1_npz", type=Path, default=Path("raw/silentspeller_dataset/p1_2328_old_dataset.npz"))
    ap.add_argument("--subj2_npz", type=Path, default=Path("raw/silentspeller_dataset/thad_2328_old_dataset.npz"))
    ap.add_argument("--subj3_npz", type=Path, default=Path("raw/silentspeller_dataset/john_2328_dataset.npz"))
    ap.add_argument("--subj4_npz", type=Path, default=Path("raw/silentspeller_dataset/su_1167_old_dataset.npz"))
    ap.add_argument(
        "--exclude_indices_json_subj3",
        type=Path,
        default=Path("results/dataset_audit_silentspeller_2026-02-24/exclusions/john_2328_exclude_indices.json"),
    )
    ap.add_argument("--out_csv", type=Path, default=Path("results/uc20260226/p3ms_conditions.csv"))
    ap.add_argument(
        "--out_fig",
        type=Path,
        default=Path("docs/report/figures/uc20260226/p3ms_delta_vs_similarity.png"),
    )
    ap.add_argument("--out_md", type=Path, default=Path("docs/report/p3ms_conditions_2026-02-26.md"))
    args = ap.parse_args()

    repo_root = _find_repo_root()
    msx_metrics = args.msx_metrics_csv if args.msx_metrics_csv.is_absolute() else (repo_root / args.msx_metrics_csv)
    uc_to4_metrics = args.uc_to4_metrics_csv if args.uc_to4_metrics_csv.is_absolute() else (repo_root / args.uc_to4_metrics_csv)

    subj_npz = {
        1: args.subj1_npz if args.subj1_npz.is_absolute() else (repo_root / args.subj1_npz),
        2: args.subj2_npz if args.subj2_npz.is_absolute() else (repo_root / args.subj2_npz),
        3: args.subj3_npz if args.subj3_npz.is_absolute() else (repo_root / args.subj3_npz),
        4: args.subj4_npz if args.subj4_npz.is_absolute() else (repo_root / args.subj4_npz),
    }
    exclude_subj3_path = (
        args.exclude_indices_json_subj3
        if args.exclude_indices_json_subj3.is_absolute()
        else (repo_root / args.exclude_indices_json_subj3)
    )

    out_csv = args.out_csv if args.out_csv.is_absolute() else (repo_root / args.out_csv)
    out_fig = args.out_fig if args.out_fig.is_absolute() else (repo_root / args.out_fig)
    out_md = args.out_md if args.out_md.is_absolute() else (repo_root / args.out_md)

    for p in [msx_metrics, uc_to4_metrics]:
        if not p.exists():
            raise SystemExit(f"missing required input: {p}")

    msx_rows = _read_csv_rows(msx_metrics)
    if len(msx_rows) != 652:
        raise SystemExit(f"msx completeness gate: expected 652 rows but got {len(msx_rows)}")
    uc_rows = _read_csv_rows(uc_to4_metrics)
    if len(uc_rows) != 24:
        raise SystemExit(f"uc_to4 completeness gate: expected 24 rows but got {len(uc_rows)}")

    _require_columns(msx_rows, ["protocol", "split_id", "model_family", "greedy_test_cer", "note"], context="msx_metrics_csv")
    _require_columns(uc_rows, ["protocol", "split_id", "model_family", "greedy_test_cer", "note"], context="uc_to4_metrics_csv")

    # Extract CER per seed for:
    # - P3 uni_gru (baseline note) to build the corresponding single-source baselines
    # - P3MS uni_gru (msx:p3ms note) for 1..3 targets
    p3: Dict[Tuple[int, int], Dict[int, float]] = {}
    p3ms: Dict[Tuple[int, int, int], Dict[int, float]] = {}

    def _insert(mapping: Dict, key, seed: int, val: float, *, context: str) -> None:
        mapping.setdefault(key, {})
        if seed in mapping[key]:
            raise SystemExit(f"Duplicate seed entry: {context} key={key} seed={seed}")
        mapping[key][seed] = float(val)

    # msx: single-source P3 (baseline vector)
    for r in msx_rows:
        if (r.get("note") or "").strip() != "baseline:multi_subj":
            continue
        if (r.get("protocol") or "").strip() != "P3":
            continue
        if _variant_id(r) != "uni_gru":
            continue
        gid, seed, srcs, tgt = _parse_split_id("P3", (r.get("split_id") or "").strip())
        src = srcs[0]
        cer = _to_float(r.get("greedy_test_cer", ""), context=f"msx/P3/{gid}/seed{seed}/cer")
        _insert(p3, (src, tgt), seed, cer, context="msx_p3")

    # msx: P3MS (vector only)
    for r in msx_rows:
        if (r.get("note") or "").strip() != "msx:p3ms":
            continue
        if (r.get("protocol") or "").strip() != "P3MS":
            continue
        if _variant_id(r) != "uni_gru":
            continue
        gid, seed, srcs, tgt = _parse_split_id("P3MS", (r.get("split_id") or "").strip())
        src_a, src_b = int(srcs[0]), int(srcs[1])
        cer = _to_float(r.get("greedy_test_cer", ""), context=f"msx/P3MS/{gid}/seed{seed}/cer")
        _insert(p3ms, (src_a, src_b, tgt), seed, cer, context="msx_p3ms")

    # uc: to4 runs include both P3 and P3MS, vector only
    for r in uc_rows:
        prot = (r.get("protocol") or "").strip()
        if prot not in {"P3", "P3MS"}:
            raise SystemExit(f"Unexpected protocol in uc_to4_metrics: {prot}")
        if _variant_id(r) != "uni_gru":
            raise SystemExit(f"Unexpected non-vector row in uc_to4_metrics: model_family={r.get('model_family')}")
        if prot == "P3":
            gid, seed, srcs, tgt = _parse_split_id("P3", (r.get("split_id") or "").strip())
            src = srcs[0]
            cer = _to_float(r.get("greedy_test_cer", ""), context=f"uc/P3/{gid}/seed{seed}/cer")
            _insert(p3, (src, tgt), seed, cer, context="uc_p3")
        else:
            gid, seed, srcs, tgt = _parse_split_id("P3MS", (r.get("split_id") or "").strip())
            src_a, src_b = int(srcs[0]), int(srcs[1])
            cer = _to_float(r.get("greedy_test_cer", ""), context=f"uc/P3MS/{gid}/seed{seed}/cer")
            _insert(p3ms, (src_a, src_b, tgt), seed, cer, context="uc_p3ms")

    # Basic presence gates
    if not p3ms:
        raise SystemExit("No P3MS entries found (msx:p3ms + uc_to4).")
    for (src_a, src_b, tgt), per_seed in sorted(p3ms.items()):
        seeds = sorted(per_seed.keys())
        if seeds != [0, 1, 2, 3]:
            raise SystemExit(f"P3MS seed gate failed for {(src_a, src_b, tgt)}: got seeds={seeds}")
        for src in (src_a, src_b):
            if (src, tgt) not in p3:
                raise SystemExit(f"Missing single-source P3 direction for src={src} tgt={tgt}")
            s2 = sorted(p3[(src, tgt)].keys())
            if s2 != [0, 1, 2, 3]:
                raise SystemExit(f"P3 seed gate failed for {(src, tgt)}: got seeds={s2}")

    # Load channel-mean/contact stats from raw NPZ
    exclude_subj3: List[int] = []
    if exclude_subj3_path.exists():
        exclude_subj3 = _parse_exclude_indices(exclude_subj3_path)

    subj_stats: Dict[int, Dict[str, object]] = {}
    for sid in [1, 2, 3, 4]:
        ex = exclude_subj3 if sid == 3 else None
        ch_mean, overall, total_frames = _channel_means_from_npz(subj_npz[sid], exclude_indices=ex)
        subj_stats[sid] = {
            "ch_mean": ch_mean,
            "overall_mean_contact": float(overall),
            "total_frames": int(total_frames),
            "path": str(subj_npz[sid]),
        }

    # Build rows
    out_rows: List[Dict[str, object]] = []
    xs: List[float] = []
    ys: List[float] = []
    labs: List[str] = []

    def _seed_mean(vals: Sequence[float]) -> float:
        return float(mean(list(vals))) if vals else float("nan")

    for (src_a, src_b, tgt) in sorted(p3ms.keys(), key=lambda t: (t[2], t[0], t[1])):
        p3ms_seed = [p3ms[(src_a, src_b, tgt)][s] for s in [0, 1, 2, 3]]
        cer_p3ms = _seed_mean(p3ms_seed)
        # For each seed, average the two single-source directions, then average across seeds.
        p3_single_seed_means = []
        for s in [0, 1, 2, 3]:
            p3_single_seed_means.append(0.5 * (p3[(src_a, tgt)][s] + p3[(src_b, tgt)][s]))
        cer_p3_single_mean = _seed_mean(p3_single_seed_means)
        delta_cer = float(cer_p3ms - cer_p3_single_mean)

        ch_a = subj_stats[src_a]["ch_mean"]
        ch_b = subj_stats[src_b]["ch_mean"]
        ch_t = subj_stats[tgt]["ch_mean"]
        corr_a_t = _pearson(ch_a, ch_t)
        corr_b_t = _pearson(ch_b, ch_t)
        corr_src_src = _pearson(ch_a, ch_b)
        corr_src_tgt_mean = float(np.nanmean([corr_a_t, corr_b_t]))

        c_a = float(subj_stats[src_a]["overall_mean_contact"])
        c_b = float(subj_stats[src_b]["overall_mean_contact"])
        c_t = float(subj_stats[tgt]["overall_mean_contact"])
        ratio_a_t = float("nan") if c_t == 0.0 else float(c_a / c_t)
        ratio_b_t = float("nan") if c_t == 0.0 else float(c_b / c_t)
        ratio_mean = float(np.nanmean([ratio_a_t, ratio_b_t]))

        group = f"subj{src_a}{src_b}to{tgt}"
        out_rows.append(
            {
                "group": group,
                "src_a": src_a,
                "src_b": src_b,
                "tgt": tgt,
                "cer_p3ms_mean": cer_p3ms,
                "cer_p3_single_mean": cer_p3_single_mean,
                "delta_cer": delta_cer,
                "corr_srcA_tgt": corr_a_t,
                "corr_srcB_tgt": corr_b_t,
                "corr_src_tgt_mean": corr_src_tgt_mean,
                "corr_src_src": corr_src_src,
                "overall_mean_contact_srcA": c_a,
                "overall_mean_contact_srcB": c_b,
                "overall_mean_contact_tgt": c_t,
                "contact_ratio_srcA_over_tgt": ratio_a_t,
                "contact_ratio_srcB_over_tgt": ratio_b_t,
                "contact_ratio_mean": ratio_mean,
            }
        )

        if math.isfinite(corr_src_tgt_mean) and math.isfinite(delta_cer):
            xs.append(float(corr_src_tgt_mean))
            ys.append(float(delta_cer))
            labs.append(group)

    _write_csv(
        out_csv,
        out_rows,
        fieldnames=[
            "group",
            "src_a",
            "src_b",
            "tgt",
            "cer_p3ms_mean",
            "cer_p3_single_mean",
            "delta_cer",
            "corr_srcA_tgt",
            "corr_srcB_tgt",
            "corr_src_tgt_mean",
            "corr_src_src",
            "overall_mean_contact_srcA",
            "overall_mean_contact_srcB",
            "overall_mean_contact_tgt",
            "contact_ratio_srcA_over_tgt",
            "contact_ratio_srcB_over_tgt",
            "contact_ratio_mean",
        ],
    )

    if xs and ys:
        _save_scatter(
            out_fig,
            xs=xs,
            ys=ys,
            labels=labs,
            title="P3MS delta(CER) vs src-target similarity (channel-mean corr)",
        )

    # Report (evidence-only, numbers derived from out_rows)
    deltas = [float(r["delta_cer"]) for r in out_rows if isinstance(r.get("delta_cer"), (int, float)) and math.isfinite(float(r["delta_cer"]))]
    corr_means = [
        float(r["corr_src_tgt_mean"])
        for r in out_rows
        if isinstance(r.get("corr_src_tgt_mean"), (int, float)) and math.isfinite(float(r["corr_src_tgt_mean"]))
    ]
    md = []
    md.append("# P3MS condition analysis (uc20260226)\n")
    md.append("## Inputs\n")
    md.append(f"- msx_metrics_csv: `{msx_metrics}`\n")
    md.append(f"- uc_to4_metrics_csv: `{uc_to4_metrics}`\n")
    md.append("- raw_npz:\n")
    for sid in [1, 2, 3, 4]:
        md.append(f"  - subj{sid}: `{subj_stats[sid]['path']}`\n")
    md.append(f"- subj3_exclusions: `{exclude_subj3_path}`\n")
    md.append("\n## Outputs\n")
    md.append(f"- `results/uc20260226/p3ms_conditions.csv`\n")
    md.append(f"- `docs/report/figures/uc20260226/p3ms_delta_vs_similarity.png`\n")
    md.append("\n## Summary (observations only)\n")
    if deltas:
        md.append(f"- delta_cer range (P3MS - mean(P3 singles)): [{min(deltas):.6f}, {max(deltas):.6f}]\n")
    if corr_means:
        md.append(f"- mean(src-target corr) range: [{min(corr_means):.6f}, {max(corr_means):.6f}]\n")
    md.append("- See the CSV for per-group values and the scatter plot for the delta-vs-similarity view.\n")
    _write_text(out_md, "".join(md))

    print(f"[OK] wrote: {out_csv}")
    print(f"[OK] wrote: {out_fig}")
    print(f"[OK] wrote: {out_md}")


if __name__ == "__main__":
    main()

