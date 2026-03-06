#!/usr/bin/env python3
"""Generate cmdlists to create K=64 subset dataset pickles for msx20260224.

This script does not execute commands.
It emits per-GPU cmdlists compatible with scripts/rebuttal/run_cmdlist.py.

Inputs
- Baseline matrix (ms20260224) with dataset_pickle paths under data/ms20260224/
- K64 subset defs JSON produced by msx_define_k64_subsets.py

Outputs
- <out_dir>/<name>.gpu<g>.txt
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


P1P2_RE = re.compile(r"^subj(?P<subj>[1-4])_seed(?P<seed>\d+)$")
P3_RE = re.compile(r"^subj(?P<src>[1-3])to(?P<tgt>[1-3])_seed(?P<seed>\d+)$")


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (expected scripts/ and src/)")


def _parse_int_list(spec: str) -> List[int]:
    out: List[int] = []
    for part in (spec or "").split(","):
        part = part.strip()
        if not part:
            continue
        out.append(int(part))
    if not out:
        raise SystemExit("--gpus must be a non-empty comma-separated list (e.g., 0,1,2,3)")
    return out


def _read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _assign_round_robin(items: List[Tuple[str, str]], gpus: List[int]) -> Dict[int, List[Tuple[str, str]]]:
    out: Dict[int, List[Tuple[str, str]]] = {g: [] for g in gpus}
    for idx, item in enumerate(items):
        g = gpus[idx % len(gpus)]
        out[g].append(item)
    return out


def _write_cmdlist(path: Path, lines: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for line in lines:
            f.write(line.rstrip() + "\n")


def _subset_pkl_path(dataset_pickle: str, *, out_tag: str, subset_method: str) -> str:
    p = Path(dataset_pickle)
    parts = list(p.parts)
    if len(parts) < 3 or parts[0] != "data":
        raise ValueError(f"Unexpected dataset_pickle path: {dataset_pickle}")
    parts[1] = out_tag
    stem = Path(parts[-1]).stem
    parts[-1] = f"{stem}_{subset_method}.pkl"
    return str(Path(*parts))


def _src_subject(protocol: str, split_id: str) -> int:
    if protocol in {"P1", "P2"}:
        m = P1P2_RE.match(split_id)
        if not m:
            raise ValueError(f"Unexpected split_id for {protocol}: {split_id}")
        return int(m.group("subj"))
    if protocol == "P3":
        m = P3_RE.match(split_id)
        if not m:
            raise ValueError(f"Unexpected split_id for P3: {split_id}")
        return int(m.group("src"))
    raise ValueError(f"Unsupported protocol for K64 subsets: {protocol}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate cmdlists to build K=64 subset pickles (msx20260224).")
    ap.add_argument("--baseline_matrix", type=Path, required=True)
    ap.add_argument("--subset_defs_json", type=Path, required=True)
    ap.add_argument("--out_tag", type=str, default="msx20260224")
    ap.add_argument("--gpus", type=str, required=True)
    ap.add_argument("--out_dir", type=Path, default=Path("sweeps/msx20260224/cmds"))
    ap.add_argument("--name", type=str, default="msx_make_k64_subsets")
    ap.add_argument("--python_bin", type=str, default=".venv/bin/python")
    ap.add_argument("--resume", action="store_true", help="Skip commands whose out_pkl already exists.")
    args = ap.parse_args()

    repo_root = _find_repo_root()
    baseline_matrix = args.baseline_matrix if args.baseline_matrix.is_absolute() else (repo_root / args.baseline_matrix)
    subset_defs_json = args.subset_defs_json if args.subset_defs_json.is_absolute() else (repo_root / args.subset_defs_json)
    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)

    if not baseline_matrix.exists():
        raise SystemExit(f"baseline_matrix not found: {baseline_matrix}")
    if not subset_defs_json.exists():
        raise SystemExit(f"subset_defs_json not found: {subset_defs_json}")

    gpus = _parse_int_list(args.gpus)
    rows = _read_rows(baseline_matrix)
    if not rows:
        raise SystemExit(f"No rows in baseline_matrix: {baseline_matrix}")

    defs = json.loads(subset_defs_json.read_text(encoding="utf-8"))
    subjects = defs.get("subjects", {})
    transfer = defs.get("transfer_subj1_topk64")
    random64 = defs.get("random64_seed20260224")
    if not isinstance(subjects, dict) or not transfer or not random64:
        raise SystemExit("subset_defs_json missing required keys: subjects / transfer_subj1_topk64 / random64_seed20260224")

    methods = [
        "within_topk64",
        "within_fps2k64",
        "transfer_subj1_topk64",
        "random64_seed20260224",
    ]

    jobs: List[Tuple[str, str]] = []  # (out_pkl, cmd)
    for r in rows:
        protocol = (r.get("protocol") or "").strip()
        if protocol not in {"P1", "P2", "P3"}:
            continue
        split_id = (r.get("split_id") or "").strip()
        in_pkl = (r.get("dataset_pickle") or "").strip()
        if not split_id or not in_pkl:
            continue

        subj = _src_subject(protocol, split_id)
        subj_key = f"subj{subj}"
        if subj_key not in subjects:
            raise SystemExit(f"subset_defs_json missing subject key: {subj_key}")

        idx_within_topk = subjects[subj_key].get("topk64")
        idx_within_fps2k = subjects[subj_key].get("fps2k64")
        if not idx_within_topk or not idx_within_fps2k:
            raise SystemExit(f"subset_defs_json missing topk64/fps2k64 for {subj_key}")

        indices_by_method = {
            "within_topk64": idx_within_topk,
            "within_fps2k64": idx_within_fps2k,
            "transfer_subj1_topk64": transfer,
            "random64_seed20260224": random64,
        }

        for method in methods:
            idxs = indices_by_method[method]
            out_pkl = _subset_pkl_path(in_pkl, out_tag=args.out_tag, subset_method=method)
            out_abs = (repo_root / out_pkl) if not Path(out_pkl).is_absolute() else Path(out_pkl)
            if args.resume and out_abs.exists():
                continue

            cmd = (
                f"{args.python_bin} scripts/rebuttal/ed_make_subset_pickle.py"
                f" --in_pkl {in_pkl}"
                f" --out_pkl {out_pkl}"
                f" --subset_id {method}"
                f" --indices \"{' '.join(str(int(i)) for i in idxs)}\""
            )
            jobs.append((out_pkl, cmd))

    if not jobs:
        raise SystemExit("No subset jobs to write (everything already exists?)")

    assigned = _assign_round_robin(jobs, gpus)
    out_dir.mkdir(parents=True, exist_ok=True)

    for g in gpus:
        out_path = out_dir / f"{args.name}.gpu{g}.txt"
        lines: List[str] = []
        lines.append(f"# generated_by: {Path(__file__).as_posix()}")
        lines.append(f"# baseline_matrix: {baseline_matrix}")
        lines.append(f"# subset_defs_json: {subset_defs_json}")
        lines.append(f"# out_tag: {args.out_tag}")
        lines.append(f"# resume: {int(bool(args.resume))}")
        lines.append("")
        for _, cmd in assigned.get(g, []):
            lines.append(cmd)
        _write_cmdlist(out_path, lines)
        print(f"Wrote {out_path} ({len(assigned.get(g, []))} cmds)")


if __name__ == "__main__":
    main()

