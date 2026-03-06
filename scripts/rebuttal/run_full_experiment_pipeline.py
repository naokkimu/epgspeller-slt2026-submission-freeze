#!/usr/bin/env python3
"""
Run the full sweep pipeline end-to-end with stage chaining.

Default behavior:
  1) run stage2 until no planned/running rows remain
  2) run stage1 until no planned/running rows remain
  3) aggregate final summaries
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple

OPS_DIR = Path("sweeps/ops")
PIPELINE_HEARTBEAT_JSON = OPS_DIR / "pipeline_heartbeat.json"
PIPELINE_EVENTS_JSONL = OPS_DIR / "pipeline_events.jsonl"


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _write_json_atomic(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp") as tf:
        tf.write(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))
        tf.write("\n")
        tmp_path = Path(tf.name)
    os.replace(str(tmp_path), str(path))


def _append_event(event_type: str, **kwargs) -> None:
    OPS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"ts": dt.datetime.now().isoformat(timespec="seconds"), "event_type": event_type}
    payload.update(kwargs)
    with PIPELINE_EVENTS_JSONL.open("a") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")


def _load_stage_ids(stage_csv: Path) -> Set[str]:
    if not stage_csv.exists():
        return set()
    return {r.get("run_id", "") for r in _read_csv(stage_csv) if r.get("run_id", "")}


def _count_statuses(run_status_csv: Path, stage_ids: Set[str]) -> Dict[str, int]:
    rows = _read_csv(run_status_csv)
    scoped = [r for r in rows if r.get("run_id", "") in stage_ids]
    counts = {"done": 0, "running": 0, "planned": 0, "retry_pending": 0, "failed": 0, "other": 0}
    for r in scoped:
        s = (r.get("status", "") or "").strip().lower()
        if s in counts:
            counts[s] += 1
        else:
            counts["other"] += 1
    counts["total"] = len(scoped)
    return counts


def _remaining(counts: Dict[str, int]) -> int:
    return counts.get("running", 0) + counts.get("planned", 0) + counts.get("retry_pending", 0)


def _build_worker_cmd(
    *,
    python_bin: str,
    run_status_csv: Path,
    stage1_csv: Path,
    stage2_csv: Path,
    stage: str,
    sleep_sec: int,
    stale_minutes: int,
    max_concurrent: int,
    cuda_devices: str,
    lock_path: Path,
    progress_stale_minutes: int,
) -> List[str]:
    return [
        python_bin,
        "scripts/rebuttal/run_sweep_worker.py",
        "--run_status_csv",
        str(run_status_csv),
        "--stage1_csv",
        str(stage1_csv),
        "--stage2_csv",
        str(stage2_csv),
        "--stage",
        stage,
        "--sleep_sec",
        str(sleep_sec),
        "--stale_minutes",
        str(stale_minutes),
        "--max_concurrent",
        str(max_concurrent),
        "--cuda_devices",
        cuda_devices,
        "--lock_path",
        str(lock_path),
        "--progress_stale_minutes",
        str(progress_stale_minutes),
    ]


def _terminate_worker(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    proc.send_signal(signal.SIGTERM)
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=10)


def _run_stage(
    *,
    stage_name: str,
    stage_ids: Set[str],
    run_status_csv: Path,
    worker_cmd: List[str],
    poll_sec: int,
    max_restarts: int,
    restart_backoff_sec: int,
    dry_run: bool,
) -> Tuple[bool, Dict[str, int]]:
    counts = _count_statuses(run_status_csv, stage_ids)
    print(
        f"[pipeline] {stage_name} precheck: total={counts['total']} done={counts['done']} "
        f"running={counts['running']} planned={counts['planned']} retry_pending={counts['retry_pending']} failed={counts['failed']}",
        flush=True,
    )
    if _remaining(counts) == 0:
        print(f"[pipeline] {stage_name} already complete; skip worker launch.", flush=True)
        return True, counts

    if dry_run:
        print(f"[pipeline] dry-run {stage_name} worker cmd: {' '.join(worker_cmd)}", flush=True)
        return True, counts

    print(f"[pipeline] launching {stage_name} worker", flush=True)
    restart_count = 0
    proc = subprocess.Popen(worker_cmd)
    _append_event("worker_started", stage=stage_name, pid=proc.pid, restart_count=restart_count)
    try:
        while True:
            time.sleep(poll_sec)
            counts = _count_statuses(run_status_csv, stage_ids)
            _write_json_atomic(
                PIPELINE_HEARTBEAT_JSON,
                {
                    "ts": dt.datetime.now().isoformat(timespec="seconds"),
                    "pid": os.getpid(),
                    "stage": stage_name,
                    "worker_pid": proc.pid,
                    "restart_count": restart_count,
                    "counts": counts,
                },
            )
            print(
                f"[pipeline] {stage_name} status: total={counts['total']} done={counts['done']} "
                f"running={counts['running']} planned={counts['planned']} retry_pending={counts['retry_pending']} failed={counts['failed']}",
                flush=True,
            )
            if _remaining(counts) == 0:
                print(f"[pipeline] {stage_name} reached zero remaining rows.", flush=True)
                break
            rc = proc.poll()
            if rc is not None:
                if rc == 0 and _remaining(counts) > 0:
                    _append_event("worker_exited_unexpectedly", stage=stage_name, rc=rc, restart_count=restart_count, counts=counts)
                elif rc != 0:
                    _append_event("worker_exited_nonzero", stage=stage_name, rc=rc, restart_count=restart_count, counts=counts)
                if _remaining(counts) == 0:
                    break
                restart_count += 1
                if restart_count > max_restarts:
                    print(f"[pipeline] {stage_name} worker restart cap exceeded ({max_restarts})", flush=True)
                    _append_event("worker_restart_cap_exceeded", stage=stage_name, max_restarts=max_restarts, counts=counts)
                    return False, counts
                backoff = restart_backoff_sec * restart_count
                print(f"[pipeline] restarting {stage_name} worker in {backoff}s (attempt {restart_count}/{max_restarts})", flush=True)
                _append_event("worker_restart_scheduled", stage=stage_name, backoff_sec=backoff, restart_count=restart_count)
                time.sleep(backoff)
                proc = subprocess.Popen(worker_cmd)
                _append_event("worker_restarted", stage=stage_name, pid=proc.pid, restart_count=restart_count)
    finally:
        _terminate_worker(proc)
    return True, counts


def _run_aggregation(
    *,
    python_bin: str,
    run_status_csv: Path,
    stage1_csv: Path,
    stage2_csv: Path,
    aggregate_out: Path | None,
    dry_run: bool,
) -> bool:
    cmd = [
        python_bin,
        "scripts/rebuttal/aggregate_sweep_results.py",
        "--run_status_csv",
        str(run_status_csv),
        "--stage1_csv",
        str(stage1_csv),
        "--stage2_csv",
        str(stage2_csv),
        "--mode",
        "all",
    ]
    if dry_run:
        print(f"[pipeline] dry-run aggregate cmd: {' '.join(cmd)}", flush=True)
        return True

    print("[pipeline] running final aggregation", flush=True)
    if aggregate_out is None:
        rc = subprocess.run(cmd).returncode
        return rc == 0
    aggregate_out.parent.mkdir(parents=True, exist_ok=True)
    with aggregate_out.open("w") as f:
        rc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT).returncode
    print(f"[pipeline] aggregate report written: {aggregate_out}", flush=True)
    return rc == 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run full sweep pipeline with automatic stage chaining.")
    parser.add_argument("--run_status_csv", type=Path, default=Path("sweeps/run_status.csv"))
    parser.add_argument("--stage1_csv", type=Path, default=Path("sweeps/stage1_screening_matrix.csv"))
    parser.add_argument("--stage2_csv", type=Path, default=Path("sweeps/stage2_confirmation_matrix.csv"))
    parser.add_argument("--python_bin", type=str, default=".venv/bin/python")
    parser.add_argument("--poll_sec", type=int, default=60)
    parser.add_argument("--worker_sleep_sec", type=int, default=15)
    parser.add_argument("--stale_minutes", type=int, default=720)
    parser.add_argument("--progress_stale_minutes", type=int, default=20)
    parser.add_argument("--worker_lock_path", type=Path, default=Path("sweeps/.run_sweep_worker.lock"))
    parser.add_argument("--stage2_max_concurrent", type=int, default=6)
    parser.add_argument("--stage2_cuda_devices", type=str, default="0,1,2,3,4,5")
    parser.add_argument("--stage1_max_concurrent", type=int, default=2)
    parser.add_argument("--stage1_cuda_devices", type=str, default="6,7")
    parser.add_argument("--max_restarts", type=int, default=10)
    parser.add_argument("--restart_backoff_sec", type=int, default=20)
    parser.add_argument("--skip_stage2", action="store_true")
    parser.add_argument("--skip_stage1", action="store_true")
    parser.add_argument("--skip_aggregate", action="store_true")
    parser.add_argument("--aggregate_out", type=Path, default=Path("sweeps/final_aggregate_report.txt"))
    parser.add_argument("--dry_run", action="store_true")
    args = parser.parse_args()

    stage1_ids = _load_stage_ids(args.stage1_csv)
    stage2_ids = _load_stage_ids(args.stage2_csv)
    ok = True

    if not args.skip_stage2:
        stage2_cmd = _build_worker_cmd(
            python_bin=args.python_bin,
            run_status_csv=args.run_status_csv,
            stage1_csv=args.stage1_csv,
            stage2_csv=args.stage2_csv,
            stage="stage2",
            sleep_sec=args.worker_sleep_sec,
            stale_minutes=args.stale_minutes,
            max_concurrent=args.stage2_max_concurrent,
            cuda_devices=args.stage2_cuda_devices,
            lock_path=args.worker_lock_path,
            progress_stale_minutes=args.progress_stale_minutes,
        )
        st_ok, _ = _run_stage(
            stage_name="stage2",
            stage_ids=stage2_ids,
            run_status_csv=args.run_status_csv,
            worker_cmd=stage2_cmd,
            poll_sec=args.poll_sec,
            max_restarts=args.max_restarts,
            restart_backoff_sec=args.restart_backoff_sec,
            dry_run=args.dry_run,
        )
        ok = ok and st_ok

    if ok and (not args.skip_stage1):
        stage1_cmd = _build_worker_cmd(
            python_bin=args.python_bin,
            run_status_csv=args.run_status_csv,
            stage1_csv=args.stage1_csv,
            stage2_csv=args.stage2_csv,
            stage="stage1",
            sleep_sec=args.worker_sleep_sec,
            stale_minutes=args.stale_minutes,
            max_concurrent=args.stage1_max_concurrent,
            cuda_devices=args.stage1_cuda_devices,
            lock_path=args.worker_lock_path,
            progress_stale_minutes=args.progress_stale_minutes,
        )
        st_ok, _ = _run_stage(
            stage_name="stage1",
            stage_ids=stage1_ids,
            run_status_csv=args.run_status_csv,
            worker_cmd=stage1_cmd,
            poll_sec=args.poll_sec,
            max_restarts=args.max_restarts,
            restart_backoff_sec=args.restart_backoff_sec,
            dry_run=args.dry_run,
        )
        ok = ok and st_ok

    if ok and (not args.skip_aggregate):
        ok = ok and _run_aggregation(
            python_bin=args.python_bin,
            run_status_csv=args.run_status_csv,
            stage1_csv=args.stage1_csv,
            stage2_csv=args.stage2_csv,
            aggregate_out=args.aggregate_out,
            dry_run=args.dry_run,
        )

    if not ok:
        print("[pipeline] FAILED", flush=True)
        sys.exit(1)
    print("[pipeline] COMPLETE", flush=True)


if __name__ == "__main__":
    main()
