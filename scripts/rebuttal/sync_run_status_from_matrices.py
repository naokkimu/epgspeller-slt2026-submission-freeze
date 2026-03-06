#!/usr/bin/env python3
"""
Rebuild sweeps/run_status.csv from stage matrices.

Optionally preserves existing per-run metrics/status fields if run_id already exists.
"""

from __future__ import annotations

import argparse
import csv
import os
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple

RUN_STATUS_FIELDS = [
    "run_id",
    "status",
    "started_at",
    "finished_at",
    "protocol",
    "model_path",
    "eval_greedy_test_json",
    "eval_lex_train_json",
    "eval_lex_all_json",
    "greedy_test_cer",
    "lex_train_test_cer",
    "lex_all_test_cer",
    "error_note",
]


def read_csv(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    with path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def read_stage(path: Path) -> List[Dict[str, str]]:
    _, rows = read_csv(path)
    return rows


def stage_tag(row: Dict[str, str], stage: str) -> str:
    if stage == "stage1":
        if row.get("protocol") == "P2":
            return "stage1_transfer"
        return "stage1"
    rank = (row.get("selection_rank") or "").strip()
    if row.get("protocol") == "P3":
        return f"stage2_top{rank}_cross" if rank else "stage2_cross"
    return f"stage2_top{rank}" if rank else "stage2"


def build_rows(
    stage1_rows: List[Dict[str, str]],
    stage2_rows: List[Dict[str, str]],
    existing_by_run: Dict[str, Dict[str, str]],
    reset_existing: bool,
) -> List[Dict[str, str]]:
    merged_by_run: Dict[str, Dict[str, str]] = {}

    def _make_entry(src: Dict[str, str], stage: str) -> Dict[str, str]:
        rid = src["run_id"]
        protocol = src.get("protocol", "")
        note = stage_tag(src, stage)
        base = {k: "" for k in RUN_STATUS_FIELDS}
        base["run_id"] = rid
        base["protocol"] = protocol
        base["status"] = "planned"
        base["error_note"] = note

        old = existing_by_run.get(rid)
        if old and not reset_existing:
            for k in RUN_STATUS_FIELDS:
                if k in {"run_id", "protocol"}:
                    continue
                if old.get(k, ""):
                    base[k] = old[k]
            # Keep stage tag authoritative even if old error_note existed.
            if old.get("status", ""):
                base["status"] = old["status"]
            base["error_note"] = note if base["status"] in {"planned", "running"} else (old.get("error_note") or note)
        return base

    def _merge_or_add(src: Dict[str, str], stage: str) -> None:
        rid = src["run_id"]
        new_entry = _make_entry(src, stage)
        old_entry = merged_by_run.get(rid)
        if old_entry is None:
            merged_by_run[rid] = new_entry
            return

        # Deduplicate same run_id across stage matrices.
        old_note = old_entry.get("error_note", "")
        new_note = new_entry.get("error_note", "")
        if old_note and new_note and new_note not in old_note:
            old_entry["error_note"] = f"{old_note}+{new_note}"
        elif not old_note:
            old_entry["error_note"] = new_note

    for row in stage1_rows:
        _merge_or_add(row, "stage1")
    for row in stage2_rows:
        _merge_or_add(row, "stage2")

    return list(merged_by_run.values())


def write_run_status(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", newline="", delete=False, dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp") as tf:
        f = tf
        w = csv.DictWriter(f, fieldnames=RUN_STATUS_FIELDS)
        w.writeheader()
        w.writerows(rows)
        tmp_path = Path(tf.name)
    os.replace(str(tmp_path), str(path))


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync run_status.csv from stage matrices.")
    parser.add_argument("--stage1_csv", type=Path, default=Path("sweeps/stage1_screening_matrix.csv"))
    parser.add_argument("--stage2_csv", type=Path, default=Path("sweeps/stage2_confirmation_matrix.csv"))
    parser.add_argument("--run_status_csv", type=Path, default=Path("sweeps/run_status.csv"))
    parser.add_argument("--reset_existing", action="store_true", help="Ignore existing run_status fields and regenerate fresh planned rows.")
    parser.add_argument("--dry_run", action="store_true")
    args = parser.parse_args()

    stage1 = read_stage(args.stage1_csv)
    stage2 = read_stage(args.stage2_csv)
    _, existing_rows = read_csv(args.run_status_csv)
    existing_by_run = {r["run_id"]: r for r in existing_rows if r.get("run_id")}

    merged = build_rows(stage1, stage2, existing_by_run, args.reset_existing)
    if args.dry_run:
        print(f"stage1_rows={len(stage1)}")
        print(f"stage2_rows={len(stage2)}")
        print(f"existing_rows={len(existing_rows)}")
        print(f"merged_rows={len(merged)}")
        return

    write_run_status(args.run_status_csv, merged)
    print(f"Wrote {len(merged)} rows to {args.run_status_csv}")


if __name__ == "__main__":
    main()
