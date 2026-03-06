#!/usr/bin/env python3
"""
Continuous sweep worker:
- consumes run rows from sweeps/run_status.csv
- runs one training at a time
- executes eval chain after training completion
- updates ledger fields and transitions
"""

from __future__ import annotations

import atexit
import argparse
import csv
import datetime as dt
import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch


OPS_DIR = Path("sweeps/ops")
ATTEMPTS_JSON = OPS_DIR / "run_attempts.json"
RUN_GPU_MAP_JSON = OPS_DIR / "run_gpu_map.json"
WORKER_EVENTS_JSONL = OPS_DIR / "worker_events.jsonl"
WORKER_HEARTBEAT_JSON = OPS_DIR / "worker_heartbeat.json"


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def parse_iso(ts: str) -> Optional[dt.datetime]:
    s = (ts or "").strip()
    if not s:
        return None
    try:
        return dt.datetime.fromisoformat(s)
    except Exception:
        return None


def classify_failure(note: str) -> str:
    n = (note or "").lower()
    if "out of memory" in n or "cuda oom" in n or "oom" in n:
        return "oom"
    if "prepare failed" in n or "missing from stage matrices" in n:
        return "config"
    if "dataset" in n or "file not found" in n:
        return "data"
    if "orphan" in n or "stale timeout" in n or "progress stale" in n or "eval_failed" in n:
        return "transient"
    return "infra"


def retry_limit_for_class(cls: str) -> int:
    limits = {
        "transient": 3,
        "infra": 2,
        "oom": 1,
        "data": 0,
        "config": 0,
    }
    return limits.get(cls, 0)


def load_attempts() -> Dict[str, int]:
    raw = _read_json(ATTEMPTS_JSON, {})
    if not isinstance(raw, dict):
        return {}
    out: Dict[str, int] = {}
    for k, v in raw.items():
        try:
            out[str(k)] = int(v)
        except Exception:
            continue
    return out


def save_attempts(attempts: Dict[str, int]) -> None:
    _write_json_atomic(ATTEMPTS_JSON, attempts)


def load_run_gpu_map() -> Dict[str, Dict[str, str]]:
    raw = _read_json(RUN_GPU_MAP_JSON, {})
    if not isinstance(raw, dict):
        return {}
    out: Dict[str, Dict[str, str]] = {}
    for k, v in raw.items():
        if isinstance(v, dict):
            out[str(k)] = {str(kk): str(vv) for kk, vv in v.items()}
    return out


def save_run_gpu_map(run_gpu_map: Dict[str, Dict[str, str]]) -> None:
    _write_json_atomic(RUN_GPU_MAP_JSON, run_gpu_map)


