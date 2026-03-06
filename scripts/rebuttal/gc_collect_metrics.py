#!/usr/bin/env python3
"""Collect metrics from matrix CSV(s) + logs/<run_id>/eval_*.json.

This produces a tidy CSV suitable for plotting and reporting.

Features
- Supports retry suffix: if <run_id>_retryN exists and is complete, prefer the highest N.
- Validates required eval artifacts.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


RETRY_RE = re.compile(r"^(?P<base>.+)_retry(?P<n>\d+)$")


def _read_rows(paths: Sequence[Path]) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for p in paths:
        with p.open("r", newline="") as f:
            out.extend(list(csv.DictReader(f)))
    return out


def _load_json(path: Path) -> Dict:
    return json.loads(path.read_text())


def _to_float(v) -> Optional[float]:
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        return None


def _find_run_dir(logs_dir: Path, run_id_base: str, *, require_lex: bool) -> Tuple[Path, str]:
    """Return (run_dir, run_id_used)."""

    def _is_complete(run_dir: Path) -> bool:
        g = run_dir / "eval_greedy_test.json"
        if not g.exists():
            return False
        if require_lex:
            if not (run_dir / "eval_lex_train.json").exists():
                return False
            if not (run_dir / "eval_lex_all.json").exists():
                return False
        return True

    candidates: List[Tuple[int, str, Path]] = []

    base_dir = logs_dir / run_id_base
    if base_dir.exists():
        candidates.append((0, run_id_base, base_dir))

    glob_pat = f"{run_id_base}_retry*"
    for p in logs_dir.glob(glob_pat):
        if not p.is_dir():
            continue
        m = RETRY_RE.match(p.name)
        if not m:
            continue
        try:
            n = int(m.group("n"))
        except Exception:
            continue
        candidates.append((n, p.name, p))

    # Prefer the highest retry number that is complete.
    for n, rid, p in sorted(candidates, key=lambda x: x[0], reverse=True):
        if _is_complete(p):
            return p, rid

    # If nothing complete, return base if it exists (for diagnostics).
    if base_dir.exists():
        return base_dir, run_id_base

    raise FileNotFoundError(f"No log dir found for run_id base: {run_id_base}")


def _extract_greedy_metrics(payload: Dict) -> Dict[str, str]:
    sm = payload.get("streaming_metrics", {}) if isinstance(payload, dict) else {}
    out = {
        "greedy_test_cer": str(payload.get("cer", "")),
        "greedy_test_wer": str(payload.get("wer", "")),
        "n_samples": str(payload.get("n_samples", "")),
        "total_chars": str(payload.get("total_chars", "")),
        "total_edits": str(payload.get("total_edits", "")),
        "param_count": str(payload.get("param_count", "")),
        "train_seed": str(payload.get("seed", "")),
        "split_seed": str(payload.get("split_seed", "")),
        "stream_rtf": str(sm.get("rtf", "")),
        "stream_chunk_latency_ms": str(sm.get("chunk_latency_ms", "")),
        "stream_end_to_end_latency_ms": str(sm.get("end_to_end_latency_ms", "")),
        "stream_first_output_latency_ms": str(sm.get("first_output_latency_ms", "")),
        "stream_model_family": str(sm.get("model_family", "")),
        "stream_streaming_ready": str(sm.get("streaming_ready", "")),
    }
    return out


def _extract_lex_metrics(payload: Dict, prefix: str) -> Dict[str, str]:
    return {
        f"{prefix}_cer": str(payload.get("cer", "")),
        f"{prefix}_wer": str(payload.get("wer", "")),
        f"{prefix}_lexicon_source": str(payload.get("lexicon_source", "")),
        f"{prefix}_lexicon_size": str(payload.get("lexicon_size", "")),
    }


def _write_csv(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def main() -> None:
    ap = argparse.ArgumentParser(description="Collect eval metrics into a tidy results CSV.")
    ap.add_argument("--matrix_csv", type=Path, nargs="+", required=True)
    ap.add_argument("--logs_dir", type=Path, default=Path("logs"))
    ap.add_argument("--out_csv", type=Path, default=None)
    ap.add_argument("--require_lex", action="store_true", help="Require eval_lex_train/all.json (default).")
    ap.add_argument("--allow_missing_lex", action="store_true", help="Only require greedy eval.")
    ap.add_argument(
        "--allow_incomplete",
        action="store_true",
        help="Write partial results even if some runs are missing/incomplete; write a missing report and exit 0.",
    )
    ap.add_argument(
        "--missing_out",
        type=Path,
        default=None,
        help="Write missing/incomplete run reasons (text). Default: <out_csv>.missing.txt",
    )
    args = ap.parse_args()

    require_lex = True
    if args.allow_missing_lex:
        require_lex = False
    if args.require_lex:
        require_lex = True

    rows = _read_rows(args.matrix_csv)
    if not rows:
        raise SystemExit("No rows found in matrix CSV(s).")

    if args.out_csv is None:
        if len(args.matrix_csv) == 1:
            name = args.matrix_csv[0].stem
        else:
            name = "gc_results"
        args.out_csv = Path(f"sweeps/gc20260216/results/{name}.results.csv")

    out_rows: List[Dict[str, str]] = []
    missing: List[str] = []

    for r in rows:
        run_id_base = (r.get("run_id") or "").strip()
        if not run_id_base:
            continue

        try:
            run_dir, run_id_used = _find_run_dir(args.logs_dir, run_id_base, require_lex=require_lex)
        except Exception as e:
            missing.append(f"{run_id_base}: {e}")
            continue

        greedy_path = run_dir / "eval_greedy_test.json"
        if not greedy_path.exists():
            missing.append(f"{run_id_base}: missing {greedy_path}")
            continue

        greedy = _load_json(greedy_path)
        lex_train_path = run_dir / "eval_lex_train.json"
        lex_all_path = run_dir / "eval_lex_all.json"

        if require_lex and (not lex_train_path.exists() or not lex_all_path.exists()):
            missing.append(
                f"{run_id_base}: missing lex evals (train={lex_train_path.exists()} all={lex_all_path.exists()})"
            )
            continue

        lex_train = _load_json(lex_train_path) if lex_train_path.exists() else {}
        lex_all = _load_json(lex_all_path) if lex_all_path.exists() else {}

        merged: Dict[str, str] = {}
        # Carry through key matrix columns (string form).
        for k, v in r.items():
            merged[k] = v

        merged["run_id_base"] = run_id_base
        merged["run_id_used"] = run_id_used
        merged["run_dir"] = str(run_dir)
        merged["eval_greedy_test_json"] = str(greedy_path)
        merged["eval_lex_train_json"] = str(lex_train_path) if lex_train_path.exists() else ""
        merged["eval_lex_all_json"] = str(lex_all_path) if lex_all_path.exists() else ""

        merged.update(_extract_greedy_metrics(greedy))
        if lex_train:
            merged.update(_extract_lex_metrics(lex_train, "lex_train"))
        if lex_all:
            merged.update(_extract_lex_metrics(lex_all, "lex_all"))

        out_rows.append(merged)

    if missing and not args.allow_incomplete:
        print("Missing or incomplete runs:")
        for m in missing[:50]:
            print("-", m)
        if len(missing) > 50:
            print(f"... ({len(missing) - 50} more)")
        raise SystemExit(2)
    if missing and args.allow_incomplete:
        print("Missing or incomplete runs (allow_incomplete=1):")
        for m in missing[:50]:
            print("-", m)
        if len(missing) > 50:
            print(f"... ({len(missing) - 50} more)")
        if args.missing_out is None:
            args.missing_out = args.out_csv.with_suffix(".missing.txt")
        args.missing_out.parent.mkdir(parents=True, exist_ok=True)
        args.missing_out.write_text("\n".join(missing) + "\n")
        print(f"Wrote missing report: {args.missing_out} ({len(missing)} missing)")

    if not out_rows:
        raise SystemExit("No complete runs found; nothing to write.")

    # Determine output schema: matrix columns + collected metrics.
    # NOTE: input matrices may have different columns (e.g., subset_id / ts2vec args).
    # Use an ordered union of all keys to avoid silently dropping columns that are not
    # present in the first matrix file.
    matrix_fields: List[str] = []
    for rr in rows:
        for k in rr.keys():
            if k not in matrix_fields:
                matrix_fields.append(k)

    metric_fields = [
        "run_id_base",
        "run_id_used",
        "run_dir",
        "eval_greedy_test_json",
        "eval_lex_train_json",
        "eval_lex_all_json",
        "greedy_test_cer",
        "greedy_test_wer",
        "lex_train_cer",
        "lex_train_wer",
        "lex_all_cer",
        "lex_all_wer",
        "param_count",
        "n_samples",
        "total_chars",
        "total_edits",
        "train_seed",
        "split_seed",
        "stream_rtf",
        "stream_chunk_latency_ms",
        "stream_end_to_end_latency_ms",
        "stream_first_output_latency_ms",
        "stream_model_family",
        "stream_streaming_ready",
        "lex_train_lexicon_source",
        "lex_train_lexicon_size",
        "lex_all_lexicon_source",
        "lex_all_lexicon_size",
    ]

    fieldnames = [
        *matrix_fields,
        *[f for f in metric_fields if f not in matrix_fields],
    ]

    _write_csv(args.out_csv, out_rows, fieldnames)
    print(f"Wrote {args.out_csv} ({len(out_rows)} rows)")


if __name__ == "__main__":
    main()
