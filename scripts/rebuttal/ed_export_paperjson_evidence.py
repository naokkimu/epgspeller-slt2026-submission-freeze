#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class EvalMetrics:
    cer: float
    wer: float
    rtf: Optional[float]
    chunk_latency_ms: Optional[float]
    end_to_end_latency_ms: Optional[float]
    first_output_latency_ms: Optional[float]
    streaming_ready: Optional[bool]
    param_count: Optional[int]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _as_float(d: Dict[str, Any], key: str) -> Optional[float]:
    v = d.get(key)
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        return None


def _as_int(d: Dict[str, Any], key: str) -> Optional[int]:
    v = d.get(key)
    if v is None:
        return None
    try:
        return int(v)
    except Exception:
        return None


def _load_eval_metrics(path: Path) -> EvalMetrics:
    d = _load_json(path)
    if not isinstance(d, dict):
        raise ValueError(f"eval json must be an object: {path}")

    cer = float(d["cer"])
    wer = float(d["wer"])

    sm = d.get("streaming_metrics")
    if sm is None or not isinstance(sm, dict):
        sm = {}

    return EvalMetrics(
        cer=cer,
        wer=wer,
        rtf=_as_float(sm, "rtf"),
        chunk_latency_ms=_as_float(sm, "chunk_latency_ms"),
        end_to_end_latency_ms=_as_float(sm, "end_to_end_latency_ms"),
        first_output_latency_ms=_as_float(sm, "first_output_latency_ms"),
        streaming_ready=(bool(sm.get("streaming_ready")) if "streaming_ready" in sm else None),
        param_count=_as_int(d, "param_count"),
    )


def _read_matrix_rows(matrix_csv: Path) -> List[Dict[str, str]]:
    with matrix_csv.open(newline="") as f:
        return list(csv.DictReader(f))


def _filter_rows(
    rows: Sequence[Dict[str, str]],
    *,
    protocol: str,
    model_family: str,
    subset_ids: Sequence[str],
) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    subset_set = {s.strip() for s in subset_ids}
    for r in rows:
        if r.get("protocol", "").strip() != protocol:
            continue
        if r.get("model_family", "").strip() != model_family:
            continue
        if r.get("subset_id", "").strip() not in subset_set:
            continue
        out.append(r)
    return out


def _mean_std_sample(xs: Sequence[float]) -> Tuple[float, float]:
    if not xs:
        raise ValueError("mean/std requires at least 1 value")
    m = sum(xs) / len(xs)
    if len(xs) == 1:
        return m, 0.0
    v = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return m, v ** 0.5


