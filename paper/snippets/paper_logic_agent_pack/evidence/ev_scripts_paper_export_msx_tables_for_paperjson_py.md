# ev_scripts_paper_export_msx_tables_for_paperjson_py

- kind: `data`
- path: `scripts/paper/export_msx_tables_for_paperjson.py`
- sha256: `2100f045c5b121e7167cbb5cb59136bc2e6d61f8b64b2663f8fc317e4d801e84`
- size_bytes: 20650
- root_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- abs_path_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/scripts/paper/export_msx_tables_for_paperjson.py`

## Excerpt

```text
#!/usr/bin/env python3
"""Export compact paper-ready CSV tables from msx20260224 metrics.

This script is evidence-only:
- Input is the aggregated metrics CSV produced by scripts/rebuttal/gc_collect_metrics.py.
- Output tables are deterministic summaries (no learning, no randomness).

Outputs (under --out_dir):
- table_main.csv
- table_spatial_k124.csv
- table_k64_methods.csv
- table_spatial_k64.csv
- table_p3ms.csv
- table_kshot.csv

Notes
- The input msx_all_metrics.csv is expected to contain *all* runs (missing=0).
- Row-count and schema gates are fail-fast to prevent silently truncated papers.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from statistics import mean
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


def _fmt_fixed(x: float, ndigits: int) -> str:
    return f"{float(x):.{int(ndigits)}f}"


def _spatial_variant_label(variant_id: str) -> str:
    v = (variant_id or "").strip()
    if v.startswith("uni_gru"):
        return "vector"
    if v.startswith("rowcol_uni_gru"):
        return "rowcol"
    if v.startswith("spatial2d_uni_gru_aug0"):
        return "spatial2d"
    if v.startswith("spatial2d_uni_gru_aug1"):
        return "spatial2d_aug"
    return v


def _k64_method_label(variant_id: str) -> str:
    v = (variant_id or "").strip()
    m = {
        "uni_gru_within_topk64": "within_topk",
        "uni_gru_within_fps2k64": "within_fps2k",
        "uni_gru_transfer_subj1_topk64": "transfer_topk",
        "uni_gru_random64_seed20260224": "random",
    }
    return m.get(v, v)


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


def _require_columns(rows: Sequence[Mapping[str, str]], keys: Sequence[str], *, context: str) -> None:
    if not rows:
        raise SystemExit(f"{context}: empty rows")
    missing = [k for k in keys if k not in rows[0]]
    if missing:
        raise SystemExit(f"{context}: missing columns: {missing}")


def _variant_id(row: Mapping[str, str]) -> str:
    mf = (row.get("model_family") or "").strip()
    if not mf:
        raise ValueError("Missing model_family")
    if mf == "spatial2d_uni_gru":
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
    """Return (group_id, seed, extra) for deterministic aggregation."""
    s = (split_id or "").strip()

    def _must_int(x: str) -> int:
        return int(x)

    if protocol in {"P1", "P2"}:
        # subj{1..4}_seed{0..3}
        if not s.startswith("subj") or "_seed" not in s:
            raise ValueError(f"Unexpected split_id for {protocol}: {s}")
        subj_part, seed_part = s.split("_seed", 1)
        subj = _must_int(subj_part.replace("subj", ""))
        seed = _must_int(seed_part)
        return f"subj{subj}", seed, ""

    if protocol == "P3":
        # subj{src}to{tgt}_seed{0..3}
        if not s.startswith("subj") or "to" not in s or "_seed" not in s:
            raise ValueError(f"Unexpected split_id for P3: {s}")
        core, seed_part = s.split("_seed", 1)
        seed = _must_int(seed_part)
        src_tgt = core.replace("subj", "")
        src, tgt = src_tgt.split("to", 1)
        return f"subj{_must_int(src)}to{_must_int(tgt)}", seed, ""

    if protocol == "P3MS":
        # subj{srca}{srcb}to{tgt}_seed{0..3}
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
        # subj{N}_seed{0..3}_k{1|2}
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


def _summarize_over_groups(rows: Sequence[Mapping[str, str]], *, protocol: str, variant: str) -> Dict[str, object]:
    groups = _group_seed_matrix(rows, protocol=protocol, variant=variant)

    def _group_seed_vals(key: str, gid: str) -> List[float]:
        return [_to_float(groups[gid][s][key], context=f"{protocol}/{variant}/{gid}/seed{s}/{key}") for s in [0, 1, 2, 3]]

    # group means across seeds
    group_means: Dict[str, Dict[str, float]] = {}
    for gid in sorted(groups.keys()):
        group_means[gid] = {
            "greedy_test_cer": float(mean(_group_seed_vals("greedy_test_cer", gid))),
            "stream_rtf": float(mean(_group_seed_vals("stream_rtf", gid))),
            "lex_train_cer": float(mean(_group_seed_vals("lex_train_cer", gid))),
            "lex_all_cer": float(mean(_group_seed_vals("lex_all_cer", gid))),
        }

    def _metric_across_groups(metric: str) -> Tuple[float, float]:
        xs = [group_means[gid][metric] for gid in sorted(group_means.keys())]
        return _mean_std(xs)

    cer_m, cer_s = _metric_across_groups("greedy_test_cer")
    rtf_m, rtf_s = _metric_across_groups("stream_rtf")
    ltr_m, ltr_s = _metric_across_groups("lex_train_cer")
    lal_m, lal_s = _metric_across_groups("lex_all_cer")

    return {
        "protocol": protocol,
        "variant": variant,
        "n_groups": len(group_means),
        "greedy_cer_mean": cer_m,
        "greedy_cer_std": cer_s,
        "rtf_mean": rtf_m,
        "rtf_std": rtf_s,
        "lex_train_cer_mean": ltr_m,
        "lex_train_cer_std": ltr_s,
        "lex_all_cer_mean": lal_m,
        "lex_all_cer_std": lal_s,
    }


def _summarize_over_seeds(rows: Sequence[Mapping[str, str]], *, protocol: str, variant: str, group_id_prefix: str) -> Dict[str, object]:
    groups = _group_seed_matrix(rows, protocol=protocol, variant=variant)
    # Select exactly one group for deterministic reporting.
    keys = sorted([g for g in groups.keys() if g.startswith(group_id_prefix)])
    if len(keys) != 1:
        raise SystemExit(f"Expected exactly one group starting with {group_id_prefix!r} for protocol={protocol} variant={variant}, got: {keys}")
    gid = keys[0]

    def _seed_vals(key: str) -> List[float]:
        return [_to_float(groups[gid][s][key], context=f"{protocol}/{variant}/{gid}/seed{s}/{key}") for s in [0, 1, 2, 3]]

    cer_m, cer_s = _mean_std(_seed_vals("greedy_test_cer"))
    rtf_m, rtf_s = _mean_std(_seed_vals("stream_rtf"))
    ltr_m, ltr_s = _mean_std(_seed_vals("lex_train_cer"))
    lal_m, lal_s = _mean_std(_seed_vals("lex_all_cer"))

    return {
        "protocol": protocol,
        "group": gid,
        "variant": variant,
        "n_seeds": 4,
        "greedy_cer_mean": cer_m,
        "greedy_cer_std": cer_s,
        "rtf_mean": rtf_m,
        "rtf_std": rtf_s,
        "lex_train_cer_mean": ltr_m,
        "lex_train_cer_std": ltr_s,
        "lex_all_cer_mean": lal_m,
        "lex_all_cer_std": lal_s,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Export compact msx20260224 tables for paperjson.")
    ap.add_argument(
        "--metrics_csv",
        type=Path,
        default=Path("sweeps/msx20260224/results/msx_all_metrics.csv"),
        help="Aggregated metrics CSV (missing=0).",
    )
    ap.add_argument(
        "--out_dir",
        type=Path,
        default=Path("results/msx20260224/paper_tables"),
        help="Output directory for compact CSV tables.",
    )
    args = ap.parse_args()

    repo_root = _find_repo_root()
    metrics_csv = args.metrics_csv if args.metrics_csv.is_absolute() else (repo_root / args.metrics_csv)
    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)

    if not metrics_csv.exists():
        raise SystemExit(f"metrics_csv not found: {metrics_csv}")

    rows = _read_csv_rows(metrics_csv)
    if not rows:
        raise SystemExit(f"No rows in metrics_csv: {metrics_csv}")

    # Expected total = baseline(52) + spatial_k124(156) + k64_uni_gru(208) + spatial_k64(156) + p3ms(48) + kshot(32) = 652
    if len(rows) != 652:
        raise SystemExit(f"metrics_csv completeness gate: expected 652 rows but got {len(rows)}")

    _require_columns(
        rows,
        ["protocol", "split_id", "model_family", "greedy_test_cer", "stream_rtf", "lex_train_cer", "lex_all_cer", "note"],
        context="metrics_csv",
    )

    # Partition by note
    by_note: Dict[str, List[Dict[str, str]]] = {}
    for r in rows:
        by_note.setdefault((r.get("note") or "").strip(), []).append(r)

    baseline_rows = by_note.get("baseline:multi_subj", [])
    spatial_k124_rows = by_note.get("msx:spatial_k124", [])
    k64_rows = by_note.get("msx:k64_uni_gru", [])
    spatial_k64_rows = by_note.get("msx:spatial_k64_within_topk", [])
    p3ms_rows = by_note.get("msx:p3ms", [])
    kshot_rows = by_note.get("msx:kshot", [])

    gates = [
        ("baseline:multi_subj", 52, baseline_rows),
        ("msx:spatial_k124", 156, spatial_k124_rows),
        ("msx:k64_uni_gru", 208, k64_rows),
        ("msx:spatial_k64_within_topk", 156, spatial_k64_rows),
        ("msx:p3ms", 48, p3ms_rows),
        ("msx:kshot", 32, kshot_rows),
    ]
    for note, expected, subset in gates:
        if len(subset) != expected:
            raise SystemExit(f"note rows gate: {note}: expected {expected} rows but got {len(subset)}")

    protocols_main = ["P1", "P2", "P3"]

    # --- table_main.csv (baseline recap) ---
    main_rows: List[Dict[str, object]] = []
    for prot in protocols_main:
        s = _summarize_over_groups(baseline_rows, protocol=prot, variant="uni_gru")
        main_rows.append(
            {
                "protocol": s["protocol"],
                "variant": _spatial_variant_label(str(s["variant"])),
                "n": s["n_groups"],
                "cer_m": _fmt_fixed(float(s["greedy_cer_mean"]), 4),
                "cer_s": _fmt_fixed(float(s["greedy_cer_std"]), 4),
                "lex_all_m": _fmt_fixed(float(s["lex_all_cer_mean"]), 4),
                "lex_all_s": _fmt_fixed(float(s["lex_all_cer_std"]), 4),
                "rtf_m": _fmt_fixed(float(s["rtf_mean"]), 6),
                "rtf_s": _fmt_fixed(float(s["rtf_std"]), 6),
                "variant_id": s["variant"],
            }
        )
    _write_csv(
        out_dir / "table_main.csv",
        main_rows,
        fieldnames=[
            "protocol",
            "variant",
            "n",
            "cer_m",
            "cer_s",
            "lex_all_m",
            "lex_all_s",
            "rtf_m",
            "rtf_s",
            "variant_id",
        ],
    )

    # --- table_spatial_k124.csv (baseline + spatial front-ends at full channels) ---
    spatial_variants_k124 = [
        "uni_gru",
        "rowcol_uni_gru",
        "spatial2d_uni_gru_aug0",
        "spatial2d_uni_gru_aug1",
    ]
    spatial_k124_all = list(baseline_rows) + list(spatial_k124_rows)
    spatial_k124_out: List[Dict[str, object]] = []
    for prot in protocols_main:
        for v in spatial_variants_k124:
            s = _summarize_over_groups(spatial_k124_all, protocol=prot, variant=v)
            spatial_k124_out.append(
                {
                    "protocol": s["protocol"],
                    "variant": _spatial_variant_label(str(s["variant"])),
                    "n": s["n_groups"],
                    "cer_m": _fmt_fixed(float(s["greedy_cer_mean"]), 4),
                    "cer_s": _fmt_fixed(float(s["greedy_cer_std"]), 4),
                    "rtf_m": _fmt_fixed(float(s["rtf_mean"]), 6),
                    "rtf_s": _fmt_fixed(float(s["rtf_std"]), 6),
                    "variant_id": s["variant"],
                }
            )
    _write_csv(
        out_dir / "table_spatial_k124.csv",
        spatial_k124_out,
        fieldnames=[
            "protocol",
            "variant",
            "n",
            "cer_m",
            "cer_s",
            "rtf_m",
            "rtf_s",
            "variant_id",
        ],
    )

    # --- table_k64_methods.csv (uni_gru @ K=64 methods) ---
    k64_methods = [
        "uni_gru_within_topk64",
        "uni_gru_within_fps2k64",
        "uni_gru_transfer_subj1_topk64",
        "uni_gru_random64_seed20260224",
    ]
    k64_out: List[Dict[str, object]] = []
    for prot in protocols_main:
        for v in k64_methods:
            s = _summarize_over_groups(k64_rows, protocol=prot, variant=v)
            k64_out.append(
                {
                    "protocol": s["protocol"],
                    "method": _k64_method_label(str(s["variant"])),
                    "n": s["n_groups"],
                    "cer_m": _fmt_fixed(float(s["greedy_cer_mean"]), 4),
                    "cer_s": _fmt_fixed(float(s["greedy_cer_std"]), 4),
                    "rtf_m": _fmt_fixed(float(s["rtf_mean"]), 6),
                    "rtf_s": _fmt_fixed(float(s["rtf_std"]), 6),
                    "variant_id": s["variant"],
                }
            )
    _write_csv(
        out_dir / "table_k64_methods.csv",
        k64_out,
        fieldnames=[
            "protocol",
            "method",
            "n",
            "cer_m",
            "cer_s",
            "rtf_m",
            "rtf_s",
            "variant_id",
        ],
    )

    # --- table_spatial_k64.csv (within_topk64 subset + spatial variants) ---
    spatial_variants_k64 = [
        "uni_gru_within_topk64",
        "rowcol_uni_gru_within_topk64",
        "spatial2d_uni_gru_aug0_within_topk64",
        "spatial2d_uni_gru_aug1_within_topk64",
    ]
    spatial_k64_all = list(spatial_k64_rows) + [r for r in k64_rows if _variant_id(r) == "uni_gru_within_topk64"]
    if len(spatial_k64_all) != 156 + 52:
        # 156 spatial rows + 52 uni_gru within_topk64 rows (P1/P2/P3, 52 splits)
        raise SystemExit(f"Unexpected spatial_k64_all size: {len(spatial_k64_all)}")

    spatial_k64_out: List[Dict[str, object]] = []
    for prot in protocols_main:
        for v in spatial_variants_k64:
            s = _summarize_over_groups(spatial_k64_all, protocol=prot, variant=v)
            spatial_k64_out.append(
                {
                    "protocol": s["protocol"],
                    "variant": _spatial_variant_label(str(s["variant"])),
                    "n": s["n_groups"],
                    "cer_m": _fmt_fixed(float(s["greedy_cer_mean"]), 4),
                    "cer_s": _fmt_fixed(float(s["greedy_cer_std"]), 4),
                    "rtf_m": _fmt_fixed(float(s["rtf_mean"]), 6),
                    "rtf_s": _fmt_fixed(float(s["rtf_std"]), 6),
                    "variant_id": s["variant"],
                }
            )
    _write_csv(
        out_dir / "table_spatial_k64.csv",
        spatial_k64_out,
        fieldnames=[
            "protocol",
            "variant",
            "n",
            "cer_m",
            "cer_s",
            "rtf_m",
            "rtf_s",
            "variant_id",
        ],
    )

    # --- table_p3ms.csv (direction-wise seed stats) ---
    p3ms_variants = [
        "uni_gru",
        "rowcol_uni_gru",
        "spatial2d_uni_gru_aug0",
        "spatial2d_uni_gru_aug1",
    ]
    p3ms_dirs = ["subj23to1", "subj13to2", "subj12to3"]
    p3ms_out: List[Dict[str, object]] = []
    for d in p3ms_dirs:
        for v in p3ms_variants:
            s = _summarize_over_seeds(p3ms_rows, protocol="P3MS", variant=v, group_id_prefix=d)
            p3ms_out.append(
                {
                    "protocol": s["protocol"],
                    "group": s["group"],
                    "variant": _spatial_variant_label(str(s["variant"])),
                    "n": s["n_seeds"],
                    "cer_m": _fmt_fixed(float(s["greedy_cer_mean"]), 4),
                    "cer_s": _fmt_fixed(float(s["greedy_cer_std"]), 4),
                    "rtf_m": _fmt_fixed(float(s["rtf_mean"]), 6),
                    "rtf_s": _fmt_fixed(float(s["rtf_std"]), 6),
                    "variant_id": s["variant"],
                }
            )
    _write_csv(
        out_dir / "table_p3ms.csv",
        p3ms_out,
        fieldnames=[
            "protocol",
            "group",
            "variant",
            "n",
            "cer_m",
            "cer_s",
            "rtf_m",
            "rtf_s",
            "variant_id",
        ],
    )

    # --- table_kshot.csv (k-wise seed stats for subj3) ---
    kshot_variants = p3ms_variants
    kshot_out: List[Dict[str, object]] = []
    for k in (1, 2):
        prefix = f"subj3_k{k}"
        for v in kshot_variants:
            s = _summarize_over_seeds(kshot_rows, protocol="P2K", variant=v, group_id_prefix=prefix)
            kshot_out.append(
                {
                    "protocol": s["protocol"],
                    "group": s["group"],
                    "variant": _spatial_variant_label(str(s["variant"])),
                    "n": s["n_seeds"],
                    "cer_m": _fmt_fixed(float(s["greedy_cer_mean"]), 4),
                    "cer_s": _fmt_fixed(float(s["greedy_cer_std"]), 4),
                    "rtf_m": _fmt_fixed(float(s["rtf_mean"]), 6),
                    "rtf_s": _fmt_fixed(float(s["rtf_std"]), 6),
                    "variant_id": s["variant"],
                }
            )
    _write_csv(
        out_dir / "table_kshot.csv",
        kshot_out,
        fieldnames=[
            "protocol",
            "group",
            "variant",
            "n",
            "cer_m",
            "cer_s",
            "rtf_m",
            "rtf_s",
            "variant_id",
        ],
    )

    print(f"[OK] wrote tables under: {out_dir}")


if __name__ == "__main__":
    main()
```
