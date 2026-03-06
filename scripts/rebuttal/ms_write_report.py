#!/usr/bin/env python3
"""Write an evidence-only multi-subject report from collected metrics + split EDA.

Inputs
- metrics CSV: produced by scripts/rebuttal/gc_collect_metrics.py
- EDA dir: results/dataset_audit_silentspeller_2026-02-24 (protocol_split_summary.csv)

Outputs
- docs/report/multi_subject_results_2026-02-24.md
- docs/report/figures/ms20260224/*

No placeholder text is allowed: this script fails fast if required inputs are missing.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import math
import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np


P1P2_RE = re.compile(r"^subj(?P<subj>[1-4])_seed(?P<seed>\d+)$")
P3_RE = re.compile(r"^subj(?P<src>[1-3])to(?P<tgt>[1-3])_seed(?P<seed>\d+)$")


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (expected scripts/ and src/)")


def _read_csv_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _to_float(v: str, *, context: str) -> float:
    s = (v or "").strip()
    if s == "":
        raise ValueError(f"Missing float for {context}")
    return float(s)


def _mean_std(xs: Sequence[float]) -> Tuple[float, float]:
    arr = np.array(list(xs), dtype=np.float64)
    if arr.size == 0:
        return float("nan"), float("nan")
    if arr.size == 1:
        return float(arr[0]), 0.0
    return float(arr.mean()), float(arr.std(ddof=1))


def _fmt_mean_std(mean: float, std: float, *, ndigits: int = 4) -> str:
    if math.isnan(mean) or math.isnan(std):
        return "nan"
    return f"{mean:.{ndigits}f}±{std:.{ndigits}f}"


def _parse_group(protocol: str, split_id: str) -> Tuple[str, int]:
    """Return (group_id, seed). group_id is subject (P1/P2) or direction (P3)."""
    if protocol in {"P1", "P2"}:
        m = P1P2_RE.match(split_id)
        if not m:
            raise ValueError(f"Unexpected split_id for {protocol}: {split_id}")
        subj = int(m.group("subj"))
        seed = int(m.group("seed"))
        return f"subj{subj}", seed
    if protocol == "P3":
        m = P3_RE.match(split_id)
        if not m:
            raise ValueError(f"Unexpected split_id for P3: {split_id}")
        src = int(m.group("src"))
        tgt = int(m.group("tgt"))
        seed = int(m.group("seed"))
        return f"subj{src}to{tgt}", seed
    raise ValueError(f"Unsupported protocol: {protocol}")


def _save_scatter(
    path: Path,
    *,
    points: List[Tuple[float, float, str]],
    title: str,
    xlabel: str,
    ylabel: str,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)

    labels = sorted(set(lbl for _, _, lbl in points))
    cmap = plt.get_cmap("tab10")
    color_of = {lbl: cmap(i % 10) for i, lbl in enumerate(labels)}

    plt.figure(figsize=(6, 4))
    for lbl in labels:
        xs = [x for x, _, l in points if l == lbl]
        ys = [y for _, y, l in points if l == lbl]
        plt.scatter(xs, ys, label=lbl, alpha=0.85, s=30, color=color_of[lbl])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def main() -> None:
    ap = argparse.ArgumentParser(description="Write multi-subject report (evidence-only)")
    ap.add_argument(
        "--metrics_csv",
        type=Path,
        required=True,
        help="Metrics CSV from gc_collect_metrics.py",
    )
    ap.add_argument(
        "--eda_dir",
        type=Path,
        default=Path("results/dataset_audit_silentspeller_2026-02-24"),
        help="Directory containing protocol_split_summary.csv (from da_audit_split_npz.py)",
    )
    ap.add_argument(
        "--out_md",
        type=Path,
        default=Path("docs/report/multi_subject_results_2026-02-24.md"),
    )
    ap.add_argument(
        "--fig_dir",
        type=Path,
        default=Path("docs/report/figures/ms20260224"),
    )
    args = ap.parse_args()

    repo_root = _find_repo_root()

    metrics_csv = args.metrics_csv if args.metrics_csv.is_absolute() else (repo_root / args.metrics_csv)
    eda_dir = args.eda_dir if args.eda_dir.is_absolute() else (repo_root / args.eda_dir)
    out_md = args.out_md if args.out_md.is_absolute() else (repo_root / args.out_md)
    fig_dir = args.fig_dir if args.fig_dir.is_absolute() else (repo_root / args.fig_dir)

    if not metrics_csv.exists():
        raise SystemExit(f"Missing metrics_csv: {metrics_csv}")

    split_summary_csv = eda_dir / "protocol_split_summary.csv"
    if not split_summary_csv.exists():
        raise SystemExit(f"Missing split EDA summary: {split_summary_csv}")

    metric_rows = _read_csv_rows(metrics_csv)
    if not metric_rows:
        raise SystemExit(f"Empty metrics CSV: {metrics_csv}")

    # Build audit lookup for test partition stats
    audit_rows = _read_csv_rows(split_summary_csv)
    audit_test: Dict[str, Dict[str, float]] = {}
    for r in audit_rows:
        if (r.get("partition") or "") != "test":
            continue
        split_id = (r.get("split_id") or "").strip()
        if not split_id:
            continue
        try:
            audit_test[split_id] = {
                "overall_mean_contact": _to_float(
                    r.get("overall_mean_contact", ""), context=f"{split_id}:mean_contact"
                ),
                "T_mean": _to_float(r.get("T_mean", ""), context=f"{split_id}:T_mean"),
            }
        except Exception:
            continue

    required_metrics = ["greedy_test_cer", "stream_rtf", "lex_train_cer", "lex_all_cer"]

    # (protocol, group_id) -> metric -> seed -> value
    per_group: Dict[Tuple[str, str], Dict[str, Dict[int, float]]] = {}

    per_run_points_p1: List[Tuple[float, float, str]] = []
    per_run_points_p2: List[Tuple[float, float, str]] = []

    for r in metric_rows:
        protocol = (r.get("protocol") or "").strip()
        split_id = (r.get("split_id") or "").strip()
        if protocol not in {"P1", "P2", "P3"}:
            raise SystemExit(f"Unexpected protocol in metrics CSV: {protocol}")
        if not split_id:
            raise SystemExit("Missing split_id in metrics CSV")

        group_id, seed = _parse_group(protocol, split_id)
        key = (protocol, group_id)
        per_group.setdefault(key, {m: {} for m in required_metrics})

        for m in required_metrics:
            v = _to_float(r.get(m, ""), context=f"{protocol}/{split_id}/{m}")
            if seed in per_group[key][m]:
                raise SystemExit(f"Duplicate seed entry for {protocol}/{group_id} metric={m} seed={seed}")
            per_group[key][m][seed] = v

        # Join with EDA for scatter
        audit_split_id = f"{protocol}_{split_id}"
        if audit_split_id not in audit_test:
            raise SystemExit(f"Missing EDA test stats for split_id={audit_split_id} (need {split_summary_csv})")
        mean_contact = float(audit_test[audit_split_id]["overall_mean_contact"])
        cer = _to_float(r.get("greedy_test_cer", ""), context=f"{protocol}/{split_id}/cer")
        if protocol == "P1":
            per_run_points_p1.append((mean_contact, cer, group_id))
        if protocol == "P2":
            per_run_points_p2.append((mean_contact, cer, group_id))

    expected_seeds = [0, 1, 2, 3]

    def require_seeds(protocol: str, group_id: str, metric: str) -> None:
        got = sorted(per_group[(protocol, group_id)][metric].keys())
        if got != expected_seeds:
            raise SystemExit(f"Seed coverage mismatch for {protocol}/{group_id}/{metric}: got={got} expected={expected_seeds}")

    p1_subjects = ["subj1", "subj2", "subj3", "subj4"]
    p2_subjects = ["subj1", "subj2", "subj3"]
    p3_dirs = ["subj1to2", "subj2to1", "subj1to3", "subj3to1", "subj2to3", "subj3to2"]

    for subj in p1_subjects:
        for m in required_metrics:
            require_seeds("P1", subj, m)

    for subj in p2_subjects:
        for m in required_metrics:
            require_seeds("P2", subj, m)

    for d in p3_dirs:
        for m in required_metrics:
            require_seeds("P3", d, m)

    # Scatter plots
    fig_dir.mkdir(parents=True, exist_ok=True)
    if per_run_points_p1:
        _save_scatter(
            fig_dir / "p1_contact_vs_cer.png",
            points=per_run_points_p1,
            title="P1: test mean-contact vs greedy CER (per seed)",
            xlabel="test overall_mean_contact (EDA)",
            ylabel="greedy_test_cer",
        )
    if per_run_points_p2:
        _save_scatter(
            fig_dir / "p2_contact_vs_cer.png",
            points=per_run_points_p2,
            title="P2: test mean-contact vs greedy CER (per seed)",
            xlabel="test overall_mean_contact (EDA)",
            ylabel="greedy_test_cer",
        )

    def corr(points: List[Tuple[float, float, str]]) -> Optional[float]:
        if len(points) < 2:
            return None
        xs = np.array([x for x, _, _ in points], dtype=np.float64)
        ys = np.array([y for _, y, _ in points], dtype=np.float64)
        if float(xs.std()) == 0.0 or float(ys.std()) == 0.0:
            return None
        return float(np.corrcoef(xs, ys)[0, 1])

    corr_p1 = corr(per_run_points_p1)
    corr_p2 = corr(per_run_points_p2)

    # Write markdown
    out_md.parent.mkdir(parents=True, exist_ok=True)

    def md_table(headers: List[str], rows: List[List[str]]) -> List[str]:
        out: List[str] = []
        out.append("| " + " | ".join(headers) + " |")
        out.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for r in rows:
            out.append("| " + " | ".join(r) + " |")
        return out

    headers = ["group", "greedy CER (mean±std)", "stream RTF (mean±std)", "lex(train) CER", "lex(all) CER"]

    lines: List[str] = []
    lines.append(f"# Multi-subject results (P1/P2/P3) — {_dt.date.today().isoformat()}")
    lines.append("")
    lines.append("Evidence inputs:")
    lines.append(f"- metrics_csv: `{metrics_csv}`")
    lines.append(f"- split_eda_summary: `{split_summary_csv}`")
    lines.append("")

    # P1 table
    p1_rows: List[List[str]] = []
    for subj in p1_subjects:
        cer_mean, cer_std = _mean_std(per_group[("P1", subj)]["greedy_test_cer"].values())
        rtf_mean, rtf_std = _mean_std(per_group[("P1", subj)]["stream_rtf"].values())
        lt_mean, lt_std = _mean_std(per_group[("P1", subj)]["lex_train_cer"].values())
        la_mean, la_std = _mean_std(per_group[("P1", subj)]["lex_all_cer"].values())
        p1_rows.append(
            [
                subj,
                _fmt_mean_std(cer_mean, cer_std),
                _fmt_mean_std(rtf_mean, rtf_std),
                _fmt_mean_std(lt_mean, lt_std),
                _fmt_mean_std(la_mean, la_std),
            ]
        )

    lines.append("## P1 word-holdout (subj1–4)")
    lines.append("")
    lines.extend(md_table(headers, p1_rows))
    lines.append("")

    # P2 table
    p2_rows: List[List[str]] = []
    for subj in p2_subjects:
        cer_mean, cer_std = _mean_std(per_group[("P2", subj)]["greedy_test_cer"].values())
        rtf_mean, rtf_std = _mean_std(per_group[("P2", subj)]["stream_rtf"].values())
        lt_mean, lt_std = _mean_std(per_group[("P2", subj)]["lex_train_cer"].values())
        la_mean, la_std = _mean_std(per_group[("P2", subj)]["lex_all_cer"].values())
        p2_rows.append(
            [
                subj,
                _fmt_mean_std(cer_mean, cer_std),
                _fmt_mean_std(rtf_mean, rtf_std),
                _fmt_mean_std(lt_mean, lt_std),
                _fmt_mean_std(la_mean, la_std),
            ]
        )

    lines.append("## P2 Protocol-S instance-holdout (subj1–3; subj4 excluded)")
    lines.append("")
    lines.extend(md_table(headers, p2_rows))
    lines.append("")
    lines.append("Protocol note:")
    lines.append("- `subj4` is excluded from P2/P3 because Protocol-S construction requires count≥2 per kept word (see dataset audit).")
    lines.append("")

    # P3 table
    p3_rows: List[List[str]] = []
    all_p3_vals: Dict[str, List[float]] = {m: [] for m in required_metrics}
    for d in p3_dirs:
        cer_mean, cer_std = _mean_std(per_group[("P3", d)]["greedy_test_cer"].values())
        rtf_mean, rtf_std = _mean_std(per_group[("P3", d)]["stream_rtf"].values())
        lt_mean, lt_std = _mean_std(per_group[("P3", d)]["lex_train_cer"].values())
        la_mean, la_std = _mean_std(per_group[("P3", d)]["lex_all_cer"].values())
        p3_rows.append(
            [
                d,
                _fmt_mean_std(cer_mean, cer_std),
                _fmt_mean_std(rtf_mean, rtf_std),
                _fmt_mean_std(lt_mean, lt_std),
                _fmt_mean_std(la_mean, la_std),
            ]
        )
        for m in required_metrics:
            all_p3_vals[m].extend(list(per_group[("P3", d)][m].values()))

    cer_mean, cer_std = _mean_std(all_p3_vals["greedy_test_cer"])
    rtf_mean, rtf_std = _mean_std(all_p3_vals["stream_rtf"])
    lt_mean, lt_std = _mean_std(all_p3_vals["lex_train_cer"])
    la_mean, la_std = _mean_std(all_p3_vals["lex_all_cer"])
    p3_rows.append(
        [
            "overall (all dirs; 24 runs)",
            _fmt_mean_std(cer_mean, cer_std),
            _fmt_mean_std(rtf_mean, rtf_std),
            _fmt_mean_std(lt_mean, lt_std),
            _fmt_mean_std(la_mean, la_std),
        ]
    )

    lines.append("## P3 cross-subject (6 directions over subj1–3)")
    lines.append("")
    lines.extend(md_table(headers, p3_rows))
    lines.append("")

    lines.append("## EDA-linked plots")
    lines.append("")
    lines.append(f"- `{fig_dir}`")
    if (fig_dir / "p1_contact_vs_cer.png").exists():
        lines.append(f"  - `p1_contact_vs_cer.png` (Pearson corr={corr_p1 if corr_p1 is not None else 'n/a'})")
    if (fig_dir / "p2_contact_vs_cer.png").exists():
        lines.append(f"  - `p2_contact_vs_cer.png` (Pearson corr={corr_p2 if corr_p2 is not None else 'n/a'})")
    lines.append("")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {out_md}")


if __name__ == "__main__":
    main()
