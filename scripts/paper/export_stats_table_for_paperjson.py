#!/usr/bin/env python3
"""Export compact statistics table with confidence intervals and paired tests.

Evidence-only:
- Inputs are aggregated metrics CSVs from completed runs.
- Outputs are deterministic summaries; no learning or randomness.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from statistics import mean
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from scipy import stats


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise SystemExit("Could not locate repo root (expected scripts/ and src/)")


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


def _sample_std(xs: Sequence[float]) -> float:
    if not xs:
        return float("nan")
    if len(xs) == 1:
        return 0.0
    m = mean(xs)
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return math.sqrt(var)


def _mean_std(xs: Sequence[float]) -> Tuple[float, float]:
    if not xs:
        return float("nan"), float("nan")
    if len(xs) == 1:
        return float(xs[0]), 0.0
    return float(mean(xs)), float(_sample_std(xs))


def _ci_t(mean_val: float, std_val: float, n: int) -> Tuple[float, float]:
    if n < 2:
        raise SystemExit(f"t-interval requires n>=2, got n={n}")
    if std_val == 0.0:
        return mean_val, mean_val
    sem = std_val / math.sqrt(n)
    lo, hi = stats.t.interval(0.95, df=n - 1, loc=mean_val, scale=sem)
    return float(lo), float(hi)


def _paired_t_p(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise SystemExit("paired t-test requires equal-length samples")
    if len(a) < 2:
        raise SystemExit("paired t-test requires at least two paired samples")
    diffs = [x - y for x, y in zip(a, b)]
    if max(abs(d) for d in diffs) == 0.0:
        return 1.0
    res = stats.ttest_rel(a, b)
    p = float(res.pvalue)
    if math.isnan(p):
        return 1.0
    return p


def _holm_adjust(pvals: List[float]) -> List[float]:
    m = len(pvals)
    if m == 0:
        return []
    order = sorted(range(m), key=lambda i: pvals[i])
    adj = [0.0] * m
    prev = 0.0
    for rank, idx in enumerate(order):
        raw = pvals[idx] * (m - rank)
        raw = min(1.0, raw)
        adj_val = max(prev, raw)
        adj[idx] = adj_val
        prev = adj_val
    return adj


def _variant_id(row: Mapping[str, str]) -> str:
    mf = (row.get("model_family") or "").strip()
    if not mf:
        raise ValueError("Missing model_family")
    if mf.startswith("spatial2d"):
        aug = (row.get("enable_spatial_aug") or "").strip() or "0"
        base = f"{mf}_aug{aug}"
        subset_method = (row.get("subset_method") or "").strip()
        if subset_method:
            return f"{base}_{subset_method}"
        return base
    subset_method = (row.get("subset_method") or "").strip()
    if subset_method:
        return f"{mf}_{subset_method}"
    return mf


def _parse_group(protocol: str, split_id: str) -> Tuple[str, int, str]:
    s = (split_id or "").strip()

    def _must_int(x: str) -> int:
        return int(x)

    if protocol in {"P1", "P2"}:
        if not s.startswith("subj") or "_seed" not in s:
            raise ValueError(f"Unexpected split_id for {protocol}: {s}")
        subj_part, seed_part = s.split("_seed", 1)
        subj = _must_int(subj_part.replace("subj", ""))
        seed = _must_int(seed_part)
        return f"subj{subj}", seed, ""

    if protocol == "P3":
        if not s.startswith("subj") or "to" not in s or "_seed" not in s:
            raise ValueError(f"Unexpected split_id for P3: {s}")
        core, seed_part = s.split("_seed", 1)
        seed = _must_int(seed_part)
        src_tgt = core.replace("subj", "")
        src, tgt = src_tgt.split("to", 1)
        return f"subj{_must_int(src)}to{_must_int(tgt)}", seed, ""

    if protocol == "P3MS":
        if not s.startswith("subj") or "to" not in s or "_seed" not in s:
            raise ValueError(f"Unexpected split_id for P3MS: {s}")
        core, seed_part = s.split("_seed", 1)
        seed = _must_int(seed_part)
        srcs_tgt = core.replace("subj", "")
        srcs, tgt = srcs_tgt.split("to", 1)
        if len(srcs) != 2:
            raise ValueError(f"Unexpected multi-source prefix: {srcs_tgt}")
        return f"subj{_must_int(srcs[0])}{_must_int(srcs[1])}to{_must_int(tgt)}", seed, ""

    if protocol == "P2K":
        if not s.startswith("subj") or "_seed" not in s or "_k" not in s:
            raise ValueError(f"Unexpected split_id for P2K: {s}")
        before_k, k_part = s.rsplit("_k", 1)
        core, seed_part = before_k.split("_seed", 1)
        subj = _must_int(core.replace("subj", ""))
        seed = _must_int(seed_part)
        k = _must_int(k_part)
        return f"subj{subj}_k{k}", seed, f"k{k}"

    raise ValueError(f"Unsupported protocol: {protocol}")


def _group_seed_matrix(rows: Sequence[Mapping[str, str]], *, protocol: str, variant: str) -> Dict[str, Dict[int, Mapping[str, str]]]:
    sel = [r for r in rows if (r.get("protocol") or "").strip() == protocol and _variant_id(r) == variant]
    if not sel:
        raise SystemExit(f"Missing rows for protocol={protocol} variant={variant}")

    groups: Dict[str, Dict[int, Mapping[str, str]]] = {}
    for r in sel:
        gid, seed, _ = _parse_group(protocol, (r.get("split_id") or "").strip())
        groups.setdefault(gid, {})
        if seed in groups[gid]:
            raise SystemExit(f"Duplicate seed for protocol={protocol} variant={variant} group={gid} seed={seed}")
        groups[gid][seed] = r

    for gid, per_seed in groups.items():
        seeds = sorted(per_seed.keys())
        if seeds != [0, 1, 2, 3]:
            raise SystemExit(f"Expected seeds [0,1,2,3] for protocol={protocol} variant={variant} group={gid} but got {seeds}")

    return groups


def _group_seed_values(
    rows: Sequence[Mapping[str, str]], *, protocol: str, variant: str, metric_key: str
) -> Dict[str, List[float]]:
    groups = _group_seed_matrix(rows, protocol=protocol, variant=variant)
    out: Dict[str, List[float]] = {}
    for gid, per_seed in groups.items():
        out[gid] = [
            _to_float(per_seed[s][metric_key], context=f"{protocol}/{variant}/{gid}/seed{s}/{metric_key}")
            for s in [0, 1, 2, 3]
        ]
    return out


def _label_spatial_variant(variant_id: str) -> str:
    v = (variant_id or "").strip()
    mapping = {
        "uni_gru": "vec",
        "rowcol_uni_gru": "rowcol",
        "spatial2d_uni_gru_aug0": "grid",
        "spatial2d_uni_gru_aug1": "grid_aug",
        "spatial2d_patchpool_uni_gru_aug0": "patch",
        "spatial2d_patchpool_uni_gru_aug1": "patch_aug",
    }
    return mapping.get(v, v)


def _label_k64_method(variant_id: str) -> str:
    v = (variant_id or "").strip()
    mapping = {
        "uni_gru_within_topk64": "topk",
        "uni_gru_within_fps2k64": "fps2k",
        "uni_gru_transfer_subj1_topk64": "xfer",
        "uni_gru_random64_seed20260224": "rand",
    }
    return mapping.get(v, v)


def _label_grid_variant(variant_id: str) -> str:
    v = (variant_id or "").strip()
    mapping = {
        "uni_gru": "vec",
        "rowcol_uni_gru": "rowcol",
        "spatial2d_uni_gru_aug0": "grid",
        "spatial2d_uni_gru_aug1": "grid_aug",
    }
    return mapping.get(v, v)


def _label_group_p3ms(group_id: str) -> str:
    if group_id.startswith("subj") and "to" in group_id:
        core = group_id.replace("subj", "")
        if "to" in core:
            srcs, tgt = core.split("to", 1)
            return f"{srcs}>{tgt}"
    return group_id


def _label_group_kshot(group_id: str) -> str:
    return group_id.replace("subj", "", 1).replace("_k", "k")


def _label_table(table: str) -> str:
    mapping = {
        "spatial_all": "sp",
        "k64_all": "k64",
        "p3ms": "ms",
        "kshot": "ks",
        "to4": "to4",
    }
    return mapping.get(table, table)


def _emit_stats_row(
    rows: List[Dict[str, object]],
    table: str,
    group: str,
    variant: str,
    values: Sequence[float],
    *,
    pval: float | None,
    p_entries: List[Tuple[str, int, float]],
) -> None:
    n = len(values)
    m, s = _mean_std(values)
    ci_lo, ci_hi = _ci_t(m, s, n)
    tbl_label = _label_table(table)
    row = {
        "tbl": tbl_label,
        "grp": group,
        "var": variant,
        "mean_sd": f"{m:.2f}±{s:.2f}",
        "ci": f"[{ci_lo:.2f},{ci_hi:.2f}]",
        "p_adj": "",
    }
    rows.append(row)
    if pval is not None:
        p_entries.append((tbl_label, len(rows) - 1, pval))


def _apply_holm(rows: List[Dict[str, object]], p_entries: List[Tuple[str, int, float]]) -> None:
    by_table: Dict[str, List[Tuple[int, float]]] = {}
    for table, idx, p in p_entries:
        by_table.setdefault(table, []).append((idx, p))
    for table, items in by_table.items():
        pvals = [p for _, p in items]
        adj = _holm_adjust(pvals)
        for (idx, _), p_adj in zip(items, adj):
            rows[idx]["p_adj"] = f"{p_adj:.2f}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Export compact statistics table for paperjson.")
    ap.add_argument(
        "--msx_metrics_csv",
        type=Path,
        default=Path("sweeps/msx20260224/results/msx_all_metrics.csv"),
        help="Aggregated msx metrics CSV (missing=0).",
    )
    ap.add_argument(
        "--uc_patchpool_metrics_csv",
        type=Path,
        default=Path("sweeps/uc20260226/results/uc_spatial2d_patchpool_metrics.csv"),
        help="Aggregated patchpool metrics CSV (missing=0).",
    )
    ap.add_argument(
        "--uc_to4_metrics_csv",
        type=Path,
        default=Path("sweeps/uc20260226/results/uc_to4_metrics.csv"),
        help="Aggregated to4 metrics CSV (missing=0).",
    )
    ap.add_argument(
        "--out_csv",
        type=Path,
        default=Path("results/paper_layout_2026-03-03/table_stats_compact.csv"),
        help="Output CSV path.",
    )
    args = ap.parse_args()

    repo_root = _find_repo_root()
    msx_csv = args.msx_metrics_csv if args.msx_metrics_csv.is_absolute() else (repo_root / args.msx_metrics_csv)
    patch_csv = (
        args.uc_patchpool_metrics_csv
        if args.uc_patchpool_metrics_csv.is_absolute()
        else (repo_root / args.uc_patchpool_metrics_csv)
    )
    to4_csv = args.uc_to4_metrics_csv if args.uc_to4_metrics_csv.is_absolute() else (repo_root / args.uc_to4_metrics_csv)
    out_csv = args.out_csv if args.out_csv.is_absolute() else (repo_root / args.out_csv)

    if not msx_csv.exists():
        raise SystemExit(f"missing required input: {msx_csv}")
    if not patch_csv.exists():
        raise SystemExit(f"missing required input: {patch_csv}")
    if not to4_csv.exists():
        raise SystemExit(f"missing required input: {to4_csv}")

    msx_rows = _read_csv_rows(msx_csv)
    patch_rows = _read_csv_rows(patch_csv)
    to4_rows = _read_csv_rows(to4_csv)

    if len(msx_rows) != 652:
        raise SystemExit(f"msx completeness gate: expected 652 rows but got {len(msx_rows)}")
    if len(patch_rows) != 104:
        raise SystemExit(f"patchpool completeness gate: expected 104 rows but got {len(patch_rows)}")
    if len(to4_rows) != 24:
        raise SystemExit(f"to4 completeness gate: expected 24 rows but got {len(to4_rows)}")

    _require_columns(
        msx_rows,
        [
            "protocol",
            "split_id",
            "model_family",
            "enable_spatial_aug",
            "subset_method",
            "greedy_test_cer",
            "stream_rtf",
            "lex_all_cer",
            "note",
        ],
        context="msx_metrics_csv",
    )
    _require_columns(
        patch_rows,
        [
            "protocol",
            "split_id",
            "model_family",
            "enable_spatial_aug",
            "greedy_test_cer",
            "stream_rtf",
            "lex_all_cer",
            "note",
        ],
        context="uc_patchpool_metrics_csv",
    )
    _require_columns(
        to4_rows,
        ["protocol", "split_id", "model_family", "greedy_test_cer", "stream_rtf", "lex_all_cer", "note"],
        context="uc_to4_metrics_csv",
    )

    # Partition msx rows by note
    by_note: Dict[str, List[Dict[str, str]]] = {}
    for r in msx_rows:
        by_note.setdefault((r.get("note") or "").strip(), []).append(r)

    baseline_rows = by_note.get("baseline:multi_subj", [])
    spatial_k124_rows = by_note.get("msx:spatial_k124", [])
    k64_rows = by_note.get("msx:k64_uni_gru", [])
    p3ms_rows = by_note.get("msx:p3ms", [])
    kshot_rows = by_note.get("msx:kshot", [])

    gates = [
        ("baseline:multi_subj", 52, baseline_rows),
        ("msx:spatial_k124", 156, spatial_k124_rows),
        ("msx:k64_uni_gru", 208, k64_rows),
        ("msx:p3ms", 48, p3ms_rows),
        ("msx:kshot", 32, kshot_rows),
    ]
    for note, expected, subset in gates:
        if len(subset) != expected:
            raise SystemExit(f"note rows gate: {note}: expected {expected} rows but got {len(subset)}")

    rows: List[Dict[str, object]] = []
    p_entries: List[Tuple[str, str, int, float]] = []

    # --- spatial_all ---
    spatial_all = list(baseline_rows) + list(spatial_k124_rows) + list(patch_rows)
    spatial_variants = [
        "uni_gru",
        "rowcol_uni_gru",
        "spatial2d_uni_gru_aug0",
        "spatial2d_uni_gru_aug1",
        "spatial2d_patchpool_uni_gru_aug0",
        "spatial2d_patchpool_uni_gru_aug1",
    ]
    for protocol in ["P1", "P2", "P3"]:
        metric_key = "greedy_test_cer"
        base_groups = _group_seed_values(spatial_all, protocol=protocol, variant="uni_gru", metric_key=metric_key)
        base_means = {gid: float(mean(vals)) for gid, vals in base_groups.items()}
        base_vals = [base_means[gid] for gid in sorted(base_means.keys())]
        for variant in spatial_variants:
            groups = _group_seed_values(spatial_all, protocol=protocol, variant=variant, metric_key=metric_key)
            group_means = {gid: float(mean(vals)) for gid, vals in groups.items()}
            if set(group_means.keys()) != set(base_means.keys()):
                raise SystemExit(f"Group mismatch for protocol={protocol} variant={variant}")
            vals = [group_means[gid] for gid in sorted(group_means.keys())]
            pval = None
            if variant != "uni_gru":
                pval = _paired_t_p(vals, base_vals)
            _emit_stats_row(
                rows,
                "spatial_all",
                protocol,
                _label_spatial_variant(variant),
                vals,
                pval=pval,
                p_entries=p_entries,
            )

    # --- k64_all ---
    k64_variants = [
        "uni_gru_within_topk64",
        "uni_gru_within_fps2k64",
        "uni_gru_transfer_subj1_topk64",
        "uni_gru_random64_seed20260224",
    ]
    for protocol in ["P1", "P2", "P3"]:
        metric_key = "greedy_test_cer"
        base_groups = _group_seed_values(k64_rows, protocol=protocol, variant="uni_gru_within_topk64", metric_key=metric_key)
        base_means = {gid: float(mean(vals)) for gid, vals in base_groups.items()}
        base_vals = [base_means[gid] for gid in sorted(base_means.keys())]
        for variant in k64_variants:
            groups = _group_seed_values(k64_rows, protocol=protocol, variant=variant, metric_key=metric_key)
            group_means = {gid: float(mean(vals)) for gid, vals in groups.items()}
            if set(group_means.keys()) != set(base_means.keys()):
                raise SystemExit(f"Group mismatch for protocol={protocol} variant={variant}")
            vals = [group_means[gid] for gid in sorted(group_means.keys())]
            pval = None
            if variant != "uni_gru_within_topk64":
                pval = _paired_t_p(vals, base_vals)
            _emit_stats_row(
                rows,
                "k64_all",
                protocol,
                _label_k64_method(variant),
                vals,
                pval=pval,
                p_entries=p_entries,
            )

    # --- p3ms ---
    p3ms_variants = ["uni_gru", "rowcol_uni_gru", "spatial2d_uni_gru_aug0", "spatial2d_uni_gru_aug1"]
    metric_key = "greedy_test_cer"
    base_groups = _group_seed_values(p3ms_rows, protocol="P3MS", variant="uni_gru", metric_key=metric_key)
    for group_id in sorted(base_groups.keys()):
        base_vals = base_groups[group_id]
        for variant in p3ms_variants:
            groups = _group_seed_values(p3ms_rows, protocol="P3MS", variant=variant, metric_key=metric_key)
            if group_id not in groups:
                raise SystemExit(f"Missing group {group_id} for variant {variant} in P3MS")
            vals = groups[group_id]
            pval = None
            if variant != "uni_gru":
                pval = _paired_t_p(vals, base_vals)
            _emit_stats_row(
                rows,
                "p3ms",
                _label_group_p3ms(group_id),
                _label_grid_variant(variant),
                vals,
                pval=pval,
                p_entries=p_entries,
            )

    # --- kshot ---
    kshot_variants = ["uni_gru", "rowcol_uni_gru", "spatial2d_uni_gru_aug0", "spatial2d_uni_gru_aug1"]
    metric_key = "greedy_test_cer"
    base_groups = _group_seed_values(kshot_rows, protocol="P2K", variant="uni_gru", metric_key=metric_key)
    for group_id in sorted(base_groups.keys()):
        base_vals = base_groups[group_id]
        for variant in kshot_variants:
            groups = _group_seed_values(kshot_rows, protocol="P2K", variant=variant, metric_key=metric_key)
            if group_id not in groups:
                raise SystemExit(f"Missing group {group_id} for variant {variant} in P2K")
            vals = groups[group_id]
            pval = None
            if variant != "uni_gru":
                pval = _paired_t_p(vals, base_vals)
            _emit_stats_row(
                rows,
                "kshot",
                _label_group_kshot(group_id),
                _label_grid_variant(variant),
                vals,
                pval=pval,
                p_entries=p_entries,
            )

    # --- to4 generalization ---
    for protocol in ["P3", "P3MS"]:
        metric_key = "greedy_test_cer"
        groups = _group_seed_values(to4_rows, protocol=protocol, variant="uni_gru", metric_key=metric_key)
        for gid in sorted(groups.keys()):
            proto_label = "P3" if protocol == "P3" else "MS"
            _emit_stats_row(
                rows,
                "to4",
                f"{proto_label} {_label_group_p3ms(gid)}",
                "vec",
                groups[gid],
                pval=None,
                p_entries=p_entries,
            )

    _apply_holm(rows, p_entries)

    # Stable ordering
    table_order = ["sp", "k64", "ms", "ks", "to4"]
    variant_order = {
        "sp": ["vec", "rowcol", "grid", "grid_aug", "patch", "patch_aug"],
        "k64": ["topk", "fps2k", "xfer", "rand"],
        "ms": ["vec", "rowcol", "grid", "grid_aug"],
        "ks": ["vec", "rowcol", "grid", "grid_aug"],
        "to4": ["vec"],
    }
    group_order = {
        "sp": ["P1", "P2", "P3"],
        "k64": ["P1", "P2", "P3"],
        "ms": ["23>1", "13>2", "12>3"],
        "ks": ["3k1", "3k2"],
        "to4": [
            "P3 1>4",
            "P3 2>4",
            "P3 3>4",
            "MS 12>4",
            "MS 13>4",
            "MS 23>4",
        ],
    }
    def _sort_key(r: Mapping[str, object]) -> Tuple[int, int, int]:
        t = str(r.get("tbl", ""))
        g = str(r.get("grp", ""))
        v = str(r.get("var", ""))
        return (
            table_order.index(t) if t in table_order else 99,
            group_order.get(t, []).index(g) if g in group_order.get(t, []) else 99,
            variant_order.get(t, []).index(v) if v in variant_order.get(t, []) else 99,
        )

    rows_sorted = sorted(rows, key=_sort_key)

    _write_csv(
        out_csv,
        rows_sorted,
        fieldnames=["tbl", "grp", "var", "mean_sd", "ci", "p_adj"],
    )


if __name__ == "__main__":
    main()
