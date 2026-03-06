#!/usr/bin/env python3
"""Collect eval_dropout_*.json into a tidy CSV for plotting/reporting."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from pathlib import Path
from typing import Dict, List, Tuple


def _read_json(path: Path) -> Dict:
    return json.loads(path.read_text())


def _mean_std(xs: List[float]) -> Tuple[float, float, int]:
    xs = [float(x) for x in xs if x is not None and not math.isnan(float(x))]
    if not xs:
        return float("nan"), float("nan"), 0
    if len(xs) == 1:
        return xs[0], float("nan"), 1
    return float(statistics.mean(xs)), float(statistics.stdev(xs)), len(xs)


def _write_csv(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def main() -> None:
    ap = argparse.ArgumentParser(description="Collect dropout eval JSONs into a summary CSV.")
    ap.add_argument("--run_ids", type=str, nargs="+", required=True, help="Base run_ids (directory names under logs/)")
    ap.add_argument("--logs_dir", type=Path, default=Path("logs"))
    ap.add_argument("--out_csv", type=Path, default=Path("sweeps/ed20260217/results/dropout_summary.csv"))
    args = ap.parse_args()

    rows: List[Dict[str, str]] = []

    for rid in args.run_ids:
        run_dir = args.logs_dir / rid
        if not run_dir.exists():
            raise SystemExit(f"run_dir not found: {run_dir}")
        files = sorted(run_dir.glob("eval_dropout_q*_rep*.json"))
        if not files:
            raise SystemExit(f"No dropout eval JSONs found under {run_dir}")

        # group by drop_rate
        by_q: Dict[float, List[Dict]] = {}
        for p in files:
            payload = _read_json(p)
            q = float(payload["drop_rate"])
            by_q.setdefault(q, []).append(payload)

        for q, recs in sorted(by_q.items(), key=lambda t: t[0]):
            masked_cers = [float(r["masked_cer"]) for r in recs]
            masked_wers = [float(r["masked_wer"]) for r in recs]
            deltas = [r.get("delta_cer") for r in recs if r.get("delta_cer") is not None]
            baseline = recs[0].get("baseline_cer")

            m_cer, s_cer, n = _mean_std(masked_cers)
            m_wer, s_wer, _ = _mean_std(masked_wers)
            m_d, s_d, n_d = _mean_std([float(x) for x in deltas]) if deltas else (float("nan"), float("nan"), 0)

            rows.append(
                {
                    "run_id": rid,
                    "drop_rate": f"{q:.3f}",
                    "n_reps": str(n),
                    "baseline_cer": f"{float(baseline):.6f}" if baseline is not None else "",
                    "masked_cer_mean": f"{m_cer:.6f}",
                    "masked_cer_std": f"{s_cer:.6f}" if not math.isnan(s_cer) else "nan",
                    "masked_wer_mean": f"{m_wer:.6f}",
                    "masked_wer_std": f"{s_wer:.6f}" if not math.isnan(s_wer) else "nan",
                    "delta_cer_mean": f"{m_d:.6f}" if not math.isnan(m_d) else "nan",
                    "delta_cer_std": f"{s_d:.6f}" if not math.isnan(s_d) else "nan",
                    "delta_cer_n": str(n_d),
                }
            )

    fieldnames = [
        "run_id",
        "drop_rate",
        "n_reps",
        "baseline_cer",
        "masked_cer_mean",
        "masked_cer_std",
        "masked_wer_mean",
        "masked_wer_std",
        "delta_cer_mean",
        "delta_cer_std",
        "delta_cer_n",
    ]
    _write_csv(args.out_csv, rows, fieldnames)
    print(f"Wrote {args.out_csv} ({len(rows)} rows)")


if __name__ == "__main__":
    main()

