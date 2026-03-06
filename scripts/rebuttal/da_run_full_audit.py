#!/usr/bin/env python3
"""Run the full dataset audit (raw + protocol splits) and generate a human-readable report.

This is a transparent driver that:
1) Audits four raw datasets under raw/silentspeller_dataset/:
   - john_2328_dataset.npz (new)
   - su_1167_old_dataset.npz (new)
   - p1_2328_old_dataset.npz (existing)
   - thad_2328_old_dataset.npz (existing)
2) Runs fixed pairwise comparisons and emits diff heatmaps.
3) Audits existing protocol split NPZs under raw_dataset/:
   - P1 word-holdout splits (subj1..subj4 × seed0..3)
   - P2 Protocol-S instance-holdout splits (subj1..subj3 × seed0..3)
   - P3 Protocol-S cross-subject splits (subj1/2/3 directions × seed0..3)
4) Writes inputs_manifest.md and report.md under the output directory.

No training/evaluation is run here; this is data-only auditing.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (expected scripts/ and src/)")


def _sha256(path: Path, *, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _read_csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _md_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    out: List[str] = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def _run(cmd: List[str]) -> None:
    print("[RUN]", " ".join(cmd))
    subprocess.run(cmd, check=True)


def _maybe_write_default_exclusions(path: Path) -> None:
    if path.exists():
        return
    payload = {
        "dataset_id": "john_2328",
        "exclude_indices": [509, 674, 1631, 1941],
        "reason": "all-zero samples detected in local audit; verify via da_audit_raw_npz.py",
        "created_at": _dt.date.today().isoformat(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Run full dataset audit and report generation.")
    ap.add_argument("--raw_dir", type=Path, default=Path("raw/silentspeller_dataset"))
    ap.add_argument(
        "--out_dir", type=Path, default=Path("results/dataset_audit_silentspeller_2026-02-24")
    )
    ap.add_argument("--smartpalate_csv", type=Path, default=Path("scripts/smartpalate_distribution.csv"))
    args = ap.parse_args()

    repo_root = _find_repo_root()
    py = repo_root / ".venv" / "bin" / "python"
    if not py.exists():
        raise SystemExit(f"python not found: {py}")

    raw_dir = args.raw_dir if args.raw_dir.is_absolute() else (repo_root / args.raw_dir)
    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)
    sp_csv = args.smartpalate_csv if args.smartpalate_csv.is_absolute() else (repo_root / args.smartpalate_csv)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "figures").mkdir(parents=True, exist_ok=True)
    (out_dir / "exclusions").mkdir(parents=True, exist_ok=True)

    # --- Raw datasets ---
    datasets: List[Tuple[str, Path]] = [
        ("john_2328", raw_dir / "john_2328_dataset.npz"),
        ("su_1167_old", raw_dir / "su_1167_old_dataset.npz"),
        ("p1_2328_old", raw_dir / "p1_2328_old_dataset.npz"),
        ("thad_2328_old", raw_dir / "thad_2328_old_dataset.npz"),
    ]

    for _, p in datasets:
        if not p.exists():
            raise SystemExit(f"Missing dataset file: {p}")
    if not sp_csv.exists():
        raise SystemExit(f"Missing smartpalate CSV: {sp_csv}")

    excl_john = out_dir / "exclusions" / "john_2328_exclude_indices.json"
    _maybe_write_default_exclusions(excl_john)

    audit_py = repo_root / "scripts" / "rebuttal" / "da_audit_raw_npz.py"
    compare_py = repo_root / "scripts" / "rebuttal" / "da_compare_raw_npz.py"
    split_audit_py = repo_root / "scripts" / "rebuttal" / "da_audit_split_npz.py"

    # --- Run raw audits ---
    for ds_id, npz_path in datasets:
        cmd = [
            str(py),
            str(audit_py),
            "--npz",
            str(npz_path),
            "--dataset_id",
            ds_id,
            "--smartpalate_csv",
            str(sp_csv),
            "--out_dir",
            str(out_dir),
        ]
        if ds_id == "john_2328":
            cmd += ["--exclude_indices_json", str(excl_john)]
        _run(cmd)

    # --- Pairwise comparisons (fixed set) ---
    def path_of(ds_id: str) -> Path:
        for k, p in datasets:
            if k == ds_id:
                return p
        raise KeyError(ds_id)

    comparisons = [
        ("john_2328", "p1_2328_old"),
        ("john_2328", "su_1167_old"),
        ("su_1167_old", "p1_2328_old"),
    ]
    for a, b in comparisons:
        _run(
            [
                str(py),
                str(compare_py),
                "--a_npz",
                str(path_of(a)),
                "--b_npz",
                str(path_of(b)),
                "--a_id",
                a,
                "--b_id",
                b,
                "--smartpalate_csv",
                str(sp_csv),
                "--out_dir",
                str(out_dir),
            ]
        )

    # --- Protocol split audits (P1/P2) ---
    fig_dir_splits = out_dir / "figures" / "protocol_splits"
    fig_dir_splits.mkdir(parents=True, exist_ok=True)

    split_dir = repo_root / "raw_dataset"

    split_files: List[Tuple[str, str, int, str, Path]] = []  # (split_id, protocol, seed, subject, path)

    # P1: word-holdout splits (subj1..subj4 × seed0..3)
    for subj in ["subj1", "subj2", "subj3", "subj4"]:
        for seed in range(4):
            split_files.append(
                (
                    f"P1_{subj}_seed{seed}",
                    "P1",
                    seed,
                    subj,
                    split_dir / f"train_test_competition_split_seed{seed}_{subj}_ds1.npz",
                )
            )

    # P2: Protocol-S instance-holdout (subj1..subj3 × seed0..3)
    for subj in ["subj1", "subj2", "subj3"]:
        for seed in range(4):
            split_files.append(
                (
                    f"P2_{subj}_seed{seed}",
                    "P2",
                    seed,
                    subj,
                    split_dir / f"protocolS_split_seed{seed}_{subj}_ds1.npz",
                )
            )

    # P3: Protocol-S cross-subject (ordered pairs over subj1..subj3) × seed0..3
    for direction in [
        "subj1to2",
        "subj2to1",
        "subj1to3",
        "subj3to1",
        "subj2to3",
        "subj3to2",
    ]:
        for seed in range(4):
            split_files.append(
                (
                    f"P3_{direction}_seed{seed}",
                    "P3",
                    seed,
                    direction,
                    split_dir / f"protocolSx_split_seed{seed}_{direction}_ds1.npz",
                )
            )

    for _, _, _, _, p in split_files:
        if not p.exists():
            raise SystemExit(f"Missing split NPZ file: {p}")

    for split_id, protocol, seed, subject, p in split_files:
        cmd = [
            str(py),
            str(split_audit_py),
            "--split_npz",
            str(p),
            "--split_id",
            split_id,
            "--protocol",
            protocol,
            "--seed",
            str(seed),
            "--smartpalate_csv",
            str(sp_csv),
            "--out_dir",
            str(out_dir),
            "--fig_dir",
            str(fig_dir_splits),
        ]
        if subject:
            cmd += ["--subject", subject]
        _run(cmd)

    # --- inputs_manifest.md ---
    try:
        import numpy as np  # type: ignore

        numpy_ver = np.__version__
    except Exception:
        numpy_ver = "unknown"

    manifest_lines: List[str] = []
    manifest_lines.append(f"# Inputs manifest (dataset audit) — { _dt.date.today().isoformat() }")
    manifest_lines.append("")
    manifest_lines.append("## Environment")
    manifest_lines.append(f"- python: `{sys.version.split()[0]}`")
    manifest_lines.append(f"- numpy: `{numpy_ver}`")
    manifest_lines.append(f"- platform: `{platform.platform()}`")
    manifest_lines.append("")
    manifest_lines.append("## Command")
    manifest_lines.append("```")
    manifest_lines.append(" ".join([str(py), str(Path("scripts/rebuttal/da_run_full_audit.py"))] + sys.argv[1:]))
    manifest_lines.append("```")
    manifest_lines.append("")

    manifest_lines.append("## Input files (raw datasets)")
    for ds_id, p in datasets:
        sha = _sha256(p)
        manifest_lines.append(f"- `{p}`")
        manifest_lines.append(f"  - dataset_id: `{ds_id}`")
        manifest_lines.append(f"  - size_bytes: `{p.stat().st_size}`")
        manifest_lines.append(f"  - sha256: `{sha}`")

    manifest_lines.append("")
    manifest_lines.append(f"- `{sp_csv}` (SmartPalate 16×16 proxy map)")
    manifest_lines.append(f"  - size_bytes: `{sp_csv.stat().st_size}`")
    manifest_lines.append(f"  - sha256: `{_sha256(sp_csv)}`")

    manifest_lines.append("")
    manifest_lines.append("## Exclusions")
    manifest_lines.append(f"- `{excl_john}`")

    manifest_lines.append("")
    manifest_lines.append("## Input files (protocol split NPZ: P1/P2/P3)")
    for split_id, protocol, seed, subject, p in split_files:
        sha = _sha256(p)
        manifest_lines.append(f"- `{p}`")
        manifest_lines.append(f"  - split_id: `{split_id}`")
        manifest_lines.append(f"  - protocol: `{protocol}`")
        manifest_lines.append(f"  - seed: `{seed}`")
        if subject:
            manifest_lines.append(f"  - subject: `{subject}`")
        manifest_lines.append(f"  - size_bytes: `{p.stat().st_size}`")
        manifest_lines.append(f"  - sha256: `{sha}`")

    _write_text(out_dir / "inputs_manifest.md", "\n".join(manifest_lines) + "\n")

    # --- report.md ---
    summary_rows = _read_csv_rows(out_dir / "dataset_summary.csv")
    pair_rows = _read_csv_rows(out_dir / "pairwise_comparison.csv")
    zero_rows = _read_csv_rows(out_dir / "all_zero_samples.csv")

    split_summary_rows = _read_csv_rows(out_dir / "protocol_split_summary.csv")

    by_key: Dict[Tuple[str, str], Dict[str, str]] = {
        ((r.get("dataset_id") or ""), (r.get("view") or "")): r for r in summary_rows
    }

    report: List[str] = []
    inputs_manifest_md = "inputs_manifest.md"
    figures_md = "figures"
    protocol_splits_md = "protocol_splits"
    empty_str = ""
    dataset_a_key = "dataset_a"
    view_a_key = "view_a"
    dataset_b_key = "dataset_b"
    view_b_key = "view_b"
    protocol_split_vocab_sets_json = "protocol_split_vocab_sets.json"
    report.append(f"# Dataset audit report — { _dt.date.today().isoformat() }")
    report.append("")
    report.append(f"- Output directory: `{out_dir}`")
    report.append(f"- Inputs manifest: `{out_dir / inputs_manifest_md}`")
    report.append("")

    report.append("## 1) Dataset-level summary (raw view + john excluded view)")
    report.append("")
    headers = [
        "dataset_id",
        "view",
        "n_samples",
        "n_vocab",
        "T(min/med/mean/max)",
        "total_frames",
        "mean_contact",
        "all_zero",
        "dead_ch",
        "label_occ_hist",
    ]
    table_rows: List[List[str]] = []
    for ds_id in ["john_2328", "su_1167_old", "p1_2328_old", "thad_2328_old"]:
        views = ["raw", "excluded"] if ds_id == "john_2328" else ["raw"]
        for view in views:
            r = by_key.get((ds_id, view))
            if not r:
                continue
            table_rows.append(
                [
                    ds_id,
                    view,
                    r.get("n_samples", ""),
                    r.get("n_unique_labels", ""),
                    "{}/{}/{}/{}".format(
                        r.get("T_min", ""), r.get("T_median", ""), r.get("T_mean", ""), r.get("T_max", "")
                    ),
                    r.get("total_frames", ""),
                    r.get("overall_mean_contact", ""),
                    r.get("all_zero_samples", ""),
                    r.get("dead_channels", ""),
                    r.get("label_occurrence_hist_json", ""),
                ]
            )
    report.append(_md_table(headers, table_rows))
    report.append("")

    report.append("## 2) Figures")
    report.append("")
    report.append(f"- `{out_dir / figures_md}`")
    report.append("  - `T_hist_<dataset_id>_<view>.png`")
    report.append("  - `contact_rate_hist_<dataset_id>_<view>.png`")
    report.append("  - `channel_mean_heatmap16x16_<dataset_id>_<view>.png`")
    report.append("  - `channel_mean_diff_heatmap16x16_<A>_minus_<B>.png`")
    report.append("")
    report.append(f"- `{out_dir / figures_md / protocol_splits_md}`")
    report.append("  - `T_hist_<split_id>_<partition>.png`")
    report.append("  - `contact_rate_hist_<split_id>_<partition>.png`")
    report.append("  - `channel_mean_heatmap16x16_<split_id>_<partition>.png`")
    report.append("")

    report.append("## 3) Pairwise comparisons (mean pattern correlation)")
    report.append("")
    if pair_rows:
        ptab: List[List[str]] = []
        for r in pair_rows:
            ptab.append(
                [
                    f"{r.get(dataset_a_key, empty_str)}({r.get(view_a_key, empty_str)})",
                    f"{r.get(dataset_b_key, empty_str)}({r.get(view_b_key, empty_str)})",
                    r.get("mean_pattern_corr", ""),
                    r.get("mean_contact_a", ""),
                    r.get("mean_contact_b", ""),
                    r.get("mean_contact_ratio_a_over_b", ""),
                ]
            )
        report.append(
            _md_table(
                ["A", "B", "corr(mean_pattern)", "mean_contact(A)", "mean_contact(B)", "ratio(A/B)"],
                ptab,
            )
        )
    else:
        report.append("pairwise_comparison.csv is empty (unexpected).")
    report.append("")

    report.append("## 4) All-zero samples (raw view)")
    report.append("")
    if zero_rows:
        ztab: List[List[str]] = []
        for r in zero_rows:
            ztab.append(
                [
                    r.get("dataset_id", ""),
                    r.get("idx", ""),
                    r.get("label", ""),
                    r.get("T", ""),
                    r.get("word_count_before", ""),
                    r.get("word_count_after_excl", ""),
                    r.get("excluded_flag", ""),
                ]
            )
        report.append(
            _md_table(
                ["dataset_id", "idx", "label", "T", "count_before", "count_after_excl", "excluded"],
                ztab,
            )
        )
        report.append("")
        report.append("Handling note (evidence-only):")
        report.append("- If you can re-export the raw trials, prefer re-export over keeping label+all-zero input.")
        report.append("- Otherwise, proceed with an explicit exclusion list (`exclusions/john_2328_exclude_indices.json`).")
    else:
        report.append("No all-zero samples detected.")
    report.append("")

    report.append("## 5) Protocol split EDA (P1/P2/P3)")
    report.append("")
    report.append(
        "Protocol integrity checks are enforced by `scripts/rebuttal/da_audit_split_npz.py` and would abort on violation."
    )
    report.append("")

    if split_summary_rows:
        # P1 table
        p1 = [r for r in split_summary_rows if (r.get("protocol") == "P1")]
        p1_sorted = sorted(
            p1,
            key=lambda r: (
                int(r.get("seed", "0") or 0),
                str(r.get("partition", "")),
            ),
        )
        report.append("### 5.1 P1 word-holdout splits (subj1..subj4 × seed0..3)")
        report.append("")
        p1_tab: List[List[str]] = []
        for r in p1_sorted:
            p1_tab.append(
                [
                    r.get("split_id", ""),
                    r.get("partition", ""),
                    r.get("n_samples", ""),
                    r.get("n_unique_labels", ""),
                    "{}/{}/{}/{}".format(
                        r.get("T_min", ""), r.get("T_median", ""), r.get("T_mean", ""), r.get("T_max", "")
                    ),
                    r.get("total_frames", ""),
                    r.get("overall_mean_contact", ""),
                    r.get("all_zero_samples", ""),
                    r.get("dead_channels", ""),
                    r.get("label_occurrence_hist_json", ""),
                ]
            )
        report.append(
            _md_table(
                [
                    "split_id",
                    "partition",
                    "n_samples",
                    "n_vocab",
                    "T(min/med/mean/max)",
                    "total_frames",
                    "mean_contact",
                    "all_zero",
                    "dead_ch",
                    "label_occ_hist",
                ],
                p1_tab,
            )
        )
        report.append("")

        # P2 table
        p2 = [r for r in split_summary_rows if (r.get("protocol") == "P2")]
        p2_sorted = sorted(
            p2,
            key=lambda r: (
                str(r.get("subject", "")),
                int(r.get("seed", "0") or 0),
                str(r.get("partition", "")),
            ),
        )
        report.append("### 5.2 P2 Protocol-S instance-holdout splits (subj1..subj3 × seed0..3)")
        report.append("")
        p2_tab: List[List[str]] = []
        for r in p2_sorted:
            p2_tab.append(
                [
                    r.get("split_id", ""),
                    r.get("subject", ""),
                    r.get("partition", ""),
                    r.get("n_samples", ""),
                    r.get("n_unique_labels", ""),
                    "{}/{}/{}/{}".format(
                        r.get("T_min", ""), r.get("T_median", ""), r.get("T_mean", ""), r.get("T_max", "")
                    ),
                    r.get("total_frames", ""),
                    r.get("overall_mean_contact", ""),
                    r.get("all_zero_samples", ""),
                    r.get("dead_channels", ""),
                    r.get("label_occurrence_hist_json", ""),
                ]
            )
        report.append(
            _md_table(
                [
                    "split_id",
                    "subject",
                    "partition",
                    "n_samples",
                    "n_vocab",
                    "T(min/med/mean/max)",
                    "total_frames",
                    "mean_contact",
                    "all_zero",
                    "dead_ch",
                    "label_occ_hist",
                ],
                p2_tab,
            )
        )
        report.append("")



        # P3 table
        p3 = [r for r in split_summary_rows if (r.get("protocol") == "P3")]
        p3_sorted = sorted(
            p3,
            key=lambda r: (
                str(r.get("subject", "")),
                int(r.get("seed", "0") or 0),
                str(r.get("partition", "")),
            ),
        )
        report.append("### 5.3 P3 Protocol-S cross-subject splits (subj1/2/3 directions × seed0..3)")
        report.append("")
        p3_tab: List[List[str]] = []
        for r in p3_sorted:
            p3_tab.append(
                [
                    r.get("split_id", ""),
                    r.get("subject", ""),
                    r.get("partition", ""),
                    r.get("n_samples", ""),
                    r.get("n_unique_labels", ""),
                    "{}/{}/{}/{}".format(
                        r.get("T_min", ""), r.get("T_median", ""), r.get("T_mean", ""), r.get("T_max", "")
                    ),
                    r.get("total_frames", ""),
                    r.get("overall_mean_contact", ""),
                    r.get("all_zero_samples", ""),
                    r.get("dead_channels", ""),
                    r.get("label_occurrence_hist_json", ""),
                ]
            )
        report.append(
            _md_table(
                [
                    "split_id",
                    "direction",
                    "partition",
                    "n_samples",
                    "n_vocab",
                    "T(min/med/mean/max)",
                    "total_frames",
                    "mean_contact",
                    "all_zero",
                    "dead_ch",
                    "label_occ_hist",
                ],
                p3_tab,
            )
        )
        report.append("")
        report.append("Split vocab sets (JSON):")
        report.append(f"- `{out_dir / protocol_split_vocab_sets_json}`")

    else:
        report.append("protocol_split_summary.csv is empty (unexpected).")

    report.append("")

    report.append("## 6) How this strengthens the research (grounded in this audit)")
    report.append("")
    report.append("- Data volume: use `total_frames` and the T/contact histograms to justify stability and stress-tests.")
    report.append(
        "- Domain shift: use `mean_contact`, `corr(mean_pattern)`, and the 16×16 diff heatmaps to quantify distribution differences."
    )
    report.append(
        "- Protocol clarity: P1/P2/P3 split NPZs are audited with explicit integrity checks and per-partition distribution summaries (seed/subject/direction)."
    )
    report.append(
        "- Repeat renditions: Protocol-S split scripts subsample exactly 2 renditions per kept word (count>=2 after exclusions) and record kept/dropped vocab for auditability."
    )
    report.append(
        "- Integrity: the all-zero anomaly is pinned (indices+labels+T) and handled reproducibly via the exclusion list."
    )
    report.append("")

    _write_text(out_dir / "report.md", "\n".join(report) + "\n")

    print(f"[OK] audit complete: {out_dir}")


if __name__ == "__main__":
    main()