def export_h13_rowcol_vs_vector(
    *,
    repo_root: Path,
    out_csv: Path,
    snapshot_date: str,
) -> None:
    subset_ids = ["topk_k32", "fps2k_k32", "topk_k64", "fps2k_k64"]

    vector_matrix = repo_root / "sweeps/ed20260217/matrices/ed_p1_kcurve_deterministic.csv"
    rowcol_matrix = repo_root / "sweeps/ed20260217/matrices/ed_p1_rowcol_compare.csv"

    vector_rows = _filter_rows(
        _read_matrix_rows(vector_matrix),
        protocol="P1",
        model_family="uni_gru",
        subset_ids=subset_ids,
    )
    rowcol_rows = _filter_rows(
        _read_matrix_rows(rowcol_matrix),
        protocol="P1",
        model_family="rowcol_uni_gru",
        subset_ids=subset_ids,
    )

    if len(vector_rows) != 16:
        raise ValueError(f"Expected 16 vector rows (4 subsets x 4 seeds), got {len(vector_rows)}")
    if len(rowcol_rows) != 16:
        raise ValueError(f"Expected 16 rowcol rows (4 subsets x 4 seeds), got {len(rowcol_rows)}")

    out_csv.parent.mkdir(parents=True, exist_ok=True)

    records: List[Dict[str, Any]] = []

    def add_rows(rows: Sequence[Dict[str, str]], *, frontend: str, matrix_path: Path) -> None:
        for r in rows:
            run_id = r["run_id"].strip()
            split_id = r.get("split_id", "").strip()
            subset_id = r.get("subset_id", "").strip()
            subset_method = r.get("subset_method", "").strip()
            subset_K = r.get("subset_K", "").strip()
            model_family = r.get("model_family", "").strip()

            log_dir = repo_root / "logs" / run_id
            greedy_path = log_dir / "eval_greedy_test.json"
            lex_train_path = log_dir / "eval_lex_train.json"
            lex_all_path = log_dir / "eval_lex_all.json"

            for p in (greedy_path, lex_train_path, lex_all_path):
                if not p.exists():
                    raise FileNotFoundError(f"Missing required eval file: {p}")

            greedy = _load_eval_metrics(greedy_path)
            lex_train = _load_eval_metrics(lex_train_path)
            lex_all = _load_eval_metrics(lex_all_path)

            records.append(
                {
                    "snapshot_date": snapshot_date,
                    "protocol": "P1",
                    "split_id": split_id,
                    "subset_id": subset_id,
                    "subset_method": subset_method,
                    "subset_K": int(subset_K) if subset_K else "",
                    "frontend": frontend,
                    "model_family": model_family,
                    "run_id": run_id,
                    "matrix_csv": str(matrix_path),
                    "greedy_cer": greedy.cer,
                    "greedy_wer": greedy.wer,
                    "greedy_rtf": greedy.rtf,
                    "greedy_chunk_latency_ms": greedy.chunk_latency_ms,
                    "greedy_end_to_end_latency_ms": greedy.end_to_end_latency_ms,
                    "greedy_first_output_latency_ms": greedy.first_output_latency_ms,
                    "greedy_streaming_ready": greedy.streaming_ready,
                    "param_count": greedy.param_count,
                    "lex_train_cer": lex_train.cer,
                    "lex_train_wer": lex_train.wer,
                    "lex_all_cer": lex_all.cer,
                    "lex_all_wer": lex_all.wer,
                }
            )

    add_rows(vector_rows, frontend="vector", matrix_path=vector_matrix)
    add_rows(rowcol_rows, frontend="rowcol", matrix_path=rowcol_matrix)

    # Deterministic ordering
    records.sort(
        key=lambda x: (
            str(x["frontend"]),
            str(x["subset_id"]),
            int(x["subset_K"]) if isinstance(x["subset_K"], int) else -1,
            str(x["split_id"]),
            str(x["run_id"]),
        )
    )

    fieldnames = list(records[0].keys()) if records else []
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for rec in records:
            w.writerow(rec)