def read_csv(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    with path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_csv_atomic(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        newline="",
        delete=False,
        dir=str(path.parent),
        prefix=f".{path.name}.",
        suffix=".tmp",
    ) as tf:
        writer = csv.DictWriter(tf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        tmp_path = Path(tf.name)
    os.replace(str(tmp_path), str(path))


def _ensure_ops_dir() -> None:
    OPS_DIR.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def _write_json_atomic(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        dir=str(path.parent),
        prefix=f".{path.name}.",
        suffix=".tmp",
    ) as tf:
        tf.write(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))
        tf.write("\n")
        tmp_path = Path(tf.name)
    os.replace(str(tmp_path), str(path))


def append_event(event_type: str, **kwargs) -> None:
    _ensure_ops_dir()
    payload = {"ts": now_iso(), "event_type": event_type}
    payload.update(kwargs)
    with WORKER_EVENTS_JSONL.open("a") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")


def write_heartbeat(**kwargs) -> None:
    _ensure_ops_dir()
    payload = {"ts": now_iso(), "pid": os.getpid()}
    payload.update(kwargs)
    _write_json_atomic(WORKER_HEARTBEAT_JSON, payload)


def row_for_run(rows: List[Dict[str, str]], run_id: str) -> Dict[str, str]:
    for row in rows:
        if row["run_id"] == run_id:
            return row
    raise KeyError(f"run_id not found: {run_id}")


def load_stage_rows(stage_csv: Path) -> Dict[str, Dict[str, str]]:
    _, rows = read_csv(stage_csv)
    return {r["run_id"]: r for r in rows}


def run_cmd(cmd: str) -> int:
    p = subprocess.run(cmd, shell=True)
    return int(p.returncode)


def run_cmd_background(cmd: str) -> int:
    p = subprocess.Popen(cmd, shell=True)
    return int(p.pid)


def run_cmd_capture(cmd: str) -> Tuple[int, str]:
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = (p.stdout or "") + (p.stderr or "")
    return int(p.returncode), output


def train_pids_for_run(run_id: str) -> List[int]:
    cmd = f"pgrep -f \"python scripts/train.py .*--run_id {run_id}\""
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.returncode != 0:
        return []
    pids: List[int] = []
    for line in p.stdout.splitlines():
        s = line.strip()
        if not s:
            continue
        try:
            pids.append(int(s))
        except ValueError:
            continue
    return sorted(set(pids))


def all_train_run_pids() -> Dict[str, List[int]]:
    cmd = "pgrep -af \"python scripts/train.py\""
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.returncode != 0:
        return {}
    by_run: Dict[str, List[int]] = {}
    run_pat = re.compile(r"--run_id\s+(\S+)")
    for line in p.stdout.splitlines():
        s = line.strip()
        if not s:
            continue
        parts = s.split(maxsplit=1)
        if not parts:
            continue
        try:
            pid = int(parts[0])
        except ValueError:
            continue
        m = run_pat.search(s)
        if not m:
            continue
        rid = m.group(1)
        by_run.setdefault(rid, []).append(pid)
    for rid in by_run:
        by_run[rid] = sorted(set(by_run[rid]))
    return by_run


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def kill_pids(pids: List[int]) -> None:
    if not pids:
        return
    joined = " ".join(str(x) for x in pids)
    subprocess.run(f"kill {joined}", shell=True, check=False)


def acquire_lock(lock_path: Path) -> None:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except FileExistsError:
            old_pid = None
            try:
                old_pid = int(lock_path.read_text().strip())
            except Exception:
                old_pid = None
            if old_pid:
                try:
                    os.kill(old_pid, 0)
                    raise SystemExit(f"Another worker is active (pid={old_pid}).")
                except OSError:
                    pass
            lock_path.unlink(missing_ok=True)

    def _cleanup() -> None:
        lock_path.unlink(missing_ok=True)

    atexit.register(_cleanup)


def cuda_available() -> bool:
    try:
        return bool(torch.cuda.is_available())
    except Exception:
        return False


def eval_paths(run_id: str) -> Dict[str, str]:
    root = f"logs/{run_id}"
    return {
        "model_path": root,
        "greedy": f"{root}/eval_greedy_test.json",
        "lex_train": f"{root}/eval_lex_train.json",
        "lex_all": f"{root}/eval_lex_all.json",
        "metrics": f"{root}/metrics.json",
    }


def latest_progress_age_minutes(run_id: str, started_at: Optional[dt.datetime]) -> Optional[float]:
    """
    Read progress age from train-time heartbeat files only.
    Ignore artifacts older than the current running window (started_at),
    which prevents false stale detection when reusing an existing run_id directory.
    """
    root = Path("logs") / run_id
    if not root.exists():
        return None
    candidates = [root / "trainingStats", root / "modelWeights"]
    latest = 0.0
    started_ts = started_at.timestamp() if started_at is not None else 0.0
    for fp in candidates:
        if not fp.exists() or (not fp.is_file()):
            continue
        mt = fp.stat().st_mtime
        if mt < started_ts:
            continue
        if mt > latest:
            latest = mt
    if latest <= 0:
        return None
    return (time.time() - latest) / 60.0


def metric_from_json(path: Path) -> Optional[float]:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
    except Exception:
        return None
    v = data.get("cer")
    try:
        return float(v)
    except Exception:
        return None


def reconcile_orphan_running_rows(
    run_status_csv: Path,
    python_bin: str,
    attempts: Dict[str, int],
    stage_by_run_id: Dict[str, str],
) -> None:
    """
    Recover ledger rows left in `running` after worker interruption.
    Policy:
    - If training is still active for run_id: keep running.
    - If metrics.json exists and eval artifacts are complete: mark done.
    - If metrics.json exists but eval artifacts are missing: run eval chain, then mark done/failed.
    - If no training pid and no metrics: mark failed (orphaned running row).
    """
    _, rows = read_csv(run_status_csv)
    running_rows = [r for r in rows if r.get("status") == "running"]
    if not running_rows:
        return

    for r in running_rows:
        run_id = r["run_id"]
        p = eval_paths(run_id)
        metrics_path = Path(p["metrics"])
        greedy_path = Path(p["greedy"])
        lex_train_path = Path(p["lex_train"])
        lex_all_path = Path(p["lex_all"])
        pids = train_pids_for_run(run_id)

        if pids:
            continue

        if metrics_path.exists():
            if greedy_path.exists() and lex_train_path.exists() and lex_all_path.exists():
                g = metric_from_json(greedy_path)
                lt = metric_from_json(lex_train_path)
                la = metric_from_json(lex_all_path)
                update_running_row(
                    run_status_csv,
                    run_id,
                    "done",
                    finished=True,
                    model_path=p["model_path"],
                    eval_greedy=p["greedy"],
                    eval_lex_train=p["lex_train"],
                    eval_lex_all=p["lex_all"],
                    greedy_cer="" if g is None else f"{g:.6f}",
                    lex_train_cer="" if lt is None else f"{lt:.6f}",
                    lex_all_cer="" if la is None else f"{la:.6f}",
                    error_note="recovered_running_row_from_artifacts",
                )
                append_event("orphan_recovered_done", run_id=run_id, mode="artifacts_complete")
                continue

            ok, reason = run_eval_chain(run_id, python_bin)
            if not ok:
                queue_retry_or_fail(
                    run_status_csv,
                    run_id,
                    f"recovered_running_eval_failed: {reason}",
                    attempts,
                    model_path=p["model_path"],
                    stage_by_run_id=stage_by_run_id,
                )
                continue

            g = metric_from_json(greedy_path)
            lt = metric_from_json(lex_train_path)
            la = metric_from_json(lex_all_path)
            update_running_row(
                run_status_csv,
                run_id,
                "done",
                finished=True,
                model_path=p["model_path"],
                eval_greedy=p["greedy"],
                eval_lex_train=p["lex_train"],
                eval_lex_all=p["lex_all"],
                greedy_cer="" if g is None else f"{g:.6f}",
                lex_train_cer="" if lt is None else f"{lt:.6f}",
                lex_all_cer="" if la is None else f"{la:.6f}",
                error_note="recovered_running_eval_completed",
            )
            append_event("orphan_recovered_done", run_id=run_id, mode="eval_backfill")
            continue

        queue_retry_or_fail(
            run_status_csv,
            run_id,
            "orphaned_running_row_no_train_pid_no_metrics",
            attempts,
            model_path=p["model_path"],
            stage_by_run_id=stage_by_run_id,
        )


def run_eval_chain(run_id: str, python_bin: str, cuda_device: Optional[str] = None) -> Tuple[bool, str]:
    p = eval_paths(run_id)
    cuda_prefix = f"CUDA_VISIBLE_DEVICES={cuda_device} " if cuda_device is not None else ""
    cmds = [
        (
            "greedy",
            f"{cuda_prefix}{python_bin} scripts/rebuttal/eval_greedy_clean.py "
            f"--model_path {p['model_path']} --partition test --device cuda --frame_ms 10.0 --out_json {p['greedy']}",
        ),
        (
            "lex_train",
            f"{cuda_prefix}{python_bin} scripts/rebuttal/eval_lexicon_project.py "
            f"--pred_json {p['greedy']} --lexicon_source train --out_json {p['lex_train']}",
        ),
        (
            "lex_all",
            f"{cuda_prefix}{python_bin} scripts/rebuttal/eval_lexicon_project.py "
            f"--pred_json {p['greedy']} --lexicon_source all --out_json {p['lex_all']}",
        ),
    ]
    for name, cmd in cmds:
        code = run_cmd(cmd)
        if code != 0:
            return False, f"{name} failed (exit={code})"
    return True, ""


def stage_from_note(note: str) -> str:
    n = (note or "").strip()
    if n.startswith("stage2"):
        return "stage2"
    if n.startswith("stage1"):
        return "stage1"
    return "unknown"


def stage_prefix(note: str) -> str:
    n = (note or "").strip()
    if n.startswith("stage1"):
        return "stage1"
    if n.startswith("stage2"):
        return "stage2"
    return "stage_unknown"


def normalize_stage_tags(run_status_csv: Path, stage1_ids: set[str], stage2_ids: set[str]) -> None:
    fields, rows = read_csv(run_status_csv)
    changed = False
    for r in rows:
        s = (r.get("status", "") or "").strip()
        if s not in {"planned", "running", "retry_pending"}:
            continue
        note = r.get("error_note", "") or ""
        if stage_prefix(note) != "stage_unknown":
            continue
        rid = r.get("run_id", "")
        recovered = "stage_unknown"
        if rid in stage2_ids:
            recovered = "stage2"
        elif rid in stage1_ids:
            recovered = "stage1"
        if recovered == "stage_unknown":
            continue
        suffix = ""
        if "::" in note:
            suffix = note.split("::", 1)[1]
        elif note and not note.startswith(recovered):
            suffix = note
        r["error_note"] = f"{recovered}::{suffix}" if suffix else recovered
        changed = True
    if changed:
        write_csv_atomic(run_status_csv, fields, rows)


def pick_next_planned(rows: List[Dict[str, str]], stage: Optional[str]) -> Optional[str]:
    for r in rows:
        if r["status"] != "planned":
            continue
        s = stage_from_note(r.get("error_note", ""))
        if stage and s != stage:
            continue
        return r["run_id"]
    return None


def build_train_cmd(
    run: Dict[str, str], run_id: str, python_bin: str, cuda_device: Optional[str] = None
) -> str:
    model_family = (run.get("model_family") or "gru").strip()
    cuda_prefix = f"CUDA_VISIBLE_DEVICES={cuda_device} " if cuda_device is not None else ""
    cmd = [
        f"{cuda_prefix}{python_bin} scripts/train.py",
        f"--dataset_path {run['dataset_pickle']}",
        f"--run_id {run_id}",
        f"--model_family {model_family}",
        f"--n_units {run['n_units']}",
        f"--n_layers {run['n_layers']}",
        f"--stride_len {run['stride_len']}",
        f"--kernel_len {run['kernel_len']}",
        f"--n_batch {run['n_batch']}",
        f"--seed {run['train_seed']}",
        f"--white_noise_sd {run.get('white_noise_sd', '0.8') or '0.8'}",
        f"--constant_offset_sd {run.get('constant_offset_sd', '0.2') or '0.2'}",
        f"--gaussian_smooth_width {run.get('gaussian_smooth_width', '2.0') or '2.0'}",
        "--disable_day_embed",
    ]
    proj = (run.get("input_proj_dim") or "").strip()
    if proj:
        cmd.append(f"--input_proj_dim {proj}")
    tcn_layers = (run.get("tcn_layers") or "").strip()
    if tcn_layers:
        cmd.append(f"--tcn_layers {tcn_layers}")
    tcn_kernel_size = (run.get("tcn_kernel_size") or "").strip()
    if tcn_kernel_size:
        cmd.append(f"--tcn_kernel_size {tcn_kernel_size}")
    transformer_heads = (run.get("transformer_heads") or "").strip()
    if transformer_heads:
        cmd.append(f"--transformer_heads {transformer_heads}")
    transformer_layers = (run.get("transformer_layers") or "").strip()
    if transformer_layers:
        cmd.append(f"--transformer_layers {transformer_layers}")
    transformer_ff_mult = (run.get("transformer_ff_mult") or "").strip()
    if transformer_ff_mult:
        cmd.append(f"--transformer_ff_mult {transformer_ff_mult}")
    if (run.get("specaug_on") or "").strip() in {"1", "true", "True"}:
        cmd.append("--enable_online_specaug")
    return " ".join(cmd)


def build_prep_cmd(run: Dict[str, str], python_bin: str) -> str:
    return (
        f"{python_bin} scripts/prepare_silentspeller_dataset.py "
        f"--split_path {run['split_npz']} "
        f"--n_components {run['n_components']} "
        f"--downsample_factor {run['downsample_factor']} "
        f"--electrode_regions {run['electrode_regions']} "
        f"--output_path {run['dataset_pickle']}"
    )


def _extract_max_pca_components(error_output: str) -> Optional[int]:
    """
    Parse sklearn PCA error:
      n_components=32 must be between 0 and min(n_samples, n_features)=31 ...
    """
    m = re.search(r"min\(n_samples,\s*n_features\)\s*=\s*(\d+)", error_output)
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None


def can_transition(prev: str, nxt: str) -> bool:
    prev_s = (prev or "").strip().lower()
    nxt_s = (nxt or "").strip().lower()
    if prev_s == nxt_s:
        return True
    allowed = {
        "planned": {"running", "retry_pending", "failed"},
        "retry_pending": {"planned", "failed"},
        "running": {"done", "failed", "retry_pending"},
        "failed": {"retry_pending", "planned"},
        "done": set(),
    }
    return nxt_s in allowed.get(prev_s, set())


def update_running_row(
    run_status_csv: Path,
    run_id: str,
    status: str,
    *,
    finished: bool = False,
    model_path: str = "",
    eval_greedy: str = "",
    eval_lex_train: str = "",
    eval_lex_all: str = "",
    greedy_cer: str = "",
    lex_train_cer: str = "",
    lex_all_cer: str = "",
    error_note: str = "",
) -> None:
    fields, rows = read_csv(run_status_csv)
    row = row_for_run(rows, run_id)
    prev_status = row.get("status", "")
    if not can_transition(prev_status, status):
        raise RuntimeError(f"Invalid status transition for {run_id}: {prev_status} -> {status}")
    row["status"] = status
    if status == "running" and not row.get("started_at"):
        row["started_at"] = now_iso()
    if status in {"planned", "retry_pending"}:
        row["started_at"] = ""
        row["finished_at"] = ""
    if finished:
        row["finished_at"] = now_iso()
    if model_path:
        row["model_path"] = model_path
    if eval_greedy:
        row["eval_greedy_test_json"] = eval_greedy
    if eval_lex_train:
        row["eval_lex_train_json"] = eval_lex_train
    if eval_lex_all:
        row["eval_lex_all_json"] = eval_lex_all
    if greedy_cer:
        row["greedy_test_cer"] = greedy_cer
    if lex_train_cer:
        row["lex_train_test_cer"] = lex_train_cer
    if lex_all_cer:
        row["lex_all_test_cer"] = lex_all_cer
    if error_note != "":
        row["error_note"] = error_note
    write_csv_atomic(run_status_csv, fields, rows)


def queue_retry_or_fail(
    run_status_csv: Path,
    run_id: str,
    reason: str,
    attempts: Dict[str, int],
    model_path: str = "",
    stage_by_run_id: Optional[Dict[str, str]] = None,
) -> None:
    _, rows = read_csv(run_status_csv)
    current_row = row_for_run(rows, run_id)
    prefix = stage_prefix(current_row.get("error_note", ""))
    if prefix == "stage_unknown" and stage_by_run_id is not None:
        prefix = stage_by_run_id.get(run_id, "stage_unknown")
    cls = classify_failure(reason)
    attempts[run_id] = attempts.get(run_id, 0) + 1
    save_attempts(attempts)
    limit = retry_limit_for_class(cls)
    note = f"{prefix}::{reason} | class={cls} | retry={attempts[run_id]}/{limit}"
    if attempts[run_id] <= limit:
        update_running_row(
            run_status_csv,
            run_id,
            "retry_pending",
            finished=True,
            model_path=model_path,
            error_note=note,
        )
        append_event("retry_queued", run_id=run_id, reason=reason, failure_class=cls, retry=attempts[run_id], retry_limit=limit)
        return
    update_running_row(
        run_status_csv,
        run_id,
        "failed",
        finished=True,
        model_path=model_path,
        error_note=note,
    )
    append_event("retry_exhausted", run_id=run_id, reason=reason, failure_class=cls, retry=attempts[run_id], retry_limit=limit)


def promote_retry_pending_rows(run_status_csv: Path) -> None:
    fields, rows = read_csv(run_status_csv)
    changed = False
    for r in rows:
        if r.get("status") != "retry_pending":
            continue
        r["status"] = "planned"
        r["started_at"] = ""
        r["finished_at"] = ""
        changed = True
        append_event("retry_promoted_to_planned", run_id=r.get("run_id", ""))
    if changed:
        write_csv_atomic(run_status_csv, fields, rows)


def reconcile_live_pids_with_ledger(
    run_status_csv: Path,
    run_gpu_map: Dict[str, Dict[str, str]],
    active_stage: Optional[str],
) -> Dict[str, List[int]]:
    """
    Enforce ledger/process consistency.
    - Kill train pids for rows not in `running`.
    - For each running run_id keep at most one pid.
    - Drop stale run_gpu_map entries with dead pids or non-running rows.
    Returns surviving run_id -> [pid].
    """
    _, rows = read_csv(run_status_csv)
    by_id = {r["run_id"]: r for r in rows}
    live_by_run = all_train_run_pids()
    changed_map = False

    for run_id, pids in list(live_by_run.items()):
        row = by_id.get(run_id)
        if row is None:
            kill_pids(pids)
            append_event("orphan_pid_killed", run_id=run_id, killed_pids=pids, reason="run_id_missing_in_ledger")
            del live_by_run[run_id]
            continue
        status = (row.get("status") or "").strip()
        stage_ok = (active_stage is None) or (stage_from_note(row.get("error_note", "")) == active_stage)
        if status != "running" or (not stage_ok):
            kill_pids(pids)
            append_event(
                "orphan_pid_killed",
                run_id=run_id,
                killed_pids=pids,
                reason=f"status={status}, stage_ok={stage_ok}",
            )
            del live_by_run[run_id]
            continue
        if len(pids) > 1:
            keep = pids[0]
            drop = pids[1:]
            kill_pids(drop)
            append_event("duplicate_pid_killed", run_id=run_id, kept_pid=keep, killed_pids=drop)
            live_by_run[run_id] = [keep]

    for run_id, meta in list(run_gpu_map.items()):
        row = by_id.get(run_id)
        if row is None or (row.get("status") != "running"):
            run_gpu_map.pop(run_id, None)
            changed_map = True
            continue
        pid_s = (meta or {}).get("pid", "").strip()
        if not pid_s:
            continue
        try:
            pid_i = int(pid_s)
        except ValueError:
            run_gpu_map.pop(run_id, None)
            changed_map = True
            continue
        if not pid_alive(pid_i):
            run_gpu_map.pop(run_id, None)
            changed_map = True
    if changed_map:
        save_run_gpu_map(run_gpu_map)

    return live_by_run


def run_worker(
    run_status_csv: Path,
    stage1_csv: Path,
    stage2_csv: Path,
    stage: Optional[str],
    sleep_sec: int,
    stale_minutes: int,
    smoke: bool,
    require_cuda: bool,
    python_bin: str,
    max_concurrent: int,
    cuda_devices: List[str],
    progress_stale_minutes: int,
) -> None:
    stage1_rows = load_stage_rows(stage1_csv)
    stage2_rows = load_stage_rows(stage2_csv)
    stage_rows = {}
    stage_rows.update(stage1_rows)
    stage_rows.update(stage2_rows)
    stage_by_run_id: Dict[str, str] = {}
    for rid in stage1_rows:
        stage_by_run_id[rid] = "stage1"
    for rid in stage2_rows:
        stage_by_run_id[rid] = "stage2"
    normalize_stage_tags(run_status_csv, set(stage1_rows.keys()), set(stage2_rows.keys()))
    attempts = load_attempts()
    run_gpu_map = load_run_gpu_map()
    rr_idx = 0

    if require_cuda and not cuda_available():
        raise SystemExit("CUDA is not available in PyTorch runtime. Aborting worker.")

    while True:
        promote_retry_pending_rows(run_status_csv)
        reconcile_orphan_running_rows(run_status_csv, python_bin, attempts, stage_by_run_id)
        live_by_run = reconcile_live_pids_with_ledger(run_status_csv, run_gpu_map, stage)
        _, rows = read_csv(run_status_csv)
        running = [r for r in rows if r["status"] == "running"]
        active_running_ids = {r["run_id"] for r in running}
        active_leases = 0
        for rid in active_running_ids:
            if rid in live_by_run and live_by_run[rid]:
                active_leases += 1
        write_heartbeat(
            stage=(stage or "all"),
            running=len(running),
            planned=len([r for r in rows if r["status"] == "planned"]),
            retry_pending=len([r for r in rows if r["status"] == "retry_pending"]),
            active_train_pids=sum(len(v) for v in live_by_run.values()),
            active_leases=active_leases,
        )

        for r in running:
            run_id = r["run_id"]
            pids = live_by_run.get(run_id, [])
            if len(pids) > 1:
                kill_pids(pids[1:])
                append_event("duplicate_pid_killed", run_id=run_id, killed_pids=pids[1:])
            p = eval_paths(run_id)
            metrics_path = Path(p["metrics"])
            gpu_meta = run_gpu_map.get(run_id, {})
            cuda_device = gpu_meta.get("cuda_device", cuda_devices[0] if cuda_devices else "")
            cuda_device = cuda_device if cuda_device != "" else None
            if metrics_path.exists():
                ok, reason = run_eval_chain(run_id, python_bin, cuda_device=cuda_device)
                if not ok:
                    queue_retry_or_fail(
                        run_status_csv,
                        run_id,
                        reason,
                        attempts,
                        model_path=p["model_path"],
                        stage_by_run_id=stage_by_run_id,
                    )
                    continue

                g = metric_from_json(Path(p["greedy"]))
                lt = metric_from_json(Path(p["lex_train"]))
                la = metric_from_json(Path(p["lex_all"]))
                update_running_row(
                    run_status_csv,
                    run_id,
                    "done",
                    finished=True,
                    model_path=p["model_path"],
                    eval_greedy=p["greedy"],
                    eval_lex_train=p["lex_train"],
                    eval_lex_all=p["lex_all"],
                    greedy_cer="" if g is None else f"{g:.6f}",
                    lex_train_cer="" if lt is None else f"{lt:.6f}",
                    lex_all_cer="" if la is None else f"{la:.6f}",
                    error_note=r.get("error_note", ""),
                )
                run_gpu_map.pop(run_id, None)
                save_run_gpu_map(run_gpu_map)
                append_event("run_done", run_id=run_id, greedy_cer="" if g is None else f"{g:.6f}")
                continue

            started = parse_iso(r.get("started_at", ""))
            if started is not None:
                age_min = (dt.datetime.now() - started).total_seconds() / 60.0
                artifact_age = latest_progress_age_minutes(run_id, started)
                if artifact_age is not None and artifact_age >= progress_stale_minutes:
                    stalled_pids = train_pids_for_run(run_id)
                    if stalled_pids:
                        kill_pids(stalled_pids)
                        append_event(
                            "progress_stale_pid_killed",
                            run_id=run_id,
                            killed_pids=stalled_pids,
                            artifact_age_min=artifact_age,
                            threshold_min=progress_stale_minutes,
                        )
                    queue_retry_or_fail(
                        run_status_csv,
                        run_id,
                        f"progress stale exceeded ({progress_stale_minutes} min, artifact_age={artifact_age:.1f})",
                        attempts,
                        model_path=p["model_path"],
                        stage_by_run_id=stage_by_run_id,
                    )
                    run_gpu_map.pop(run_id, None)
                    save_run_gpu_map(run_gpu_map)
                    continue
                if age_min >= stale_minutes:
                    stale_pids = train_pids_for_run(run_id)
                    if stale_pids:
                        kill_pids(stale_pids)
                        append_event("stale_pid_killed", run_id=run_id, killed_pids=stale_pids, age_min=age_min)
                    queue_retry_or_fail(
                        run_status_csv,
                        run_id,
                        f"stale timeout exceeded ({stale_minutes} min)",
                        attempts,
                        model_path=p["model_path"],
                        stage_by_run_id=stage_by_run_id,
                    )
                    run_gpu_map.pop(run_id, None)
                    save_run_gpu_map(run_gpu_map)

        _, rows = read_csv(run_status_csv)
        running = [r for r in rows if r["status"] == "running"]
        live_by_run = reconcile_live_pids_with_ledger(run_status_csv, run_gpu_map, stage)
        running_ids = {r["run_id"] for r in running}
        active_leases = sum(1 for rid in running_ids if rid in live_by_run and live_by_run[rid])
        slots = max(0, max_concurrent - active_leases)
        if slots == 0:
            time.sleep(sleep_sec)
            continue

        launched_any = False
        for _ in range(slots):
            _, rows = read_csv(run_status_csv)
            next_run_id = pick_next_planned(rows, stage)
            if not next_run_id:
                break

            if next_run_id not in stage_rows:
                queue_retry_or_fail(
                    run_status_csv,
                    next_run_id,
                    "run_id missing from stage matrices",
                    attempts,
                    stage_by_run_id=stage_by_run_id,
                )
                continue

            if smoke:
                cfg = stage_rows[next_run_id]
                print(f"SMOKE next_run_id={next_run_id}")
                print(build_prep_cmd(cfg, python_bin))
                print(build_train_cmd(cfg, next_run_id, python_bin))
                print("SMOKE ok")
                return

            stale_same = all_train_run_pids().get(next_run_id, [])
            if stale_same:
                kill_pids(stale_same)
                append_event("prelaunch_stale_pid_killed", run_id=next_run_id, killed_pids=stale_same)

            update_running_row(run_status_csv, next_run_id, "running")
            cfg = stage_rows[next_run_id]
            prep_cmd = build_prep_cmd(cfg, python_bin)

            prep_code, prep_out = run_cmd_capture(prep_cmd)
            if prep_code != 0:
                max_comp = _extract_max_pca_components(prep_out)
                requested = (cfg.get("n_components") or "").strip()
                if max_comp is not None and requested not in {"", "-1"}:
                    try:
                        requested_i = int(requested)
                    except ValueError:
                        requested_i = None
                    if requested_i is not None and requested_i > max_comp:
                        cfg_retry = dict(cfg)
                        cfg_retry["n_components"] = str(max_comp)
                        prep_cmd_retry = build_prep_cmd(cfg_retry, python_bin)
                        retry_code, _ = run_cmd_capture(prep_cmd_retry)
                        if retry_code == 0:
                            cfg = cfg_retry
                            prep_code = 0
                        else:
                            prep_code = retry_code

            if prep_code != 0:
                queue_retry_or_fail(
                    run_status_csv,
                    next_run_id,
                    f"prepare failed (exit={prep_code})",
                    attempts,
                    stage_by_run_id=stage_by_run_id,
                )
                continue

            cuda_device = cuda_devices[rr_idx % len(cuda_devices)] if cuda_devices else None
            rr_idx += 1
            train_cmd = build_train_cmd(cfg, next_run_id, python_bin, cuda_device=cuda_device)
            pid = run_cmd_background(train_cmd)
            run_gpu_map[next_run_id] = {
                "cuda_device": cuda_device or "",
                "pid": str(pid),
                "launched_at": now_iso(),
                "cmd": train_cmd,
            }
            save_run_gpu_map(run_gpu_map)
            append_event("train_launched", run_id=next_run_id, pid=pid, cuda_device=(cuda_device or ""))
            launched_any = True

        _, rows = read_csv(run_status_csv)
        running = [r for r in rows if r["status"] == "running"]
        next_run_id = pick_next_planned(rows, stage)
        if (not running) and (not next_run_id):
            print("No planned rows left for selected stage. Worker exits.")
            break
        if running or launched_any:
            time.sleep(sleep_sec)
            continue

        time.sleep(sleep_sec)


def parse_cuda_devices(arg: str) -> List[str]:
    parts = [x.strip() for x in (arg or "").split(",") if x.strip()]
    return parts or ["0"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run sweep rows continuously from run_status ledger.")
    parser.add_argument("--run_status_csv", type=Path, default=Path("sweeps/run_status.csv"))
    parser.add_argument("--stage1_csv", type=Path, default=Path("sweeps/stage1_screening_matrix.csv"))
    parser.add_argument("--stage2_csv", type=Path, default=Path("sweeps/stage2_confirmation_matrix.csv"))
    parser.add_argument("--stage", choices=["stage1", "stage2"], default=None)
    parser.add_argument("--sleep_sec", type=int, default=30)
    parser.add_argument("--stale_minutes", type=int, default=180)
    parser.add_argument("--smoke", action="store_true", help="Validate next-run selection and command generation without executing jobs.")
    parser.add_argument("--lock_path", type=Path, default=Path("sweeps/.run_sweep_worker.lock"))
    parser.add_argument("--require_cuda", action="store_true", default=True, help="Fail fast when CUDA is unavailable.")
    parser.add_argument("--allow_cpu", action="store_true", help="Override --require_cuda and allow CPU-only training.")
    parser.add_argument("--python_bin", type=str, default=".venv/bin/python")
    parser.add_argument("--max_concurrent", type=int, default=1, help="Maximum concurrent training jobs.")
    parser.add_argument("--cuda_devices", type=str, default="0", help="Comma-separated CUDA device IDs for round-robin assignment.")
    parser.add_argument("--progress_stale_minutes", type=int, default=20, help="Kill and retry running jobs when log artifacts stop updating.")
    args = parser.parse_args()

    _ensure_ops_dir()
    append_event(
        "worker_boot",
        stage=(args.stage or "all"),
        sleep_sec=args.sleep_sec,
        stale_minutes=args.stale_minutes,
        max_concurrent=args.max_concurrent,
        cuda_devices=args.cuda_devices,
    )
    acquire_lock(args.lock_path)

    run_worker(
        run_status_csv=args.run_status_csv,
        stage1_csv=args.stage1_csv,
        stage2_csv=args.stage2_csv,
        stage=args.stage,
        sleep_sec=args.sleep_sec,
        stale_minutes=args.stale_minutes,
        smoke=args.smoke,
        require_cuda=(args.require_cuda and (not args.allow_cpu)),
        python_bin=args.python_bin,
        max_concurrent=max(1, int(args.max_concurrent)),
        cuda_devices=parse_cuda_devices(args.cuda_devices),
        progress_stale_minutes=max(1, int(args.progress_stale_minutes)),
    )
    append_event("worker_exit", stage=(args.stage or "all"))


if __name__ == "__main__":
    main()
