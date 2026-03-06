#!/usr/bin/env python3
"""Generate a CPU cmdlist to create subset dataset pickles for P1 seeds.

This script does not execute commands.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Sequence


def _read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _parse_seeds(s: str) -> List[int]:
    out: List[int] = []
    for part in (s or "").split(","):
        part = part.strip()
        if not part:
            continue
        out.append(int(part))
    if not out:
        raise SystemExit("--seeds must be non-empty (e.g., 0,1,2,3)")
    return out


def _write_lines(path: Path, lines: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for line in lines:
            f.write(line.rstrip() + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Make cmdlist to generate subset pickles (CPU).")
    ap.add_argument("--subset_defs", type=Path, required=True)
    ap.add_argument("--base_pkl_dir", type=Path, default=Path("data/gc20260216"))
    ap.add_argument("--out_pkl_dir", type=Path, default=Path("data/ed20260217"))
    ap.add_argument("--seeds", type=str, default="0,1,2,3")
    ap.add_argument("--python_bin", type=str, default=".venv/bin/python")
    ap.add_argument("--out_cmdlist", type=Path, default=Path("sweeps/ed20260217/cmds/ed20260217_subset_prep.cpu.txt"))
    args = ap.parse_args()

    rows = _read_rows(args.subset_defs)
    if not rows:
        raise SystemExit(f"No rows in subset_defs: {args.subset_defs}")
    seeds = _parse_seeds(args.seeds)

    lines: List[str] = []
    lines.append(f"# subset_defs={args.subset_defs}")
    lines.append(f"# base_pkl_dir={args.base_pkl_dir} out_pkl_dir={args.out_pkl_dir}")
    lines.append("")

    n_total = 0
    n_skipped = 0
    for r in rows:
        subset_id = (r.get("subset_id") or "").strip()
        idxs = (r.get("indices_space_separated") or "").strip()
        if not subset_id or not idxs:
            continue
        for seed in seeds:
            in_pkl = args.base_pkl_dir / f"P1_seed{seed}_raw_ds1_el-all.pkl"
            out_pkl = args.out_pkl_dir / f"P1_seed{seed}_raw_ds1_{subset_id}.pkl"
            n_total += 1
            if out_pkl.exists():
                n_skipped += 1
                continue
            # Quote indices as a single shell argument.
            cmd = (
                f"{args.python_bin} scripts/rebuttal/ed_make_subset_pickle.py "
                f"--in_pkl {in_pkl} --out_pkl {out_pkl} --subset_id {subset_id} --indices \"{idxs}\""
            )
            lines.append(cmd)

    _write_lines(args.out_cmdlist, lines)
    print(f"Wrote {args.out_cmdlist} ({n_total - n_skipped} cmds; skipped {n_skipped} existing pkls)")


if __name__ == "__main__":
    main()

