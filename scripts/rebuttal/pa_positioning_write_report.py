#!/usr/bin/env python3
"""Write an evidence-grounded positioning report (paper-ready English).

This report is *evidence-only*:
- Prior-work facts are drawn from the frozen survey JSON exports.
- Our spatial claims are drawn from the H11–H13 evidence CSV snapshots.

The script fails if the hard assertions implied by H11–H13 do not hold.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def _fmt_mean_std(mean: float, std: float, *, ndigits: int = 4) -> str:
    return f"{mean:.{ndigits}f}±{std:.{ndigits}f}"


def _parse_setting(setting: str) -> Dict[str, str]:
    # setting is like: "subset_method=topk, K=32, frontend=vector"
    out: Dict[str, str] = {}
    for part in setting.split(","):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def _collect_prior_citekeys(prior_rows: List[Dict[str, str]]) -> Dict[str, List[str]]:
    buckets: Dict[str, List[str]] = {}
    for r in prior_rows:
        cite = (r.get("citation_key") or "").strip()
        if not cite or cite == "null":
            continue
        tc = (r.get("task_class") or "").strip()
        buckets.setdefault(tc, []).append(cite)

    # de-dup stable
    for k, xs in list(buckets.items()):
        seen = set()
        out: List[str] = []
        for x in xs:
            if x in seen:
                continue
            out.append(x)
            seen.add(x)
        buckets[k] = out
    return buckets


def _cite_list(xs: List[str]) -> str:
    if not xs:
        return ""
    return "\\cite{" + ",".join(xs) + "}"


def _extract_w_descriptions(path: Path) -> Dict[str, str]:
    # Parse the first markdown table rows like: | W1 | **...** (...) | ... |
    txt = path.read_text()
    out: Dict[str, str] = {}
    for line in txt.splitlines():
        line = line.strip()
        if not line.startswith("| W"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 2:
            continue
        wcode = parts[0]
        desc = parts[1]
        # strip markdown bold
        desc = desc.replace("**", "")
        # short description: before first parenthesis
        desc_short = desc.split("(", 1)[0].strip()
        if wcode and wcode not in out:
            out[wcode] = desc_short
    return out


def _build_h11_table(ours_rows: List[Dict[str, str]]) -> Tuple[str, str]:
    # returns (markdown_table, evidence_path)
    rows = [r for r in ours_rows if r.get("finding_id") == "H11" and r.get("metric") in {"greedy_cer", "greedy_rtf"}]
    if not rows:
        raise ValueError("No H11 rows found in ours_csv")

    evidence_paths = sorted({r.get("evidence_path") for r in rows if r.get("evidence_path")})
    evidence_path = evidence_paths[0] if evidence_paths else ""

    # key: (subset_method, K, frontend) -> metric -> (mean,std)
    d: Dict[Tuple[str, str, str], Dict[str, Tuple[float, float]]] = {}
    for r in rows:
        meta = _parse_setting(r["setting"])
        key = (meta.get("subset_method", ""), meta.get("K", ""), meta.get("frontend", ""))
        d.setdefault(key, {})[r["metric"]] = (float(r["mean"]), float(r["std"]))

    # Build rows we care about
    wanted = []
    for subset_method, k in [
        ("topk", "32"),
        ("fps2k", "32"),
        ("topk", "64"),
        ("fps2k", "64"),
        ("topk", "96"),
        ("fps2k", "96"),
        ("all", "124"),
    ]:
        wanted.append((subset_method, k))

    md_lines = []
    md_lines.append("| subset_method | K | vec CER | s2d CER | ΔCER(s2d-vec) | vec rtf | s2d rtf |")
    md_lines.append("|---|---:|---:|---:|---:|---:|---:|")

    # Assertions for H11
    for subset_method, k in wanted:
        vec = d.get((subset_method, k, "vector"), {})
        s2d = d.get((subset_method, k, "spatial2d"), {})
        if "greedy_cer" not in vec or "greedy_cer" not in s2d:
            raise KeyError(f"Missing greedy_cer for H11 subset_method={subset_method} K={k}")
        if "greedy_rtf" not in vec or "greedy_rtf" not in s2d:
            raise KeyError(f"Missing greedy_rtf for H11 subset_method={subset_method} K={k}")

        vec_cer_m, vec_cer_s = vec["greedy_cer"]
        s2d_cer_m, s2d_cer_s = s2d["greedy_cer"]
        vec_rtf_m, vec_rtf_s = vec["greedy_rtf"]
        s2d_rtf_m, s2d_rtf_s = s2d["greedy_rtf"]

        # H11 claim used elsewhere: s2d CER mean is higher and rtf is higher.
        if not (s2d_cer_m > vec_cer_m):
            raise AssertionError(
                f"H11 assertion failed: expected s2d CER > vec CER for {subset_method} K={k} ({s2d_cer_m} vs {vec_cer_m})"
            )
        if not (s2d_rtf_m > vec_rtf_m):
            raise AssertionError(
                f"H11 assertion failed: expected s2d rtf > vec rtf for {subset_method} K={k} ({s2d_rtf_m} vs {vec_rtf_m})"
            )

        md_lines.append(
            "| "
            + subset_method
            + " | "
            + k
            + " | "
            + _fmt_mean_std(vec_cer_m, vec_cer_s)
            + " | "
            + _fmt_mean_std(s2d_cer_m, s2d_cer_s)
            + " | "
            + f"{(s2d_cer_m - vec_cer_m):+.4f}"
            + " | "
            + f"{vec_rtf_m:.4f}"
            + " | "
            + f"{s2d_rtf_m:.4f}"
            + " |"
        )

    return "\n".join(md_lines), evidence_path


def _build_h13_table(ours_rows: List[Dict[str, str]]) -> Tuple[str, str]:
    rows = [r for r in ours_rows if r.get("finding_id") == "H13" and r.get("metric") in {"greedy_cer", "greedy_rtf"}]
    if not rows:
        raise ValueError("No H13 rows found in ours_csv")

    evidence_paths = sorted({r.get("evidence_path") for r in rows if r.get("evidence_path")})
    evidence_path = evidence_paths[0] if evidence_paths else ""

    d: Dict[Tuple[str, str, str], Dict[str, Tuple[float, float]]] = {}
    for r in rows:
        meta = _parse_setting(r["setting"])
        key = (meta.get("subset_method", ""), meta.get("K", ""), meta.get("frontend", ""))
        d.setdefault(key, {})[r["metric"]] = (float(r["mean"]), float(r["std"]))

    wanted = []
    for subset_method, k in [
        ("topk", "32"),
        ("fps2k", "32"),
        ("topk", "64"),
        ("fps2k", "64"),
    ]:
        wanted.append((subset_method, k))

    md_lines = []
    md_lines.append("| subset_method | K | vec CER | rowcol CER | ΔCER(rowcol-vec) | vec rtf | rowcol rtf |")
    md_lines.append("|---|---:|---:|---:|---:|---:|---:|")

    for subset_method, k in wanted:
        vec = d.get((subset_method, k, "vector"), {})
        rc = d.get((subset_method, k, "rowcol"), {})
        if "greedy_cer" not in vec or "greedy_cer" not in rc:
            raise KeyError(f"Missing greedy_cer for H13 subset_method={subset_method} K={k}")
        if "greedy_rtf" not in vec or "greedy_rtf" not in rc:
            raise KeyError(f"Missing greedy_rtf for H13 subset_method={subset_method} K={k}")

        vec_cer_m, vec_cer_s = vec["greedy_cer"]
        rc_cer_m, rc_cer_s = rc["greedy_cer"]
        vec_rtf_m, _ = vec["greedy_rtf"]
        rc_rtf_m, _ = rc["greedy_rtf"]

        # H13 supported claim: for K=32/64 (topk/fps2k) abs diff < 0.01, and rowcol rtf higher.
        if k in {"32", "64"} and subset_method in {"topk", "fps2k"}:
            if not (abs(rc_cer_m - vec_cer_m) < 0.01):
                raise AssertionError(
                    f"H13 assertion failed: abs(rowcol-vec) >= 0.01 for {subset_method} K={k} ({rc_cer_m} vs {vec_cer_m})"
                )
            if not (rc_rtf_m > vec_rtf_m):
                raise AssertionError(
                    f"H13 assertion failed: expected rowcol rtf > vec rtf for {subset_method} K={k} ({rc_rtf_m} vs {vec_rtf_m})"
                )

        md_lines.append(
            "| "
            + subset_method
            + " | "
            + k
            + " | "
            + _fmt_mean_std(vec_cer_m, vec_cer_s)
            + " | "
            + _fmt_mean_std(rc_cer_m, rc_cer_s)
            + " | "
            + f"{(rc_cer_m - vec_cer_m):+.4f}"
            + " | "
            + f"{vec_rtf_m:.4f}"
            + " | "
            + f"{rc_rtf_m:.4f}"
            + " |"
        )

    return "\n".join(md_lines), evidence_path


def _build_h12_table(ours_rows: List[Dict[str, str]]) -> Tuple[str, str]:
    rows = [r for r in ours_rows if r.get("finding_id") == "H12" and r.get("metric") == "delta_cer"]
    if not rows:
        raise ValueError("No H12 rows found in ours_csv")

    evidence_paths = sorted({r.get("evidence_path") for r in rows if r.get("evidence_path")})
    evidence_path = evidence_paths[0] if evidence_paths else ""

    # key: (enable_spatial_aug, drop_rate) -> (mean,std)
    d: Dict[Tuple[str, str], Tuple[float, float]] = {}
    for r in rows:
        meta = _parse_setting(r["setting"])
        aug = meta.get("enable_spatial_aug", "")
        dr = meta.get("drop_rate", "")
        d[(aug, dr)] = (float(r["mean"]), float(r["std"]))

    drop_rates = ["0.0", "0.1", "0.2", "0.3"]
    md_lines = []
    md_lines.append("| drop_rate | ΔCER (aug=0) | ΔCER (aug=1) |")
    md_lines.append("|---:|---:|---:|")

    for dr in drop_rates:
        if ("0", dr) not in d or ("1", dr) not in d:
            raise KeyError(f"Missing H12 delta_cer for drop_rate={dr}")
        m0, s0 = d[("0", dr)]
        m1, s1 = d[("1", dr)]

        # H12 supported claim: for q in {0.1,0.2,0.3}, aug=1 lower degradation.
        if dr in {"0.1", "0.2", "0.3"}:
            if not (m1 < m0):
                raise AssertionError(
                    f"H12 assertion failed: expected ΔCER(aug=1) < ΔCER(aug=0) at drop_rate={dr} ({m1} vs {m0})"
                )

        md_lines.append(
            f"| {dr} | {_fmt_mean_std(m0, s0)} | {_fmt_mean_std(m1, s1)} |"
        )

    return "\n".join(md_lines), evidence_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prior_tax_csv", required=True)
    ap.add_argument("--ours_csv", required=True)
    ap.add_argument("--review_weakness_md", required=True)
    ap.add_argument("--related_work_md", required=True)
    ap.add_argument("--out_md", required=True)
    ap.add_argument("--fig_dir", required=True)
    args = ap.parse_args()

    prior_tax_csv = Path(args.prior_tax_csv)
    ours_csv = Path(args.ours_csv)
    review_weakness_md = Path(args.review_weakness_md)
    related_work_md = Path(args.related_work_md)
    out_md = Path(args.out_md)
    fig_dir = Path(args.fig_dir)

    for p in [prior_tax_csv, ours_csv, review_weakness_md, related_work_md]:
        if not p.exists():
            raise FileNotFoundError(p)

    prior_rows = _read_csv(prior_tax_csv)
    ours_rows = _read_csv(ours_csv)

    prior_cites = _collect_prior_citekeys(prior_rows)
    w_desc = _extract_w_descriptions(review_weakness_md)

    # Build H11–H13 tables (and assert implied claims).
    h11_table, h11_ev = _build_h11_table(ours_rows)
    h12_table, h12_ev = _build_h12_table(ours_rows)
    h13_table, h13_ev = _build_h13_table(ours_rows)

    # Prior-work cite buckets (shortcuts)
    cites_survey = []
    for k in ["survey_method"]:
        cites_survey.extend(prior_cites.get(k, []))

    cites_spelling = prior_cites.get("silent_spelling_text_entry", [])
    cites_closed = prior_cites.get("silent_speech_recognition_closed_vocab", [])
    cites_gen = prior_cites.get("speech_reconstruction_generation", [])
    cites_map = prior_cites.get("mapping_prediction", [])
    cites_instr = prior_cites.get("instrumentation_visualization", [])

    # Ensure key anchors exist for positioning statement
    # (Fail fast if survey set is missing expected anchors.)
    required_anchor = ["kimura2022silentspeller", "dong2024rehearsse", "graves2006connectionist"]
    have = {r.get("citation_key") for r in prior_rows}
    missing = [x for x in required_anchor if x not in have]
    if missing:
        raise AssertionError(f"Missing expected anchor citekeys in prior_work_taxonomy.csv: {missing}")

    out_lines: List[str] = []
    out_lines.append("# Positioning Analysis: EPGSpeller in the SSI/EPG spatial landscape (2026-02-18)")
    out_lines.append("")
    out_lines.append("This document positions **EPGSpeller** within an **EPG-centered Silent Speech Interface (SSI)** related-work space using a fixed multi-lens taxonomy.")
    out_lines.append("All statements are grounded in repository evidence: the frozen related-work survey exports and the H11–H13 experiment evidence snapshots.")
    out_lines.append("")

    out_lines.append("## 1. One-paragraph positioning statement")
    out_lines.append("")
    out_lines.append(
        "EPGSpeller is positioned as an **EPG-centered silent spelling/text-entry** study within SSI, focusing on **open-vocabulary character-level decoding** (CTC-style) rather than constrained-vocabulary recognition or speech reconstruction pipelines. "
        "Within our frozen survey set, the closest task anchors for open-vocabulary silent spelling are SilentSpeller and ReHEarSSE "
        + _cite_list(["kimura2022silentspeller", "dong2024rehearsse"])
        + ", and the decoding formulation is grounded in the CTC objective "
        + _cite_list(["graves2006connectionist"])
        + "." 
    )
    out_lines.append("")

    out_lines.append("## 2. Positioning by lens (V1–V6)")
    out_lines.append("")

    out_lines.append("### V1: Task / output unit")
    out_lines.append("")
    out_lines.append(
        "Within the frozen survey set, silent spelling/text-entry systems are represented by "
        + _cite_list(cites_spelling)
        + ". Closed-vocabulary SSI recognition is represented by "
        + _cite_list(cites_closed)
        + ". Speech reconstruction/generation pipelines provide a contrasting SSI framing "
        + _cite_list(cites_gen)
        + "." 
    )
    out_lines.append("")

    out_lines.append("### V2: Decoding constraint")
    out_lines.append("")
    out_lines.append(
        "Open-vocabulary spelling relies on character-level decoding that can compose unseen words, while several SSI pipelines use stronger lexicon/dictionary constraints. "
        "In our frozen survey set, open-vocabulary spelling uses CTC-like decoding "
        + _cite_list(["kimura2022silentspeller", "dong2024rehearsse", "graves2006connectionist"])
        + ", whereas constrained pipelines appear in ultrasound-based reconstruction systems "
        + _cite_list(["hueber2010development"])
        + "." 
    )
    out_lines.append("")

    out_lines.append("### V3: Spatial inductive bias (EPG is spatial; what happens when we exploit layout?)")
    out_lines.append("")
    out_lines.append(
        "EPG produces spatial tongue–palate contact patterns whose layout and visualization have been emphasized in foundational and device/visualization work "
        + _cite_list(cites_instr)
        + ". Historical EPG representation studies also investigate explicit reduction/compression of contact patterns "
        + _cite_list(["hardcastle1991epg", "carreira1998dimensionality"])
        + "." 
    )
    out_lines.append("")
    out_lines.append(
        "In our experiments, we directly test whether explicitly reconstructing a 16×16 grid and applying a 2D conv front-end improves over a vector baseline (H11), and whether a geometry-aware row/col compression retains performance (H13). "
        "The evidence-grounded results are summarized in Section 3." 
    )
    out_lines.append("")

    out_lines.append("### V4: Robustness / augmentation")
    out_lines.append("")
    out_lines.append(
        "SSI surveys highlight robustness challenges from sensor variability and noise "
        + _cite_list(["denby2010silent", "gonzalez2020silent", "lee2021biosignal", "freitas2017an"])
        + ". SpecAugment provides a widely used feature-masking augmentation baseline in ASR "
        + _cite_list(["park2019specaugment"])
        + "." 
    )
    out_lines.append("")
    out_lines.append(
        "For spatial models, we evaluate a spatial augmentation (block dropout + shift) and quantify its effect on robustness to fixed electrode dropout (H12), summarized in Section 3." 
    )
    out_lines.append("")

    out_lines.append("### V5: Sensor design / electrode selection")
    out_lines.append("")
    out_lines.append(
        "EPG devices and electrode layouts are device-specific, motivating explicit discussion of layout/design constraints "
        + _cite_list(["hardcastle1989new", "verhoeven2019visualisation", "woo2021design"])
        + ". Our broader `ed20260217` study (outside this document) focuses on electrode importance and K-budget trade-offs for next-EPG design." 
    )
    out_lines.append("")

    out_lines.append("### V6: Protocol / generalization")
    out_lines.append("")
    out_lines.append(
        "EPGSpeller is designed with multiple protocols (P1/P2/XSUB) as described in the roadmap, but the H11–H13 spatial analyses in this document are grounded in P1 (seed0–3) evidence only. We do not extrapolate these findings to P2/P3 without additional runs." 
    )
    out_lines.append("")

    out_lines.append("## 3. Evidence-grounded spatial findings (H11–H13)")
    out_lines.append("")

    out_lines.append("### H11: 16×16 reconstruction + 2D conv front-end vs vector baseline")
    out_lines.append("")
    out_lines.append(f"Evidence snapshot CSV: `{h11_ev}`")
    out_lines.append("")
    out_lines.append(h11_table)
    out_lines.append("")
    out_lines.append(
        "**Conclusion (H11):** For P1 (seed0–3) across the evaluated settings, the 2D conv front-end (spatial2d) yields **higher** greedy test CER than the vector baseline, and also incurs **higher** streaming RTF. "
        "Therefore, under this implementation and dataset protocol, explicit 16×16 reconstruction + 2D conv does **not** improve performance and is slower." 
    )
    out_lines.append("")

    out_lines.append("### H12: Spatial augmentation and robustness to fixed electrode dropout")
    out_lines.append("")
    out_lines.append(f"Evidence snapshot CSV: `{h12_ev}`")
    out_lines.append("")
    out_lines.append(h12_table)
    out_lines.append("")
    out_lines.append(
        "**Conclusion (H12):** Under fixed electrode dropout rates q∈{0.1,0.2,0.3}, training with spatial augmentation (enable_spatial_aug=1) yields **lower mean CER degradation (ΔCER)** than without spatial augmentation (enable_spatial_aug=0). "
        "This supports the claim that 2D-enabled spatial augmentation can improve robustness to electrode failures, at least for the spatial2d front-end." 
    )
    out_lines.append("")

    out_lines.append("### H13: Row/col compression (geometry-aware 1D pooling) vs vector baseline")
    out_lines.append("")
    out_lines.append(f"Evidence snapshot CSV: `{h13_ev}`")
    out_lines.append("")
    out_lines.append(h13_table)
    out_lines.append("")
    out_lines.append(
        "**Conclusion (H13):** For K=32 and K=64 (topk/fps2k), the row/col compression model’s greedy test CER mean differs from the vector baseline by <0.01 absolute, while its streaming RTF is higher. "
        "Thus, this particular row/col compression preserves accuracy but does not improve streaming efficiency in the current implementation." 
    )
    out_lines.append("")

    out_lines.append("## 4. Review-weakness closure map (W1–W9) for this evidence bundle")
    out_lines.append("")
    out_lines.append("Figure: `w_matrix_evidence_map.png` (binary mapping)")
    out_lines.append("")

    # Build a small W table using the extracted descriptions (when present)
    out_lines.append("| Weakness | Short description | Notes |")
    out_lines.append("|---|---|---|")
    for w in [f"W{i}" for i in range(1, 10)]:
        desc = w_desc.get(w, "")
        note = "Covered by evidence bundles" if w in {"W1", "W4", "W6", "W7", "W8"} else "Not covered by this bundle"
        out_lines.append(f"| {w} | {desc} | {note} |")

    out_lines.append("")

    out_lines.append("## 5. Figures")
    out_lines.append("")
    out_lines.append(f"- {fig_dir / 'positioning_space_systems.png'}")
    out_lines.append(f"- {fig_dir / 'positioning_space_representation.png'}")
    out_lines.append(f"- {fig_dir / 'w_matrix_evidence_map.png'}")
    out_lines.append("")

    out_lines.append("## 6. Limits and future work (proposal; not a claim)")
    out_lines.append("")
    out_lines.append(
        "- The H11–H13 findings are grounded in P1 only; extending the same comparisons to P2/XSUB is required before making protocol-general statements.\n"
        "- Explicit 2D reconstruction did not improve accuracy in H11; future work could test alternative spatial encoders (e.g., graph-based or 3D palate-aware models) and re-check implementation choices without changing the evidence reported here.\n"
        "- Robustness gains from spatial augmentation were demonstrated under synthetic fixed dropout (H12); additional robustness axes (session drift, sensor shift) would require new evidence runs."
    )
    out_lines.append("")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(out_lines) + "\n")

    print(f"Wrote report: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
