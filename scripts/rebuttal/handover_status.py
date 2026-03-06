#!/usr/bin/env python3
"""Quick takeover status report for active sweeps."""

from __future__ import annotations

import csv
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RUN_STATUS_CSV = REPO_ROOT / "sweeps" / "run_status.csv"
OPS_DIR = REPO_ROOT / "sweeps" / "ops"
STALE_THRESHOLD_MIN = 15.0


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def load_rows() -> list[dict[str, str]]:
    with RUN_STATUS_CSV.open("r", newline="") as f:
        return list(csv.DictReader(f))


def list_live_run_ids() -> list[str]:
    result = subprocess.run(
        ["pgrep", "-af", "python scripts/train.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(f"pgrep failed: rc={result.returncode}")
    if not result.stdout.strip():
        return []
    pattern = re.compile(r"--run_id\s+(\S+)")
    run_ids: list[str] = []
    for line in result.stdout.splitlines():
        m = pattern.search(line)
        if m:
            run_ids.append(m.group(1))
    return run_ids


def age_minutes(path: Path) -> float:
    return (now_utc().timestamp() - path.stat().st_mtime) / 60.0


def summarize_staleness(running_run_ids: list[str]) -> tuple[int, list[tuple[str, float]]]:
    stale: list[tuple[str, float]] = []
    for run_id in running_run_ids:
        log_dir = REPO_ROOT / "logs" / run_id
        candidates = list(log_dir.glob("trainingStats*")) + list(log_dir.glob("modelWeights*"))
        if not candidates:
            stale.append((run_id, float("inf")))
            continue
        freshest = min(age_minutes(p) for p in candidates)
        if freshest > STALE_THRESHOLD_MIN:
            stale.append((run_id, freshest))
    stale.sort(key=lambda x: x[1], reverse=True)
    return len(stale), stale


def heartbeat_info() -> dict[str, str]:
    info: dict[str, str] = {}
    for name in ("worker_heartbeat.json", "pipeline_heartbeat.json"):
        path = OPS_DIR / name
        if not path.exists():
            info[name] = "missing"
            continue
        try:
            with path.open("r") as f:
                payload = json.load(f)
            ts = payload.get("timestamp") or payload.get("updated_at")
            if ts:
                info[name] = str(ts)
            else:
                mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()
                info[name] = f"file_mtime_utc={mtime}"
        except Exception:
            info[name] = "unreadable"
    return info


def main() -> None:
    rows = load_rows()
    status_counts = Counter(row.get("status", "") for row in rows)

    running_rows = [row for row in rows if row.get("status") == "running"]
    running_ids = {row["run_id"] for row in running_rows}

    live_ids = list_live_run_ids()
    live_unique = set(live_ids)

    running_with_live = len(running_ids & live_unique)
    running_without_live = len(running_ids - live_unique)
    live_not_running = len(live_unique - running_ids)

    stale_count, stale_detail = summarize_staleness([r["run_id"] for r in running_rows])
    hb = heartbeat_info()

    print("# Handover Status")
    print(f"ledger_counts={dict(status_counts)}")
    print(
        f"live_train_processes={len(live_ids)} "
        f"live_unique_run_ids={len(live_unique)} "
        f"running_rows={len(running_rows)}"
    )
    print(
        f"running_with_live={running_with_live} "
        f"running_without_live={running_without_live} "
        f"live_not_running={live_not_running}"
    )
    print(f"stale_running_rows_gt_{int(STALE_THRESHOLD_MIN)}m={stale_count}")
    if stale_detail:
        for run_id, minutes in stale_detail[:20]:
            age = "no_artifact" if minutes == float("inf") else f"{minutes:.1f}m"
            print(f"stale: {run_id} age={age}")
    print("heartbeat_timestamps:")
    for name, ts in hb.items():
        print(f"- {name}: {ts}")


if __name__ == "__main__":
    main()
