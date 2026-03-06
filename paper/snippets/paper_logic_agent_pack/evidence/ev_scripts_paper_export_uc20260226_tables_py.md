# ev_scripts_paper_export_uc20260226_tables_py

- kind: `data`
- path: `scripts/paper/export_uc20260226_tables.py`
- sha256: `936113afcbce65fbf7e4a2da7d66e8459d23e70188ad5f5db61492fdcbee0991`
- size_bytes: 18515
- root_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- abs_path_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/scripts/paper/export_uc20260226_tables.py`

## Excerpt

```text
#!/usr/bin/env python3
"""Export compact paper-ready CSV tables for the uc20260226 sprint.

This script is evidence-only:
- Inputs are aggregated metrics CSVs produced by scripts/rebuttal/gc_collect_metrics.py.
- Outputs are deterministic summaries (no learning, no randomness).

Outputs (under --out_dir):
- table_spatial_k124_with_patchpool.csv
- table_to4_generalization.csv

Gates
- Fails fast if required input files are missing or incomplete.
- Assumes msx20260224 metrics are frozen and complete (652 rows).
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from statistics import mean
from typing import Dict, List, Mapping, Sequence, Tuple


def _fmt_fixed(x: float, ndigits: int) -> str:
    return f"{float(x):.{int(ndigits)}f}"


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
    if v.startswith("spatial2d_patchpool_uni_gru_aug0"):
        return "patchpool"
    if v.startswith("spatial2d_patchpool_uni_gru_aug1"):
        return "patchpool_aug"
    return v


def _parse_group(protocol: str, split_id: str) -> Tuple[str, int]:
    """Return (group_id, seed) for deterministic aggregation."""
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
        return f"subj{subj}", seed

    if protocol == "P3":
        # subj{src}to{tgt}_seed{0..3}
        if not s.startswith("subj") or "to" not in s or "_seed" not in s:
            raise ValueError(f"Unexpected split_id for P3: {s}")
        core, seed_part = s.split("_seed", 1)
        seed = _must_int(seed_part)
        src_tgt = core.replace("subj", "")
        src, tgt = src_tgt.split("to", 1)
        return f"subj{_must_int(src)}to{_must_int(tgt)}", seed

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
        return f"subj{_must_int(srcs[0])}{_must_int(srcs[1])}to{_must_int(tgt)}", seed

    raise ValueError(f"Unsupported protocol for grouping: {protocol}")


def _group_seed_matrix(rows: Sequence[Mapping[str, str]], *, protocol: str, variant: str) -> Dict[str, Dict[int, Mapping[str, str]]]:
    sel = [r for r in rows if (r.get("protocol") or "").strip() == protocol and _variant_id(r) == variant]
    if not sel:
        raise SystemExit(f"Missing rows for protocol={protocol} variant={variant}")

    groups: Dict[str, Dict[int, Mapping[str, str]]] = {}
    for r in sel:
        gid, seed = _parse_group(protocol, (r.get("split_id") or "").strip())
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
            "lex_all_cer": float(mean(_group_seed_vals("lex_all_cer", gid))),
        }

    def _metric_across_groups(metric: str) -> Tuple[float, float]:
        xs = [group_means[gid][metric] for gid in sorted(group_means.keys())]
        return _mean_std(xs)

    cer_m, cer_s = _metric_across_groups("greedy_test_cer")
    rtf_m, rtf_s = _metric_across_groups("stream_rtf")
    lal_m, lal_s = _metric_across_groups("lex_all_cer")

    return {
        "protocol": protocol,
        "variant": variant,
        "n_groups": len(group_means),
        "greedy_cer_mean": cer_m,
        "greedy_cer_std": cer_s,
        "rtf_mean": rtf_m,
        "rtf_std": rtf_s,
        "lex_all_cer_mean": lal_m,
        "lex_all_cer_std": lal_s,
    }


def _summarize_direction_over_seeds(rows: Sequence[Mapping[str, str]], *, protocol: str, variant: str) -> Dict[str, Dict[str, float]]:
    groups = _group_seed_matrix(rows, protocol=protocol, variant=variant)
    out: Dict[str, Dict[str, float]] = {}
    for gid in sorted(groups.keys()):
        cer = [_to_float(groups[gid][s]["greedy_test_cer"], context=f"{protocol}/{variant}/{gid}/seed{s}/greedy_test_cer") for s in [0, 1, 2, 3]]
        rtf = [_to_float(groups[gid][s]["stream_rtf"], context=f"{protocol}/{variant}/{gid}/seed{s}/stream_rtf") for s in [0, 1, 2, 3]]
        lal = [_to_float(groups[gid][s]["lex_all_cer"], context=f"{protocol}/{variant}/{gid}/seed{s}/lex_all_cer") for s in [0, 1, 2, 3]]
        cer_m, cer_s = _mean_std(cer)
        rtf_m, rtf_s = _mean_std(rtf)
        lal_m, lal_s = _mean_std(lal)
        out[gid] = {
            "cer_m": float(cer_m),
            "cer_s": float(cer_s),
            "rtf_m": float(rtf_m),
            "rtf_s": float(rtf_s),
            "lex_all_m": float(lal_m),
            "lex_all_s": float(lal_s),
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Export compact uc20260226 tables for paperjson.")
    ap.add_argument(
        "--msx_metrics_csv",
        type=Path,
        default=Path("sweeps/msx20260224/results/msx_all_metrics.csv"),
        help="Frozen msx aggregated metrics CSV (652 rows, missing=0).",
    )
    ap.add_argument(
        "--uc_patchpool_metrics_csv",
        type=Path,
        default=Path("sweeps/uc20260226/results/uc_spatial2d_patchpool_metrics.csv"),
        help="Aggregated metrics for spatial2d_patchpool (104 rows, missing=0).",
    )
    ap.add_argument(
        "--uc_to4_metrics_csv",
        type=Path,
        default=Path("sweeps/uc20260226/results/uc_to4_metrics.csv"),
        help="Aggregated metrics for to4 vector runs (24 rows, missing=0).",
    )
    ap.add_argument(
        "--skip_patchpool_table",
        action="store_true",
        help="Skip writing table_spatial_k124_with_patchpool.csv (useful while patchpool runs are still in progress).",
    )
    ap.add_argument(
        "--skip_to4_table",
        action="store_true",
        help="Skip writing table_to4_generalization.csv.",
    )
    ap.add_argument(
        "--out_dir",
        type=Path,
        default=Path("results/uc20260226/paper_tables"),
        help="Output directory for compact CSV tables.",
    )
    args = ap.parse_args()

    repo_root = _find_repo_root()
    msx_metrics = args.msx_metrics_csv if args.msx_metrics_csv.is_absolute() else (repo_root / args.msx_metrics_csv)
    uc_to4_metrics = args.uc_to4_metrics_csv if args.uc_to4_metrics_csv.is_absolute() else (repo_root / args.uc_to4_metrics_csv)
    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)

    if not msx_metrics.exists():
        raise SystemExit(f"missing required input: {msx_metrics}")
    if not args.skip_to4_table and not uc_to4_metrics.exists():
        raise SystemExit(f"missing required input: {uc_to4_metrics}")

    uc_patchpool_metrics = None
    if not args.skip_patchpool_table:
        p = args.uc_patchpool_metrics_csv if args.uc_patchpool_metrics_csv.is_absolute() else (repo_root / args.uc_patchpool_metrics_csv)
        if not p.exists():
            raise SystemExit(f"missing required input: {p}")
        uc_patchpool_metrics = p

    msx_rows = _read_csv_rows(msx_metrics)
    if len(msx_rows) != 652:
        raise SystemExit(f"msx completeness gate: expected 652 rows but got {len(msx_rows)}")

    uc_patch_rows: List[Dict[str, str]] = []
    if uc_patchpool_metrics is not None:
        uc_patch_rows = _read_csv_rows(uc_patchpool_metrics)
        if len(uc_patch_rows) != 104:
            raise SystemExit(f"uc patchpool completeness gate: expected 104 rows but got {len(uc_patch_rows)}")

    uc_to4_rows: List[Dict[str, str]] = []
    if not args.skip_to4_table:
        uc_to4_rows = _read_csv_rows(uc_to4_metrics)
        if len(uc_to4_rows) != 24:
            raise SystemExit(f"uc to4 completeness gate: expected 24 rows but got {len(uc_to4_rows)}")

    _require_columns(
        msx_rows,
        ["protocol", "split_id", "model_family", "enable_spatial_aug", "greedy_test_cer", "stream_rtf", "lex_all_cer", "note"],
        context="msx_metrics_csv",
    )
    if uc_patch_rows:
        _require_columns(
            uc_patch_rows,
            ["protocol", "split_id", "model_family", "enable_spatial_aug", "greedy_test_cer", "stream_rtf", "lex_all_cer", "note"],
            context="uc_patchpool_metrics_csv",
        )
    if uc_to4_rows:
        _require_columns(
            uc_to4_rows,
            ["protocol", "split_id", "model_family", "greedy_test_cer", "stream_rtf", "lex_all_cer", "note"],
            context="uc_to4_metrics_csv",
        )

    if not args.skip_patchpool_table:
        # --- table_spatial_k124_with_patchpool.csv ---
        baseline_rows = [r for r in msx_rows if (r.get("note") or "").strip() == "baseline:multi_subj"]
        spatial_k124_rows = [r for r in msx_rows if (r.get("note") or "").strip() == "msx:spatial_k124"]
        patchpool_rows = list(uc_patch_rows)

        gates = [
            ("baseline:multi_subj", 52, baseline_rows),
            ("msx:spatial_k124", 156, spatial_k124_rows),
            ("uc:spatial2d_patchpool_k124", 104, patchpool_rows),
        ]
        for note, expected, subset in gates:
            if len(subset) != expected:
                raise SystemExit(f"row-count gate failed: {note}: expected {expected} but got {len(subset)}")

        spatial_all = list(baseline_rows) + list(spatial_k124_rows) + list(patchpool_rows)
        protocols_main = ["P1", "P2", "P3"]
        spatial_variants = [
            "uni_gru",
            "rowcol_uni_gru",
            "spatial2d_uni_gru_aug0",
            "spatial2d_uni_gru_aug1",
            "spatial2d_patchpool_uni_gru_aug0",
            "spatial2d_patchpool_uni_gru_aug1",
        ]

        spatial_out: List[Dict[str, object]] = []
        for prot in protocols_main:
            for v in spatial_variants:
                s = _summarize_over_groups(spatial_all, protocol=prot, variant=v)
                spatial_out.append(
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
            out_dir / "table_spatial_k124_with_patchpool.csv",
            spatial_out,
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

    if not args.skip_to4_table:
        # --- table_to4_generalization.csv ---
        to4_p3 = [r for r in uc_to4_rows if (r.get("protocol") or "").strip() == "P3"]
        to4_p3ms = [r for r in uc_to4_rows if (r.get("protocol") or "").strip() == "P3MS"]
        if len(to4_p3) != 12:
            raise SystemExit(f"to4 P3 row-count gate: expected 12 but got {len(to4_p3)}")
        if len(to4_p3ms) != 12:
            raise SystemExit(f"to4 P3MS row-count gate: expected 12 but got {len(to4_p3ms)}")

        # direction-wise summaries (over seeds)
        p3_dir = _summarize_direction_over_seeds(uc_to4_rows, protocol="P3", variant="uni_gru")
        p3ms_dir = _summarize_direction_over_seeds(uc_to4_rows, protocol="P3MS", variant="uni_gru")

        out_rows: List[Dict[str, object]] = []

        def _emit_dir_rows(protocol: str, dir_stats: Dict[str, Dict[str, float]]) -> None:
            for gid in sorted(dir_stats.keys()):
                s = dir_stats[gid]
                out_rows.append(
                    {
                        "protocol": protocol,
                        "level": "direction",
                        "group": gid,
                        "variant": "vector",
                        "n": 4,
                        "cer_m": _fmt_fixed(float(s["cer_m"]), 4),
                        "cer_s": _fmt_fixed(float(s["cer_s"]), 4),
                        "lex_all_m": _fmt_fixed(float(s["lex_all_m"]), 4),
                        "lex_all_s": _fmt_fixed(float(s["lex_all_s"]), 4),
                        "rtf_m": _fmt_fixed(float(s["rtf_m"]), 6),
                        "rtf_s": _fmt_fixed(float(s["rtf_s"]), 6),
                    }
                )

        def _emit_agg_row(protocol: str, dir_stats: Dict[str, Dict[str, float]]) -> None:
            cer_m, cer_s = _mean_std([dir_stats[k]["cer_m"] for k in sorted(dir_stats.keys())])
            rtf_m, rtf_s = _mean_std([dir_stats[k]["rtf_m"] for k in sorted(dir_stats.keys())])
            lal_m, lal_s = _mean_std([dir_stats[k]["lex_all_m"] for k in sorted(dir_stats.keys())])
            out_rows.append(
                {
                    "protocol": protocol,
                    "level": "across_directions",
                    "group": "ALL_to4",
                    "variant": "vector",
                    "n": len(dir_stats),
                    "cer_m": _fmt_fixed(float(cer_m), 4),
                    "cer_s": _fmt_fixed(float(cer_s), 4),
                    "lex_all_m": _fmt_fixed(float(lal_m), 4),
                    "lex_all_s": _fmt_fixed(float(lal_s), 4),
                    "rtf_m": _fmt_fixed(float(rtf_m), 6),
                    "rtf_s": _fmt_fixed(float(rtf_s), 6),
                }
            )

        _emit_dir_rows("P3", p3_dir)
        _emit_agg_row("P3", p3_dir)
        _emit_dir_rows("P3MS", p3ms_dir)
        _emit_agg_row("P3MS", p3ms_dir)

        _write_csv(
            out_dir / "table_to4_generalization.csv",
            out_rows,
            fieldnames=[
                "protocol",
                "level",
                "group",
                "variant",
                "n",
                "cer_m",
                "cer_s",
                "lex_all_m",
                "lex_all_s",
                "rtf_m",
                "rtf_s",
            ],
        )

    print(f"[OK] wrote uc tables under: {out_dir}")


if __name__ == "__main__":
    main()
```
