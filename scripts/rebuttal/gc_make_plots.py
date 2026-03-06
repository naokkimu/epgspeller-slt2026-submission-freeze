#!/usr/bin/env python3
"""Generate figures for gap-closure results.

Input
- One or more tidy results CSVs from gc_collect_metrics.py

Output
- PNG figures under docs/report/figures/<tag>/

This script only plots what it can find in the provided results.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Optional, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _read_results(paths: Sequence[Path]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for p in paths:
        with p.open("r", newline="") as f:
            rows.extend(list(csv.DictReader(f)))
    return rows


def _f(v: str) -> Optional[float]:
    s = (v or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None


def _i(v: str) -> Optional[int]:
    s = (v or "").strip()
    if not s:
        return None
    try:
        return int(float(s))
    except Exception:
        return None


def _mean_std(xs: List[float]) -> Tuple[float, float]:
    if not xs:
        return float("nan"), float("nan")
    if len(xs) == 1:
        return float(xs[0]), float("nan")
    return float(statistics.mean(xs)), float(statistics.stdev(xs))


def _filter(rows: List[Dict[str, str]], pred) -> List[Dict[str, str]]:
    return [r for r in rows if pred(r)]


def _by_protocol(rows: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    out: Dict[str, List[Dict[str, str]]] = {"P1": [], "P2": [], "P3": []}
    for r in rows:
        proto = (r.get("protocol") or "").strip()
        if proto in out:
            out[proto].append(r)
    return out


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def _extract_axis_token(note: str, prefix: str) -> Optional[str]:
    if not note:
        return None
    if not note.startswith(prefix):
        return None
    return note[len(prefix) :]


def plot_axis_a(rows: List[Dict[str, str]], out_dir: Path) -> None:
    axis_rows = _filter(rows, lambda r: (r.get("note") or "").startswith("axisA:"))
    base_rows = _filter(rows, lambda r: (r.get("note") or "") == "baseline")
    if not axis_rows or not base_rows:
        return

    # region -> list cer per protocol
    byp = _by_protocol(axis_rows)
    base_by_proto = _by_protocol(base_rows)

    region_levels = [
        "anterior",
        "middle",
        "posterior",
        "left",
        "right",
        "anterior middle",
        "middle posterior",
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 4), sharey=True)
    for ax, proto in zip(axes, ["P1", "P2", "P3"]):
        proto_rows = byp.get(proto, [])
        if not proto_rows:
            ax.set_title(f"{proto} (no data)")
            continue

        means: List[float] = []
        stds: List[float] = []
        for reg in region_levels:
            cer_xs = [_f(r.get("greedy_test_cer", "")) for r in proto_rows if r.get("electrode_regions", "") == reg]
            cer_vals = [x for x in cer_xs if x is not None]
            m, s = _mean_std(cer_vals)
            means.append(m)
            stds.append(s)

        x = np.arange(len(region_levels))
        ax.bar(x, means, yerr=stds, capsize=3)
        ax.set_xticks(x)
        ax.set_xticklabels([r.replace(" ", "\n") for r in region_levels], rotation=0)
        ax.set_title(proto)
        ax.set_xlabel("electrode_regions")
        if proto == "P1":
            ax.set_ylabel("CER (mean±std over splits)")

        # baseline reference
        base_vals = [_f(r.get("greedy_test_cer", "")) for r in base_by_proto.get(proto, [])]
        base_vals = [x for x in base_vals if x is not None]
        if base_vals:
            bmean = float(statistics.mean(base_vals))
            ax.axhline(bmean, color="black", linewidth=1, linestyle="--")
            ax.text(0.01, bmean, "baseline(all)", va="bottom", ha="left", fontsize=8)

    fig.suptitle("Axis A: electrode region ablation")
    _save(fig, out_dir / "axisA_regions.png")


def plot_axis_c(rows: List[Dict[str, str]], out_dir: Path) -> None:
    axis_rows = _filter(rows, lambda r: (r.get("note") or "").startswith("axisC:"))
    base_rows = _filter(rows, lambda r: (r.get("note") or "") == "baseline")
    if not axis_rows or not base_rows:
        return

    # Build combined rows for axis C (include baseline raw+proj64)
    combined = list(axis_rows)
    for r in base_rows:
        n_components = _i(r.get("n_components", ""))
        proj = r.get("input_proj_dim", "").strip() or ""
        if n_components == -1 and proj == "64":
            # Treat as axis C baseline cell
            r2 = dict(r)
            r2["note"] = "axisC:raw:proj64"
            combined.append(r2)

    # n_components levels and proj levels
    n_levels = [-1, 16, 32, 64]
    p_levels = ["", "64"]  # projNone, proj64

    fig, axes = plt.subplots(1, 3, figsize=(16, 4), sharey=True)
    for ax, proto in zip(axes, ["P1", "P2", "P3"]):
        proto_rows = [r for r in combined if (r.get("protocol") or "") == proto]
        if not proto_rows:
            ax.set_title(f"{proto} (no data)")
            continue

        mat = np.full((len(n_levels), len(p_levels)), np.nan, dtype=float)
        for i_n, n in enumerate(n_levels):
            for i_p, p in enumerate(p_levels):
                vals = []
                for r in proto_rows:
                    if _i(r.get("n_components", "")) != n:
                        continue
                    proj = r.get("input_proj_dim", "").strip() or ""
                    if proj != p:
                        continue
                    v = _f(r.get("greedy_test_cer", ""))
                    if v is not None:
                        vals.append(v)
                if vals:
                    mat[i_n, i_p] = float(statistics.mean(vals))

        im = ax.imshow(mat, aspect="auto", cmap="viridis")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["projNone", "proj64"])
        ax.set_yticks(list(range(len(n_levels))))
        ax.set_yticklabels(["raw" if n == -1 else f"pca{n}" for n in n_levels])
        ax.set_title(proto)
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                if not math.isnan(mat[i, j]):
                    ax.text(j, i, f"{mat[i,j]:.3f}", ha="center", va="center", color="white", fontsize=8)

    fig.suptitle("Axis C: representation (PCA) × input projection")
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.8)
    cbar.set_label("CER (mean over splits)")
    _save(fig, out_dir / "axisC_repr_proj_heatmap.png")


def plot_axis_d(rows: List[Dict[str, str]], out_dir: Path) -> None:
    axis_rows = _filter(rows, lambda r: (r.get("note") or "").startswith("axisD:"))
    base_rows = _filter(rows, lambda r: (r.get("note") or "") == "baseline")
    if not axis_rows or not base_rows:
        return

    combined = list(axis_rows) + list(base_rows)

    fig, axes = plt.subplots(1, 3, figsize=(16, 4), sharey=True)
    for ax, proto in zip(axes, ["P1", "P2", "P3"]):
        proto_rows = [r for r in combined if (r.get("protocol") or "") == proto]
        if not proto_rows:
            ax.set_title(f"{proto} (no data)")
            continue

        xs = [1, 2, 4]
        means = []
        stds = []
        for ds in xs:
            vals = [_f(r.get("greedy_test_cer", "")) for r in proto_rows if _i(r.get("downsample_factor", "")) == ds]
            vals = [v for v in vals if v is not None]
            m, s = _mean_std(vals)
            means.append(m)
            stds.append(s)

        ax.errorbar(xs, means, yerr=stds, marker="o", linewidth=2, capsize=3)
        ax.set_xticks(xs)
        ax.set_xlabel("downsample_factor")
        ax.set_title(proto)
        if proto == "P1":
            ax.set_ylabel("CER (mean±std over splits)")

    fig.suptitle("Axis D: temporal downsampling")
    _save(fig, out_dir / "axisD_downsample_curve.png")


def _pareto_front(points: List[Tuple[float, float, str]]) -> List[str]:
    """Return ids on Pareto front for (x=param_count, y=CER) minimize both."""
    # Sort by x ascending, then scan for y improvements.
    pts = sorted(points, key=lambda t: (t[0], t[1]))
    front: List[str] = []
    best_y = float("inf")
    for x, y, pid in pts:
        if y < best_y:
            front.append(pid)
            best_y = y
    return front


def plot_axis_e(rows: List[Dict[str, str]], out_dir: Path) -> None:
    axis_rows = _filter(rows, lambda r: (r.get("note") or "").startswith("axisE:"))
    base_rows = _filter(rows, lambda r: (r.get("note") or "") == "baseline")
    if not axis_rows or not base_rows:
        return

    combined = list(axis_rows) + list(base_rows)

    # Aggregate by capacity config per protocol.
    def cfg_key(r: Dict[str, str]) -> Tuple[int, int, int, int]:
        return (
            int(float(r.get("n_units", "0") or 0)),
            int(float(r.get("n_layers", "0") or 0)),
            int(float(r.get("stride_len", "0") or 0)),
            int(float(r.get("kernel_len", "0") or 0)),
        )

    fig, axes = plt.subplots(1, 3, figsize=(16, 4), sharey=True)
    for ax, proto in zip(axes, ["P1", "P2", "P3"]):
        proto_rows = [r for r in combined if (r.get("protocol") or "") == proto]
        if not proto_rows:
            ax.set_title(f"{proto} (no data)")
            continue

        by_cfg: DefaultDict[Tuple[int, int, int, int], List[Dict[str, str]]] = defaultdict(list)
        for r in proto_rows:
            by_cfg[cfg_key(r)].append(r)

        pts: List[Tuple[float, float, str]] = []
        for cfg, rs in by_cfg.items():
            cer_vals = [_f(x.get("greedy_test_cer", "")) for x in rs]
            cer_vals = [v for v in cer_vals if v is not None]
            if not cer_vals:
                continue
            cer_m = float(statistics.mean(cer_vals))
            pc_vals = [_f(x.get("param_count", "")) for x in rs]
            pc_vals = [v for v in pc_vals if v is not None]
            if not pc_vals:
                continue
            pc = float(statistics.mean(pc_vals))
            pid = f"u{cfg[0]}_l{cfg[1]}_s{cfg[2]}_k{cfg[3]}"
            pts.append((pc, cer_m, pid))

        if not pts:
            ax.set_title(f"{proto} (no points)")
            continue

        front_ids = set(_pareto_front(pts))
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        colors = ["tab:red" if p[2] in front_ids else "tab:blue" for p in pts]
        ax.scatter(xs, ys, c=colors, alpha=0.8)
        ax.set_xlabel("param_count")
        ax.set_title(proto)
        if proto == "P1":
            ax.set_ylabel("CER (mean over splits)")

    fig.suptitle("Axis E: capacity trade-off (Pareto highlighted)")
    _save(fig, out_dir / "axisE_capacity_scatter.png")


def plot_axis_f(rows: List[Dict[str, str]], out_dir: Path) -> None:
    spec_rows = _filter(rows, lambda r: (r.get("note") or "") == "axisF:spec0")
    noise_rows = _filter(rows, lambda r: (r.get("note") or "").startswith("axisF:"))
    base_rows = _filter(rows, lambda r: (r.get("note") or "") == "baseline")
    if not base_rows:
        return

    # SpecAug delta plot
    if spec_rows:
        fig, ax = plt.subplots(1, 1, figsize=(7, 4))
        protos = ["P1", "P2", "P3"]
        deltas = []
        stds = []
        for proto in protos:
            b = [_f(r.get("greedy_test_cer", "")) for r in base_rows if (r.get("protocol") or "") == proto]
            s0 = [_f(r.get("greedy_test_cer", "")) for r in spec_rows if (r.get("protocol") or "") == proto]
            b = [v for v in b if v is not None]
            s0 = [v for v in s0 if v is not None]
            if not b or not s0:
                deltas.append(float("nan"))
                stds.append(float("nan"))
                continue
            # Pairwise delta across splits by split_id
            b_by = {r.get("split_id"): _f(r.get("greedy_test_cer", "")) for r in base_rows if (r.get("protocol") or "") == proto}
            s_by = {r.get("split_id"): _f(r.get("greedy_test_cer", "")) for r in spec_rows if (r.get("protocol") or "") == proto}
            pair = []
            for sid, bv in b_by.items():
                sv = s_by.get(sid)
                if bv is None or sv is None:
                    continue
                pair.append(sv - bv)
            m, s = _mean_std(pair)
            deltas.append(m)
            stds.append(s)

        x = np.arange(len(protos))
        ax.bar(x, deltas, yerr=stds, capsize=3)
        ax.axhline(0.0, color="black", linewidth=1)
        ax.set_xticks(x)
        ax.set_xticklabels(protos)
        ax.set_ylabel("ΔCER (spec0 - spec1)")
        ax.set_title("Axis F-1: SpecAug on/off")
        _save(fig, out_dir / "axisF_specaug_delta.png")

    # Noise sensitivity curves
    if noise_rows:
        # Identify variants by note tag (axisF:wn0 etc) excluding spec0.
        variants = [
            ("white_noise_sd", [("baseline", 0.8), ("wn0", 0.0), ("wn1p6", 1.6)]),
            ("constant_offset_sd", [("baseline", 0.2), ("co0", 0.0), ("co0p4", 0.4)]),
            ("gaussian_smooth_width", [("baseline", 2.0), ("gs0", 0.0), ("gs4", 4.0)]),
        ]

        fig, axes = plt.subplots(3, 3, figsize=(16, 10), sharey=False)
        for row_idx, (param_name, pts_def) in enumerate(variants):
            for col_idx, proto in enumerate(["P1", "P2", "P3"]):
                ax = axes[row_idx, col_idx]
                xs: List[float] = []
                ys: List[float] = []
                es: List[float] = []
                for tag_name, val in pts_def:
                    if tag_name == "baseline":
                        rs = [r for r in base_rows if (r.get("protocol") or "") == proto]
                    else:
                        rs = [
                            r
                            for r in noise_rows
                            if (r.get("protocol") or "") == proto
                            and (r.get("note") or "") == f"axisF:{tag_name}"
                        ]
                    cer_vals = [_f(r.get("greedy_test_cer", "")) for r in rs]
                    cer_vals = [v for v in cer_vals if v is not None]
                    m, s = _mean_std(cer_vals)
                    xs.append(val)
                    ys.append(m)
                    es.append(s)

                ax.errorbar(xs, ys, yerr=es, marker="o", linewidth=2, capsize=3)
                ax.set_title(f"{proto}")
                ax.set_xlabel(param_name)
                ax.set_ylabel("CER")

        fig.suptitle("Axis F-2: noise sensitivity (one-factor-at-a-time)")
        _save(fig, out_dir / "axisF_noise_sensitivity.png")


def plot_family_compare(rows: List[Dict[str, str]], out_dir: Path) -> None:
    fam_rows = _filter(rows, lambda r: (r.get("note") or "").startswith("family:"))
    base_rows = _filter(rows, lambda r: (r.get("note") or "") == "baseline")
    if not fam_rows or not base_rows:
        return

    fig, axes = plt.subplots(1, 3, figsize=(16, 4), sharey=True)
    for ax, proto in zip(axes, ["P1", "P2", "P3"]):
        proto_base = [r for r in base_rows if (r.get("protocol") or "") == proto]
        proto_fam = [r for r in fam_rows if (r.get("protocol") or "") == proto]
        if not proto_base or not proto_fam:
            ax.set_title(f"{proto} (no data)")
            continue

        families = [
            ("uni_gru", proto_base),
            ("causal_tcn", [r for r in proto_fam if (r.get("model_family") or "") == "causal_tcn"]),
            ("mini_transformer", [r for r in proto_fam if (r.get("model_family") or "") == "mini_transformer"]),
        ]

        labels = []
        means = []
        stds = []
        for name, rs in families:
            vals = [_f(r.get("greedy_test_cer", "")) for r in rs]
            vals = [v for v in vals if v is not None]
            m, s = _mean_std(vals)
            labels.append(name)
            means.append(m)
            stds.append(s)

        x = np.arange(len(labels))
        ax.bar(x, means, yerr=stds, capsize=3)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=20)
        ax.set_title(proto)
        if proto == "P1":
            ax.set_ylabel("CER (mean±std over splits)")

    fig.suptitle("Family comparison (baseline vs TCN vs transformer)")
    _save(fig, out_dir / "family_compare.png")


def _read_occlusion_csv(path: Path) -> List[Dict[str, str]]:
    lines = path.read_text().splitlines()
    # Skip comment header and blank lines until a CSV header.
    start = 0
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        if line.startswith("#"):
            continue
        start = i
        break
    if start >= len(lines):
        return []
    reader = csv.DictReader(lines[start:])
    return list(reader)


def plot_axis_b_occlusion(rows: List[Dict[str, str]], out_dir: Path) -> None:
    # Use baseline runs as the set to average.
    base_rows = _filter(rows, lambda r: (r.get("note") or "") == "baseline")
    if not base_rows:
        return

    by_proto = _by_protocol(base_rows)

    # Channel importance
    fig1, axes1 = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    any_channel = False
    for ax, proto in zip(axes1, ["P1", "P2", "P3"]):
        arrays: List[np.ndarray] = []
        for r in by_proto.get(proto, []):
            run_dir = Path(r.get("run_dir") or "")
            p = run_dir / "occlusion_channel_importance.csv"
            if not p.exists():
                continue
            recs = _read_occlusion_csv(p)
            if not recs:
                continue
            # Expect channel column
            chan = [int(x["channel"]) for x in recs]
            delta = [float(x["delta_cer"]) for x in recs]
            order = np.argsort(chan)
            arr = np.array([delta[i] for i in order], dtype=float)
            arrays.append(arr)

        if not arrays:
            ax.set_title(f"{proto} (missing occlusion files)")
            continue

        any_channel = True
        mat = np.stack(arrays, axis=0)
        mean = mat.mean(axis=0)
        std = mat.std(axis=0, ddof=1) if mat.shape[0] > 1 else np.full_like(mean, np.nan)
        x = np.arange(mean.shape[0])
        ax.plot(x, mean, linewidth=1.5)
        ax.fill_between(x, mean - std, mean + std, alpha=0.2)
        ax.set_ylabel("ΔCER")
        ax.set_title(proto)

    if any_channel:
        axes1[-1].set_xlabel("channel index")
        fig1.suptitle("Axis B: channel occlusion importance (mean±std over splits)")
        _save(fig1, out_dir / "axisB_occlusion_channel_indexed.png")
    else:
        plt.close(fig1)

    # Region importance
    fig2, axes2 = plt.subplots(1, 3, figsize=(16, 4), sharey=True)
    any_region = False
    region_levels = [
        "anterior",
        "middle",
        "posterior",
        "left",
        "right",
        "anterior middle",
        "middle posterior",
        "all",
    ]

    for ax, proto in zip(axes2, ["P1", "P2", "P3"]):
        mats: List[Dict[str, float]] = []
        for r in by_proto.get(proto, []):
            run_dir = Path(r.get("run_dir") or "")
            p = run_dir / "occlusion_region_importance.csv"
            if not p.exists():
                continue
            recs = _read_occlusion_csv(p)
            if not recs:
                continue
            mats.append({x["region"]: float(x["delta_cer"]) for x in recs if x.get("region")})

        if not mats:
            ax.set_title(f"{proto} (missing occlusion files)")
            continue

        any_region = True
        means = []
        stds = []
        for reg in region_levels:
            xs = [m.get(reg) for m in mats if reg in m]
            xs = [float(x) for x in xs if x is not None]
            m, s = _mean_std(xs)
            means.append(m)
            stds.append(s)

        x = np.arange(len(region_levels))
        ax.bar(x, means, yerr=stds, capsize=3)
        ax.set_xticks(x)
        ax.set_xticklabels([r.replace(" ", "\n") for r in region_levels])
        ax.set_title(proto)
        if proto == "P1":
            ax.set_ylabel("ΔCER (mean±std)")

    if any_region:
        fig2.suptitle("Axis B: region occlusion importance")
        _save(fig2, out_dir / "axisB_occlusion_region_bar.png")
    else:
        plt.close(fig2)


def write_ts2vec_table(rows: List[Dict[str, str]], out_dir: Path) -> None:
    ts2 = _filter(rows, lambda r: (r.get("note") or "") == "ts2vec:minimal")
    base = _filter(rows, lambda r: (r.get("note") or "") == "baseline")
    if not ts2 or not base:
        return

    base_by = {(r.get("protocol"), r.get("split_id")): r for r in base}
    out_path = out_dir / "ts2vec_minimal_comparison.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "protocol",
        "split_id",
        "baseline_run_id",
        "ts2vec_run_id",
        "baseline_cer",
        "ts2vec_cer",
        "delta_cer",
    ]

    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in ts2:
            key = (r.get("protocol"), r.get("split_id"))
            b = base_by.get(key)
            if not b:
                continue
            bcer = _f(b.get("greedy_test_cer", ""))
            tcer = _f(r.get("greedy_test_cer", ""))
            if bcer is None or tcer is None:
                continue
            w.writerow(
                {
                    "protocol": key[0] or "",
                    "split_id": key[1] or "",
                    "baseline_run_id": b.get("run_id_used") or b.get("run_id") or "",
                    "ts2vec_run_id": r.get("run_id_used") or r.get("run_id") or "",
                    "baseline_cer": f"{bcer:.6f}",
                    "ts2vec_cer": f"{tcer:.6f}",
                    "delta_cer": f"{(tcer - bcer):.6f}",
                }
            )


def main() -> None:
    ap = argparse.ArgumentParser(description="Make gap-closure plots from collected results.")
    ap.add_argument("--results_csv", type=Path, nargs="+", required=True)
    ap.add_argument("--out_dir", type=Path, default=Path("docs/report/figures/gc20260216"))
    args = ap.parse_args()

    rows = _read_results(args.results_csv)
    if not rows:
        raise SystemExit("No rows loaded from results CSV(s).")

    _ensure_dir(args.out_dir)

    plot_axis_a(rows, args.out_dir)
    plot_axis_c(rows, args.out_dir)
    plot_axis_d(rows, args.out_dir)
    plot_axis_e(rows, args.out_dir)
    plot_axis_f(rows, args.out_dir)
    plot_family_compare(rows, args.out_dir)
    plot_axis_b_occlusion(rows, args.out_dir)
    write_ts2vec_table(rows, args.out_dir)

    print(f"Wrote figures under {args.out_dir}")


if __name__ == "__main__":
    main()
