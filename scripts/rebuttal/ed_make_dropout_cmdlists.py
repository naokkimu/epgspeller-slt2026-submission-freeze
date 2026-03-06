#!/usr/bin/env python3
"""Generate GPU cmdlists for fixed-dropout evaluation.

This is a transparent batch helper:
- Reads each run's dataset pickle path from `logs/<run_id>/args` (pickle).
- Emits 1 line = 1 command that can be executed by `scripts/rebuttal/run_cmdlist.py`.
- Optional `--resume` skips commands whose output JSON already exists.

Outputs:
- <out_dir>/<name>.gpu<gpu>.txt

Notes:
- This script does not execute anything.
- It refuses to generate commands for missing `logs/<run_id>/args` or missing dataset pickle.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import math
import pickle
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "src").is_dir():
            return p
    raise RuntimeError("Could not locate repo root (expected scripts/ and src/)")


def _parse_int_list(spec: str) -> List[int]:
    spec = spec.strip()
    if not spec:
        return []

    # range forms: 0..9 or 0-9
    m = re.fullmatch(r"\s*(\d+)\s*(?:\.\.|-)\s*(\d+)\s*", spec)
    if m:
        a = int(m.group(1))
        b = int(m.group(2))
        if b < a:
            raise ValueError(f"Invalid range: {spec}")
        return list(range(a, b + 1))

    parts = [p.strip() for p in spec.split(",") if p.strip()]
    out: List[int] = []
    for p in parts:
        if not re.fullmatch(r"\d+", p):
            raise ValueError(f"Invalid int list element: {p!r}")
        out.append(int(p))
    return out


def _parse_float_list(spec: str) -> List[float]:
    parts = [p.strip() for p in spec.split(",") if p.strip()]
    out: List[float] = []
    for p in parts:
        try:
            out.append(float(p))
        except ValueError as e:
            raise ValueError(f"Invalid float list element: {p!r}") from e
    return out


def _q_tag(q: float) -> str:
    s = f"{q:.3f}".rstrip("0").rstrip(".")
    return s.replace(".", "p")


def _parse_split_seed(*, run_id: str, dataset_path: str) -> int:
    # Prefer dataset path (more reliable than run_id because run_id also contains trainseed*).
    for s in (dataset_path, run_id):
        m = re.search(r"(?:^|/)P1_seed(\d+)", s)
        if m:
            return int(m.group(1))
        m = re.search(r"^P1_seed(\d+)", s)
        if m:
            return int(m.group(1))
    return 0


def _load_pickle(path: Path) -> Dict:
    return pickle.loads(path.read_bytes())


@dataclass(frozen=True)
class DropoutJob:
    run_id: str
    dataset_pickle: str
    split_seed: int
    drop_rate: float
    rep: int

    @property
    def out_json_rel(self) -> str:
        qtag = _q_tag(self.drop_rate)
        return f"logs/{self.run_id}/eval_dropout_q{qtag}_rep{self.rep}.json"

    def to_cmd(self, *, python: str, device: str, partition: str) -> str:
        return (
            f"{python} scripts/rebuttal/ed_eval_fixed_dropout.py"
            f" --model_path logs/{self.run_id}"
            f" --dataset_pickle {self.dataset_pickle}"
            f" --partition {partition}"
            f" --device {device}"
            f" --drop_rate {self.drop_rate}"
            f" --rep {self.rep}"
            f" --seed {self.split_seed}"
        )


def _round_robin_assign(jobs: Sequence[DropoutJob], gpus: Sequence[int]) -> Dict[int, List[DropoutJob]]:
    if not gpus:
        raise ValueError("gpus list is empty")
    out: Dict[int, List[DropoutJob]] = {g: [] for g in gpus}
    for i, job in enumerate(jobs):
        out[gpus[i % len(gpus)]].append(job)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate cmdlists for ed_eval_fixed_dropout.py")
    ap.add_argument("--run_ids", type=str, nargs="+", required=True)
    ap.add_argument("--drop_rates", type=str, required=True, help="Comma-separated, e.g. 0,0.1,0.2,0.3")
    ap.add_argument("--reps", type=str, required=True, help="Comma-list or range, e.g. 0..9")
    ap.add_argument("--gpus", type=str, required=True, help="Comma-separated GPU ids, e.g. 0,1,2,3")
    ap.add_argument("--device", type=str, default="cuda")
    ap.add_argument("--partition", type=str, default="test", choices=["test", "competition"])
    ap.add_argument("--logs_dir", type=Path, default=Path("logs"))
    ap.add_argument("--out_dir", type=Path, default=Path("sweeps/ed20260217/cmds"))
    ap.add_argument("--name", type=str, required=True)
    ap.add_argument("--python", type=str, default=".venv/bin/python")
    ap.add_argument("--resume", action="store_true", help="Skip commands whose output JSON already exists")
    args = ap.parse_args()

    repo_root = _find_repo_root()
    logs_dir = args.logs_dir if args.logs_dir.is_absolute() else (repo_root / args.logs_dir)
    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)

    drop_rates = _parse_float_list(args.drop_rates)
    if not drop_rates:
        raise SystemExit("--drop_rates produced empty list")
    for q in drop_rates:
        if not (0.0 <= q <= 0.95) or math.isnan(q):
            raise SystemExit(f"Invalid drop_rate: {q}")

    reps = _parse_int_list(args.reps)
    if not reps:
        raise SystemExit("--reps produced empty list")
    if any(r < 0 for r in reps):
        raise SystemExit("--reps must be >=0")

    gpus = _parse_int_list(args.gpus)
    if not gpus:
        raise SystemExit("--gpus produced empty list")

    jobs: List[DropoutJob] = []

    for rid in args.run_ids:
        run_dir = logs_dir / rid
        args_path = run_dir / "args"
        if not args_path.exists():
            raise SystemExit(f"Missing args file: {args_path}")

        payload = _load_pickle(args_path)
        dataset_path = payload.get("datasetPath")
        if not dataset_path:
            raise SystemExit(f"datasetPath missing in {args_path}")
        if not isinstance(dataset_path, str):
            raise SystemExit(f"datasetPath is not a string in {args_path}")

        dataset_abs = (repo_root / dataset_path) if not Path(dataset_path).is_absolute() else Path(dataset_path)
        if not dataset_abs.exists():
            raise SystemExit(f"dataset_pickle not found for {rid}: {dataset_abs}")

        split_seed = _parse_split_seed(run_id=rid, dataset_path=dataset_path)

        for q in drop_rates:
            for rep in reps:
                job = DropoutJob(run_id=rid, dataset_pickle=dataset_path, split_seed=split_seed, drop_rate=q, rep=rep)
                if args.resume and (repo_root / job.out_json_rel).exists():
                    continue
                jobs.append(job)

    if not jobs:
        raise SystemExit("No jobs to write (everything already exists?)")

    assigned = _round_robin_assign(jobs, gpus)

    out_dir.mkdir(parents=True, exist_ok=True)
    ts = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for g in gpus:
        out_path = out_dir / f"{args.name}.gpu{g}.txt"
        lines: List[str] = []
        lines.append(f"# generated_by: {Path(__file__).as_posix()}")
        lines.append(f"# generated_at: {ts}")
        lines.append(f"# name: {args.name}")
        lines.append(f"# device: {args.device}")
        lines.append(f"# partition: {args.partition}")
        lines.append(f"# logs_dir: {logs_dir}")
        lines.append(f"# run_ids: {' '.join(args.run_ids)}")
        lines.append(f"# drop_rates: {args.drop_rates}")
        lines.append(f"# reps: {args.reps}")
        lines.append("")

        for job in assigned.get(g, []):
            lines.append(job.to_cmd(python=args.python, device=args.device, partition=args.partition).strip())

        out_path.write_text("\n".join(lines) + "\n")
        print(f"Wrote {out_path} ({len(assigned.get(g, []))} cmds)")


if __name__ == "__main__":
    main()

