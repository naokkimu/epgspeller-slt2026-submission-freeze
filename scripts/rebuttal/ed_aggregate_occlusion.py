#!/usr/bin/env python3
"""Aggregate baseline occlusion CSVs into a stable channel-importance table (P1).

Inputs
- Baseline matrix CSV (e.g., sweeps/gc20260216/matrices/gc_baseline.csv)
- For each selected run_id:
  - logs/<run_id>/occlusion_channel_importance.csv

Outputs (default under sweeps/ed20260217/importance/)
- P1_channel_importance.csv:
    channel, mean_delta_cer, std_delta_cer, n, frac_positive, frac_negative, rank_mean_delta
- P1_rank_stability.md:
    Spearman rank correlations + topK Jaccard overlaps across seeds
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


def _read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _read_csv_after_comments(path: Path) -> List[Dict[str, str]]:
    lines = path.read_text().splitlines()
    start = None
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        if line.startswith("#"):
            continue
        start = i
        break
    if start is None:
        return []
    return list(csv.DictReader(lines[start:]))


def _f(v: str) -> Optional[float]:
    s = (v or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None


def _ranks(values: Sequence[float]) -> List[float]:
    """1..n ranks with average for ties (ascending by value)."""
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = ((i + j) / 2.0) + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def _pearson(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y) or not x:
        return float("nan")
    mx = statistics.mean(x)
    my = statistics.mean(y)
    num = 0.0
    dx = 0.0
    dy = 0.0
    for xi, yi in zip(x, y):
        a = xi - mx
        b = yi - my
        num += a * b
        dx += a * a
        dy += b * b
    den = math.sqrt(dx * dy)
    return (num / den) if den > 0 else float("nan")


def _spearman(x: Sequence[float], y: Sequence[float]) -> float:
    return _pearson(_ranks(list(x)), _ranks(list(y)))


def _jaccard(a: Sequence[int], b: Sequence[int]) -> float:
    sa = set(a)
    sb = set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def _write_csv(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def _md_table(headers: List[str], rows: List[List[str]]) -> str:
    out: List[str] = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Aggregate baseline occlusion CSVs into channel importance (P1).")
    ap.add_argument("--baseline_csv", type=Path, required=True)
    ap.add_argument("--logs_dir", type=Path, default=Path("logs"))
    ap.add_argument("--protocol", type=str, default="P1")
    ap.add_argument("--out_dir", type=Path, default=Path("sweeps/ed20260217/importance"))
    args = ap.parse_args()

    base_rows = _read_rows(args.baseline_csv)
    sel = [r for r in base_rows if (r.get("protocol") or "").strip() == args.protocol]
    if not sel:
        raise SystemExit(f"No rows for protocol={args.protocol} in {args.baseline_csv}")

    # seed_key -> channel -> delta
    per_seed: Dict[str, Dict[int, float]] = {}

    for r in sel:
        split_id = (r.get("split_id") or "").strip()
        rid = (r.get("run_id") or "").strip()
        if not split_id or not rid:
            continue
        p = args.logs_dir / rid / "occlusion_channel_importance.csv"
        if not p.exists():
            raise SystemExit(f"Missing occlusion CSV: {p}")
        recs = _read_csv_after_comments(p)
        if not recs:
            raise SystemExit(f"Empty occlusion CSV: {p}")
        m: Dict[int, float] = {}
        for rec in recs:
            ch = rec.get("channel", "").strip()
            d = _f(rec.get("delta_cer", ""))
            if not ch or d is None:
                continue
            m[int(ch)] = float(d)
        if len(m) < 10:
            raise SystemExit(f"Too few channels parsed from {p} (got {len(m)})")
        per_seed[split_id] = m

    # Aggregate across seeds.
    all_channels = sorted({ch for m in per_seed.values() for ch in m.keys()})
    if not all_channels:
        raise SystemExit("No channels found in occlusion CSVs.")

    out_rows: List[Dict[str, str]] = []
    for ch in all_channels:
        xs = [per_seed[s].get(ch) for s in sorted(per_seed.keys()) if ch in per_seed[s]]
        xs_f = [float(x) for x in xs if x is not None]
        if not xs_f:
            continue
        mean = statistics.mean(xs_f)
        std = statistics.stdev(xs_f) if len(xs_f) > 1 else float("nan")
        n = len(xs_f)
        frac_pos = sum(1 for x in xs_f if x > 0) / n
        frac_neg = sum(1 for x in xs_f if x < 0) / n
        out_rows.append(
            {
                "channel": str(ch),
                "mean_delta_cer": f"{mean:.6f}",
                "std_delta_cer": f"{std:.6f}" if not math.isnan(std) else "nan",
                "n": str(n),
                "frac_positive": f"{frac_pos:.3f}",
                "frac_negative": f"{frac_neg:.3f}",
            }
        )

    # Rank by mean_delta_cer desc (most important first).
    means = [float(r["mean_delta_cer"]) for r in out_rows]
    order = sorted(range(len(out_rows)), key=lambda i: means[i], reverse=True)
    for rank, idx in enumerate(order, start=1):
        out_rows[idx]["rank_mean_delta"] = str(rank)

    out_rows.sort(key=lambda r: int(r["channel"]))
    out_csv = args.out_dir / f"{args.protocol}_channel_importance.csv"
    _write_csv(
        out_csv,
        out_rows,
        [
            "channel",
            "mean_delta_cer",
            "std_delta_cer",
            "n",
            "frac_positive",
            "frac_negative",
            "rank_mean_delta",
        ],
    )
    print(f"Wrote {out_csv} ({len(out_rows)} channels)")

    # Stability report.
    seeds = sorted(per_seed.keys())
    # Align arrays by channel order (0..max in all_channels, but keep existing list).
    ch_list = all_channels
    deltas_by_seed = {s: [per_seed[s].get(ch, 0.0) for ch in ch_list] for s in seeds}

    spearman_rows: List[List[str]] = []
    for i in range(len(seeds)):
        for j in range(i + 1, len(seeds)):
            a = seeds[i]
            b = seeds[j]
            rho = _spearman(deltas_by_seed[a], deltas_by_seed[b])
            spearman_rows.append([a, b, f"{rho:.4f}"])

    topKs = [32, 64, 96]
    # Build per-seed topK sets (by descending delta_cer within seed).
    top_sets: Dict[Tuple[str, int], List[int]] = {}
    for s in seeds:
        # sort channels by delta desc, then channel asc for determinism
        ranked = sorted(ch_list, key=lambda ch: (-per_seed[s].get(ch, 0.0), ch))
        for k in topKs:
            top_sets[(s, k)] = ranked[:k]

    jaccard_rows: List[List[str]] = []
    for k in topKs:
        vals: List[float] = []
        for i in range(len(seeds)):
            for j in range(i + 1, len(seeds)):
                a = seeds[i]
                b = seeds[j]
                jac = _jaccard(top_sets[(a, k)], top_sets[(b, k)])
                vals.append(jac)
                jaccard_rows.append([str(k), a, b, f"{jac:.4f}"])
        if vals:
            jaccard_rows.append([str(k), "mean", "", f"{statistics.mean(vals):.4f}"])
            jaccard_rows.append([str(k), "min", "", f"{min(vals):.4f}"])

    md: List[str] = []
    md.append(f"# Rank stability ({args.protocol})")
    md.append("")
    md.append(f"- baseline_csv: `{args.baseline_csv}`")
    md.append(f"- logs_dir: `{args.logs_dir}`")
    md.append(f"- runs: {len(sel)} (seeds={', '.join(seeds)})")
    md.append("")
    md.append("## Spearman correlation (delta_cer rankings)")
    md.append("")
    md.append(_md_table(["seed_a", "seed_b", "spearman_rho"], spearman_rows))
    md.append("")
    md.append("## TopK Jaccard overlap (channel sets)")
    md.append("")
    md.append(_md_table(["K", "seed_a", "seed_b", "jaccard"], jaccard_rows))
    md.append("")

    out_md = args.out_dir / f"{args.protocol}_rank_stability.md"
    out_md.write_text("\n".join(md) + "\n")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()

