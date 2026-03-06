#!/usr/bin/env python3
"""Make transparent cmdlists from gap-closure matrix CSVs.

This utility does not execute commands.

Modes
- prep: dataset preparation (deduplicated by dataset_pickle)
- train_eval: train + greedy eval + lexicon evals (3 JSONs)

Output
- One cmdlist per GPU id (round-robin assignment).
- Comment lines (# ...) and blank lines are allowed by the runner.

Resume support
- With --resume (train_eval only):
  - Skip runs that are already complete (base or any _retryN).
  - If base log dir exists but is incomplete, schedule a new _retryN+1.
  - Never overwrites existing log dirs.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


THREAD_CAP_ENV = {
    "OMP_NUM_THREADS": "8",
    "MKL_NUM_THREADS": "8",
    "OPENBLAS_NUM_THREADS": "8",
    "NUMEXPR_NUM_THREADS": "8",
    "PYTHONUNBUFFERED": "1",
}

RETRY_RE = re.compile(r"^(?P<base>.+)_retry(?P<n>\d+)$")


def _env_hint() -> str:
    return " ".join([f"{k}={v}" for k, v in THREAD_CAP_ENV.items()])


def _read_rows(paths: Sequence[Path]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for p in paths:
        with p.open("r", newline="") as f:
            rows.extend(list(csv.DictReader(f)))
    return rows


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


def _boolish(v: str) -> bool:
    return (v or "").strip() in {"1", "true", "True", "yes", "YES"}


def _maybe_int(v: str) -> Optional[int]:
    s = (v or "").strip()
    if not s:
        return None
    return int(s)


def _is_complete(run_dir: Path, *, require_lex: bool) -> bool:
    if not (run_dir / "eval_greedy_test.json").exists():
        return False
    if require_lex:
        if not (run_dir / "eval_lex_train.json").exists():
            return False
        if not (run_dir / "eval_lex_all.json").exists():
            return False
    return True


def _max_retry_n(logs_dir: Path, run_id_base: str) -> int:
    max_n = 0
    for p in logs_dir.glob(f"{run_id_base}_retry*"):
        if not p.is_dir():
            continue
        m = RETRY_RE.match(p.name)
        if not m:
            continue
        try:
            n = int(m.group("n"))
        except Exception:
            continue
        max_n = max(max_n, n)
    return max_n


def _select_run_id_for_resume(logs_dir: Path, run_id_base: str, *, require_lex: bool) -> Optional[str]:
    """Return run_id to execute, or None if a complete run already exists."""

    base_dir = logs_dir / run_id_base

    # If base is complete, skip.
    if base_dir.exists() and _is_complete(base_dir, require_lex=require_lex):
        return None

    # If any retry is complete, skip.
    for p in logs_dir.glob(f"{run_id_base}_retry*"):
        if not p.is_dir():
            continue
        m = RETRY_RE.match(p.name)
        if not m:
            continue
        if _is_complete(p, require_lex=require_lex):
            return None

    # If base does not exist, schedule base.
    if not base_dir.exists():
        return run_id_base

    # Base exists but is incomplete: schedule next retry.
    next_n = _max_retry_n(logs_dir, run_id_base) + 1
    return f"{run_id_base}_retry{next_n}"


def _dataset_prep_cmd(row: Dict[str, str], python_bin: str) -> str:
    cmd: List[str] = [
        python_bin,
        "scripts/prepare_silentspeller_dataset.py",
        "--split_path",
        row["split_npz"],
        "--n_components",
        row["n_components"],
        "--downsample_factor",
        row["downsample_factor"],
        "--electrode_regions",
    ]
    # electrode_regions is space-separated (e.g., "anterior middle")
    cmd.extend([p for p in (row["electrode_regions"] or "all").split() if p])

    if _boolish(row.get("apply_ts2vec", "0")):
        cmd.append("--apply_ts2vec")
        out_dims = row.get("ts2vec_output_dims", "") or "320"
        epochs = row.get("ts2vec_epochs", "") or "100"
        hidden = row.get("ts2vec_hidden_dims", "") or "64"
        depth = row.get("ts2vec_depth", "") or "10"
        batch = row.get("ts2vec_batch_size", "") or "16"
        cmd.extend(["--ts2vec_output_dims", str(out_dims)])
        cmd.extend(["--ts2vec_epochs", str(epochs)])
        cmd.extend(["--ts2vec_hidden_dims", str(hidden)])
        cmd.extend(["--ts2vec_depth", str(depth)])
        cmd.extend(["--ts2vec_batch_size", str(batch)])

    cmd.extend(["--output_path", row["dataset_pickle"]])
    return " ".join(cmd)


def _train_cmd(row: Dict[str, str], python_bin: str) -> str:
    model_family = (row.get("model_family", "") or "gru").strip()
    cmd: List[str] = [
        python_bin,
        "scripts/train.py",
        "--dataset_path",
        row["dataset_pickle"],
        "--run_id",
        row["run_id"],
        "--model_family",
        model_family,
        "--n_units",
        row["n_units"],
        "--n_layers",
        row["n_layers"],
        "--stride_len",
        row["stride_len"],
        "--kernel_len",
        row["kernel_len"],
        "--n_batch",
        row["n_batch"],
        "--seed",
        row["train_seed"],
        "--white_noise_sd",
        row.get("white_noise_sd", "0.8") or "0.8",
        "--constant_offset_sd",
        row.get("constant_offset_sd", "0.2") or "0.2",
        "--gaussian_smooth_width",
        row.get("gaussian_smooth_width", "2.0") or "2.0",
        "--disable_day_embed",
    ]

    input_proj_dim = _maybe_int(row.get("input_proj_dim", ""))
    if input_proj_dim is not None:
        cmd.extend(["--input_proj_dim", str(input_proj_dim)])

    # Always pass these if present (train.py supports them for all families).
    for k, flag in [
        ("tcn_layers", "--tcn_layers"),
        ("tcn_kernel_size", "--tcn_kernel_size"),
        ("transformer_heads", "--transformer_heads"),
        ("transformer_layers", "--transformer_layers"),
        ("transformer_ff_mult", "--transformer_ff_mult"),
    ]:
        v = row.get(k, "").strip()
        if v:
            cmd.extend([flag, v])

    if (row.get("specaug_on", "").strip() or "0") in {"1", "true", "True"}:
        cmd.append("--enable_online_specaug")

    if _boolish(row.get("enable_spatial_aug", "0")):
        cmd.append("--enable_spatial_aug")

    return " ".join(cmd)


def _eval_cmds(row: Dict[str, str], python_bin: str, device: str) -> List[str]:
    rid = row["run_id"]
    root = f"logs/{rid}"
    greedy_json = f"{root}/eval_greedy_test.json"
    frame_ms = (row.get("frame_ms", "") or "10.0").strip() or "10.0"

    return [
        f"{python_bin} scripts/rebuttal/eval_greedy_clean.py --model_path {root} --partition test --device {device} --frame_ms {frame_ms} --out_json {greedy_json}",
        f"{python_bin} scripts/rebuttal/eval_lexicon_project.py --pred_json {greedy_json} --lexicon_source train --out_json {root}/eval_lex_train.json",
        f"{python_bin} scripts/rebuttal/eval_lexicon_project.py --pred_json {greedy_json} --lexicon_source all --out_json {root}/eval_lex_all.json",
    ]


def _write_cmdlist(path: Path, lines: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for line in lines:
            f.write(line.rstrip() + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate cmdlists from gap-closure matrices.")
    ap.add_argument("--matrix_csv", type=Path, nargs="+", required=True)
    ap.add_argument("--mode", type=str, required=True, choices=["prep", "train_eval"])
    ap.add_argument("--gpus", type=str, required=True, help="Comma-separated GPU ids (e.g., 0,1,2,3)")
    ap.add_argument("--out_dir", type=Path, default=Path("sweeps/gc20260216/cmds"))
    ap.add_argument(
        "--name",
        type=str,
        default=None,
        help="Output prefix. Defaults to matrix stem (single) or gc (multi).",
    )
    ap.add_argument("--python_bin", type=str, default=".venv/bin/python")
    ap.add_argument("--device", type=str, default="cuda", help="Device string passed to eval scripts (default: cuda)")

    # Resume helpers (train_eval only)
    ap.add_argument("--resume", action="store_true", help="Skip complete runs; retry incomplete ones with _retryN.")
    ap.add_argument("--logs_dir", type=Path, default=Path("logs"))
    ap.add_argument("--allow_missing_lex", action="store_true", help="Treat greedy-only as complete (not recommended).")
    args = ap.parse_args()

    gpus = _parse_gpus(args.gpus)
    rows = _read_rows(args.matrix_csv)
    if not rows:
        raise SystemExit("No rows loaded from matrix CSV(s).")

    name = args.name
    if not name:
        if len(args.matrix_csv) == 1:
            name = args.matrix_csv[0].stem
        else:
            name = "gc"

    if args.mode == "prep":
        # Deduplicate by dataset_pickle path.
        seen = set()
        items: List[Tuple[str, List[str]]] = []
        for r in rows:
            dp = (r.get("dataset_pickle") or "").strip()
            if not dp or dp in seen:
                continue
            seen.add(dp)
            cmd = _dataset_prep_cmd(r, args.python_bin)
            items.append((dp, [cmd]))

        assigned: Dict[int, List[Tuple[str, List[str]]]] = {g: [] for g in gpus}
        for idx, item in enumerate(items):
            g = gpus[idx % len(gpus)]
            assigned[g].append(item)

        for g in gpus:
            out_path = args.out_dir / f"{name}.prep.gpu{g}.txt"
            lines: List[str] = []
            lines.append(f"# mode=prep rows={len(rows)} unique_dataset_pickles={len(items)}")
            lines.append(f"# env_hint={_env_hint()}")
            lines.append("")
            for dp, cmds in assigned[g]:
                lines.append(f"# dataset_pickle={dp}")
                lines.extend(cmds)
                lines.append("")
            _write_cmdlist(out_path, lines)
            print(f"Wrote {out_path} ({len(assigned[g])} prep cmds)")
        return

    # train_eval
    require_lex = not args.allow_missing_lex

    run_items: List[Tuple[str, str, List[str]]] = []
    skipped_complete = 0
    scheduled_base = 0
    scheduled_retry = 0

    for r in rows:
        base_rid = (r.get("run_id") or "").strip()
        if not base_rid:
            continue

        rid = base_rid
        if args.resume:
            sel = _select_run_id_for_resume(args.logs_dir, base_rid, require_lex=require_lex)
            if sel is None:
                skipped_complete += 1
                continue
            rid = sel

        row_use = dict(r)
        row_use["run_id"] = rid
        cmds = [_train_cmd(row_use, args.python_bin)] + _eval_cmds(row_use, args.python_bin, device=args.device)

        if args.resume:
            if rid == base_rid:
                scheduled_base += 1
            else:
                scheduled_retry += 1

        run_items.append((base_rid, rid, cmds))

    assigned2: Dict[int, List[Tuple[str, str, List[str]]]] = {g: [] for g in gpus}
    for idx, item in enumerate(run_items):
        g = gpus[idx % len(gpus)]
        assigned2[g].append(item)

    for g in gpus:
        out_path = args.out_dir / f"{name}.train_eval.gpu{g}.txt"
        lines: List[str] = [
            f"# mode=train_eval rows={len(rows)}",
            f"# device={args.device}",
            f"# env_hint={_env_hint()}",
        ]
        if args.resume:
            lines.append(
                f"# resume=1 skipped_complete={skipped_complete} scheduled_base={scheduled_base} scheduled_retry={scheduled_retry} require_lex={1 if require_lex else 0}"
            )
        lines.append("")

        for base_rid, rid, cmds in assigned2[g]:
            if args.resume and rid != base_rid:
                lines.append(f"# run_id_base={base_rid}")
                lines.append(f"# run_id={rid}")
            else:
                lines.append(f"# run_id={rid}")
            lines.extend(cmds)
            lines.append("")

        _write_cmdlist(out_path, lines)
        print(f"Wrote {out_path} ({len(assigned2[g])} runs)")


if __name__ == "__main__":
    main()