def export_h11_spatial2d_vs_vector(
    *,
    repo_root: Path,
    out_csv: Path,
    snapshot_date: str,
) -> None:
    subset_ids = [
        "topk_k32",
        "fps2k_k32",
        "topk_k64",
        "fps2k_k64",
        "topk_k96",
        "fps2k_k96",
        "el-all",
    ]

    vector_kcurve_matrix = repo_root / "sweeps/ed20260217/matrices/ed_p1_kcurve_deterministic.csv"
    vector_baseline_matrix = repo_root / "sweeps/gc20260216/matrices/gc_baseline.csv"
    spatial2d_matrix = repo_root / "sweeps/ed20260217/matrices/ed_p1_spatial2d_compare.csv"

    vector_rows = _filter_rows(
        _read_matrix_rows(vector_kcurve_matrix),
        protocol="P1",
        model_family="uni_gru",
        subset_ids=[s for s in subset_ids if s != "el-all"],
    )
    if len(vector_rows) != 24:
        raise ValueError(f"Expected 24 vector rows (6 subsets x 4 seeds), got {len(vector_rows)}")

    baseline_rows_raw = _read_matrix_rows(vector_baseline_matrix)
    baseline_rows: List[Dict[str, str]] = []
    for r in baseline_rows_raw:
        if r.get("protocol", "").strip() != "P1":
            continue
        if r.get("model_family", "").strip() != "uni_gru":
            continue
        if r.get("electrode_regions", "").strip() != "all":
            continue
        split_id = r.get("split_id", "").strip()
        if split_id not in {"seed0", "seed1", "seed2", "seed3"}:
            continue
        baseline_rows.append(r)
    baseline_rows.sort(key=lambda x: x.get("split_id", ""))
    if len(baseline_rows) != 4:
        raise ValueError(f"Expected 4 baseline rows (P1 seed0-3), got {len(baseline_rows)}")

    spatial2d_rows = _filter_rows(
        _read_matrix_rows(spatial2d_matrix),
        protocol="P1",
        model_family="spatial2d_uni_gru",
        subset_ids=subset_ids,
    )
    if len(spatial2d_rows) != 28:
        raise ValueError(f"Expected 28 spatial2d rows (6 subsets + el-all) x 4 seeds, got {len(spatial2d_rows)}")

    out_csv.parent.mkdir(parents=True, exist_ok=True)

    records: List[Dict[str, Any]] = []

    def add_row(
        *,
        run_id: str,
        split_id: str,
        subset_id: str,
        subset_method: str,
        subset_K: int,
        frontend: str,
        model_family: str,
        matrix_path: Path,
    ) -> None:
        log_dir = repo_root / "logs" / run_id
        greedy_path = log_dir / "eval_greedy_test.json"
        lex_train_path = log_dir / "eval_lex_train.json"
        lex_all_path = log_dir / "eval_lex_all.json"

        for p in (greedy_path, lex_train_path, lex_all_path):
            if not p.exists():
                raise FileNotFoundError(f"Missing required eval file: {p}")

        greedy = _load_eval_metrics(greedy_path)
        lex_train = _load_eval_metrics(lex_train_path)
        lex_all = _load_eval_metrics(lex_all_path)

        records.append(
            {
                "snapshot_date": snapshot_date,
                "protocol": "P1",
                "split_id": split_id,
                "subset_id": subset_id,
                "subset_method": subset_method,
                "subset_K": subset_K,
                "frontend": frontend,
                "model_family": model_family,
                "run_id": run_id,
                "matrix_csv": str(matrix_path),
                "greedy_cer": greedy.cer,
                "greedy_wer": greedy.wer,
                "greedy_rtf": greedy.rtf,
                "greedy_chunk_latency_ms": greedy.chunk_latency_ms,
                "greedy_end_to_end_latency_ms": greedy.end_to_end_latency_ms,
                "greedy_first_output_latency_ms": greedy.first_output_latency_ms,
                "greedy_streaming_ready": greedy.streaming_ready,
                "param_count": greedy.param_count,
                "lex_train_cer": lex_train.cer,
                "lex_train_wer": lex_train.wer,
                "lex_all_cer": lex_all.cer,
                "lex_all_wer": lex_all.wer,
            }
        )

    for r in vector_rows:
        add_row(
            run_id=r["run_id"].strip(),
            split_id=r.get("split_id", "").strip(),
            subset_id=r.get("subset_id", "").strip(),
            subset_method=r.get("subset_method", "").strip(),
            subset_K=int(r.get("subset_K", "0") or "0"),
            frontend="vector",
            model_family=r.get("model_family", "").strip(),
            matrix_path=vector_kcurve_matrix,
        )

    for r in baseline_rows:
        add_row(
            run_id=r["run_id"].strip(),
            split_id=r.get("split_id", "").strip(),
            subset_id="el-all",
            subset_method="all",
            subset_K=124,
            frontend="vector",
            model_family=r.get("model_family", "").strip(),
            matrix_path=vector_baseline_matrix,
        )

    for r in spatial2d_rows:
        add_row(
            run_id=r["run_id"].strip(),
            split_id=r.get("split_id", "").strip(),
            subset_id=r.get("subset_id", "").strip(),
            subset_method=r.get("subset_method", "").strip(),
            subset_K=int(r.get("subset_K", "0") or "0"),
            frontend="spatial2d",
            model_family=r.get("model_family", "").strip(),
            matrix_path=spatial2d_matrix,
        )

    records.sort(
        key=lambda x: (
            str(x["frontend"]),
            str(x["subset_id"]),
            int(x["subset_K"]),
            str(x["split_id"]),
            str(x["run_id"]),
        )
    )

    fieldnames = list(records[0].keys()) if records else []
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for rec in records:
            w.writerow(rec)


