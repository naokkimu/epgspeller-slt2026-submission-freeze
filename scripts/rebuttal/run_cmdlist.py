#!/usr/bin/env python3
"""Run a cmdlist sequentially with explicit environment injection.

This is intentionally simple and "non-orchestrator":
- No auto-skip, no auto-retry, no dynamic scheduling.
- Stop immediately on the first command failure.
- One command per log file for post-mortem.

Expected usage (4 panes):
  .venv/bin/python scripts/rebuttal/run_cmdlist.py --cuda 0 --cmdlist sweeps/gc20260216/cmds/<name>.train_eval.gpu0.txt --log_dir sweeps/gc20260216/runlogs
  ... gpu1/gpu2/gpu3
"""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List


THREAD_CAP_ENV: Dict[str, str] = {
    "OMP_NUM_THREADS": "8",
    "MKL_NUM_THREADS": "8",
    "OPENBLAS_NUM_THREADS": "8",
    "NUMEXPR_NUM_THREADS": "8",
    "PYTHONUNBUFFERED": "1",
}


def _load_cmds(path: Path) -> List[str]:
    raw_lines = path.read_text().splitlines()
    cmds: List[str] = []
    for line in raw_lines:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        cmds.append(line.rstrip())
    return cmds


def _write_header(f, *, cmd: str, idx: int, total: int, cuda: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write(f"# started_at={now}\n")
    f.write(f"# index={idx}/{total}\n")
    f.write(f"# cuda_visible_devices={cuda}\n")
    f.write(f"# cwd={os.getcwd()}\n")
    f.write("# injected_env=" + " ".join([f"{k}={v}" for k, v in THREAD_CAP_ENV.items()]) + "\n")
    f.write(f"# cmd={cmd}\n")
    f.write("\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Run a cmdlist sequentially (stop on first failure).")
    ap.add_argument("--cmdlist", type=Path, required=True)
    ap.add_argument("--cuda", type=int, required=True)
    ap.add_argument("--log_dir", type=Path, required=True)
    ap.add_argument("--dry_run", action="store_true")
    args = ap.parse_args()

    cmds = _load_cmds(args.cmdlist)
    if not cmds:
        raise SystemExit(f"No runnable commands found in {args.cmdlist}")

    args.log_dir.mkdir(parents=True, exist_ok=True)

    run_log_dir = args.log_dir / f"{args.cmdlist.stem}.cuda{args.cuda}"
    run_log_dir.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    env.update(THREAD_CAP_ENV)
    env["CUDA_VISIBLE_DEVICES"] = str(args.cuda)

    total = len(cmds)
    print(f"Loaded {total} commands from {args.cmdlist}")
    print(f"Logging root: {args.log_dir}")
    print(f"Logging dir:  {run_log_dir}")
    print(f"CUDA_VISIBLE_DEVICES={args.cuda}")

    for i, cmd in enumerate(cmds, start=1):
        log_path = run_log_dir / f"cmd_{i:04d}.log"
        print(f"[{i}/{total}] {cmd}")
        if args.dry_run:
            continue

        with log_path.open("w") as f:
            _write_header(f, cmd=cmd, idx=i, total=total, cuda=args.cuda)
            f.flush()
            start = time.perf_counter()
            proc = subprocess.run(
                cmd,
                shell=True,
                stdout=f,
                stderr=subprocess.STDOUT,
                env=env,
            )
            elapsed = max(0.0, time.perf_counter() - start)
            f.write("\n")
            f.write(f"# returncode={proc.returncode}\n")
            f.write(f"# elapsed_seconds={elapsed:.3f}\n")

        if proc.returncode != 0:
            print(f"Command failed (returncode={proc.returncode}). See {log_path}", file=sys.stderr)
            raise SystemExit(proc.returncode)

    print("All commands completed successfully.")


if __name__ == "__main__":
    main()
