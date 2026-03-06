#!/usr/bin/env python3
"""Generate positioning plots for EPGSpeller spatial analysis.

Outputs (under --out_dir):
- positioning_space_systems.png
- positioning_space_representation.png
- w_matrix_evidence_map.png

Design constraints:
- No pandas/seaborn.
- Deterministic placement (stable jitter).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


SPATIAL_REPR_ORDER = [
    "vector_no_layout",
    "linear_compression",
    "geometry_aware_nonimage",
    "explicit_2d_image",
    "not_applicable",
]

VOCAB_CONSTRAINT_ORDER = [
    "open_vocab",
    "lexicon_or_dictionary_constrained",
    "closed_vocab",
    "n_a",
]

SENSOR_DESIGN_ORDER = [
    "none",
    "representation_reduction",
    "electrode_selection_importance",
    "layout_device_design",
]


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _stable_jitter(key: str, *, width: float = 0.18) -> float:
    h = hashlib.md5(key.encode("utf-8")).hexdigest()
    # map first 8 hex digits to [0,1)
    u = int(h[:8], 16) / 0xFFFFFFFF
    return (u - 0.5) * 2.0 * width


def _cat_index(v: str, order: List[str], *, field: str, paper_id: str) -> int:
    if v not in order:
        raise ValueError(f"Unknown {field}={v!r} for paper_id={paper_id}")
    return order.index(v)


def _year_to_color(year: str, years: List[int]) -> Tuple[float, float, float, float]:
    try:
        y = int(float(year))
    except Exception:
        y = None
    if not years or y is None:
        return (0.5, 0.5, 0.5, 0.8)
    mn, mx = min(years), max(years)
    if mn == mx:
        t = 0.5
    else:
        t = (y - mn) / (mx - mn)
    return plt.cm.viridis(t)


def _plot_systems(prior: List[Dict[str, str]], out_path: Path) -> None:
    system_task_classes = {
        "silent_spelling_text_entry",
        "silent_speech_recognition_closed_vocab",
        "speech_reconstruction_generation",
    }

    pts = [r for r in prior if r.get("task_class") in system_task_classes]

    years = [int(float(r["year"])) for r in pts if (r.get("year") or "").strip().isdigit()]

    fig, ax = plt.subplots(figsize=(10, 5.2))

    for r in pts:
        pid = r["paper_id"]
        x = _cat_index(r["spatial_representation"], SPATIAL_REPR_ORDER, field="spatial_representation", paper_id=pid)
        y = _cat_index(r["vocab_constraint"], VOCAB_CONSTRAINT_ORDER, field="vocab_constraint", paper_id=pid)
        xj = x + _stable_jitter(pid + "|x")
        yj = y + _stable_jitter(pid + "|y")
        c = _year_to_color(r.get("year", ""), years)
        ax.scatter([xj], [yj], s=70, c=[c], marker="o", edgecolors="k", linewidths=0.5, alpha=0.9)

    # Our three points (explicitly placed)
    ours = [
        {"label": "EPGSpeller (vector)", "x": "vector_no_layout", "y": "open_vocab"},
        {"label": "EPGSpeller (spatial2d)", "x": "explicit_2d_image", "y": "open_vocab"},
        {"label": "EPGSpeller (rowcol)", "x": "geometry_aware_nonimage", "y": "open_vocab"},
    ]
    for o in ours:
        x = SPATIAL_REPR_ORDER.index(o["x"]) + 0.0
        y = VOCAB_CONSTRAINT_ORDER.index(o["y"]) + 0.0
        ax.scatter([x], [y], s=140, c=[[0.85, 0.2, 0.2, 0.95]], marker="*", edgecolors="k", linewidths=0.8)
        ax.text(x + 0.05, y + 0.05, o["label"], fontsize=9)

    ax.set_xticks(range(len(SPATIAL_REPR_ORDER)))
    ax.set_xticklabels(SPATIAL_REPR_ORDER, rotation=20, ha="right")
    ax.set_yticks(range(len(VOCAB_CONSTRAINT_ORDER)))
    ax.set_yticklabels(VOCAB_CONSTRAINT_ORDER)
    ax.set_xlabel("spatial_representation")
    ax.set_ylabel("vocab_constraint")
    ax.set_title("Positioning space (system-like papers) + EPGSpeller variants")
    ax.grid(True, which="both", axis="both", linestyle=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def _plot_representation(prior: List[Dict[str, str]], out_path: Path) -> None:
    # EPG-related only
    pts = []
    for r in prior:
        mod = (r.get("modality") or "")
        if "EPG" in mod or "Electropalatography" in mod:
            pts.append(r)

    years = [int(float(r["year"])) for r in pts if (r.get("year") or "").strip().isdigit()]

    fig, ax = plt.subplots(figsize=(10, 5.2))

    for r in pts:
        pid = r["paper_id"]
        x = _cat_index(r["spatial_representation"], SPATIAL_REPR_ORDER, field="spatial_representation", paper_id=pid)
        y = _cat_index(r["sensor_design_focus"], SENSOR_DESIGN_ORDER, field="sensor_design_focus", paper_id=pid)
        xj = x + _stable_jitter(pid + "|x")
        yj = y + _stable_jitter(pid + "|y")
        c = _year_to_color(r.get("year", ""), years)
        ax.scatter([xj], [yj], s=70, c=[c], marker="o", edgecolors="k", linewidths=0.5, alpha=0.9)

    ours = [
        {"label": "EPGSpeller (vector)", "x": "vector_no_layout", "y": "electrode_selection_importance"},
        {"label": "EPGSpeller (spatial2d)", "x": "explicit_2d_image", "y": "electrode_selection_importance"},
        {"label": "EPGSpeller (rowcol)", "x": "geometry_aware_nonimage", "y": "electrode_selection_importance"},
    ]
    for o in ours:
        x = SPATIAL_REPR_ORDER.index(o["x"]) + 0.0
        y = SENSOR_DESIGN_ORDER.index(o["y"]) + 0.0
        ax.scatter([x], [y], s=140, c=[[0.85, 0.2, 0.2, 0.95]], marker="*", edgecolors="k", linewidths=0.8)
        ax.text(x + 0.05, y + 0.05, o["label"], fontsize=9)

    ax.set_xticks(range(len(SPATIAL_REPR_ORDER)))
    ax.set_xticklabels(SPATIAL_REPR_ORDER, rotation=20, ha="right")
    ax.set_yticks(range(len(SENSOR_DESIGN_ORDER)))
    ax.set_yticklabels(SENSOR_DESIGN_ORDER)
    ax.set_xlabel("spatial_representation")
    ax.set_ylabel("sensor_design_focus")
    ax.set_title("Positioning space (EPG-related prior work) + EPGSpeller variants")
    ax.grid(True, which="both", axis="both", linestyle=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def _plot_w_matrix(out_path: Path) -> None:
    w_rows = [
        "W1",
        "W2",
        "W3",
        "W4",
        "W5",
        "W6",
        "W7",
        "W8",
        "W9",
    ]
    cols = [
        "related_work_survey",
        "H11_spatial2d_vs_vector",
        "H12_spatial_aug_dropout",
        "H13_rowcol_vs_vector",
        "ed_design_results_report",
    ]

    # Explicit mapping: 1 means the evidence bundle directly supports the rebuttal action.
    # If a weakness is not addressed by these bundles, it stays 0.
    M = np.array(
        [
            # W1 positioning
            [1, 1, 1, 1, 1],
            # W2 baseline comparison (not covered by these evidence bundles)
            [0, 0, 0, 0, 0],
            # W3 generalization (not covered here)
            [0, 0, 0, 0, 0],
            # W4 split robustness (multi-seed variability)
            [0, 1, 1, 1, 1],
            # W5 specaug/PCA consistency (not covered here)
            [0, 0, 0, 0, 0],
            # W6 writing/exposition (related-work restructuring)
            [1, 0, 0, 0, 0],
            # W7 representation rationale (spatial front-ends + reductions)
            [0, 1, 1, 1, 1],
            # W8 practicality/efficiency (RTF vs K discussion in design results)
            [0, 0, 0, 0, 1],
            # W9 basic CTC (not covered here)
            [0, 0, 0, 0, 0],
        ],
        dtype=int,
    )

    fig, ax = plt.subplots(figsize=(10, 4.5))
    im = ax.imshow(M, cmap="Greys", vmin=0, vmax=1)

    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=25, ha="right")
    ax.set_yticks(range(len(w_rows)))
    ax.set_yticklabels(w_rows)
    ax.set_title("Evidence bundle ↔ review weakness map (binary)")

    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, str(M[i, j]), ha="center", va="center", fontsize=9, color="red" if M[i, j] else "black")

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prior_tax_csv", required=True)
    ap.add_argument("--ours_csv", required=True)
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()

    prior_tax_csv = Path(args.prior_tax_csv)
    ours_csv = Path(args.ours_csv)
    out_dir = Path(args.out_dir)

    if not prior_tax_csv.exists():
        raise FileNotFoundError(prior_tax_csv)
    if not ours_csv.exists():
        raise FileNotFoundError(ours_csv)

    out_dir.mkdir(parents=True, exist_ok=True)

    prior = _read_csv(prior_tax_csv)

    _plot_systems(prior, out_dir / "positioning_space_systems.png")
    _plot_representation(prior, out_dir / "positioning_space_representation.png")
    _plot_w_matrix(out_dir / "w_matrix_evidence_map.png")

    print(f"Wrote figures under: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
