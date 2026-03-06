#!/usr/bin/env python3
"""Make figures for EPG design sweeps (P1, K-curve).

Inputs
- Tidy results CSV produced by gc_collect_metrics.py (must include baseline + ed matrices)
- P1 subset definitions CSV (for layout plots)

Outputs (default)
- docs/report/figures/ed20260217/*.png
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


K_LIST = [16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120]


def _read_rows(paths: Sequence[Path]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for p in paths:
        with p.open("r", newline="") as f:
            rows.extend(list(csv.DictReader(f)))
    return rows


def _read_subset_defs(path: Path) -> Dict[str, List[int]]:
    with path.open("r", newline="") as f:
        rows = list(csv.DictReader(f))
    out: Dict[str, List[int]] = {}
    for r in rows:
        sid = (r.get("subset_id") or "").strip()
        idxs = (r.get("indices_space_separated") or "").strip()
        if not sid or not idxs:
            continue
        out[sid] = [int(x) for x in idxs.split()]
    return out


def _f(v: str) -> Optional[float]:
    s = (v or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None


def _mean_std(xs: List[float]) -> Tuple[float, float, int]:
    xs = [float(x) for x in xs if x is not None and not math.isnan(float(x))]
    if not xs:
        return float("nan"), float("nan"), 0
    if len(xs) == 1:
        return xs[0], float("nan"), 1
    return float(statistics.mean(xs)), float(statistics.stdev(xs)), len(xs)


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".pdf":
        fig.savefig(path, bbox_inches="tight")
    else:
        fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def _filter(rows: List[Dict[str, str]], pred) -> List[Dict[str, str]]:
    return [r for r in rows if pred(r)]


def _baseline_p1(rows: List[Dict[str, str]]) -> Tuple[float, float]:
    base = _filter(rows, lambda r: (r.get("protocol") or "") == "P1" and (r.get("note") or "") == "baseline")
    cers = [_f(r.get("greedy_test_cer", "")) for r in base]
    cers = [x for x in cers if x is not None]
    if not cers:
        raise SystemExit("No P1 baseline rows found (need baseline matrix included in results).")
    return float(statistics.mean(cers)), float(statistics.stdev(cers)) if len(cers) > 1 else float("nan")


def plot_cer_vs_k(rows: List[Dict[str, str]], out_dir: Path) -> None:
    base_mean, _ = _baseline_p1(rows)
    ed = _filter(rows, lambda r: (r.get("protocol") or "") == "P1" and (r.get("note") or "").startswith("ed:"))

    def collect(method: str, k: int) -> List[float]:
        xs = []
        for r in ed:
            if (r.get("note") or "") != "ed:kcurve":
                continue
            if (r.get("subset_method") or "") != method:
                continue
            if int(float(r.get("subset_K") or 0)) != k:
                continue
            v = _f(r.get("greedy_test_cer", ""))
            if v is not None:
                xs.append(v)
        return xs

    def collect_random_seed_means(k: int) -> List[float]:
        by_seed: Dict[str, List[float]] = {}
        for r in ed:
            if (r.get("note") or "") != "ed:kcurve":
                continue
            if (r.get("subset_method") or "") != "random":
                continue
            if int(float(r.get("subset_K") or 0)) != k:
                continue
            seed = (r.get("split_id") or "").strip()
            v = _f(r.get("greedy_test_cer", ""))
            if not seed or v is None:
                continue
            by_seed.setdefault(seed, []).append(v)
        seed_means: List[float] = []
        for seed, vals in sorted(by_seed.items()):
            if vals:
                seed_means.append(float(statistics.mean(vals)))
        return seed_means

    top_means, top_stds = [], []
    fps_means, fps_stds = [], []
    rnd_means, rnd_stds = [], []
    for k in K_LIST:
        m, s, _ = _mean_std(collect("topk", k))
        top_means.append(m)
        top_stds.append(s)
        m, s, _ = _mean_std(collect("fps2k", k))
        fps_means.append(m)
        fps_stds.append(s)
        # randomK: average replicates within each seed, then mean±std over seeds
        m, s, _ = _mean_std(collect_random_seed_means(k))
        rnd_means.append(m)
        rnd_stds.append(s)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(K_LIST, top_means, yerr=top_stds, marker="o", label="topK (importance)")
    ax.errorbar(K_LIST, fps_means, yerr=fps_stds, marker="o", label="fps2k (diverse)")
    ax.plot(K_LIST, rnd_means, marker="o", linestyle="--", label="random (mean)")
    ax.fill_between(
        K_LIST,
        [m - s if (not math.isnan(m) and not math.isnan(s)) else m for m, s in zip(rnd_means, rnd_stds)],
        [m + s if (not math.isnan(m) and not math.isnan(s)) else m for m, s in zip(rnd_means, rnd_stds)],
        alpha=0.2,
        linewidth=0,
    )
    ax.axhline(base_mean, color="black", linestyle="--", linewidth=1, label="baseline K=124")
    ax.set_xlabel("K (channels)")
    ax.set_ylabel("CER (mean±std over seeds/replicates)")
    ax.set_title("P1: CER vs K")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=8)
    _save(fig, out_dir / "cer_vs_k.png")


def plot_cer_rtf_vs_k(rows: List[Dict[str, str]], out_dir: Path) -> None:
    base_mean, _ = _baseline_p1(rows)
    ed = _filter(rows, lambda r: (r.get("protocol") or "") == "P1" and (r.get("note") or "").startswith("ed:"))

    def collect(method: str, k: int, metric: str) -> List[float]:
        xs: List[float] = []
        for r in ed:
            if (r.get("note") or "") != "ed:kcurve":
                continue
            if (r.get("subset_method") or "") != method:
                continue
            if int(float(r.get("subset_K") or 0)) != k:
                continue
            v = _f(r.get(metric, ""))
            if v is not None:
                xs.append(v)
        return xs

    def collect_random_seed_means(k: int, metric: str) -> List[float]:
        by_seed: Dict[str, List[float]] = {}
        for r in ed:
            if (r.get("note") or "") != "ed:kcurve":
                continue
            if (r.get("subset_method") or "") != "random":
                continue
            if int(float(r.get("subset_K") or 0)) != k:
                continue
            seed = (r.get("split_id") or "").strip()
            v = _f(r.get(metric, ""))
            if seed and v is not None:
                by_seed.setdefault(seed, []).append(v)
        return [float(statistics.mean(vs)) for _, vs in sorted(by_seed.items()) if vs]

    def mean_std_for(method: str, k: int, metric: str) -> Tuple[float, float]:
        if method == "random":
            xs = collect_random_seed_means(k, metric)
        else:
            xs = collect(method, k, metric)
        m, s, _ = _mean_std(xs)
        return m, s

    cer = {m: [mean_std_for(m, k, "greedy_test_cer") for k in K_LIST] for m in ("topk", "fps2k", "random")}
    rtf = {m: [mean_std_for(m, k, "stream_rtf") for k in K_LIST] for m in ("topk", "fps2k", "random")}

    style = {
        "font.size": 8,
        "axes.titlesize": 8,
        "axes.labelsize": 8,
        "legend.fontsize": 7,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "axes.linewidth": 0.6,
    }
    with plt.rc_context(style):
        fig, axes = plt.subplots(
            2, 1, figsize=(3.35, 3.6), sharex=True, constrained_layout=True
        )
        ax_cer, ax_rtf = axes

        colors = {"topk": "#1f77b4", "fps2k": "#ff7f0e", "random": "#2ca02c"}
        labels = {"topk": "topk", "fps2k": "fps2k", "random": "random"}

        for method in ("topk", "fps2k", "random"):
            cer_means = [m for m, _ in cer[method]]
            cer_stds = [s if not math.isnan(s) else 0.0 for _, s in cer[method]]
            ax_cer.plot(
                K_LIST,
                cer_means,
                marker="o",
                linewidth=1.2,
                markersize=3,
                color=colors[method],
                label=labels[method],
                linestyle="--" if method == "random" else "-",
            )
            ax_cer.fill_between(
                K_LIST,
                [m - s for m, s in zip(cer_means, cer_stds)],
                [m + s for m, s in zip(cer_means, cer_stds)],
                color=colors[method],
                alpha=0.12,
                linewidth=0,
            )
        ax_cer.axhline(base_mean, color="black", linewidth=0.8, linestyle="--", label="full budget")
        ax_cer.set_ylabel("CER")
        ax_cer.grid(True, axis="y", alpha=0.3)
        ax_cer.legend(frameon=False, ncol=2, loc="upper right")

        for method in ("topk", "fps2k", "random"):
            rtf_means = [m for m, _ in rtf[method]]
            rtf_stds = [s if not math.isnan(s) else 0.0 for _, s in rtf[method]]
            ax_rtf.plot(
                K_LIST,
                rtf_means,
                marker="o",
                linewidth=1.2,
                markersize=3,
                color=colors[method],
                label=labels[method],
                linestyle="--" if method == "random" else "-",
            )
            ax_rtf.fill_between(
                K_LIST,
                [m - s for m, s in zip(rtf_means, rtf_stds)],
                [m + s for m, s in zip(rtf_means, rtf_stds)],
                color=colors[method],
                alpha=0.12,
                linewidth=0,
            )
        ax_rtf.set_ylabel("streaming RTF")
        ax_rtf.set_xlabel("Electrode budget (K)")
        ax_rtf.grid(True, axis="y", alpha=0.3)
        ax_rtf.set_xticks(K_LIST[::2])
        ax_rtf.set_xticklabels([str(k) for k in K_LIST[::2]])

    _save(fig, out_dir / "cer_rtf_vs_k.png")
    _save(fig, out_dir / "cer_rtf_vs_k.pdf")


def plot_delta_curves(rows: List[Dict[str, str]], out_dir: Path) -> None:
    base_mean, _ = _baseline_p1(rows)
    ed = _filter(rows, lambda r: (r.get("protocol") or "") == "P1" and (r.get("note") or "") == "ed:kcurve")

    def mean_for(method: str, k: int) -> float:
        if method != "random":
            xs = [
                _f(r.get("greedy_test_cer", ""))
                for r in ed
                if (r.get("subset_method") or "") == method and int(float(r.get("subset_K") or 0)) == k
            ]
            xs = [x for x in xs if x is not None]
            return float(statistics.mean(xs)) if xs else float("nan")

        # random: mean-of-replicates within each seed, then mean over seeds
        by_seed: Dict[str, List[float]] = {}
        for r in ed:
            if (r.get("subset_method") or "") != "random":
                continue
            if int(float(r.get("subset_K") or 0)) != k:
                continue
            seed = (r.get("split_id") or "").strip()
            v = _f(r.get("greedy_test_cer", ""))
            if not seed or v is None:
                continue
            by_seed.setdefault(seed, []).append(v)
        seed_means = [float(statistics.mean(vs)) for _, vs in sorted(by_seed.items()) if vs]
        return float(statistics.mean(seed_means)) if seed_means else float("nan")

    top = [mean_for("topk", k) for k in K_LIST]
    fps = [mean_for("fps2k", k) for k in K_LIST]
    rnd = [mean_for("random", k) for k in K_LIST]

    # topK - random
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(K_LIST, [t - r for t, r in zip(top, rnd)], marker="o")
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_xlabel("K")
    ax.set_ylabel("ΔCER (topK - random)")
    ax.set_title("P1: topK advantage over random")
    ax.grid(True, alpha=0.3)
    _save(fig, out_dir / "delta_topk_minus_random.png")

    # fps - top
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(K_LIST, [f - t for f, t in zip(fps, top)], marker="o")
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_xlabel("K")
    ax.set_ylabel("ΔCER (fps2k - topK)")
    ax.set_title("P1: diversity vs pure-importance")
    ax.grid(True, alpha=0.3)
    _save(fig, out_dir / "delta_fps2k_minus_topk.png")

    # Δ vs baseline
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(K_LIST, [t - base_mean for t in top], marker="o", label="topK")
    ax.plot(K_LIST, [f - base_mean for f in fps], marker="o", label="fps2k")
    ax.plot(K_LIST, [r - base_mean for r in rnd], marker="o", linestyle="--", label="random")
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_xlabel("K")
    ax.set_ylabel("ΔCER (vs baseline K=124)")
    ax.set_title("P1: loss relative to 124ch baseline")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    _save(fig, out_dir / "delta_vs_baseline.png")


def plot_rtf_vs_k(rows: List[Dict[str, str]], out_dir: Path) -> None:
    ed = _filter(rows, lambda r: (r.get("protocol") or "") == "P1" and (r.get("note") or "") == "ed:kcurve")

    def mean_rtf(method: str, k: int) -> float:
        def _rtf(rec: Dict[str, str]) -> Optional[float]:
            return _f(rec.get("stream_rtf", ""))

        if method != "random":
            xs = [_rtf(r) for r in ed if (r.get("subset_method") or "") == method and int(float(r.get("subset_K") or 0)) == k]
            xs = [x for x in xs if x is not None]
            return float(statistics.mean(xs)) if xs else float("nan")

        by_seed: Dict[str, List[float]] = {}
        for r in ed:
            if (r.get("subset_method") or "") != "random":
                continue
            if int(float(r.get("subset_K") or 0)) != k:
                continue
            seed = (r.get("split_id") or "").strip()
            v = _rtf(r)
            if not seed or v is None:
                continue
            by_seed.setdefault(seed, []).append(v)
        seed_means = [float(statistics.mean(vs)) for _, vs in sorted(by_seed.items()) if vs]
        return float(statistics.mean(seed_means)) if seed_means else float("nan")

    top = [mean_rtf("topk", k) for k in K_LIST]
    fps = [mean_rtf("fps2k", k) for k in K_LIST]
    rnd = [mean_rtf("random", k) for k in K_LIST]

    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(K_LIST, top, marker="o", label="topK")
    ax.plot(K_LIST, fps, marker="o", label="fps2k")
    ax.plot(K_LIST, rnd, marker="o", linestyle="--", label="random")
    ax.set_xlabel("K")
    ax.set_ylabel("stream_rtf (mean)")
    ax.set_title("P1: streaming RTF vs K (from eval_greedy_test.json)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    _save(fig, out_dir / "rtf_vs_k.png")


def plot_frontend_compare(rows: List[Dict[str, str]], out_dir: Path) -> None:
    """Compare vector vs spatial2d vs rowcol front-ends for selected K.

    Expects H11/H13 matrices to be included in results collection.
    """

    def _sel(
        *,
        note: str,
        subset_method: Optional[str],
        subset_k: Optional[int],
    ) -> List[Dict[str, str]]:
        out: List[Dict[str, str]] = []
        for r in rows:
            if (r.get("protocol") or "") != "P1":
                continue
            if (r.get("note") or "") != note:
                continue
            if subset_method is not None and (r.get("subset_method") or "") != subset_method:
                continue
            if subset_k is not None:
                try:
                    if int(float(r.get("subset_K") or 0)) != int(subset_k):
                        continue
                except Exception:
                    continue
            out.append(r)
        return out

    def _metric_mean_std(sel: List[Dict[str, str]], key: str) -> Tuple[float, float, int]:
        xs = [_f(r.get(key, "")) for r in sel]
        xs2 = [x for x in xs if x is not None]
        return _mean_std(xs2)

    # Only proceed if spatial results are present.
    have_spatial = any((r.get("note") or "").startswith("ed:spatial2d_") for r in rows if (r.get("protocol") or "") == "P1")
    have_rowcol = any((r.get("note") or "").startswith("ed:rowcol_") for r in rows if (r.get("protocol") or "") == "P1")
    if not have_spatial and not have_rowcol:
        print("[skip] No H11/H13 rows found for frontend comparison.")
        return

    configs: List[Tuple[str, Optional[str], Optional[int]]] = []
    for k in (32, 64, 96):
        for method in ("topk", "fps2k"):
            configs.append((f"K{k} {method}", method, int(k)))
    configs.append(("K124 all", None, None))  # baseline rows don't carry subset fields

    frontends = ["vector", "spatial2d", "rowcol"]
    colors = {"vector": "#1f77b4", "spatial2d": "#ff7f0e", "rowcol": "#2ca02c"}

    def _summary(frontend: str, label: str, method: Optional[str], k: Optional[int], metric: str) -> Tuple[float, float, int]:
        if label == "K124 all":
            if frontend == "vector":
                sel = _sel(note="baseline", subset_method=None, subset_k=None)
            elif frontend == "spatial2d":
                sel = _sel(note="ed:spatial2d_compare_baseline124", subset_method=None, subset_k=None)
            elif frontend == "rowcol":
                sel = _sel(note="ed:rowcol_compare_baseline124", subset_method=None, subset_k=None)
            else:
                sel = []
            return _metric_mean_std(sel, metric)

        if method is None or k is None:
            return float("nan"), float("nan"), 0

        if frontend == "vector":
            sel = _sel(note="ed:kcurve", subset_method=method, subset_k=k)
        elif frontend == "spatial2d":
            sel = _sel(note="ed:spatial2d_compare", subset_method=method, subset_k=k)
        elif frontend == "rowcol":
            sel = _sel(note="ed:rowcol_compare", subset_method=method, subset_k=k)
        else:
            sel = []
        return _metric_mean_std(sel, metric)

    # Build arrays for plotting.
    x = np.arange(len(configs), dtype=float)
    width = 0.22

    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax_cer, ax_rtf = axes

    for i, fe in enumerate(frontends):
        xs = x + (i - (len(frontends) - 1) / 2.0) * width

        cer_means, cer_stds = [], []
        rtf_means, rtf_stds = [], []
        for label, method, k in configs:
            m, s, n = _summary(fe, label, method, k, "greedy_test_cer")
            cer_means.append(m)
            cer_stds.append(s if (n >= 2 and not math.isnan(s)) else 0.0)
            m2, s2, n2 = _summary(fe, label, method, k, "stream_rtf")
            rtf_means.append(m2)
            rtf_stds.append(s2 if (n2 >= 2 and not math.isnan(s2)) else 0.0)

        # Mask out missing bars (n==0).
        cer_valid = [not math.isnan(v) for v in cer_means]
        rtf_valid = [not math.isnan(v) for v in rtf_means]

        ax_cer.bar(
            [xs[j] for j in range(len(xs)) if cer_valid[j]],
            [cer_means[j] for j in range(len(xs)) if cer_valid[j]],
            width=width,
            color=colors.get(fe, None),
            label=fe,
            yerr=[cer_stds[j] for j in range(len(xs)) if cer_valid[j]],
            capsize=2,
            alpha=0.9,
        )
        ax_rtf.bar(
            [xs[j] for j in range(len(xs)) if rtf_valid[j]],
            [rtf_means[j] for j in range(len(xs)) if rtf_valid[j]],
            width=width,
            color=colors.get(fe, None),
            label=fe,
            yerr=[rtf_stds[j] for j in range(len(xs)) if rtf_valid[j]],
            capsize=2,
            alpha=0.9,
        )

    ax_cer.set_ylabel("greedy CER (mean±std over seeds)")
    ax_cer.set_title("P1: front-end comparison (vector vs 2D conv vs row/col compression)")
    ax_cer.grid(True, axis="y", alpha=0.25)
    ax_cer.legend(fontsize=8, ncol=3, loc="upper left")

    ax_rtf.set_ylabel("stream_rtf (mean±std over seeds)")
    ax_rtf.grid(True, axis="y", alpha=0.25)
    ax_rtf.set_xticks(x)
    ax_rtf.set_xticklabels([c[0] for c in configs], rotation=30, ha="right", fontsize=8)

    _save(fig, out_dir / "compare_frontends_k32_64_96.png")


def plot_dropout_spatial2d_aug_vs_noaug(dropout_csv: Path, out_dir: Path) -> None:
    if not dropout_csv.exists():
        print(f"[skip] dropout_csv not found: {dropout_csv}")
        return

    with dropout_csv.open("r", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print(f"[skip] empty dropout_csv: {dropout_csv}")
        return

    def group_of(run_id: str) -> Optional[str]:
        rid = run_id or ""
        if "spatial2d_uni_gru" not in rid:
            return None
        if "spaug1" in rid:
            return "spatial_aug=1"
        if "spaug0" in rid:
            return "spatial_aug=0"
        return None

    by_group_q: Dict[str, Dict[float, List[float]]] = {}
    for r in rows:
        rid = (r.get("run_id") or "").strip()
        g = group_of(rid)
        if g is None:
            continue
        q = _f(r.get("drop_rate", ""))
        d = _f(r.get("delta_cer_mean", ""))
        if q is None or d is None or math.isnan(q) or math.isnan(d):
            continue
        by_group_q.setdefault(g, {}).setdefault(float(q), []).append(float(d))

    if not by_group_q:
        print("[skip] No spatial2d rows in dropout_csv.")
        return

    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    for g, by_q in sorted(by_group_q.items()):
        qs = sorted(by_q.keys())
        means, stds = [], []
        for q in qs:
            m, s, _ = _mean_std(by_q[q])
            means.append(m)
            stds.append(s if not math.isnan(s) else 0.0)
        ax.errorbar(qs, means, yerr=stds, marker="o", label=g, capsize=2)

    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_xlabel("drop_rate q (fixed electrode failure rate)")
    ax.set_ylabel("ΔCER (masked - clean)")
    ax.set_title("Spatial2D: dropout robustness (train aug on/off)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    _save(fig, out_dir / "dropout_spatial2d_aug_vs_noaug.png")


def _load_sp_map(csv_path: Path):
    import importlib.util
    import sys

    here = Path(__file__).resolve()
    repo_root = None
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            repo_root = p
            break
    if repo_root is None:
        raise RuntimeError("Failed to locate repo root.")

    mod_path = repo_root / "scripts" / "rebuttal" / "ed_smartpalate_map.py"
    spec = importlib.util.spec_from_file_location("ed_smartpalate_map", str(mod_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to import {mod_path}")
    mod = importlib.util.module_from_spec(spec)
    # dataclasses relies on the module being present in sys.modules during exec.
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod.load_map(csv_path)


def plot_layouts(subset_defs: Dict[str, List[int]], out_dir: Path, smartpalate_csv: Path) -> None:
    sp = _load_sp_map(smartpalate_csv)
    coords = sp.channel_to_rc

    def plot_one(subset_id: str, title: str, out_name: str) -> None:
        idxs = subset_defs.get(subset_id)
        if not idxs:
            return
        mapped = [ch for ch in idxs if ch in coords]
        unmapped = [ch for ch in idxs if ch not in coords]

        all_xy = np.array([(c, r) for ch, (r, c) in coords.items()], dtype=float)
        sel_xy = np.array([(coords[ch][1], coords[ch][0]) for ch in mapped], dtype=float) if mapped else np.zeros((0, 2))

        fig, ax = plt.subplots(figsize=(4.2, 4.2))
        if len(all_xy) > 0:
            ax.scatter(all_xy[:, 0], all_xy[:, 1], s=10, c="#bbbbbb", linewidths=0)
        if len(sel_xy) > 0:
            ax.scatter(sel_xy[:, 0], sel_xy[:, 1], s=28, c="#d62728", linewidths=0)
        ax.set_aspect("equal")
        ax.set_xlim(-0.5, 15.5)
        ax.set_ylim(15.5, -0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"{title}\nK={len(idxs)} mapped={len(mapped)} unmapped={len(unmapped)}", fontsize=9)
        _save(fig, out_dir / out_name)

    for k in (32, 64, 96):
        plot_one(f"topk_k{k}", f"topK k={k}", f"layout_topk_k{k}.png")
        plot_one(f"fps2k_k{k}", f"fps2k k={k}", f"layout_fps2k_k{k}.png")

    # harmful channels plot (complement of prune_harmful)
    pruned = subset_defs.get("prune_harmful")
    if pruned:
        harmful = sorted(set(range(124)) - set(pruned))
        subset_defs2 = dict(subset_defs)
        subset_defs2["harmful"] = harmful
        plot_one("harmful", "harmful channels", "layout_harmful_channels.png")


def main() -> None:
    ap = argparse.ArgumentParser(description="Make EPG design plots from collected results.")
    ap.add_argument("--results_csv", type=Path, nargs="+", required=True)
    ap.add_argument("--subset_defs", type=Path, default=Path("sweeps/ed20260217/subsets/P1_subset_defs.csv"))
    ap.add_argument("--smartpalate_csv", type=Path, default=Path("scripts/smartpalate_distribution.csv"))
    ap.add_argument("--dropout_spatial_csv", type=Path, default=Path("sweeps/ed20260217/results/dropout_summary_spatial2d.csv"))
    ap.add_argument("--out_dir", type=Path, default=Path("docs/report/figures/ed20260217"))
    ap.add_argument("--only_kcurve", action="store_true")
    args = ap.parse_args()

    rows = _read_rows(args.results_csv)
    if not rows:
        raise SystemExit("No rows loaded from results_csv.")
    _ensure_dir(args.out_dir)
    if args.only_kcurve:
        plot_cer_rtf_vs_k(rows, args.out_dir)
        print(f"Wrote k-curve figure under {args.out_dir}")
        return

    subset_defs = _read_subset_defs(args.subset_defs)
    plot_cer_vs_k(rows, args.out_dir)
    plot_cer_rtf_vs_k(rows, args.out_dir)
    plot_delta_curves(rows, args.out_dir)
    plot_rtf_vs_k(rows, args.out_dir)
    plot_layouts(subset_defs, args.out_dir, args.smartpalate_csv)
    plot_frontend_compare(rows, args.out_dir)
    plot_dropout_spatial2d_aug_vs_noaug(args.dropout_spatial_csv, args.out_dir)

    print(f"Wrote figures under {args.out_dir}")


if __name__ == "__main__":
    main()
