#!/usr/bin/env python3
"""Extract prior-work survey JSON into a flat CSV.

This script is intentionally dependency-light (no pandas): it reads the
`results/related_work_survey_epgspeller_2026-02-17/results/*.json` files and
writes a reproducible CSV containing all *required* fields from `fields.yaml`
plus minimal provenance columns.

Citekeys:
- `references.json` may contain multiple BibTeX entries per paper_id (e.g., arXiv
  vs venue version). We choose a single citekey per paper_id deterministically:
  prefer DOI-bearing and non-arXiv entries; otherwise prefer non-PDF URLs.

No numbers are invented: values are stringified from the JSON payloads.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


def _stringify(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, str):
        return v
    if isinstance(v, (int, float, bool)):
        return str(v)
    return json.dumps(v, ensure_ascii=False, sort_keys=True)


def _load_required_fields(fields_yaml: Path) -> List[str]:
    obj = yaml.safe_load(fields_yaml.read_text())
    if not isinstance(obj, dict):
        raise ValueError(f"Invalid YAML (expected dict): {fields_yaml}")

    cats = obj.get("field_categories")
    if not isinstance(cats, list):
        raise ValueError("fields.yaml missing field_categories list")

    required: List[str] = []
    seen = set()
    for cat in cats:
        if not isinstance(cat, dict):
            continue
        fields = cat.get("fields")
        if not isinstance(fields, list):
            continue
        for f in fields:
            if not isinstance(f, dict):
                continue
            name = f.get("name")
            req = f.get("required")
            if req is True:
                if not isinstance(name, str) or not name.strip():
                    raise ValueError("fields.yaml has required field with empty name")
                if name in seen:
                    continue
                required.append(name)
                seen.add(name)

    if not required:
        raise ValueError("No required fields found in fields.yaml")
    return required


def _primary_source_urls(payload: Dict[str, Any]) -> List[str]:
    srcs = payload.get("sources")
    if not isinstance(srcs, list):
        return []
    urls: List[str] = []
    for s in srcs:
        if not isinstance(s, dict):
            continue
        u = s.get("url")
        if isinstance(u, str) and u.strip():
            urls.append(u.strip())
    # keep deterministic order (as in JSON)
    out: List[str] = []
    seen = set()
    for u in urls:
        if u in seen:
            continue
        out.append(u)
        seen.add(u)
    return out


@dataclass(frozen=True)
class _RefEntry:
    citekey: str
    venue: str
    doi: Optional[str]
    url: str


def _is_arxiv(e: _RefEntry) -> bool:
    v = (e.venue or "").lower()
    u = (e.url or "").lower()
    return ("arxiv" in v) or ("arxiv.org" in u)


def _url_is_pdf(e: _RefEntry) -> bool:
    return (e.url or "").lower().endswith(".pdf")


def _choose_citekey(cands: List[_RefEntry]) -> str:
    if not cands:
        raise ValueError("Empty candidates")

    def _rank(e: _RefEntry):
        # lower is better
        doi_missing = 1 if (e.doi is None or str(e.doi).strip() == "") else 0
        arxiv = 1 if _is_arxiv(e) else 0
        pdf = 1 if _url_is_pdf(e) else 0
        ref_like = 1 if e.citekey.startswith("ref") else 0
        return (doi_missing, arxiv, pdf, ref_like, len(e.citekey), e.citekey)

    return sorted(cands, key=_rank)[0].citekey


def _load_citekey_map(references_json: Path) -> Dict[str, str]:
    doc = json.loads(references_json.read_text())
    if not isinstance(doc, dict):
        raise ValueError("references.json must be an object")
    entries = doc.get("entries")
    if not isinstance(entries, list):
        raise ValueError("references.json missing entries list")

    cand_map: Dict[str, List[_RefEntry]] = {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        citekey = e.get("citekey")
        from_items = e.get("from_items")
        if not isinstance(citekey, str) or not citekey.strip():
            continue
        if not isinstance(from_items, list):
            continue

        venue = str(e.get("venue") or "")
        doi = e.get("doi")
        url = str(e.get("url") or "")
        ref_e = _RefEntry(citekey=citekey.strip(), venue=venue, doi=doi if isinstance(doi, str) else None, url=url)

        for it in from_items:
            if not isinstance(it, str) or not it.endswith(".json"):
                continue
            paper_id = Path(it).stem
            if not paper_id:
                continue
            cand_map.setdefault(paper_id, []).append(ref_e)

    out: Dict[str, str] = {}
    for paper_id, cands in cand_map.items():
        out[paper_id] = _choose_citekey(cands)

    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--survey_dir",
        required=True,
        help="Directory containing per-paper JSON files (e.g., results/.../results)",
    )
    ap.add_argument(
        "--out_csv",
        required=True,
        help="Output CSV path (e.g., results/.../prior_work_raw.csv)",
    )
    args = ap.parse_args()

    survey_dir = Path(args.survey_dir)
    if not survey_dir.is_dir():
        raise FileNotFoundError(f"survey_dir not found: {survey_dir}")

    fields_yaml = survey_dir.parent / "fields.yaml"
    if not fields_yaml.exists():
        raise FileNotFoundError(f"fields.yaml not found next to survey_dir: {fields_yaml}")

    references_json = survey_dir.parent / "references.json"
    if not references_json.exists():
        raise FileNotFoundError(f"references.json not found next to survey_dir: {references_json}")

    required_fields = _load_required_fields(fields_yaml)
    citekey_map = _load_citekey_map(references_json)

    json_paths = sorted(survey_dir.glob("*.json"))
    if not json_paths:
        raise FileNotFoundError(f"No JSON files found under: {survey_dir}")

    rows: List[Dict[str, str]] = []
    for p in json_paths:
        payload = json.loads(p.read_text())
        if not isinstance(payload, dict):
            raise ValueError(f"Survey item must be a JSON object: {p}")

        missing = [k for k in required_fields if k not in payload]
        if missing:
            raise KeyError(f"Missing required keys in {p.name}: {missing}")

        paper_id = payload.get("paper_id")
        if not isinstance(paper_id, str) or not paper_id.strip():
            raise ValueError(f"Invalid paper_id in {p.name}")
        paper_id = paper_id.strip()

        out: Dict[str, str] = {}
        for k in required_fields:
            out[k] = _stringify(payload.get(k))

        citation_key_bib = citekey_map.get(paper_id)
        citation_key_suggestion = payload.get("citation_key_suggestion")

        out["citation_key_bib"] = _stringify(citation_key_bib)
        out["citation_key_suggestion"] = _stringify(citation_key_suggestion)
        out["citation_key"] = _stringify(citation_key_bib if citation_key_bib is not None else citation_key_suggestion)

        urls = _primary_source_urls(payload)
        out["sources_count"] = str(len(urls)) if urls else "0"
        out["sources_primary_urls"] = " ".join(urls[:3])

        out["survey_json_path"] = str(p)
        rows.append(out)

    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    header = list(required_fields) + [
        "citation_key_bib",
        "citation_key_suggestion",
        "citation_key",
        "sources_count",
        "sources_primary_urls",
        "survey_json_path",
    ]

    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"Wrote {len(rows)} rows: {out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
