#!/usr/bin/env python3
"""
Aggregate run metrics from sweep run_status CSV.

Expected usage:
  - Stage-1 ranking by greedy_test_cer
  - Stage-2 mean/std per protocol
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
from typing import Dict, List, Set


def _read_rows(csv_path: Path) -> List[Dict[str, str]]:
    with csv_path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _read_run_ids(csv_path: Path | None) -> Set[str]:
    if csv_path is None:
        return set()
    if not csv_path.exists():
        return set()
    rows = _read_rows(csv_path)
    return {r.get("run_id", "") for r in rows if r.get("run_id", "")}


def _to_float(v: str) -> float | None:
    s = (v or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _fmt_stats(xs: List[float]) -> str:
    if not xs:
        return "n=0"
    if len(xs) == 1:
        return f"mean={xs[0]:.4f}, std=nan, n=1"
    return f"mean={mean(xs):.4f}, std={stdev(xs):.4f}, n={len(xs)}"


def _read_streaming_metrics(eval_json_path: str) -> Dict[str, float | None]:
    p = Path(eval_json_path or "")
    if not p.exists():
        return {"rtf": None, "chunk_latency_ms": None, "end_to_end_latency_ms": None}
    try:
        payload = json.loads(p.read_text())
    except Exception:
        return {"rtf": None, "chunk_latency_ms": None, "end_to_end_latency_ms": None}
    sm = payload.get("streaming_metrics", {}) if isinstance(payload, dict) else {}
    return {
        "rtf": _to_float(str(sm.get("rtf", ""))),
        "chunk_latency_ms": _to_float(str(sm.get("chunk_latency_ms", ""))),
        "end_to_end_latency_ms": _to_float(str(sm.get("end_to_end_latency_ms", ""))),
    }


def stage1_rank(rows: List[Dict[str, str]], stage1_ids: Set[str]) -> None:
    if stage1_ids:
        stage1 = [r for r in rows if r.get("run_id", "") in stage1_ids]
    else:
        stage1 = [r for r in rows if "stage1" in (r.get("error_note") or "")]
    scored = []
    for r in stage1:
        cer = _to_float(r.get("greedy_test_cer", ""))
        if cer is None:
            continue
        sm = _read_streaming_metrics(r.get("eval_greedy_test_json", ""))
        scored.append((cer, r["run_id"], r.get("protocol", ""), sm["rtf"], sm["chunk_latency_ms"]))
    scored.sort(key=lambda x: x[0])
    print("== Stage-1 ranking by greedy_test_cer ==")
    if not scored:
        print("No completed Stage-1 CER values yet.")
        return
    for idx, (cer, rid, proto, rtf, clat) in enumerate(scored, start=1):
        rtf_s = f"{rtf:.4f}" if rtf is not None else "na"
        clat_s = f"{clat:.2f}" if clat is not None else "na"
        print(
            f"{idx:02d}. {rid} | protocol={proto} | greedy_test_cer={cer:.4f} | "
            f"rtf={rtf_s} | chunk_latency_ms={clat_s}"
        )


def stage2_summary(rows: List[Dict[str, str]], stage2_ids: Set[str]) -> None:
    by_protocol: Dict[str, List[float]] = defaultdict(list)
    by_protocol_rtf: Dict[str, List[float]] = defaultdict(list)
    by_protocol_chunk_latency: Dict[str, List[float]] = defaultdict(list)
    by_protocol_e2e_latency: Dict[str, List[float]] = defaultdict(list)
    for r in rows:
        if stage2_ids:
            if r.get("run_id", "") not in stage2_ids:
                continue
        else:
            note = r.get("error_note") or ""
            if "stage2" not in note:
                continue
        cer = _to_float(r.get("greedy_test_cer", ""))
        if cer is None:
            continue
        proto = r.get("protocol", "UNKNOWN")
        by_protocol[proto].append(cer)
        sm = _read_streaming_metrics(r.get("eval_greedy_test_json", ""))
        if sm["rtf"] is not None:
            by_protocol_rtf[proto].append(sm["rtf"])
        if sm["chunk_latency_ms"] is not None:
            by_protocol_chunk_latency[proto].append(sm["chunk_latency_ms"])
        if sm["end_to_end_latency_ms"] is not None:
            by_protocol_e2e_latency[proto].append(sm["end_to_end_latency_ms"])
    print("== Stage-2 summary by protocol (CER + streaming) ==")
    if not by_protocol:
        print("No completed Stage-2 CER values yet.")
        return
    for proto in sorted(by_protocol.keys()):
        cer_xs = by_protocol[proto]
        rtf_xs = by_protocol_rtf.get(proto, [])
        clat_xs = by_protocol_chunk_latency.get(proto, [])
        e2e_xs = by_protocol_e2e_latency.get(proto, [])
        print(
            f"{proto}: CER[{_fmt_stats(cer_xs)}], "
            f"RTF[{_fmt_stats(rtf_xs)}], "
            f"chunk_latency_ms[{_fmt_stats(clat_xs)}], "
            f"end_to_end_latency_ms[{_fmt_stats(e2e_xs)}]"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate sweep results from run_status.csv.")
    parser.add_argument("--run_status_csv", type=Path, required=True)
    parser.add_argument("--stage1_csv", type=Path, default=Path("sweeps/stage1_screening_matrix.csv"))
    parser.add_argument("--stage2_csv", type=Path, default=Path("sweeps/stage2_confirmation_matrix.csv"))
    parser.add_argument(
        "--mode",
        type=str,
        default="all",
        choices=["stage1", "stage2", "all"],
    )
    args = parser.parse_args()

    rows = _read_rows(args.run_status_csv)
    stage1_ids = _read_run_ids(args.stage1_csv)
    stage2_ids = _read_run_ids(args.stage2_csv)
    if args.mode in {"stage1", "all"}:
        stage1_rank(rows, stage1_ids)
        print()
    if args.mode in {"stage2", "all"}:
        stage2_summary(rows, stage2_ids)


if __name__ == "__main__":
    main()