def export_h12_spatial_aug_dropout_summary(
    *,
    repo_root: Path,
    out_csv: Path,
    snapshot_date: str,
) -> None:
    source_csv = repo_root / "sweeps/ed20260217/results/dropout_summary_spatial2d.csv"
    if not source_csv.exists():
        raise FileNotFoundError(f"Missing required source CSV: {source_csv}")

    # Group delta CER across seeds for each (spaug, drop_rate).
    grouped: Dict[Tuple[int, float], List[float]] = {}
    seeds_seen: Dict[Tuple[int, float], set[str]] = {}

    with source_csv.open(newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            run_id = (row.get("run_id") or "").strip()
            if not run_id:
                continue
            if "spatial2d_uni_gru" not in run_id:
                continue
            if "sub-topk_k64" not in run_id:
                continue
            if not run_id.startswith("P1_seed"):
                continue

            if "_spaug1_" in run_id:
                spaug = 1
            elif "_spaug0_" in run_id:
                spaug = 0
            else:
                raise ValueError(f"Could not parse spaug from run_id: {run_id}")

            try:
                drop_rate = float((row.get("drop_rate") or "").strip())
            except Exception as e:
                raise ValueError(f"Invalid drop_rate for run_id {run_id}: {row.get(drop_rate)} ({e})")

            try:
                delta_cer = float((row.get("delta_cer_mean") or "").strip())
            except Exception as e:
                raise ValueError(
                    f"Invalid delta_cer_mean for run_id {run_id}: {row.get(delta_cer_mean)} ({e})"
                )

            seed = run_id.split("_", 2)[1]  # seed0/seed1/...

            key = (spaug, drop_rate)
            grouped.setdefault(key, []).append(delta_cer)
            seeds_seen.setdefault(key, set()).add(seed)

    out_csv.parent.mkdir(parents=True, exist_ok=True)

    records: List[Dict[str, Any]] = []
    for (spaug, drop_rate), deltas in sorted(grouped.items(), key=lambda t: (t[0][0], t[0][1])):
        mean, std = _mean_std_sample(deltas)
        records.append(
            {
                "snapshot_date": snapshot_date,
                "protocol": "P1",
                "subset_id": "topk_k64",
                "subset_method": "topk",
                "subset_K": 64,
                "model_family": "spatial2d_uni_gru",
                "enable_spatial_aug": spaug,
                "drop_rate": drop_rate,
                "delta_cer_mean": mean,
                "delta_cer_std": std,
                "n_seeds": len(seeds_seen.get((spaug, drop_rate), set())),
                "source_csv": str(source_csv),
            }
        )

    fieldnames = list(records[0].keys()) if records else []
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for rec in records:
            w.writerow(rec)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--export",
        default="h13_rowcol_vs_vector",
        choices=[
            "h13_rowcol_vs_vector",
            "h11_spatial2d_vs_vector",
            "h12_spatial_aug_dropout_summary",
        ],
        help="Which evidence table to export.",
    )
    p.add_argument(
        "--out_csv",
        required=True,
        help="Output CSV path (recommended under results/ or artifacts/)",
    )
    p.add_argument(
        "--snapshot_date",
        required=True,
        help="Snapshot date string (e.g., 2026-02-17)",
    )
    args = p.parse_args(argv)

    repo_root = Path(".").resolve()
    out_csv = Path(args.out_csv)

    if args.export == "h13_rowcol_vs_vector":
        export_h13_rowcol_vs_vector(repo_root=repo_root, out_csv=out_csv, snapshot_date=args.snapshot_date)
    elif args.export == "h11_spatial2d_vs_vector":
        export_h11_spatial2d_vs_vector(repo_root=repo_root, out_csv=out_csv, snapshot_date=args.snapshot_date)
    elif args.export == "h12_spatial_aug_dropout_summary":
        export_h12_spatial_aug_dropout_summary(
            repo_root=repo_root, out_csv=out_csv, snapshot_date=args.snapshot_date
        )
    else:
        raise ValueError(f"Unknown export: {args.export}")

    sha = _sha256_file(out_csv)
    print(f"Wrote: {out_csv}")
    print(f"sha256: {sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
