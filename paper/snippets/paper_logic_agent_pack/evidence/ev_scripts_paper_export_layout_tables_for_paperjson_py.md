# ev_scripts_paper_export_layout_tables_for_paperjson_py

- kind: `data`
- path: `scripts/paper/export_layout_tables_for_paperjson.py`
- sha256: `0ba9e5c602e58596ac80f759c6b59baa1402a36433e31ebbf4012f3f77c23e8e`
- size_bytes: 16947
- root_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo`
- abs_path_guess: `/Users/naokkimu/lyworks_ssd/epgspeller_local_workspace/paperlogic_full_repo/scripts/paper/export_layout_tables_for_paperjson.py`

## Excerpt

```text
#!/usr/bin/env python3
"""Export compact layout tables for paper.json.

Inputs are evidence-only artifacts produced by prior runs. This script
creates smaller tables tuned for manuscript layout without re-running
experiments.

Outputs (under --out_dir):
- table_dataset_summary.csv
- table_training_config.csv
- table_spatial_p1.csv
- table_spatial_p2.csv
- table_spatial_p3.csv
- table_spatial_all.csv
- table_k64_p1p2.csv
- table_k64_p3.csv
- table_k64_all.csv
- table_to4_compact.csv
- table_p3ms_compact.csv
- table_kshot_compact.csv
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise SystemExit("Could not locate repo root (expected scripts/ and src/)")


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fieldnames))
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def _fmt_pm(mean_str: str, std_str: str, ndigits: int) -> str:
    m = float(mean_str)
    s = float(std_str)
    return f"{m:.{ndigits}f}±{s:.{ndigits}f}"


def _require_columns(rows: Sequence[Mapping[str, str]], keys: Sequence[str], *, context: str) -> None:
    if not rows:
        raise SystemExit(f"{context}: empty rows")
    missing = [k for k in keys if k not in rows[0]]
    if missing:
        raise SystemExit(f"{context}: missing columns: {missing}")


def _order_rows(rows: Iterable[Mapping[str, str]], *, key_field: str, order: Sequence[str]) -> List[Mapping[str, str]]:
    bucket = {r[key_field]: r for r in rows}
    out = []
    for key in order:
        if key not in bucket:
            raise SystemExit(f"Missing expected {key_field}={key}")
        out.append(bucket[key])
    return out


def _write_dataset_summary(out_dir: Path, root: Path) -> None:
    path = root / "results/dataset_audit_silentspeller_2026-02-24/dataset_summary.csv"
    rows = _read_csv(path)
    _require_columns(
        rows,
        [
            "dataset_id",
            "view",
            "n_samples",
            "n_unique_labels",
            "T_median",
            "total_frames",
            "overall_mean_contact",
            "all_zero_samples",
            "exclude_indices_n",
        ],
        context="dataset_summary.csv",
    )
    order = ["p1_2328_old", "thad_2328_old", "john_2328", "su_1167_old"]
    id_map = {
        "p1_2328_old": "p1",
        "thad_2328_old": "p2",
        "john_2328": "p3",
        "su_1167_old": "p4",
    }
    raw_rows = [r for r in rows if r.get("view") == "raw" and r.get("dataset_id") in order]
    ordered = _order_rows(raw_rows, key_field="dataset_id", order=order)
    out_rows = []
    for r in ordered:
        tmed = float(r["T_median"])
        out_rows.append(
            {
                "id": id_map.get(r["dataset_id"], r["dataset_id"]),
                "N": r["n_samples"],
                "V": r["n_unique_labels"],
                "Tmed": f"{tmed:.0f}",
                "contact": f"{float(r['overall_mean_contact']):.2f}",
                "zero": r["all_zero_samples"],
            }
        )
    _write_csv(
        out_dir / "table_dataset_summary.csv",
        out_rows,
        ["id", "N", "V", "Tmed", "contact", "zero"],
    )


def _write_training_config(out_dir: Path, root: Path) -> None:
    metrics_path = root / "sweeps/msx20260224/results/msx_all_metrics.csv"
    rows = _read_csv(metrics_path)
    _require_columns(
        rows,
        [
            "n_components",
            "downsample_factor",
            "electrode_regions",
            "apply_ts2vec",
            "n_units",
            "n_layers",
            "stride_len",
            "kernel_len",
            "input_proj_dim",
            "specaug_on",
            "white_noise_sd",
            "constant_offset_sd",
            "gaussian_smooth_width",
            "frame_ms",
            "n_batch",
            "train_seed",
        ],
        context="msx_all_metrics.csv",
    )
    order = [
        "n_units",
        "n_layers",
        "stride_len",
        "kernel_len",
        "input_proj_dim",
        "specaug_on",
        "white_noise_sd",
        "constant_offset_sd",
        "gaussian_smooth_width",
        "frame_ms",
        "n_batch",
        "train_seed",
        "n_components",
        "downsample_factor",
        "electrode_regions",
        "apply_ts2vec",
    ]
    out_rows = []
    for key in order:
        values = sorted({(r.get(key) or "").strip() for r in rows})
        values = [v for v in values if v != ""]
        if len(values) != 1:
            raise SystemExit(f"Training config not constant for {key}: {values[:5]}")
        out_rows.append({"parameter": key, "value": values[0]})
    _write_csv(out_dir / "table_training_config.csv", out_rows, ["parameter", "value"])


def _write_spatial_tables(out_dir: Path, root: Path) -> None:
    path = root / "results/uc20260226/paper_tables/table_spatial_k124_with_patchpool.csv"
    rows = _read_csv(path)
    _require_columns(
        rows,
        ["protocol", "variant", "cer_m", "cer_s", "lex_all_m", "lex_all_s", "rtf_m", "rtf_s"],
        context="table_spatial_k124_with_patchpool.csv",
    )
    variant_order = ["vector", "rowcol", "spatial2d", "spatial2d_aug", "patchpool", "patchpool_aug"]
    variant_map = {
        "vector": "vec",
        "rowcol": "rowcol",
        "spatial2d": "grid",
        "spatial2d_aug": "grid_aug",
        "patchpool": "patch",
        "patchpool_aug": "patch_aug",
    }
    for protocol in ("P1", "P2", "P3"):
        prot_rows = [r for r in rows if r.get("protocol") == protocol]
        ordered = _order_rows(prot_rows, key_field="variant", order=variant_order)
        out_rows = []
        for r in ordered:
            out_rows.append(
                {
                    "variant": variant_map.get(r["variant"], r["variant"]),
                    "cer": _fmt_pm(r["cer_m"], r["cer_s"], 2),
                    "lex": _fmt_pm(r["lex_all_m"], r["lex_all_s"], 2),
                    "rtf": _fmt_pm(r["rtf_m"], r["rtf_s"], 4),
                }
            )
        _write_csv(out_dir / f"table_spatial_{protocol.lower()}.csv", out_rows, ["variant", "cer", "lex", "rtf"])


def _write_spatial_all(out_dir: Path, root: Path) -> None:
    path = root / "results/uc20260226/paper_tables/table_spatial_k124_with_patchpool.csv"
    rows = _read_csv(path)
    _require_columns(
        rows,
        ["protocol", "variant", "cer_m", "cer_s", "lex_all_m", "lex_all_s", "rtf_m", "rtf_s"],
        context="table_spatial_k124_with_patchpool.csv",
    )
    variant_order = ["vector", "rowcol", "spatial2d", "spatial2d_aug", "patchpool", "patchpool_aug"]
    variant_map = {
        "vector": "vec",
        "rowcol": "rowcol",
        "spatial2d": "grid",
        "spatial2d_aug": "grid_aug",
        "patchpool": "patch",
        "patchpool_aug": "patch_aug",
    }
    out_rows = []
    for protocol in ("P1", "P2", "P3"):
        prot_rows = [r for r in rows if r.get("protocol") == protocol]
        ordered = _order_rows(prot_rows, key_field="variant", order=variant_order)
        for r in ordered:
            out_rows.append(
                {
                    "protocol": protocol,
                    "variant": variant_map.get(r["variant"], r["variant"]),
                    "cer": _fmt_pm(r["cer_m"], r["cer_s"], 2),
                    "rtf": _fmt_pm(r["rtf_m"], r["rtf_s"], 4),
                }
            )
    _write_csv(out_dir / "table_spatial_all.csv", out_rows, ["protocol", "variant", "cer", "rtf"])


def _write_k64_tables(out_dir: Path, root: Path) -> None:
    path = root / "results/msx20260224/paper_tables/table_k64_methods.csv"
    rows = _read_csv(path)
    _require_columns(rows, ["protocol", "method", "cer_m", "cer_s", "rtf_m", "rtf_s"], context="table_k64_methods.csv")
    method_order = ["within_topk", "within_fps2k", "transfer_topk", "random"]
    method_map = {
        "within_topk": "topk",
        "within_fps2k": "fps2k",
        "transfer_topk": "xfer",
        "random": "rand",
    }

    def _build(protocols: Sequence[str]) -> List[Dict[str, object]]:
        out = []
        for p in protocols:
            prot_rows = [r for r in rows if r.get("protocol") == p]
            ordered = _order_rows(prot_rows, key_field="method", order=method_order)
            for r in ordered:
                out.append(
                    {
                        "protocol": r["protocol"],
                        "method": method_map.get(r["method"], r["method"]),
                        "cer": _fmt_pm(r["cer_m"], r["cer_s"], 3),
                        "rtf": _fmt_pm(r["rtf_m"], r["rtf_s"], 4),
                    }
                )
        return out

    _write_csv(out_dir / "table_k64_p1p2.csv", _build(["P1", "P2"]), ["protocol", "method", "cer", "rtf"])

    p3_rows = [r for r in rows if r.get("protocol") == "P3"]
    ordered = _order_rows(p3_rows, key_field="method", order=method_order)
    out_rows = [
        {
            "method": method_map.get(r["method"], r["method"]),
            "cer": _fmt_pm(r["cer_m"], r["cer_s"], 3),
            "rtf": _fmt_pm(r["rtf_m"], r["rtf_s"], 4),
        }
        for r in ordered
    ]
    _write_csv(out_dir / "table_k64_p3.csv", out_rows, ["method", "cer", "rtf"])


def _write_k64_all(out_dir: Path, root: Path) -> None:
    path = root / "results/msx20260224/paper_tables/table_k64_methods.csv"
    rows = _read_csv(path)
    _require_columns(rows, ["protocol", "method", "cer_m", "cer_s", "rtf_m", "rtf_s"], context="table_k64_methods.csv")
    method_order = ["within_topk", "within_fps2k", "transfer_topk", "random"]
    method_map = {
        "within_topk": "topk",
        "within_fps2k": "fps2k",
        "transfer_topk": "xfer",
        "random": "rand",
    }
    out_rows = []
    for protocol in ("P1", "P2", "P3"):
        prot_rows = [r for r in rows if r.get("protocol") == protocol]
        ordered = _order_rows(prot_rows, key_field="method", order=method_order)
        for r in ordered:
            out_rows.append(
                {
                    "protocol": protocol,
                    "method": method_map.get(r["method"], r["method"]),
                    "cer": _fmt_pm(r["cer_m"], r["cer_s"], 3),
                    "rtf": _fmt_pm(r["rtf_m"], r["rtf_s"], 4),
                }
            )
    _write_csv(out_dir / "table_k64_all.csv", out_rows, ["protocol", "method", "cer", "rtf"])


def _write_to4_compact(out_dir: Path, root: Path) -> None:
    path = root / "results/uc20260226/paper_tables/table_to4_generalization.csv"
    rows = _read_csv(path)
    _require_columns(
        rows,
        ["protocol", "level", "group", "cer_m", "cer_s", "lex_all_m", "lex_all_s", "rtf_m", "rtf_s"],
        context="table_to4_generalization.csv",
    )
    level_order = {"direction": 0, "across_directions": 1}
    rows_sorted = sorted(
        rows,
        key=lambda r: (r.get("protocol", ""), level_order.get(r.get("level", ""), 9), r.get("group", "")),
    )
    out_rows = []
    for r in rows_sorted:
        level = "dir" if r["level"] == "direction" else "all"
        group = r["group"]
        if group == "ALL_to4":
            group = "all->p4"
        match_pair = re.match(r"subj(\d)(\d)to(\d)$", group)
        if match_pair:
            group = f"p{match_pair.group(1)}{match_pair.group(2)}->p{match_pair.group(3)}"
        else:
            match_single = re.match(r"subj(\d+)to(\d+)$", group)
            if match_single:
                group = f"p{match_single.group(1)}->p{match_single.group(2)}"
        out_rows.append(
            {
                "proto": r["protocol"],
                "lvl": level,
                "group": group,
                "cer": _fmt_pm(r["cer_m"], r["cer_s"], 3),
                "lex": _fmt_pm(r["lex_all_m"], r["lex_all_s"], 3),
            }
        )
    _write_csv(out_dir / "table_to4_compact.csv", out_rows, ["proto", "lvl", "group", "cer", "lex"])


def _write_main_compact(out_dir: Path, root: Path) -> None:
    path = root / "results/msx20260224/paper_tables/table_main.csv"
    rows = _read_csv(path)
    _require_columns(
        rows,
        ["protocol", "variant", "n", "cer_m", "cer_s", "lex_all_m", "lex_all_s"],
        context="table_main.csv",
    )
    out_rows = []
    order = ["P1", "P2", "P3"]
    for prot in order:
        prot_rows = [r for r in rows if r.get("protocol") == prot]
        if len(prot_rows) != 1:
            raise SystemExit(f"Expected one baseline row for {prot}, got {len(prot_rows)}")
        r = prot_rows[0]
        out_rows.append(
            {
                "protocol": r["protocol"],
                "n": r["n"],
                "cer": _fmt_pm(r["cer_m"], r["cer_s"], 3),
                "lex": _fmt_pm(r["lex_all_m"], r["lex_all_s"], 3),
            }
        )
    _write_csv(out_dir / "table_main_compact.csv", out_rows, ["protocol", "n", "cer", "lex"])


def _write_p3ms_compact(out_dir: Path, root: Path) -> None:
    path = root / "results/msx20260224/paper_tables/table_p3ms.csv"
    rows = _read_csv(path)
    _require_columns(rows, ["group", "variant", "cer_m", "cer_s", "rtf_m", "rtf_s"], context="table_p3ms.csv")
    group_order = ["subj23to1", "subj13to2", "subj12to3"]
    variant_order = ["vector", "rowcol", "spatial2d", "spatial2d_aug"]
    variant_map = {
        "vector": "vec",
        "rowcol": "rowcol",
        "spatial2d": "grid",
        "spatial2d_aug": "grid_aug",
    }
    out_rows = []
    for group in group_order:
        group_rows = [r for r in rows if r.get("group") == group]
        ordered = _order_rows(group_rows, key_field="variant", order=variant_order)
        for r in ordered:
            group_label = r["group"]
            match_pair = re.match(r"subj(\d)(\d)to(\d)$", group_label)
            if match_pair:
                group_label = f"p{match_pair.group(1)}{match_pair.group(2)}->p{match_pair.group(3)}"
            out_rows.append(
                {
                    "group": group_label,
                    "variant": variant_map.get(r["variant"], r["variant"]),
                    "cer": _fmt_pm(r["cer_m"], r["cer_s"], 3),
                    "rtf": _fmt_pm(r["rtf_m"], r["rtf_s"], 4),
                }
            )
    _write_csv(out_dir / "table_p3ms_compact.csv", out_rows, ["group", "variant", "cer", "rtf"])


def _write_kshot_compact(out_dir: Path, root: Path) -> None:
    path = root / "results/msx20260224/paper_tables/table_kshot.csv"
    rows = _read_csv(path)
    _require_columns(rows, ["group", "variant", "cer_m", "cer_s", "rtf_m", "rtf_s"], context="table_kshot.csv")
    group_order = ["subj3_k1", "subj3_k2"]
    variant_order = ["vector", "rowcol", "spatial2d", "spatial2d_aug"]
    variant_map = {
        "vector": "vec",
        "rowcol": "rowcol",
        "spatial2d": "grid",
        "spatial2d_aug": "grid_aug",
    }
    out_rows = []
    for group in group_order:
        group_rows = [r for r in rows if r.get("group") == group]
        ordered = _order_rows(group_rows, key_field="variant", order=variant_order)
        for r in ordered:
            group_label = r["group"].replace("subj", "p", 1)
            out_rows.append(
                {
                    "group": group_label,
                    "variant": variant_map.get(r["variant"], r["variant"]),
                    "cer": _fmt_pm(r["cer_m"], r["cer_s"], 3),
                    "rtf": _fmt_pm(r["rtf_m"], r["rtf_s"], 4),
                }
            )
    _write_csv(out_dir / "table_kshot_compact.csv", out_rows, ["group", "variant", "cer", "rtf"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", default="results/paper_layout_2026-03-03")
    ap.add_argument("--root", default=None)
    args = ap.parse_args()
    root = Path(args.root).resolve() if args.root else _find_repo_root()
    out_dir = (root / args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    _write_dataset_summary(out_dir, root)
    _write_training_config(out_dir, root)
    _write_main_compact(out_dir, root)
    _write_spatial_tables(out_dir, root)
    _write_spatial_all(out_dir, root)
    _write_k64_tables(out_dir, root)
    _write_k64_all(out_dir, root)
    _write_to4_compact(out_dir, root)
    _write_p3ms_compact(out_dir, root)
    _write_kshot_compact(out_dir, root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
