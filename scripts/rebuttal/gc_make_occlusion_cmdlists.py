#!/usr/bin/env python3
"""Generate occlusion cmdlists for baseline runs.

Reads baseline matrix CSV (gc_baseline.csv) and emits per-GPU cmdlists that run:
- eval_occlusion_importance.py --mode channel
- eval_occlusion_importance.py --mode region

This script does not execute commands.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


def _parse_gpus(s: str) -> List[int]:
    out: List[int] = []
    for part in (s or "").split(","):
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


def _assign_round_robin(items: List[Tuple[str, List[str]]], gpus: List[int]) -> Dict[int, List[Tuple[str, List[str]]]]:
    out: Dict[int, List[Tuple[str, List[str]]]] = {g: [] for g in gpus}
    for idx, item in enumerate(items):
        g = gpus[idx % len(gpus)]
        out[g].append(item)
    return out


def _write_cmdlist(path: Path, lines: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for line in lines:
            f.write(line.rstrip() + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate baseline occlusion cmdlists (channel+region).")
    ap.add_argument("--baseline_csv", type=Path, required=True)
    ap.add_argument("--gpus", type=str, required=True)
    ap.add_argument("--out_dir", type=Path, default=Path("sweeps/gc20260216/cmds"))
    ap.add_argument("--name", type=str, default="gc20260216_baseline_occlusion")
    ap.add_argument("--python_bin", type=str, default=".venv/bin/python")
    ap.add_argument("--device", type=str, default="cuda")
    ap.add_argument("--partition", type=str, default="test", choices=["test", "competition"])
    ap.add_argument(
        "--protocol",
        type=str,
        default="",
        help="Optional protocol filter (e.g., P1). If set, baseline_csv must contain a protocol column.",
    )
    ap.add_argument(
        "--modes",
        type=str,
        default="channel,region",
        help="Comma-separated occlusion modes to run: channel,region (default: channel,region).",
    )
    args = ap.parse_args()

    gpus = _parse_gpus(args.gpus)
    rows = _read_rows(args.baseline_csv)
    if not rows:
        raise SystemExit(f"No rows found in {args.baseline_csv}")

    modes = [m.strip() for m in (args.modes or "").split(",") if m.strip()]
    if not modes:
        raise SystemExit("--modes produced an empty list")
    for m in modes:
        if m not in {"channel", "region"}:
            raise SystemExit(f"Invalid mode in --modes: {m!r} (expected channel and/or region)")

    if args.protocol:
        if "protocol" not in rows[0]:
            raise SystemExit("--protocol was provided, but baseline_csv has no protocol column")
        rows = [r for r in rows if (r.get("protocol") or "").strip() == args.protocol.strip()]
        if not rows:
            raise SystemExit(f"No rows match --protocol {args.protocol!r} in {args.baseline_csv}")

    items: List[Tuple[str, List[str]]] = []
    for r in rows:
        rid = (r.get("run_id") or "").strip()
        dp = (r.get("dataset_pickle") or "").strip()
        if not rid or not dp:
            continue
        model_path = f"logs/{rid}"
        cmds: List[str] = []
        if "channel" in modes:
            cmds.append(
                f"{args.python_bin} scripts/rebuttal/eval_occlusion_importance.py --model_path {model_path} --dataset_pickle {dp} --partition {args.partition} --mode channel --device {args.device}"
            )
        if "region" in modes:
            cmds.append(
                f"{args.python_bin} scripts/rebuttal/eval_occlusion_importance.py --model_path {model_path} --dataset_pickle {dp} --partition {args.partition} --mode region --device {args.device}"
            )
        if not cmds:
            continue
        items.append((rid, cmds))

    assigned = _assign_round_robin(items, gpus)
    for g in gpus:
        out_path = args.out_dir / f"{args.name}.gpu{g}.txt"
        lines: List[str] = []
        lines.append(f"# baseline_csv={args.baseline_csv}")
        lines.append(f"# mode=occlusion partition={args.partition} device={args.device}")
        lines.append("")
        for rid, cmds in assigned[g]:
            lines.append(f"# run_id={rid}")
            lines.extend(cmds)
            lines.append("")
        _write_cmdlist(out_path, lines)
        print(f"Wrote {out_path} ({len(assigned[g])} runs)")


if __name__ == "__main__":
    main()
