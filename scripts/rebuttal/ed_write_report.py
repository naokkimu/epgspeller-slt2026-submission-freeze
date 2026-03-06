#!/usr/bin/env python3
"""Write a markdown report for EPG design sweeps (P1, K-curve).

Data sources (all from real artifacts; no placeholders):
- `gc_collect_metrics.py` outputs (tidy CSV from logs/<run_id>/eval_*.json)
- subset definitions (`P1_subset_defs.csv`)
- aggregated occlusion importance (`P1_channel_importance.csv`)
- rank stability report (`P1_rank_stability.md`)
- optional dropout robustness summary (`dropout_summary.csv`)

This script is intentionally strict by default: it errors if required results
are incomplete. Use --allow_partial only for interim check-ins.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


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


def _read_importance(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _f(v: str) -> Optional[float]:
    s = (v or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None


def _mean_std(xs: Iterable[Optional[float]]) -> Tuple[float, float, int]:
    vals = [float(x) for x in xs if x is not None and not math.isnan(float(x))]
    if not vals:
        return float("nan"), float("nan"), 0
    if len(vals) == 1:
        return vals[0], float("nan"), 1
    return float(statistics.mean(vals)), float(statistics.stdev(vals)), len(vals)


def _md_table(headers: List[str], rows: List[List[str]]) -> str:
    out: List[str] = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def _filter(rows: List[Dict[str, str]], pred) -> List[Dict[str, str]]:
    return [r for r in rows if pred(r)]


def _baseline_p1(rows: List[Dict[str, str]]) -> Dict[str, float]:
    base = _filter(rows, lambda r: (r.get("protocol") or "") == "P1" and (r.get("note") or "") == "baseline")
    cer = [_f(r.get("greedy_test_cer", "")) for r in base]
    lex_train = [_f(r.get("lex_train_cer", "")) for r in base]
    lex_all = [_f(r.get("lex_all_cer", "")) for r in base]
    rtf = [_f(r.get("stream_rtf", "")) for r in base]
    if not [x for x in cer if x is not None]:
        raise SystemExit("No P1 baseline rows found in results CSV. Include gc_baseline.csv in collection.")
    cer_m, cer_s, cer_n = _mean_std(cer)
    lt_m, lt_s, _ = _mean_std(lex_train)
    la_m, la_s, _ = _mean_std(lex_all)
    rtf_m, rtf_s, _ = _mean_std(rtf)
    return {
        "greedy_cer_mean": cer_m,
        "greedy_cer_std": cer_s,
        "n": float(cer_n),
        "lex_train_cer_mean": lt_m,
        "lex_train_cer_std": lt_s,
        "lex_all_cer_mean": la_m,
        "lex_all_cer_std": la_s,
        "rtf_mean": rtf_m,
        "rtf_std": rtf_s,
    }


def _kcurve_seed_means(
    rows: List[Dict[str, str]],
    *,
    method: str,
    k: int,
    metric_key: str,
) -> List[float]:
    """Return per-seed means for a given method+K.

    - For non-random methods: returns the raw 4 seed values (one per seed).
    - For random: averages replicates within each seed, then returns 4 seed means.
    """
    ed = _filter(
        rows,
        lambda r: (r.get("protocol") or "") == "P1"
        and (r.get("note") or "") == "ed:kcurve"
        and (r.get("subset_method") or "") == method
        and int(float(r.get("subset_K") or 0)) == k,
    )
    if method != "random":
        vals = [_f(r.get(metric_key, "")) for r in ed]
        return [v for v in vals if v is not None]

    by_seed: Dict[str, List[float]] = {}
    for r in ed:
        seed = (r.get("split_id") or "").strip()
        v = _f(r.get(metric_key, ""))
        if not seed or v is None:
            continue
        by_seed.setdefault(seed, []).append(v)
    seed_means: List[float] = []
    for _, vs in sorted(by_seed.items()):
        if vs:
            seed_means.append(float(statistics.mean(vs)))
    return seed_means


def _kcurve_summary(
    rows: List[Dict[str, str]],
    *,
    method: str,
    metric_key: str,
) -> Dict[int, Tuple[float, float, int]]:
    out: Dict[int, Tuple[float, float, int]] = {}
    for k in K_LIST:
        seed_means = _kcurve_seed_means(rows, method=method, k=k, metric_key=metric_key)
        m, s, n = _mean_std(seed_means)
        out[k] = (m, s, n)
    return out


def _subset_summary(
    rows: List[Dict[str, str]],
    *,
    subset_id: str,
    note: str,
    metric_key: str,
) -> Tuple[float, float, int]:
    sel = _filter(
        rows,
        lambda r: (r.get("protocol") or "") == "P1"
        and (r.get("note") or "") == note
        and (r.get("subset_id") or "") == subset_id,
    )
    xs = [_f(r.get(metric_key, "")) for r in sel]
    return _mean_std(xs)


def _find_k_star(curve_means: Dict[int, float], baseline_mean: float, thr: float) -> Optional[int]:
    for k in sorted(curve_means.keys()):
        v = curve_means[k]
        if math.isnan(v):
            continue
        if (v - baseline_mean) <= thr:
            return k
    return None


def _parse_rank_stability(md_path: Path) -> Dict[str, object]:
    """Parse ed_aggregate_occlusion rank stability markdown (machine-readable summary)."""
    if not md_path.exists():
        return {"spearman": [], "jaccard": []}

    lines = md_path.read_text().splitlines()

    def parse_table(start_idx: int) -> Tuple[List[str], List[List[str]], int]:
        # Find first table header row.
        i = start_idx
        while i < len(lines) and not lines[i].startswith("|"):
            i += 1
        if i >= len(lines):
            return [], [], len(lines)
        header = [c.strip() for c in lines[i].strip("|").split("|")]
        i += 2  # skip separator
        rows: List[List[str]] = []
        while i < len(lines) and lines[i].startswith("|"):
            rows.append([c.strip() for c in lines[i].strip("|").split("|")])
            i += 1
        return header, rows, i

    spearman_rows: List[Tuple[str, str, float]] = []
    jaccard_rows: List[Tuple[int, str, str, float]] = []

    i = 0
    while i < len(lines):
        if lines[i].startswith("## Spearman"):
            _, rows2, i2 = parse_table(i)
            for r in rows2:
                if len(r) >= 3:
                    rho = _f(r[2])
                    if rho is not None:
                        spearman_rows.append((r[0], r[1], float(rho)))
            i = i2
            continue
        if lines[i].startswith("## TopK Jaccard"):
            _, rows2, i2 = parse_table(i)
            for r in rows2:
                if len(r) >= 4:
                    try:
                        k = int(r[0])
                    except Exception:
                        continue
                    jac = _f(r[3])
                    if jac is None:
                        continue
                    # Skip summary rows written by ed_aggregate_occlusion ("mean"/"min")
                    if r[1] in {"mean", "min"}:
                        continue
                    jaccard_rows.append((k, r[1], r[2], float(jac)))
            i = i2
            continue
        i += 1

    return {"spearman": spearman_rows, "jaccard": jaccard_rows}


def _summarize_rank_stability(parsed: Dict[str, object]) -> Dict[str, str]:
    spearman = parsed.get("spearman", [])
    jaccard = parsed.get("jaccard", [])

    spearman_vals = [rho for _, _, rho in spearman] if spearman else []
    s_mean = statistics.mean(spearman_vals) if spearman_vals else float("nan")
    s_min = min(spearman_vals) if spearman_vals else float("nan")

    by_k: Dict[int, List[float]] = {}
    for k, _, _, jac in jaccard or []:
        by_k.setdefault(int(k), []).append(float(jac))

    out: Dict[str, str] = {
        "spearman_mean": f"{s_mean:.4f}" if not math.isnan(s_mean) else "nan",
        "spearman_min": f"{s_min:.4f}" if not math.isnan(s_min) else "nan",
    }
    for k in (32, 64, 96):
        vals = by_k.get(k, [])
        if vals:
            out[f"jaccard_mean_k{k}"] = f"{statistics.mean(vals):.4f}"
            out[f"jaccard_min_k{k}"] = f"{min(vals):.4f}"
        else:
            out[f"jaccard_mean_k{k}"] = "nan"
            out[f"jaccard_min_k{k}"] = "nan"
    return out


def _read_dropout_summary(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    ap = argparse.ArgumentParser(description="Write EPG design report from collected results.")
    ap.add_argument("--results_csv", type=Path, nargs="+", required=True)
    ap.add_argument("--subset_defs", type=Path, required=True)
    ap.add_argument("--importance_csv", type=Path, required=True)
    ap.add_argument("--rank_stability_md", type=Path, required=True)
    ap.add_argument("--dropout_summary_csv", type=Path, default=None)
    ap.add_argument("--dropout_summary_spatial_csv", type=Path, default=None)
    ap.add_argument("--fig_dir", type=Path, default=Path("docs/report/figures/ed20260217"))
    ap.add_argument("--out_md", type=Path, default=Path("docs/report/epg_design_results_2026-02-17.md"))
    ap.add_argument("--allow_partial", action="store_true")
    args = ap.parse_args()

    rows = _read_rows(args.results_csv)
    if not rows:
        raise SystemExit("No rows loaded from results_csv.")

    subset_defs = _read_subset_defs(args.subset_defs)
    imp_rows = _read_importance(args.importance_csv)
    if not imp_rows:
        raise SystemExit(f"No rows in importance_csv: {args.importance_csv}")

    base = _baseline_p1(rows)
    base_cer = float(base["greedy_cer_mean"])

    # Core K-curve summaries (greedy CER).
    top_s = _kcurve_summary(rows, method="topk", metric_key="greedy_test_cer")
    fps_s = _kcurve_summary(rows, method="fps2k", metric_key="greedy_test_cer")
    rnd_s = _kcurve_summary(rows, method="random", metric_key="greedy_test_cer")

    # Completeness check for K-curve. (random: 4 seed means required)
    missing: List[str] = []
    for k in K_LIST:
        if top_s[k][2] < 4:
            missing.append(f"topk k={k} n={top_s[k][2]}")
        if fps_s[k][2] < 4:
            missing.append(f"fps2k k={k} n={fps_s[k][2]}")
        if rnd_s[k][2] < 4:
            missing.append(f"random k={k} n_seed_means={rnd_s[k][2]}")
    if missing and not args.allow_partial:
        raise SystemExit("Incomplete K-curve results: " + "; ".join(missing[:20]) + ("" if len(missing) <= 20 else " ..."))

    top_means = {k: top_s[k][0] for k in K_LIST}
    kstars = {
        "Δ<=0.005": _find_k_star(top_means, base_cer, 0.005),
        "Δ<=0.010": _find_k_star(top_means, base_cer, 0.010),
        "Δ<=0.020": _find_k_star(top_means, base_cer, 0.020),
    }

    # Rank stability summary.
    parsed = _parse_rank_stability(args.rank_stability_md)
    stab = _summarize_rank_stability(parsed)

    # Helpful: top channels by mean_delta_cer.
    scored: List[Tuple[float, int]] = []
    for r in imp_rows:
        ch = (r.get("channel") or "").strip()
        d = _f(r.get("mean_delta_cer", ""))
        if not ch or d is None:
            continue
        scored.append((float(d), int(ch)))
    scored.sort(key=lambda t: (-t[0], t[1]))
    top10 = scored[:10]
    bottom10 = sorted(scored, key=lambda t: (t[0], t[1]))[:10]

    # H3 prune_harmful (in kcurve matrix)
    prune_mean, prune_std, prune_n = _subset_summary(rows, subset_id="prune_harmful", note="ed:kcurve", metric_key="greedy_test_cer")
    prune_delta = (prune_mean - base_cer) if (not math.isnan(prune_mean)) else float("nan")

    # H6 front/post comparisons
    front32 = _subset_summary(rows, subset_id="front_topk_k32", note="ed:kcurve", metric_key="greedy_test_cer")
    post32 = _subset_summary(rows, subset_id="post_topk_k32", note="ed:kcurve", metric_key="greedy_test_cer")
    front64 = _subset_summary(rows, subset_id="front_topk_k64", note="ed:kcurve", metric_key="greedy_test_cer")
    post64 = _subset_summary(rows, subset_id="post_topk_k64", note="ed:kcurve", metric_key="greedy_test_cer")

    # H8 proj interaction (projNone note)
    proj_tbl: List[List[str]] = []
    for k in (16, 32, 64):
        sid = f"topk_k{k}"
        proj64 = _subset_summary(rows, subset_id=sid, note="ed:kcurve", metric_key="greedy_test_cer")
        projNone = _subset_summary(rows, subset_id=sid, note="ed:projNone", metric_key="greedy_test_cer")
        d = (projNone[0] - proj64[0]) if (not math.isnan(projNone[0]) and not math.isnan(proj64[0])) else float("nan")
        proj_tbl.append(
            [
                str(k),
                f"{proj64[0]:.4f}",
                f"{proj64[1]:.4f}" if not math.isnan(proj64[1]) else "nan",
                str(proj64[2]),
                f"{projNone[0]:.4f}",
                f"{projNone[1]:.4f}" if not math.isnan(projNone[1]) else "nan",
                str(projNone[2]),
                f"{d:+.4f}" if not math.isnan(d) else "nan",
            ]
        )

    # H4/H5 deltas across K
    delta_top_minus_rnd = {k: (top_s[k][0] - rnd_s[k][0]) for k in K_LIST}
    delta_fps_minus_top = {k: (fps_s[k][0] - top_s[k][0]) for k in K_LIST}
    h4_total = sum(1 for k in K_LIST if not math.isnan(delta_top_minus_rnd[k]))
    h4_wins = sum(1 for k in K_LIST if not math.isnan(delta_top_minus_rnd[k]) and delta_top_minus_rnd[k] < 0)
    h4_losses = sum(1 for k in K_LIST if not math.isnan(delta_top_minus_rnd[k]) and delta_top_minus_rnd[k] > 0)
    h5_small = [k for k in K_LIST if k <= 64 and not math.isnan(delta_fps_minus_top[k])]
    h5_better = sum(1 for k in h5_small if delta_fps_minus_top[k] < 0)
    h5_worse = sum(1 for k in h5_small if delta_fps_minus_top[k] > 0)

    # H10: simple Pareto table for representative Ks (best of topk vs fps2k by CER).
    pareto_rows: List[List[str]] = []
    for k in (16, 32, 64, 96, 120):
        # pick better method by CER
        top_m = top_s[k][0]
        fps_m = fps_s[k][0]
        method = "topk" if (not math.isnan(top_m) and (math.isnan(fps_m) or top_m <= fps_m)) else "fps2k"
        cer = top_m if method == "topk" else fps_m

        rtf_mean = float("nan")
        # mean RTF for the chosen method (seed means; random not used here)
        rtf_s = _kcurve_summary(rows, method=method, metric_key="stream_rtf")
        rtf_mean = rtf_s[k][0]

        pareto_rows.append(
            [
                str(k),
                method,
                f"{cer:.4f}" if not math.isnan(cer) else "nan",
                f"{(cer - base_cer):+.4f}" if not math.isnan(cer) else "nan",
                f"{rtf_mean:.4f}" if not math.isnan(rtf_mean) else "nan",
            ]
        )

    # Dropout summary (optional)
    dropout_rows: List[Dict[str, str]] = []
    if args.dropout_summary_csv is not None:
        if not args.dropout_summary_csv.exists():
            raise SystemExit(f"dropout_summary_csv not found: {args.dropout_summary_csv}")
        dropout_rows = _read_dropout_summary(args.dropout_summary_csv)

    dropout_spatial_rows: List[Dict[str, str]] = []
    if args.dropout_summary_spatial_csv is not None:
        if not args.dropout_summary_spatial_csv.exists():
            raise SystemExit(f"dropout_summary_spatial_csv not found: {args.dropout_summary_spatial_csv}")
        dropout_spatial_rows = _read_dropout_summary(args.dropout_summary_spatial_csv)

    def dropout_table_from(rows_in: List[Dict[str, str]], run_ids: List[str]) -> Optional[str]:
        if not rows_in:
            return None
        sel = [r for r in rows_in if (r.get("run_id") or "") in set(run_ids)]
        if not sel:
            return None
        by_q: Dict[str, List[float]] = {}
        for r in sel:
            q = (r.get("drop_rate") or "").strip()
            d = _f(r.get("delta_cer_mean", ""))
            if not q or d is None:
                continue
            by_q.setdefault(q, []).append(float(d))
        table: List[List[str]] = []
        for q, ds in sorted(by_q.items(), key=lambda t: float(t[0])):
            m, s, n = _mean_std(ds)
            table.append([q, f"{m:+.4f}", f"{s:.4f}" if not math.isnan(s) else "nan", str(n)])
        return _md_table(["drop_rate", "ΔCER mean", "std", "n(seeds)"], table)

    def dropout_table(run_ids: List[str]) -> Optional[str]:
        return dropout_table_from(dropout_rows, run_ids)

    # Determine concrete run_ids for dropout (spec1 vs spec0) using run_id naming convention.
    spec1_run_ids = [
        f"P1_seed{s}_raw_ds1_sub-topk_k64_uni_gru_u512_l5_s4_k32_proj64_spec1_noiseDefault_trainseed0_ed20260217"
        for s in range(4)
    ]
    spec0_run_ids = [
        f"P1_seed{s}_raw_ds1_sub-topk_k64_uni_gru_u512_l5_s4_k32_proj64_spec0_noiseDefault_trainseed0_ed20260217"
        for s in range(4)
    ]
    spatial2d_aug0_run_ids = [
        f"P1_seed{s}_raw_ds1_sub-topk_k64_spatial2d_uni_gru_u512_l5_s4_k32_proj64_spec1_spaug0_noiseDefault_trainseed0_ed20260217"
        for s in range(4)
    ]
    spatial2d_aug1_run_ids = [
        f"P1_seed{s}_raw_ds1_sub-topk_k64_spatial2d_uni_gru_u512_l5_s4_k32_proj64_spec1_spaug1_noiseDefault_trainseed0_ed20260217"
        for s in range(4)
    ]

    md: List[str] = []
    md.append("# EPG design results (P1, ed20260217)")
    md.append("")
    md.append("目的: 次EPGの電極配置（残す/増やす/捨てる）を、P1(seed0–3)の実測ログから決める。")
    md.append("")
    md.append("## Baseline (K=124)")
    md.append("")
    md.append(
        _md_table(
            ["metric", "mean", "std", "n(seeds)"],
            [
                ["greedy CER", f"{base['greedy_cer_mean']:.4f}", f"{base['greedy_cer_std']:.4f}" if not math.isnan(base["greedy_cer_std"]) else "nan", "4"],
                ["lex_train CER", f"{base['lex_train_cer_mean']:.4f}", f"{base['lex_train_cer_std']:.4f}" if not math.isnan(base["lex_train_cer_std"]) else "nan", "4"],
                ["lex_all CER", f"{base['lex_all_cer_mean']:.4f}", f"{base['lex_all_cer_std']:.4f}" if not math.isnan(base["lex_all_cer_std"]) else "nan", "4"],
                ["stream_rtf", f"{base['rtf_mean']:.4f}" if not math.isnan(base["rtf_mean"]) else "nan", f"{base['rtf_std']:.4f}" if not math.isnan(base["rtf_std"]) else "nan", "4"],
            ],
        )
    )
    md.append("")

    md.append("## H1: 電極数飽和（Budget / topK）")
    md.append("")
    md.append("**結論(自動要約):** " + ", ".join([f"{k}={v}" for k, v in kstars.items()]) + "（baselineとの差分で判定）")
    md.append("")
    table = []
    for k in K_LIST:
        m, s, n = top_s[k]
        d = m - base_cer if not math.isnan(m) else float("nan")
        table.append([str(k), f"{m:.4f}", f"{s:.4f}" if not math.isnan(s) else "nan", str(n), f"{d:+.4f}" if not math.isnan(d) else "nan"])
    md.append(_md_table(["K", "topK CER mean", "std", "n(seeds)", "Δ vs baseline"], table))
    md.append("")
    md.append(f"Figure: `{args.fig_dir / 'cer_vs_k.png'}`")
    md.append("")

    md.append("## H2: 重要度ランキングの安定性（Split-robust）")
    md.append("")
    md.append(
        f"**結論(自動要約):** Spearman(mean/min)={stab['spearman_mean']}/{stab['spearman_min']}, "
        f"Jaccard mean/min: K32={stab['jaccard_mean_k32']}/{stab['jaccard_min_k32']}, "
        f"K64={stab['jaccard_mean_k64']}/{stab['jaccard_min_k64']}, "
        f"K96={stab['jaccard_mean_k96']}/{stab['jaccard_min_k96']}."
    )
    md.append("")
    md.append(f"詳細: `{args.rank_stability_md}`")
    md.append("")
    md.append("Top-10 important channels (mean ΔCER):")
    md.append("")
    md.append(_md_table(["rank", "channel", "mean ΔCER"], [[str(i + 1), str(ch), f"{d:+.6f}"] for i, (d, ch) in enumerate(top10)]))
    md.append("")
    md.append("Bottom-10 (potentially harmful) channels (mean ΔCER):")
    md.append("")
    md.append(_md_table(["rank", "channel", "mean ΔCER"], [[str(i + 1), str(ch), f"{d:+.6f}"] for i, (d, ch) in enumerate(bottom10)]))
    md.append("")

    md.append("## H3: 有害電極（Harmful channels）")
    md.append("")
    pruned = subset_defs.get("prune_harmful")
    if pruned:
        harmful = sorted(set(range(124)) - set(pruned))
        md.append(f"- harmful_channels={len(harmful)}（subset_defs の prune_harmful 補集合）")
        md.append(f"- prune_harmful K={len(pruned)}")
        md.append("")
        md.append(
            _md_table(
                ["condition", "CER mean", "std", "n(seeds)", "Δ vs baseline"],
                [
                    ["baseline (K=124)", f"{base_cer:.4f}", f"{base['greedy_cer_std']:.4f}" if not math.isnan(base["greedy_cer_std"]) else "nan", "4", "+0.0000"],
                    ["prune_harmful", f"{prune_mean:.4f}", f"{prune_std:.4f}" if not math.isnan(prune_std) else "nan", str(prune_n), f"{prune_delta:+.4f}" if not math.isnan(prune_delta) else "nan"],
                ],
            )
        )
        md.append("")
        md.append(
            "**結論(自動要約):** "
            + ("改善した（ΔCER<0）→「有害電極」仮説を支持。" if (not math.isnan(prune_delta) and prune_delta < 0) else "改善しない（ΔCER>=0）→単純な pruning は効かない/要再定義。")
        )
        md.append("")
        md.append(f"Figure: `{args.fig_dir / 'layout_harmful_channels.png'}`")
        md.append("")
    else:
        md.append("subset_defs に prune_harmful が無い（ed_define_subsets.py を再生成）。")
        md.append("")

    md.append("## H4: topK は randomK に勝つか？")
    md.append("")
    if h4_total == 0:
        md.append("**結論(自動要約):** 未集計（randomK 未完走）。")
    else:
        md.append(
            f"**結論(自動要約):** topK が random より良い(Kの個数)={h4_wins}/{h4_total}、悪い={h4_losses}/{h4_total}（mean CERで比較）。"
        )
    md.append("")
    sample_ks = [16, 32, 64, 96, 120]
    trows: List[List[str]] = []
    for k in sample_ks:
        trows.append(
            [
                str(k),
                f"{top_s[k][0]:.4f}",
                f"{rnd_s[k][0]:.4f}",
                f"{delta_top_minus_rnd[k]:+.4f}" if not math.isnan(delta_top_minus_rnd[k]) else "nan",
            ]
        )
    md.append(_md_table(["K", "topK CER", "randomK CER", "Δ(top-random)"], trows))
    md.append("")
    md.append(f"Figure: `{args.fig_dir / 'delta_topk_minus_random.png'}`")
    md.append("")

    md.append("## H5: 空間分散（fps2k）は小Kで効くか？")
    md.append("")
    md.append(f"**結論(自動要約):** K<=64 で fps2k が topK より良い={h5_better}/{len(h5_small)}、悪い={h5_worse}/{len(h5_small)}（mean CERで比較）。")
    md.append("")
    trows = []
    for k in [16, 24, 32, 40, 48, 56, 64]:
        trows.append(
            [
                str(k),
                f"{fps_s[k][0]:.4f}",
                f"{top_s[k][0]:.4f}",
                f"{delta_fps_minus_top[k]:+.4f}" if not math.isnan(delta_fps_minus_top[k]) else "nan",
            ]
        )
    md.append(_md_table(["K", "fps2k CER", "topK CER", "Δ(fps-top)"], trows))
    md.append("")
    md.append(f"Figure: `{args.fig_dir / 'delta_fps2k_minus_topk.png'}`")
    md.append("")

    md.append("## H6: 前後重要度（Front vs Back）")
    md.append("")
    md.append(
        _md_table(
            ["subset", "K", "CER mean", "std", "n(seeds)", "Δ vs topK"],
            [
                ["front_topk_k32", "32", f"{front32[0]:.4f}", f"{front32[1]:.4f}" if not math.isnan(front32[1]) else "nan", str(front32[2]), f"{(front32[0] - top_s[32][0]):+.4f}" if (not math.isnan(front32[0]) and not math.isnan(top_s[32][0])) else "nan"],
                ["post_topk_k32", "32", f"{post32[0]:.4f}", f"{post32[1]:.4f}" if not math.isnan(post32[1]) else "nan", str(post32[2]), f"{(post32[0] - top_s[32][0]):+.4f}" if (not math.isnan(post32[0]) and not math.isnan(top_s[32][0])) else "nan"],
                ["front_topk_k64", "64", f"{front64[0]:.4f}", f"{front64[1]:.4f}" if not math.isnan(front64[1]) else "nan", str(front64[2]), f"{(front64[0] - top_s[64][0]):+.4f}" if (not math.isnan(front64[0]) and not math.isnan(top_s[64][0])) else "nan"],
                ["post_topk_k64", "64", f"{post64[0]:.4f}", f"{post64[1]:.4f}" if not math.isnan(post64[1]) else "nan", str(post64[2]), f"{(post64[0] - top_s[64][0]):+.4f}" if (not math.isnan(post64[0]) and not math.isnan(top_s[64][0])) else "nan"],
            ],
        )
    )
    md.append("")
    # Simple conclusion: which wins at K=32/64
    concl = []
    if not math.isnan(front32[0]) and not math.isnan(post32[0]):
        concl.append("K=32 は " + ("front優位" if front32[0] <= post32[0] else "post優位"))
    if not math.isnan(front64[0]) and not math.isnan(post64[0]):
        concl.append("K=64 は " + ("front優位" if front64[0] <= post64[0] else "post優位"))
    md.append("**結論(自動要約):** " + (" / ".join(concl) if concl else "未集計（結果不足）"))
    md.append("")

    md.append("## H7: 欠損耐性（Electrode failure robustness）")
    md.append("")
    t_spec1 = dropout_table(spec1_run_ids)
    t_spec0 = dropout_table(spec0_run_ids)
    if (t_spec1 is None or t_spec0 is None) and not args.allow_partial:
        raise SystemExit(
            "Dropout robustness results missing. Run ed_eval_fixed_dropout.py for spec1/spec0 models and collect with ed_collect_dropout.py."
        )
    if t_spec1 is None or t_spec0 is None:
        md.append("dropout_summary が未生成（または該当run_idが未評価）。")
        md.append("必要: `ed_eval_fixed_dropout.py` → `ed_collect_dropout.py`。")
        md.append("")
    else:
        md.append("### specaug_on=1 (topk_k64)")
        md.append("")
        md.append(t_spec1)
        md.append("")
        md.append("### specaug_on=0 (topk_k64)")
        md.append("")
        md.append(t_spec0)
        md.append("")
        md.append("**結論(自動要約):** qごとのΔCERを比較し、specaug有りの方がΔCERが小さければ「欠損耐性↑」を支持。")
        md.append("")

    md.append("## H8: 表現×電極数相互作用（proj64 vs projNone）")
    md.append("")
    if any(r[3] == "0" or r[6] == "0" for r in proj_tbl) and not args.allow_partial:
        raise SystemExit("projNone results incomplete. Ensure ed_p1_projNone.csv runs are complete and included in results.")
    md.append(_md_table(["K", "proj64 mean", "std", "n", "projNone mean", "std", "n", "Δ(projNone-proj64)"], proj_tbl))
    md.append("")
    md.append("**結論(自動要約):** Δが正なら proj64 が有利、負なら projNone が有利。小Kで|Δ|が大きいほど「相互作用」を支持。")
    md.append("")

    md.append("## H9: プロトコル転移（P1最適はP2/P3にも効くか？）")
    md.append("")
    md.append("本フェーズは **P1先行**。P2/P3は次フェーズで以下を実施する:")
    md.append("- P2/P3 baseline に channel occlusion → importance を作る")
    md.append("- P1-topK を P2/P3 に適用 vs P2/P3 再最適 topK を比較")
    md.append("")

    md.append("## H10: Pareto（CER × K × streaming）")
    md.append("")
    md.append("代表Kで、CERが良い方（topK/fps2k）を選び、stream_rtf を併記。")
    md.append("")
    md.append(_md_table(["K", "best_method", "CER mean", "Δ vs baseline", "stream_rtf mean"], pareto_rows))
    md.append("")
    md.append(f"Figure: `{args.fig_dir / 'rtf_vs_k.png'}`")
    md.append("")

    # --- H11–H13: spatial front-ends / spatial aug / row&col compression ---
    md.append("## H11: 16×16復元 + 2D Conv front-end は vector より強いか？（spatial2d_uni_gru）")
    md.append("")
    h11_rows: List[List[str]] = []

    def _summary_str(note: str, subset_id: str, key: str) -> Tuple[float, float, int]:
        return _subset_summary(rows, subset_id=subset_id, note=note, metric_key=key)

    # K={32,64,96} × {topk,fps2k} (+ baseline124)
    need_h11: List[str] = []
    for k in (32, 64, 96):
        for sid in (f"topk_k{k}", f"fps2k_k{k}"):
            v_cer = _summary_str("ed:kcurve", sid, "greedy_test_cer")
            s_cer = _summary_str("ed:spatial2d_compare", sid, "greedy_test_cer")
            v_rtf = _summary_str("ed:kcurve", sid, "stream_rtf")
            s_rtf = _summary_str("ed:spatial2d_compare", sid, "stream_rtf")
            v_lt = _summary_str("ed:kcurve", sid, "lex_train_cer")
            s_lt = _summary_str("ed:spatial2d_compare", sid, "lex_train_cer")
            v_la = _summary_str("ed:kcurve", sid, "lex_all_cer")
            s_la = _summary_str("ed:spatial2d_compare", sid, "lex_all_cer")
            if v_cer[2] < 4:
                need_h11.append(f"vector {sid} n={v_cer[2]}")
            if s_cer[2] < 4:
                need_h11.append(f"spatial2d {sid} n={s_cer[2]}")
            d = (s_cer[0] - v_cer[0]) if (not math.isnan(s_cer[0]) and not math.isnan(v_cer[0])) else float("nan")
            h11_rows.append(
                [
                    str(k),
                    sid.replace("_", " "),
                    f"{v_cer[0]:.4f}",
                    f"{v_cer[1]:.4f}" if not math.isnan(v_cer[1]) else "nan",
                    f"{s_cer[0]:.4f}",
                    f"{s_cer[1]:.4f}" if not math.isnan(s_cer[1]) else "nan",
                    f"{d:+.4f}" if not math.isnan(d) else "nan",
                    f"{v_rtf[0]:.4f}" if not math.isnan(v_rtf[0]) else "nan",
                    f"{s_rtf[0]:.4f}" if not math.isnan(s_rtf[0]) else "nan",
                    f"{v_lt[0]:.4f}" if not math.isnan(v_lt[0]) else "nan",
                    f"{s_lt[0]:.4f}" if not math.isnan(s_lt[0]) else "nan",
                    f"{v_la[0]:.4f}" if not math.isnan(v_la[0]) else "nan",
                    f"{s_la[0]:.4f}" if not math.isnan(s_la[0]) else "nan",
                ]
            )

    # baseline124 compare (vector baseline vs spatial2d baseline124)
    s2d_base_cer = _summary_str("ed:spatial2d_compare_baseline124", "el-all", "greedy_test_cer")
    s2d_base_rtf = _summary_str("ed:spatial2d_compare_baseline124", "el-all", "stream_rtf")
    s2d_base_lt = _summary_str("ed:spatial2d_compare_baseline124", "el-all", "lex_train_cer")
    s2d_base_la = _summary_str("ed:spatial2d_compare_baseline124", "el-all", "lex_all_cer")
    if s2d_base_cer[2] < 4:
        need_h11.append(f"spatial2d baseline124 n={s2d_base_cer[2]}")
    d_base = (s2d_base_cer[0] - base["greedy_cer_mean"]) if (not math.isnan(s2d_base_cer[0]) and not math.isnan(base["greedy_cer_mean"])) else float("nan")
    h11_rows.append(
        [
            "124",
            "el all",
            f"{base['greedy_cer_mean']:.4f}",
            f"{base['greedy_cer_std']:.4f}" if not math.isnan(base["greedy_cer_std"]) else "nan",
            f"{s2d_base_cer[0]:.4f}",
            f"{s2d_base_cer[1]:.4f}" if not math.isnan(s2d_base_cer[1]) else "nan",
            f"{d_base:+.4f}" if not math.isnan(d_base) else "nan",
            f"{base['rtf_mean']:.4f}" if not math.isnan(base["rtf_mean"]) else "nan",
            f"{s2d_base_rtf[0]:.4f}" if not math.isnan(s2d_base_rtf[0]) else "nan",
            f"{base['lex_train_cer_mean']:.4f}" if not math.isnan(base["lex_train_cer_mean"]) else "nan",
            f"{s2d_base_lt[0]:.4f}" if not math.isnan(s2d_base_lt[0]) else "nan",
            f"{base['lex_all_cer_mean']:.4f}" if not math.isnan(base["lex_all_cer_mean"]) else "nan",
            f"{s2d_base_la[0]:.4f}" if not math.isnan(s2d_base_la[0]) else "nan",
        ]
    )

    if need_h11 and not args.allow_partial:
        raise SystemExit("H11 incomplete results: " + "; ".join(need_h11[:20]) + ("" if len(need_h11) <= 20 else " ..."))

    md.append(
        _md_table(
            [
                "K",
                "subset",
                "vec CER",
                "std",
                "s2d CER",
                "std",
                "Δ(s2d-vec)",
                "vec rtf",
                "s2d rtf",
                "vec lex_train",
                "s2d lex_train",
                "vec lex_all",
                "s2d lex_all",
            ],
            h11_rows,
        )
    )
    md.append("")
    md.append(f"Figure: `{args.fig_dir / 'compare_frontends_k32_64_96.png'}`")
    md.append("")
    md.append("**結論(手動追記推奨):** 小Kで s2d が vector を上回る/同等なら H11 を支持。劣るなら「2D復元の利得は限定的」.")
    md.append("")

    md.append("## H12: 空間Aug（block dropout + shift）は欠損ロバスト性を上げるか？（spatial2d_uni_gru）")
    md.append("")
    t_aug0 = dropout_table_from(dropout_spatial_rows, spatial2d_aug0_run_ids)
    t_aug1 = dropout_table_from(dropout_spatial_rows, spatial2d_aug1_run_ids)
    if (t_aug0 is None or t_aug1 is None) and not args.allow_partial:
        raise SystemExit(
            "H12 dropout results missing. Run ed_eval_fixed_dropout.py for spatial2d aug0/aug1 models and collect with ed_collect_dropout.py."
        )
    if t_aug0 is None or t_aug1 is None:
        md.append("dropout_summary_spatial が未生成（または該当run_idが未評価）。")
        md.append("必要: `ed_eval_fixed_dropout.py` → `ed_collect_dropout.py`。")
        md.append("")
    else:
        md.append("### spatial_aug=0 (K=64 topk)")
        md.append("")
        md.append(t_aug0)
        md.append("")
        md.append("### spatial_aug=1 (K=64 topk)")
        md.append("")
        md.append(t_aug1)
        md.append("")
        md.append("Figure:")
        md.append(f"- `{args.fig_dir / 'dropout_spatial2d_aug_vs_noaug.png'}`")
        md.append("")
        md.append("**結論(自動要約):** qごとのΔCERが aug=1 の方が小さければ「空間Augで欠損耐性↑」を支持。")
        md.append("")

    md.append("## H13: row/col圧縮で空間情報を残せるか？（rowcol_uni_gru）")
    md.append("")
    h13_rows: List[List[str]] = []
    need_h13: List[str] = []
    for k in (32, 64):
        for sid in (f"topk_k{k}", f"fps2k_k{k}"):
            v_cer = _summary_str("ed:kcurve", sid, "greedy_test_cer")
            r_cer = _summary_str("ed:rowcol_compare", sid, "greedy_test_cer")
            v_rtf = _summary_str("ed:kcurve", sid, "stream_rtf")
            r_rtf = _summary_str("ed:rowcol_compare", sid, "stream_rtf")
            v_lt = _summary_str("ed:kcurve", sid, "lex_train_cer")
            r_lt = _summary_str("ed:rowcol_compare", sid, "lex_train_cer")
            v_la = _summary_str("ed:kcurve", sid, "lex_all_cer")
            r_la = _summary_str("ed:rowcol_compare", sid, "lex_all_cer")
            if v_cer[2] < 4:
                need_h13.append(f"vector {sid} n={v_cer[2]}")
            if r_cer[2] < 4:
                need_h13.append(f"rowcol {sid} n={r_cer[2]}")
            d = (r_cer[0] - v_cer[0]) if (not math.isnan(r_cer[0]) and not math.isnan(v_cer[0])) else float("nan")
            h13_rows.append(
                [
                    str(k),
                    sid.replace("_", " "),
                    f"{v_cer[0]:.4f}",
                    f"{r_cer[0]:.4f}",
                    f"{d:+.4f}" if not math.isnan(d) else "nan",
                    f"{v_rtf[0]:.4f}" if not math.isnan(v_rtf[0]) else "nan",
                    f"{r_rtf[0]:.4f}" if not math.isnan(r_rtf[0]) else "nan",
                    f"{v_lt[0]:.4f}" if not math.isnan(v_lt[0]) else "nan",
                    f"{r_lt[0]:.4f}" if not math.isnan(r_lt[0]) else "nan",
                    f"{v_la[0]:.4f}" if not math.isnan(v_la[0]) else "nan",
                    f"{r_la[0]:.4f}" if not math.isnan(r_la[0]) else "nan",
                ]
            )

    rowcol_base_cer = _summary_str("ed:rowcol_compare_baseline124", "el-all", "greedy_test_cer")
    rowcol_base_rtf = _summary_str("ed:rowcol_compare_baseline124", "el-all", "stream_rtf")
    rowcol_base_lt = _summary_str("ed:rowcol_compare_baseline124", "el-all", "lex_train_cer")
    rowcol_base_la = _summary_str("ed:rowcol_compare_baseline124", "el-all", "lex_all_cer")
    if rowcol_base_cer[2] < 4:
        need_h13.append(f"rowcol baseline124 n={rowcol_base_cer[2]}")
    d_rowcol_base = (rowcol_base_cer[0] - base["greedy_cer_mean"]) if (not math.isnan(rowcol_base_cer[0]) and not math.isnan(base["greedy_cer_mean"])) else float("nan")
    h13_rows.append(
        [
            "124",
            "el all",
            f"{base['greedy_cer_mean']:.4f}",
            f"{rowcol_base_cer[0]:.4f}",
            f"{d_rowcol_base:+.4f}" if not math.isnan(d_rowcol_base) else "nan",
            f"{base['rtf_mean']:.4f}" if not math.isnan(base["rtf_mean"]) else "nan",
            f"{rowcol_base_rtf[0]:.4f}" if not math.isnan(rowcol_base_rtf[0]) else "nan",
            f"{base['lex_train_cer_mean']:.4f}" if not math.isnan(base["lex_train_cer_mean"]) else "nan",
            f"{rowcol_base_lt[0]:.4f}" if not math.isnan(rowcol_base_lt[0]) else "nan",
            f"{base['lex_all_cer_mean']:.4f}" if not math.isnan(base["lex_all_cer_mean"]) else "nan",
            f"{rowcol_base_la[0]:.4f}" if not math.isnan(rowcol_base_la[0]) else "nan",
        ]
    )

    if need_h13 and not args.allow_partial:
        raise SystemExit("H13 incomplete results: " + "; ".join(need_h13[:20]) + ("" if len(need_h13) <= 20 else " ..."))

    md.append(
        _md_table(
            [
                "K",
                "subset",
                "vec CER",
                "rowcol CER",
                "Δ(rowcol-vec)",
                "vec rtf",
                "rowcol rtf",
                "vec lex_train",
                "rowcol lex_train",
                "vec lex_all",
                "rowcol lex_all",
            ],
            h13_rows,
        )
    )
    md.append("")
    md.append(f"Figure: `{args.fig_dir / 'compare_frontends_k32_64_96.png'}`")
    md.append("")
    md.append("**結論(手動追記推奨):** rowcol が CER を大きく落とさず rtf が改善するなら「圧縮で空間情報を保持」を支持。")
    md.append("")

    md.append("## 推奨設計（具体的electrode index集合）")
    md.append("")
    md.append("### K=32 / 64 / 96")
    md.append("")
    rec_rows: List[List[str]] = []
    for k in (32, 64, 96):
        top_m = top_s[k][0]
        fps_m = fps_s[k][0]
        if math.isnan(top_m) and math.isnan(fps_m):
            continue
        method = "topk" if (not math.isnan(top_m) and (math.isnan(fps_m) or top_m <= fps_m)) else "fps2k"
        sid = f"{method}_k{k}" if method != "topk" else f"topk_k{k}"
        if method == "fps2k":
            sid = f"fps2k_k{k}"
        idxs = subset_defs.get(sid)
        rec_rows.append([str(k), method, sid, f"{(top_m if method=='topk' else fps_m):.4f}", " ".join(str(i) for i in (idxs or []))])
    md.append(_md_table(["K", "method", "subset_id", "CER mean", "indices"], rec_rows))
    md.append("")
    md.append("配置図:")
    md.append(f"- `{args.fig_dir / 'layout_topk_k32.png'}` / `{args.fig_dir / 'layout_fps2k_k32.png'}`")
    md.append(f"- `{args.fig_dir / 'layout_topk_k64.png'}` / `{args.fig_dir / 'layout_fps2k_k64.png'}`")
    md.append(f"- `{args.fig_dir / 'layout_topk_k96.png'}` / `{args.fig_dir / 'layout_fps2k_k96.png'}`")
    md.append("")

    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text("\n".join(md) + "\n")
    print(f"Wrote {args.out_md}")


if __name__ == "__main__":
    main()
