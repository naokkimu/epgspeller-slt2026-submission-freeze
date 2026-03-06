#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List, Optional


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def render(paper_json: Path, out_md: Path) -> int:
    doc = _load_json(paper_json)
    if not isinstance(doc, dict):
        raise ValueError("paper.json must be an object")

    claims = doc.get("claims", [])
    evidence = doc.get("evidence", [])
    runs = doc.get("runs", [])

    if not isinstance(claims, list) or not isinstance(evidence, list) or not isinstance(runs, list):
        raise ValueError("paper.json must contain list fields")

    n_claims = len(claims)
    n_evidence = len(evidence)
    n_runs = len(runs)

    # Deterministic rule-based decision.
    if n_claims == 0:
        decision = "Reject"
        confidence = 0.90
        rationale = "No claims are registered in paper.json, so there is nothing to evaluate against evidence."
    elif n_evidence == 0:
        decision = "Reject"
        confidence = 0.85
        rationale = "Claims exist but no evidence entries are registered."
    else:
        covered = 0
        for cl in claims:
            if not isinstance(cl, dict):
                continue
            refs = None
            for key in ("evidence_ids", "evidence", "evidenceIds"):
                if key in cl:
                    refs = cl.get(key)
                    break
            if isinstance(refs, list) and any(isinstance(x, str) and x.strip() for x in refs):
                covered += 1
        frac = covered / max(1, n_claims)
        if frac < 0.5:
            decision = "Reject"
            confidence = 0.75
        elif frac < 0.8:
            decision = "Borderline"
            confidence = 0.60
        else:
            decision = "Weak Accept"
            confidence = 0.55
        rationale = f"Evidence-reference coverage: {covered}/{n_claims} claims have at least one evidence reference."

    md: List[str] = []
    md.append("# Interspeech-style evidence-only review (paper.json)")
    md.append("")

    md.append("## Decision")
    md.append(f"- Recommendation: **{decision}**")
    md.append(f"- Confidence: {confidence:.2f}")
    md.append("")

    md.append("## Registry snapshot")
    md.append(f"- Claims: {n_claims}")
    md.append(f"- Evidence: {n_evidence}")
    md.append(f"- Runs: {n_runs}")
    md.append("")

    md.append("## Rationale")
    md.append(rationale)
    md.append("")

    md.append("## Required fixes (deterministic)")
    if n_claims == 0:
        md.append("- Add at least one claim with an `id` and a clear `statement`.")
        md.append("- Register evidence files (with `path` + `sha256`) and link them from each claim.")
        md.append("- Register producing runs/experiments so evidence is traceable.")
    elif n_evidence == 0:
        md.append("- Register evidence files and link them from claims.")
    else:
        md.append("- Ensure every claim references evidence IDs, and evidence files are pinned by sha256.")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(md).rstrip() + "\n")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--paper-json", default="paper/paper.json")
    p.add_argument("--out-md", required=True)
    args = p.parse_args(argv)

    return render(paper_json=Path(args.paper_json), out_md=Path(args.out_md))


if __name__ == "__main__":
    raise SystemExit(main())
