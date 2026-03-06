#!/usr/bin/env python3
"""Write an evidence-only extended multi-subject report (msx20260224).

Inputs
- metrics CSV: produced by scripts/rebuttal/gc_collect_metrics.py (combined across matrices)
- EDA dir: results/dataset_audit_silentspeller_2026-02-24 (optional: protocol_split_summary.csv)

Outputs
- docs/report/multi_subject_extended_results_2026-02-24.md
- docs/report/figures/msx20260224/*

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
P3MS_RE = re.compile(r"^subj(?P<srca>[1-3])(?P<srcb>[1-3])to(?P<tgt>[1-3])_seed(?P<seed>\d+)$")
P2K_RE = re.compile(r"^subj(?P<subj>[1-4])_seed(?P<seed>\d+)_k(?P<k>[12])$")


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


def _to_int(v: str, *, context: str) -> int:
    s = (v or "").strip()
    if s == "":
        raise ValueError(f"Missing int for {context}")
    return int(float(s))


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


def _md_table(headers: List[str], rows: List[List[str]]) -> str:
    out: List[str] = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def _parse_group(protocol: str, split_id: str) -> Tuple[str, int, str]:
    """Return (group_id, seed, extra) where extra is optional (e.g., k for P2K)."""
    if protocol in {"P1", "P2"}:
        m = P1P2_RE.match(split_id)
        if not m:
            raise ValueError(f"Unexpected split_id for {protocol}: {split_id}")
        subj = int(m.group("subj"))
        seed = int(m.group("seed"))
        return f"subj{subj}", seed, ""
    if protocol == "P3":
        m = P3_RE.match(split_id)
        if not m:
            raise ValueError(f"Unexpected split_id for P3: {split_id}")
        src = int(m.group("src"))
        tgt = int(m.group("tgt"))
        seed = int(m.group("seed"))
        return f"subj{src}to{tgt}", seed, ""
    if protocol == "P3MS":
        m = P3MS_RE.match(split_id)
        if not m:
            raise ValueError(f"Unexpected split_id for P3MS: {split_id}")
        srca = int(m.group("srca"))
        srcb = int(m.group("srcb"))
        tgt = int(m.group("tgt"))
        seed = int(m.group("seed"))
        return f"subj{srca}{srcb}to{tgt}", seed, ""
    if protocol == "P2K":
        m = P2K_RE.match(split_id)
        if not m:
            raise ValueError(f"Unexpected split_id for P2K: {split_id}")
        subj = int(m.group("subj"))
        seed = int(m.group("seed"))
        k = int(m.group("k"))
        return f"subj{subj}_k{k}", seed, f"k{k}"
    raise ValueError(f"Unsupported protocol: {protocol}")


def _variant_id(row: Dict[str, str]) -> str:
    mf = (row.get("model_family") or "").strip()
    if not mf:
        raise ValueError("Missing model_family")
    if mf == "spatial2d_uni_gru":
        aug = (row.get("enable_spatial_aug") or "").strip()
        aug = aug if aug else "0"
        return f"{mf}_aug{aug}"
    subset_method = (row.get("subset_method") or "").strip()
    if subset_method:
        return f"{mf}_{subset_method}"
    return mf


def _save_bar(
    path: Path,
    *,
    labels: List[str],
    values: List[float],
    title: str,
    ylabel: str,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(max(6, 0.5 * len(labels)), 4))
    xs = list(range(len(labels)))
    plt.bar(xs, values)
    plt.xticks(xs, labels, rotation=45, ha="right")
    plt.title(title)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def _require_exact_row_count(rows: List[Dict[str, str]], *, expected: int, context: str) -> None:
    if len(rows) != expected:
        raise SystemExit(f"{context}: expected {expected} rows but got {len(rows)}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Write msx20260224 extended multi-subject report (evidence-only).")
    ap.add_argument("--metrics_csv", type=Path, required=True)
    ap.add_argument(
        "--eda_dir",
        type=Path,
        default=Path("results/dataset_audit_silentspeller_2026-02-24"),
        help="Optional EDA directory to link (protocol_split_summary.csv).",
    )
    ap.add_argument("--tag", type=str, default="msx20260224")
    ap.add_argument("--out_md", type=Path, default=Path("docs/report/multi_subject_extended_results_2026-02-24.md"))
    args = ap.parse_args()

    repo_root = _find_repo_root()
    metrics_csv = args.metrics_csv if args.metrics_csv.is_absolute() else (repo_root / args.metrics_csv)
    eda_dir = args.eda_dir if args.eda_dir.is_absolute() else (repo_root / args.eda_dir)
    out_md = args.out_md if args.out_md.is_absolute() else (repo_root / args.out_md)
    fig_dir = repo_root / "docs" / "report" / "figures" / args.tag

    if not metrics_csv.exists():
        raise SystemExit(f"metrics_csv not found: {metrics_csv}")

    rows = _read_csv_rows(metrics_csv)
    if not rows:
        raise SystemExit(f"No rows in metrics_csv: {metrics_csv}")

    # Expected total = baseline(52) + spatial_k124(156) + k64_uni_gru(208) + spatial_k64(156) + p3ms(48) + kshot(32) = 652
    _require_exact_row_count(rows, expected=652, context="metrics_csv completeness gate (msx20260224)")

    required_keys = [
        "protocol",
        "split_id",
        "model_family",
        "greedy_test_cer",
        "stream_rtf",
        "lex_train_cer",
        "lex_all_cer",
        "note",
    ]
    for k in required_keys:
        if k not in rows[0]:
            raise SystemExit(f"metrics_csv missing required column: {k}")

    # Partition by experiment note
    by_note: Dict[str, List[Dict[str, str]]] = {}
    for r in rows:
        by_note.setdefault((r.get("note") or "").strip(), []).append(r)

    # Baseline rows: note == "baseline:multi_subj" (from ms_baseline matrix)
    baseline_rows = by_note.get("baseline:multi_subj", [])
    _require_exact_row_count(baseline_rows, expected=52, context="baseline rows")

    spatial_k124_rows = by_note.get("msx:spatial_k124", [])
    _require_exact_row_count(spatial_k124_rows, expected=156, context="msx:spatial_k124 rows")

    k64_rows = by_note.get("msx:k64_uni_gru", [])
    _require_exact_row_count(k64_rows, expected=208, context="msx:k64_uni_gru rows")

    spatial_k64_rows = by_note.get("msx:spatial_k64_within_topk", [])
    _require_exact_row_count(spatial_k64_rows, expected=156, context="msx:spatial_k64_within_topk rows")

    p3ms_rows = by_note.get("msx:p3ms", [])
    _require_exact_row_count(p3ms_rows, expected=48, context="msx:p3ms rows")

    kshot_rows = by_note.get("msx:kshot", [])
    _require_exact_row_count(kshot_rows, expected=32, context="msx:kshot rows")

    def summarize(
        subset: List[Dict[str, str]], *, protocol: str, variant: str
    ) -> Dict[str, str]:
        sel = [r for r in subset if (r.get("protocol") or "").strip() == protocol and _variant_id(r) == variant]
        if not sel:
            raise SystemExit(f"Missing rows for protocol={protocol} variant={variant}")

        # group -> seed -> row
        groups: Dict[str, Dict[int, Dict[str, str]]] = {}
        for r in sel:
            gid, seed, _ = _parse_group(protocol, (r.get("split_id") or "").strip())
            if gid not in groups:
                groups[gid] = {}
            if seed in groups[gid]:
                raise SystemExit(f"Duplicate seed for protocol={protocol} variant={variant} group={gid} seed={seed}")
            groups[gid][seed] = r

        # group means across seeds
        group_means: Dict[str, float] = {}
        group_rtfs: Dict[str, float] = {}
        for gid, per_seed in groups.items():
            seeds = sorted(per_seed.keys())
            if seeds != [0, 1, 2, 3]:
                raise SystemExit(
                    f"Expected seeds [0,1,2,3] for protocol={protocol} variant={variant} group={gid} but got {seeds}"
                )
            cer_vals = [_to_float(per_seed[s]["greedy_test_cer"], context=f"{protocol}/{variant}/{gid}/seed{s}/cer") for s in seeds]
            rtf_vals = [_to_float(per_seed[s]["stream_rtf"], context=f"{protocol}/{variant}/{gid}/seed{s}/rtf") for s in seeds]
            group_means[gid] = float(np.mean(np.array(cer_vals, dtype=np.float64)))
            group_rtfs[gid] = float(np.mean(np.array(rtf_vals, dtype=np.float64)))

        cer_mean, cer_std = _mean_std(list(group_means.values()))
        rtf_mean, rtf_std = _mean_std(list(group_rtfs.values()))

        return {
            "n_groups": str(len(group_means)),
            "cer_mean_groups": f"{cer_mean:.6f}",
            "cer_std_groups": f"{cer_std:.6f}",
            "rtf_mean_groups": f"{rtf_mean:.6f}",
            "rtf_std_groups": f"{rtf_std:.6f}",
        }

    # Figure outputs: simple bar charts (CER by variant, grouped mean over groups)
    fig_dir.mkdir(parents=True, exist_ok=True)

    md: List[str] = []
    md.append(f"# Extended multi-subject results (tag={args.tag})")
    md.append("")
    md.append(f"- generated_at: { _dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S') }")
    md.append(f"- metrics_csv: `{metrics_csv.relative_to(repo_root)}`")
    if (eda_dir / "report.md").exists():
        md.append(f"- eda_report: `{(eda_dir / 'report.md').relative_to(repo_root)}`")
    md.append("")

    # --- Baseline recap ---
    md.append("## Baseline recap (ms20260224)")
    md.append("")
    md.append("Per-group mean±std over seeds0–3 (greedy CER / stream RTF / lex CER).")
    md.append("")

    def baseline_table(protocol: str) -> str:
        prot_rows = [r for r in baseline_rows if (r.get("protocol") or "").strip() == protocol]
        if not prot_rows:
            raise SystemExit(f"Missing baseline rows for protocol={protocol}")

        groups: Dict[str, Dict[int, Dict[str, str]]] = {}
        for r in prot_rows:
            gid, seed, _ = _parse_group(protocol, (r.get("split_id") or "").strip())
            groups.setdefault(gid, {})[seed] = r

        trows: List[List[str]] = []
        for gid in sorted(groups.keys()):
            per_seed = groups[gid]
            seeds = sorted(per_seed.keys())
            if seeds != [0, 1, 2, 3]:
                raise SystemExit(f"Baseline {protocol} {gid}: expected seeds 0..3 but got {seeds}")
            cer = [_to_float(per_seed[s]["greedy_test_cer"], context=f"baseline/{protocol}/{gid}/cer") for s in seeds]
            rtf = [_to_float(per_seed[s]["stream_rtf"], context=f"baseline/{protocol}/{gid}/rtf") for s in seeds]
            lex_tr = [_to_float(per_seed[s]["lex_train_cer"], context=f"baseline/{protocol}/{gid}/lex_train") for s in seeds]
            lex_all = [_to_float(per_seed[s]["lex_all_cer"], context=f"baseline/{protocol}/{gid}/lex_all") for s in seeds]
            trows.append(
                [
                    gid,
                    _fmt_mean_std(*_mean_std(cer)),
                    _fmt_mean_std(*_mean_std(rtf), ndigits=6),
                    _fmt_mean_std(*_mean_std(lex_tr)),
                    _fmt_mean_std(*_mean_std(lex_all)),
                ]
            )
        return _md_table(["group", "greedy CER", "stream RTF", "lex(train) CER", "lex(all) CER"], trows)

    for prot in ["P1", "P2", "P3"]:
        md.append(f"### {prot}")
        md.append("")
        md.append(baseline_table(prot))
        md.append("")

    # --- Spatial@K124 ---
    md.append("## Spatial modeling @K=124 (rowcol vs spatial2d aug0/aug1)")
    md.append("")
    md.append("Summary over groups: mean±std over per-group mean CER/RTF (seeds0–3).")
    md.append("")

    for prot in ["P1", "P2", "P3"]:
        variants = ["rowcol_uni_gru", "spatial2d_uni_gru_aug0", "spatial2d_uni_gru_aug1"]
        srows: List[List[str]] = []
        for v in variants:
            ss = summarize(spatial_k124_rows, protocol=prot, variant=v)
            srows.append(
                [
                    v,
                    f"{float(ss['cer_mean_groups']):.4f}±{float(ss['cer_std_groups']):.4f}",
                    f"{float(ss['rtf_mean_groups']):.6f}±{float(ss['rtf_std_groups']):.6f}",
                    ss["n_groups"],
                ]
            )
        md.append(f"### {prot}")
        md.append("")
        md.append(_md_table(["variant", "CER (groups)", "RTF (groups)", "n_groups"], srows))
        md.append("")

        # CER bar
        labels = [r[0] for r in srows]
        values = [float(r[1].split("±")[0]) for r in srows]
        out_png = fig_dir / f"spatial_k124_{prot}_cer_bar.png"
        _save_bar(out_png, labels=labels, values=values, title=f"Spatial@K124 {prot}: CER (group mean)", ylabel="CER")
        md.append(f"Figure: `{out_png.relative_to(repo_root)}`")
        md.append("")

    # --- K64 uni_gru ---
    md.append("## Electrode reduction @K=64 (uni_gru)")
    md.append("")
    md.append("Summary over groups: mean±std over per-group mean CER/RTF (seeds0–3).")
    md.append("")
    for prot in ["P1", "P2", "P3"]:
        variants = [
            "uni_gru_within_topk64",
            "uni_gru_within_fps2k64",
            "uni_gru_transfer_subj1_topk64",
            "uni_gru_random64_seed20260224",
        ]
        srows: List[List[str]] = []
        for v in variants:
            ss = summarize(k64_rows, protocol=prot, variant=v)
            srows.append(
                [
                    v.replace("uni_gru_", ""),
                    f"{float(ss['cer_mean_groups']):.4f}±{float(ss['cer_std_groups']):.4f}",
                    f"{float(ss['rtf_mean_groups']):.6f}±{float(ss['rtf_std_groups']):.6f}",
                    ss["n_groups"],
                ]
            )
        md.append(f"### {prot}")
        md.append("")
        md.append(_md_table(["method", "CER (groups)", "RTF (groups)", "n_groups"], srows))
        md.append("")

        labels = [r[0] for r in srows]
        values = [float(r[1].split("±")[0]) for r in srows]
        out_png = fig_dir / f"k64_{prot}_cer_bar.png"
        _save_bar(out_png, labels=labels, values=values, title=f"K=64 {prot}: CER (group mean)", ylabel="CER")
        md.append(f"Figure: `{out_png.relative_to(repo_root)}`")
        md.append("")

    # --- Spatial@K64 within_topk ---
    md.append("## Spatial modeling @K=64 (within_topk64 subsets)")
    md.append("")
    md.append("Compare uni_gru (K64 within_topk64) vs rowcol/spatial2d (aug0/aug1).")
    md.append("")
    for prot in ["P1", "P2", "P3"]:
        variants = [
            "uni_gru_within_topk64",
            "rowcol_uni_gru_within_topk64",
            "spatial2d_uni_gru_aug0",
            "spatial2d_uni_gru_aug1",
        ]
        srows: List[List[str]] = []
        for v in variants:
            src = k64_rows if v.startswith("uni_gru_") else spatial_k64_rows
            ss = summarize(src, protocol=prot, variant=v)
            srows.append(
                [
                    v.replace("uni_gru_within_topk64", "uni_gru (within_topk64)"),
                    f"{float(ss['cer_mean_groups']):.4f}±{float(ss['cer_std_groups']):.4f}",
                    f"{float(ss['rtf_mean_groups']):.6f}±{float(ss['rtf_std_groups']):.6f}",
                    ss["n_groups"],
                ]
            )
        md.append(f"### {prot}")
        md.append("")
        md.append(_md_table(["variant", "CER (groups)", "RTF (groups)", "n_groups"], srows))
        md.append("")

    # --- P3MS ---
    md.append("## P3MS: multi-source cross-subject (2SRC→1TGT)")
    md.append("")
    md.append("Note: vocabulary size may differ from single-source P3 (intersection over 3 subjects vs 2).")
    md.append("")
    for direction in ["subj23to1", "subj13to2", "subj12to3"]:
        md.append(f"### {direction}")
        md.append("")
        variants = ["uni_gru", "rowcol_uni_gru", "spatial2d_uni_gru_aug0", "spatial2d_uni_gru_aug1"]
        srows: List[List[str]] = []
        for v in variants:
            sel = [r for r in p3ms_rows if (r.get("split_id") or "").startswith(direction + "_")]
            ss = summarize(sel, protocol="P3MS", variant=v)
            # n_samples (test) mean over runs (group means over seeds). Use group-level mean from any seed.
            # Pull from the first group seed0.
            # For determinism, compute mean n_samples over groups (only 1 group here).
            run0 = [r for r in sel if _variant_id(r) == v and (r.get("split_id") or "").endswith("_seed0")]
            if not run0:
                raise SystemExit(f"Missing seed0 row for P3MS direction={direction} variant={v}")
            n_samples = _to_int(run0[0]["n_samples"], context=f"P3MS/{direction}/{v}/n_samples")
            srows.append(
                [
                    v,
                    f"{float(ss['cer_mean_groups']):.4f}±{float(ss['cer_std_groups']):.4f}",
                    f"{float(ss['rtf_mean_groups']):.6f}±{float(ss['rtf_std_groups']):.6f}",
                    str(n_samples),
                ]
            )
        md.append(_md_table(["variant", "CER (groups)", "RTF (groups)", "test n_samples(seed0)"], srows))
        md.append("")

    # --- k-shot ---
    md.append("## subj3 k-shot (k=1 vs k=2)")
    md.append("")
    variants = ["uni_gru", "rowcol_uni_gru", "spatial2d_uni_gru_aug0", "spatial2d_uni_gru_aug1"]
    for k in (1, 2):
        md.append(f"### k={k}")
        md.append("")
        sel_k = [r for r in kshot_rows if f"_k{k}" in (r.get("split_id") or "")]
        srows: List[List[str]] = []
        for v in variants:
            ss = summarize(sel_k, protocol="P2K", variant=v)
            srows.append(
                [
                    v,
                    f"{float(ss['cer_mean_groups']):.4f}±{float(ss['cer_std_groups']):.4f}",
                    f"{float(ss['rtf_mean_groups']):.6f}±{float(ss['rtf_std_groups']):.6f}",
                    ss["n_groups"],
                ]
            )
        md.append(_md_table(["variant", "CER (groups)", "RTF (groups)", "n_groups"], srows))
        md.append("")

    md.append("## Notes / evidence links")
    md.append("")
    md.append("- Split EDA (raw+splits): `results/dataset_audit_silentspeller_2026-02-24/report.md`")
    md.append("- Baseline report: `docs/report/multi_subject_results_2026-02-24.md`")
    md.append(f"- Figures (this report): `docs/report/figures/{args.tag}/`")
    md.append("")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[OK] wrote {out_md}")


if __name__ == "__main__":
    main()
