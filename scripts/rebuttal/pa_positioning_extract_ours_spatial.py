#!/usr/bin/env python3
"""Extract and normalize our spatial findings (H11–H13) into a tidy CSV.

Inputs are evidence CSV snapshots under `results/ed20260217/paperjson/`.
No numbers are invented: all aggregates are computed directly from those CSVs.

Output schema (fixed):
- finding_id: H11 | H12 | H13
- setting: human-readable condition (includes frontend and K etc)
- metric: greedy_cer | greedy_rtf | lex_train_cer | lex_all_cer | delta_cer
- mean, std: sample std (ddof=1) when n>1
- n: number of seeds
- evidence_path: path to the source evidence CSV
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


def _to_float(v: str) -> float:
    try:
        return float(v)
    except Exception:
        raise ValueError(f"Expected float, got: {v!r}")


def _mean_std(xs: List[float]) -> Tuple[float, float]:
    if not xs:
        raise ValueError("Empty list")
    m = sum(xs) / len(xs)
    if len(xs) <= 1:
        return m, 0.0
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return m, math.sqrt(var)


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _extract_frontend_group_stats(
    rows: Iterable[Dict[str, str]],
    *,
    finding_id: str,
    evidence_path: str,
    allowed_frontends: List[str],
) -> List[Dict[str, str]]:
    groups: Dict[Tuple[str, str, str], List[Dict[str, str]]] = {}
    for r in rows:
        frontend = (r.get("frontend") or "").strip()
        if frontend not in allowed_frontends:
            continue
        subset_method = (r.get("subset_method") or "").strip()
        subset_k = (r.get("subset_K") or "").strip()
        key = (frontend, subset_method, subset_k)
        groups.setdefault(key, []).append(r)

    out: List[Dict[str, str]] = []
    for (frontend, subset_method, subset_k), rs in sorted(groups.items()):
        metrics = {
            "greedy_cer": [
                _to_float(x["greedy_cer"]) for x in rs if (x.get("greedy_cer") or "") != ""
            ],
            "greedy_rtf": [
                _to_float(x["greedy_rtf"]) for x in rs if (x.get("greedy_rtf") or "") != ""
            ],
            "lex_train_cer": [
                _to_float(x["lex_train_cer"])
                for x in rs
                if (x.get("lex_train_cer") or "") != ""
            ],
            "lex_all_cer": [
                _to_float(x["lex_all_cer"])
                for x in rs
                if (x.get("lex_all_cer") or "") != ""
            ],
        }

        for metric, xs in metrics.items():
            if not xs:
                continue
            mean, std = _mean_std(xs)
            out.append(
                {
                    "finding_id": finding_id,
                    "setting": f"subset_method={subset_method}, K={subset_k}, frontend={frontend}",
                    "metric": metric,
                    "mean": f"{mean}",
                    "std": f"{std}",
                    "n": str(len(xs)),
                    "evidence_path": evidence_path,
                }
            )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--h11_csv", required=True)
    ap.add_argument("--h12_csv", required=True)
    ap.add_argument("--h13_csv", required=True)
    ap.add_argument("--out_csv", required=True)
    args = ap.parse_args()

    h11_csv = Path(args.h11_csv)
    h12_csv = Path(args.h12_csv)
    h13_csv = Path(args.h13_csv)

    for p in [h11_csv, h12_csv, h13_csv]:
        if not p.exists():
            raise FileNotFoundError(p)

    out_rows: List[Dict[str, str]] = []

    # H11: vector vs spatial2d (grouped across seeds).
    h11_rows = _read_csv(h11_csv)
    out_rows.extend(
        _extract_frontend_group_stats(
            h11_rows,
            finding_id="H11",
            evidence_path=str(h11_csv),
            allowed_frontends=["vector", "spatial2d"],
        )
    )

    # H12: spatial augmentation vs dropout degradation summary (already aggregated).
    h12_rows = _read_csv(h12_csv)
    required_cols = [
        "protocol",
        "subset_id",
        "subset_method",
        "subset_K",
        "model_family",
        "enable_spatial_aug",
        "drop_rate",
        "delta_cer_mean",
        "delta_cer_std",
        "n_seeds",
    ]
    for c in required_cols:
        if c not in (h12_rows[0].keys() if h12_rows else {}):
            raise KeyError(f"H12 CSV missing column: {c}")

    for r in h12_rows:
        mean = _to_float(r["delta_cer_mean"])
        std = _to_float(r["delta_cer_std"])
        n = int(float(r["n_seeds"]))
        setting = (
            f"subset_method={r['subset_method']}, K={r['subset_K']}, "
            f"enable_spatial_aug={r['enable_spatial_aug']}, drop_rate={r['drop_rate']}"
        )
        out_rows.append(
            {
                "finding_id": "H12",
                "setting": setting,
                "metric": "delta_cer",
                "mean": f"{mean}",
                "std": f"{std}",
                "n": str(n),
                "evidence_path": str(h12_csv),
            }
        )

    # H13: vector vs rowcol (grouped across seeds).
    h13_rows = _read_csv(h13_csv)
    out_rows.extend(
        _extract_frontend_group_stats(
            h13_rows,
            finding_id="H13",
            evidence_path=str(h13_csv),
            allowed_frontends=["vector", "rowcol"],
        )
    )

    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    header = ["finding_id", "setting", "metric", "mean", "std", "n", "evidence_path"]
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print(f"Wrote {len(out_rows)} rows: {out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
