#!/usr/bin/env python3
"""Apply an explicit taxonomy to the prior-work raw CSV.

Important: this script does *not* infer taxonomy labels heuristically.
All category assignments must be provided explicitly in `taxonomy_rules.json`.
If any paper_id is missing from the rules file, the script fails.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List


TAXONOMY_FIELDS = [
    "task_class",
    "output_unit_class",
    "vocab_constraint",
    "decoding_form",
    "spatial_representation",
    "layout_assumption",
    "augmentation_class",
    "robustness_eval",
    "sensor_design_focus",
    "protocol_class",
]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _stringify(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    return json.dumps(v, ensure_ascii=False, sort_keys=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw_csv", required=True)
    ap.add_argument("--rubric_md", required=True)
    ap.add_argument("--rules_json", required=True)
    ap.add_argument("--out_csv", default=None)
    args = ap.parse_args()

    raw_csv = Path(args.raw_csv)
    rubric_md = Path(args.rubric_md)
    rules_json = Path(args.rules_json)

    if not raw_csv.exists():
        raise FileNotFoundError(raw_csv)
    if not rubric_md.exists():
        raise FileNotFoundError(rubric_md)
    if not rules_json.exists():
        raise FileNotFoundError(rules_json)

    rules_doc = _load_json(rules_json)
    if not isinstance(rules_doc, dict):
        raise ValueError("taxonomy_rules.json must be an object")

    papers = rules_doc.get("papers")
    if not isinstance(papers, dict):
        raise ValueError("taxonomy_rules.json must contain object key: papers")

    out_rows: List[Dict[str, str]] = []

    with raw_csv.open("r", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("raw_csv has no header")

        raw_header = list(reader.fieldnames)
        for r in reader:
            paper_id = (r.get("paper_id") or "").strip()
            if not paper_id:
                raise ValueError("raw_csv row missing paper_id")

            spec = papers.get(paper_id)
            if spec is None:
                raise KeyError(f"taxonomy_rules.json missing paper_id: {paper_id}")
            if not isinstance(spec, dict):
                raise ValueError(f"rules.papers[{paper_id}] must be an object")

            for k in TAXONOMY_FIELDS:
                if k not in spec:
                    raise KeyError(f"rules.papers[{paper_id}] missing taxonomy field: {k}")

            out = dict(r)
            for k in TAXONOMY_FIELDS:
                out[k] = _stringify(spec.get(k))

            out["taxonomy_uncertain"] = _stringify(spec.get("uncertain", []))
            out["taxonomy_notes"] = _stringify(spec.get("notes", ""))
            out_rows.append(out)

    out_csv = Path(args.out_csv) if args.out_csv else raw_csv.parent / "prior_work_taxonomy.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    out_header = raw_header + TAXONOMY_FIELDS + ["taxonomy_uncertain", "taxonomy_notes"]

    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_header)
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print(f"Wrote {len(out_rows)} rows: {out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
