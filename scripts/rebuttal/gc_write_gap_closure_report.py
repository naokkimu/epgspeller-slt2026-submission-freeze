#!/usr/bin/env python3
"""Write a gap-closure results markdown report from collected metrics.

This consumes the tidy results CSV produced by gc_collect_metrics.py and optionally
uses occlusion CSVs (Axis B) if present for baseline runs.

Default output path matches the plan tag/date; you can override.

The report is data-driven: no placeholders.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Optional, Sequence, Tuple


def _read_rows(paths: Sequence[Path]) -> List[Dict[str, str]]:
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


def _mean_std(xs: List[float]) -> Tuple[float, float, int]:
    xs = [float(x) for x in xs if x is not None and not math.isnan(float(x))]
    if not xs:
        return float("nan"), float("nan"), 0
    if len(xs) == 1:
        return xs[0], float("nan"), 1
    return float(statistics.mean(xs)), float(statistics.stdev(xs)), len(xs)


def _by_protocol(rows: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    out: Dict[str, List[Dict[str, str]]] = {"P1": [], "P2": [], "P3": []}
    for r in rows:
        p = (r.get("protocol") or "").strip()
        if p in out:
            out[p].append(r)
    return out


def _note(r: Dict[str, str]) -> str:
    return (r.get("note") or "").strip()


def _read_occlusion_csv(path: Path) -> List[Dict[str, str]]:
    lines = path.read_text().splitlines()
    start = None
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        if line.startswith("#"):
            continue
        start = i
        break
    if start is None:
        return []
    return list(csv.DictReader(lines[start:]))


def _strict_counts(rows: List[Dict[str, str]]) -> Dict[str, int]:
    baseline = [r for r in rows if _note(r) == "baseline"]
    axisA = [r for r in rows if _note(r).startswith("axisA:")]
    axisC = [r for r in rows if _note(r).startswith("axisC:")]
    axisD = [r for r in rows if _note(r).startswith("axisD:")]
    axisE = [r for r in rows if _note(r).startswith("axisE:")]
    axisF_spec = [r for r in rows if _note(r) == "axisF:spec0"]
    axisF_noise = [
        r
        for r in rows
        if _note(r).startswith("axisF:") and _note(r) not in {"axisF:spec0"}
    ]
    family = [r for r in rows if _note(r).startswith("family:")]
    ts2vec = [r for r in rows if _note(r) == "ts2vec:minimal"]

    return {
        "baseline": len(baseline),
        "axisA": len(axisA),
        "axisC": len(axisC),
        "axisD": len(axisD),
        "axisE": len(axisE),
        "axisF_spec": len(axisF_spec),
        "axisF_noise": len(axisF_noise),
        "family": len(family),
        "ts2vec": len(ts2vec),
    }


def _md_table(headers: List[str], rows: List[List[str]]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Write gap-closure results markdown from tidy results CSV.")
    ap.add_argument("--results_csv", type=Path, nargs="+", required=True)
    ap.add_argument("--tag", type=str, default="gc20260216")
    ap.add_argument("--fig_dir", type=Path, default=Path("docs/report/figures/gc20260216"))
    ap.add_argument("--out_md", type=Path, default=Path("docs/report/gap_closure_results_2026-02-16.md"))
    ap.add_argument("--allow_partial", action="store_true")
    args = ap.parse_args()

    rows = _read_rows(args.results_csv)
    if not rows:
        raise SystemExit("No rows loaded from results CSV(s).")

    counts = _strict_counts(rows)
    expected = {
        "baseline": 20,
        "axisA": 140,
        "axisC": 140,
        "axisD": 40,
        "axisE": 300,
        "axisF_spec": 20,
        "axisF_noise": 120,
        "family": 40,
        "ts2vec": 5,
    }

    if not args.allow_partial:
        bad = {k: (counts[k], expected[k]) for k in expected if counts.get(k) != expected[k]}
        if bad:
            msg = " ; ".join([f"{k} got={got} expected={exp}" for k, (got, exp) in bad.items()])
            raise SystemExit(f"Incomplete results for strict report: {msg}")

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    base_rows = [r for r in rows if _note(r) == "baseline"]
    axisA_rows = [r for r in rows if _note(r).startswith("axisA:")]
    axisC_rows = [r for r in rows if _note(r).startswith("axisC:")]
    axisD_rows = [r for r in rows if _note(r).startswith("axisD:")]
    axisE_rows = [r for r in rows if _note(r).startswith("axisE:")]
    axisF_spec_rows = [r for r in rows if _note(r) == "axisF:spec0"]
    axisF_noise_rows = [
        r
        for r in rows
        if _note(r).startswith("axisF:") and _note(r) not in {"axisF:spec0"}
    ]
    family_rows = [r for r in rows if _note(r).startswith("family:")]
    ts2_rows = [r for r in rows if _note(r) == "ts2vec:minimal"]

    md: List[str] = []
    md.append(f"# Gap-closure results ({args.tag})")
    md.append("")
    md.append(f"Generated at: {now}")
    md.append("")

    md.append("## Completeness")
    md.append("")
    md.append(_md_table(["subset", "rows"], [[k, str(v)] for k, v in counts.items()]))
    md.append("")

    # Baseline summary
    md.append("## Baseline")
    md.append("")
    base_by = _by_protocol(base_rows)
    base_table: List[List[str]] = []
    for proto in ("P1", "P2", "P3"):
        vals = [_f(r.get("greedy_test_cer", "")) for r in base_by.get(proto, [])]
        vals = [v for v in vals if v is not None]
        m, s, n = _mean_std(vals)
        base_table.append([proto, f"{m:.4f}", f"{s:.4f}" if not math.isnan(s) else "nan", str(n)])
    md.append(_md_table(["protocol", "CER mean", "CER std", "n"], base_table))
    md.append("")

    md.append("### Lexicon projection (baseline)")
    md.append("")
    abs_rows: List[List[str]] = []
    delta_rows: List[List[str]] = []
    for proto in ("P1", "P2", "P3"):
        rs = base_by.get(proto, [])
        g = [_f(r.get("greedy_test_cer", "")) for r in rs]
        lt = [_f(r.get("lex_train_cer", "")) for r in rs]
        la = [_f(r.get("lex_all_cer", "")) for r in rs]
        g_vals = [x for x in g if x is not None]
        lt_vals = [x for x in lt if x is not None]
        la_vals = [x for x in la if x is not None]
        g_m, g_s, n = _mean_std(g_vals)
        lt_m, lt_s, _ = _mean_std(lt_vals)
        la_m, la_s, _ = _mean_std(la_vals)
        abs_rows.append(
            [
                proto,
                f"{g_m:.4f}",
                f"{g_s:.4f}" if not math.isnan(g_s) else "nan",
                f"{lt_m:.4f}",
                f"{lt_s:.4f}" if not math.isnan(lt_s) else "nan",
                f"{la_m:.4f}",
                f"{la_s:.4f}" if not math.isnan(la_s) else "nan",
                str(n),
            ]
        )
        d_lt = []
        d_la = []
        for r in rs:
            gv = _f(r.get("greedy_test_cer", ""))
            ltv = _f(r.get("lex_train_cer", ""))
            lav = _f(r.get("lex_all_cer", ""))
            if gv is not None and ltv is not None:
                d_lt.append(ltv - gv)
            if gv is not None and lav is not None:
                d_la.append(lav - gv)
        dlt_m, dlt_s, dlt_n = _mean_std(d_lt)
        dla_m, dla_s, dla_n = _mean_std(d_la)
        delta_rows.append(
            [
                proto,
                f"{dlt_m:.4f}",
                f"{dlt_s:.4f}" if not math.isnan(dlt_s) else "nan",
                str(dlt_n),
                f"{dla_m:.4f}",
                f"{dla_s:.4f}" if not math.isnan(dla_s) else "nan",
                str(dla_n),
            ]
        )
    md.append(
        _md_table(
            ["protocol", "greedy mean", "std", "lex_train mean", "std", "lex_all mean", "std", "n"],
            abs_rows,
        )
    )
    md.append("")
    md.append(_md_table(["protocol", "Δ(lex_train-greedy) mean", "std", "n", "Δ(lex_all-greedy) mean", "std", "n"], delta_rows))
    md.append("")

    # Axis A
    if axisA_rows:
        md.append("## Axis A — electrode regions")
        md.append("")
        region_levels = [
            "anterior",
            "middle",
            "posterior",
            "left",
            "right",
            "anterior middle",
            "middle posterior",
        ]
        byp = _by_protocol(axisA_rows)
        base_by = _by_protocol(base_rows)
        for proto in ("P1", "P2", "P3"):
            md.append(f"### {proto}")
            table_rows: List[List[str]] = []

            base_vals = [_f(r.get("greedy_test_cer", "")) for r in base_by.get(proto, [])]
            base_vals = [v for v in base_vals if v is not None]
            base_mean, base_std, base_n = _mean_std(base_vals)

            # Include baseline(all) in the comparison table.
            table_rows.append(
                [
                    "all (baseline)",
                    f"{base_mean:.4f}",
                    f"{base_std:.4f}" if not math.isnan(base_std) else "nan",
                    str(base_n),
                    "0.0000",
                ]
            )

            best_name = "all (baseline)"
            best_mean = base_mean
            for reg in region_levels:
                vals = [_f(r.get("greedy_test_cer", "")) for r in byp.get(proto, []) if (r.get("electrode_regions") or "") == reg]
                vals = [v for v in vals if v is not None]
                m, s, n = _mean_std(vals)
                d = m - base_mean if n > 0 and not math.isnan(m) and not math.isnan(base_mean) else float("nan")
                if n > 0 and not math.isnan(m) and m < best_mean:
                    best_mean = m
                    best_name = reg
                table_rows.append(
                    [reg, f"{m:.4f}", f"{s:.4f}" if not math.isnan(s) else "nan", str(n), f"{d:.4f}" if not math.isnan(d) else "nan"]
                )
            md.append(_md_table(["region", "CER mean", "CER std", "n", "Δ vs baseline"], table_rows))
            if best_name:
                md.append("")
                if best_name == "all (baseline)":
                    md.append(f"Conclusion: baseline `all` is best (mean CER={best_mean:.4f}); no subset beats it.")
                else:
                    md.append(f"Conclusion: best region setting is `{best_name}` (mean CER={best_mean:.4f}, Δ={best_mean - base_mean:.4f}).")
            md.append("")
        fig = args.fig_dir / "axisA_regions.png"
        if fig.exists():
            md.append(f"Figure: `{fig}`")
            md.append("")

    # Axis C
    if axisC_rows:
        md.append("## Axis C — representation (PCA) × input projection")
        md.append("")
        # Include baseline raw+proj64 cell.
        combined = list(axisC_rows)
        for r in base_rows:
            if _i(r.get("n_components", "")) == -1 and (r.get("input_proj_dim") or "").strip() == "64":
                r2 = dict(r)
                r2["note"] = "axisC:raw:proj64"
                combined.append(r2)

        byp = _by_protocol(combined)
        n_levels = [-1, 16, 32, 64]
        proj_levels = [("projNone", ""), ("proj64", "64")]

        for proto in ("P1", "P2", "P3"):
            md.append(f"### {proto}")
            table_rows: List[List[str]] = []
            best = ("", float("inf"))
            for n in n_levels:
                rep = "raw" if n == -1 else f"pca{n}"
                for proj_name, proj_val in proj_levels:
                    vals = []
                    for r in byp.get(proto, []):
                        if _i(r.get("n_components", "")) != n:
                            continue
                        pv = (r.get("input_proj_dim") or "").strip()
                        if pv != proj_val:
                            continue
                        v = _f(r.get("greedy_test_cer", ""))
                        if v is not None:
                            vals.append(v)
                    m, s, n_obs = _mean_std(vals)
                    label = f"{rep}×{proj_name}"
                    if n_obs > 0 and m < best[1]:
                        best = (label, m)
                    table_rows.append([label, f"{m:.4f}", f"{s:.4f}" if not math.isnan(s) else "nan", str(n_obs)])
            md.append(_md_table(["repr×proj", "CER mean", "CER std", "n"], table_rows))
            if best[0]:
                md.append("")
                md.append(f"Conclusion: best setting is `{best[0]}` (mean CER={best[1]:.4f}).")
            md.append("")

        fig = args.fig_dir / "axisC_repr_proj_heatmap.png"
        if fig.exists():
            md.append(f"Figure: `{fig}`")
            md.append("")

    # Axis D
    if axisD_rows:
        md.append("## Axis D — downsample factor")
        md.append("")
        combined = list(axisD_rows) + list(base_rows)
        byp = _by_protocol(combined)
        for proto in ("P1", "P2", "P3"):
            md.append(f"### {proto}")
            table_rows: List[List[str]] = []
            best = ("", float("inf"))
            for ds in (1, 2, 4):
                vals = [_f(r.get("greedy_test_cer", "")) for r in byp.get(proto, []) if _i(r.get("downsample_factor", "")) == ds]
                vals = [v for v in vals if v is not None]
                m, s, n = _mean_std(vals)
                if n > 0 and m < best[1]:
                    best = (f"ds{ds}", m)
                table_rows.append([f"ds{ds}", f"{m:.4f}", f"{s:.4f}" if not math.isnan(s) else "nan", str(n)])
            md.append(_md_table(["downsample", "CER mean", "CER std", "n"], table_rows))
            if best[0]:
                md.append("")
                md.append(f"Conclusion: best downsample is `{best[0]}` (mean CER={best[1]:.4f}).")
            md.append("")

        fig = args.fig_dir / "axisD_downsample_curve.png"
        if fig.exists():
            md.append(f"Figure: `{fig}`")
            md.append("")

    # Axis E
    if axisE_rows:
        md.append("## Axis E — capacity grid")
        md.append("")
        combined = list(axisE_rows) + list(base_rows)
        byp = _by_protocol(combined)

        for proto in ("P1", "P2", "P3"):
            md.append(f"### {proto}")
            # Aggregate by capacity config
            by_cfg: DefaultDict[Tuple[int, int, int, int], List[float]] = defaultdict(list)
            for r in byp.get(proto, []):
                cfg = (
                    int(float(r.get("n_units", "0") or 0)),
                    int(float(r.get("n_layers", "0") or 0)),
                    int(float(r.get("stride_len", "0") or 0)),
                    int(float(r.get("kernel_len", "0") or 0)),
                )
                v = _f(r.get("greedy_test_cer", ""))
                if v is not None:
                    by_cfg[cfg].append(v)

            ranked = []
            for cfg, vals in by_cfg.items():
                m, s, n = _mean_std(vals)
                ranked.append((m, s, n, cfg))
            ranked.sort(key=lambda t: t[0])

            top = ranked[:10]
            table_rows = []
            for m, s, n, cfg in top:
                label = f"u{cfg[0]}_l{cfg[1]}_s{cfg[2]}_k{cfg[3]}"
                table_rows.append([label, f"{m:.4f}", f"{s:.4f}" if not math.isnan(s) else "nan", str(n)])
            md.append(_md_table(["config", "CER mean", "CER std", "n"], table_rows))
            if top:
                md.append("")
                md.append(f"Conclusion: best config is `{table_rows[0][0]}` (mean CER={top[0][0]:.4f}).")
            md.append("")

        fig = args.fig_dir / "axisE_capacity_scatter.png"
        if fig.exists():
            md.append(f"Figure: `{fig}`")
            md.append("")

    # Axis F
    if axisF_spec_rows or axisF_noise_rows:
        md.append("## Axis F — augmentation (SpecAug + noise)")
        md.append("")

        # SpecAug delta
        if axisF_spec_rows:
            md.append("### SpecAug on/off")
            md.append("")
            base_by = _by_protocol(base_rows)
            spec_by = _by_protocol(axisF_spec_rows)
            table_rows = []
            for proto in ("P1", "P2", "P3"):
                b_map = {r.get("split_id"): _f(r.get("greedy_test_cer", "")) for r in base_by.get(proto, [])}
                s_map = {r.get("split_id"): _f(r.get("greedy_test_cer", "")) for r in spec_by.get(proto, [])}
                deltas = []
                for sid, bv in b_map.items():
                    sv = s_map.get(sid)
                    if bv is None or sv is None:
                        continue
                    deltas.append(sv - bv)
                m, s, n = _mean_std(deltas)
                table_rows.append([proto, f"{m:.4f}", f"{s:.4f}" if not math.isnan(s) else "nan", str(n)])
            md.append(_md_table(["protocol", "ΔCER(spec0-spec1) mean", "std", "n"], table_rows))
            md.append("")
            fig = args.fig_dir / "axisF_specaug_delta.png"
            if fig.exists():
                md.append(f"Figure: `{fig}`")
                md.append("")

        # Noise sweep
        if axisF_noise_rows:
            md.append("### Noise sensitivity (one-factor-at-a-time)")
            md.append("")
            noise_by = _by_protocol(axisF_noise_rows)
            variants = [
                ("white_noise_sd", [("baseline", 0.8), ("wn0", 0.0), ("wn1p6", 1.6)]),
                ("constant_offset_sd", [("baseline", 0.2), ("co0", 0.0), ("co0p4", 0.4)]),
                ("gaussian_smooth_width", [("baseline", 2.0), ("gs0", 0.0), ("gs4", 4.0)]),
            ]
            for proto in ("P1", "P2", "P3"):
                md.append(f"#### {proto}")
                for param, pts in variants:
                    table_rows = []
                    for tag_name, val in pts:
                        if tag_name == "baseline":
                            rs = [r for r in base_rows if (r.get("protocol") or "") == proto]
                        else:
                            rs = [r for r in noise_by.get(proto, []) if _note(r) == f"axisF:{tag_name}"]
                        vals = [_f(r.get("greedy_test_cer", "")) for r in rs]
                        vals = [v for v in vals if v is not None]
                        m, s, n = _mean_std(vals)
                        table_rows.append([param, str(val), f"{m:.4f}", f"{s:.4f}" if not math.isnan(s) else "nan", str(n)])
                    md.append(_md_table(["param", "value", "CER mean", "CER std", "n"], table_rows))
                    md.append("")

            fig = args.fig_dir / "axisF_noise_sensitivity.png"
            if fig.exists():
                md.append(f"Figure: `{fig}`")
                md.append("")

    # Family
    if family_rows:
        md.append("## Family compare")
        md.append("")
        fam_by = _by_protocol(family_rows)
        base_by = _by_protocol(base_rows)
        for proto in ("P1", "P2", "P3"):
            md.append(f"### {proto}")
            table_rows = []
            for name, rs in [
                ("uni_gru", base_by.get(proto, [])),
                ("causal_tcn", [r for r in fam_by.get(proto, []) if (r.get("model_family") or "") == "causal_tcn"]),
                ("mini_transformer", [r for r in fam_by.get(proto, []) if (r.get("model_family") or "") == "mini_transformer"]),
            ]:
                vals = [_f(r.get("greedy_test_cer", "")) for r in rs]
                vals = [v for v in vals if v is not None]
                m, s, n = _mean_std(vals)
                table_rows.append([name, f"{m:.4f}", f"{s:.4f}" if not math.isnan(s) else "nan", str(n)])
            md.append(_md_table(["family", "CER mean", "CER std", "n"], table_rows))
            # best
            best = min((float(r[1]), r[0]) for r in table_rows if r[1] != 'nan')
            md.append("")
            md.append(f"Conclusion: best family is `{best[1]}` (mean CER={best[0]:.4f}).")
            md.append("")

        fig = args.fig_dir / "family_compare.png"
        if fig.exists():
            md.append(f"Figure: `{fig}`")
            md.append("")

    # TS2Vec
    if ts2_rows:
        md.append("## TS2Vec minimal")
        md.append("")
        base_map = {(r.get("protocol"), r.get("split_id")): r for r in base_rows}
        table_rows = []
        for r in ts2_rows:
            key = (r.get("protocol"), r.get("split_id"))
            b = base_map.get(key)
            if not b:
                continue
            bcer = _f(b.get("greedy_test_cer", ""))
            tcer = _f(r.get("greedy_test_cer", ""))
            if bcer is None or tcer is None:
                continue
            table_rows.append(
                [
                    key[0] or "",
                    key[1] or "",
                    f"{bcer:.4f}",
                    f"{tcer:.4f}",
                    f"{(tcer - bcer):.4f}",
                ]
            )
        md.append(_md_table(["protocol", "split_id", "baseline CER", "ts2vec CER", "ΔCER"], table_rows))
        md.append("")

    # Axis B occlusion (optional)
    md.append("## Axis B — occlusion importance")
    md.append("")
    # Attempt to summarize region deltas if present.
    base_by = _by_protocol(base_rows)
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

    any_occl = False
    for proto in ("P1", "P2", "P3"):
        # Collect per-run occlusion deltas
        deltas_per_run: List[Dict[str, float]] = []
        for r in base_by.get(proto, []):
            run_dir = Path(r.get("run_dir") or "")
            p = run_dir / "occlusion_region_importance.csv"
            if not p.exists():
                continue
            recs = _read_occlusion_csv(p)
            if not recs:
                continue
            deltas_per_run.append({x["region"]: float(x["delta_cer"]) for x in recs if x.get("region")})

        if deltas_per_run:
            any_occl = True
            md.append(f"### {proto} (region)")
            table_rows = []
            for reg in region_levels:
                xs = [d.get(reg) for d in deltas_per_run if reg in d]
                xs = [float(x) for x in xs if x is not None]
                m, s, n = _mean_std(xs)
                table_rows.append([reg, f"{m:.4f}", f"{s:.4f}" if not math.isnan(s) else "nan", str(n)])
            md.append(_md_table(["region", "ΔCER mean", "ΔCER std", "n"], table_rows))
            md.append("")

    if not any_occl:
        md.append("Occlusion CSVs not found yet under baseline run dirs. Run `scripts/rebuttal/eval_occlusion_importance.py` after baseline runs complete.")
        md.append("")

    fig_ch = args.fig_dir / "axisB_occlusion_channel_indexed.png"
    fig_reg = args.fig_dir / "axisB_occlusion_region_bar.png"
    if fig_ch.exists():
        md.append(f"Figure (channel): `{fig_ch}`")
    if fig_reg.exists():
        md.append(f"Figure (region): `{fig_reg}`")
    if fig_ch.exists() or fig_reg.exists():
        md.append("")

    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text("\n".join(md) + "\n")
    print(f"Wrote {args.out_md}")


if __name__ == "__main__":
    main()
