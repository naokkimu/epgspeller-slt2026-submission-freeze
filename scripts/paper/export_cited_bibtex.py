#!/usr/bin/env python3
"""Export a cited-only BibTeX file from paper.json citations.

This script is evidence-only: it filters an existing BibTeX file to the
exact set of citation keys used in paper.json (ordered by first appearance
in manuscript sections).
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "scripts").is_dir() and (p / "paper").is_dir():
            return p
    raise SystemExit("Could not locate repo root (expected scripts/ and paper/)")


def _load_paper_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _collect_citations(doc: Dict) -> List[str]:
    blocks = {b.get("id"): b for b in doc.get("blocks", [])}
    citations: List[str] = []
    seen = set()
    for section in doc.get("manuscript", {}).get("sections", []):
        for block_id in section.get("blocks", []):
            block = blocks.get(block_id, {})
            for cite in block.get("citations", []) or []:
                if cite in seen:
                    continue
                seen.add(cite)
                citations.append(cite)
    return citations


def _parse_bib_entries(text: str) -> Dict[str, str]:
    entries: Dict[str, str] = {}
    i = 0
    n = len(text)
    while i < n:
        at = text.find("@", i)
        if at == -1:
            break
        j = at + 1
        while j < n and text[j] not in "{(":
            j += 1
        if j >= n:
            break
        open_ch = text[j]
        close_ch = "}" if open_ch == "{" else ")"
        k = j + 1
        while k < n and text[k].isspace():
            k += 1
        key_start = k
        while k < n and text[k] not in ",\n":
            k += 1
        key = text[key_start:k].strip()
        depth = 0
        idx = j
        while idx < n:
            ch = text[idx]
            if ch == open_ch:
                depth += 1
            elif ch == close_ch:
                depth -= 1
                if depth == 0:
                    idx += 1
                    break
            idx += 1
        entry_text = text[at:idx].strip()
        if key:
            entries[key] = entry_text
        i = idx
    return entries


def _strip_fields(entry_text: str, fields: List[str]) -> str:
    lines = entry_text.splitlines()
    keep: List[str] = []
    field_res = [re.compile(rf"^\s*{re.escape(field)}\s*=") for field in fields]
    for line in lines:
        if any(r.match(line) for r in field_res):
            continue
        keep.append(line)
    return "\n".join(keep).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper_json", default="paper/paper.json")
    ap.add_argument("--bib_in", default="paper/bibliography/references_sanitized_ascii.bib")
    ap.add_argument("--bib_out", default="paper/bibliography/references_sanitized_ascii_cited.bib")
    ap.add_argument("--root", default=None)
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else _find_repo_root()
    paper_json = root / args.paper_json
    bib_in = root / args.bib_in
    bib_out = root / args.bib_out

    if not paper_json.exists():
        raise SystemExit(f"paper.json not found: {paper_json}")
    if not bib_in.exists():
        raise SystemExit(f"bib input not found: {bib_in}")

    doc = _load_paper_json(paper_json)
    citations = _collect_citations(doc)
    if not citations:
        raise SystemExit("No citations found in paper.json")

    entries = _parse_bib_entries(bib_in.read_text(encoding="utf-8"))
    missing = [c for c in citations if c not in entries]
    if missing:
        raise SystemExit(f"Missing bib entries for cited keys: {missing}")

    stripped = [_strip_fields(entries[c], ["url", "urldate"]) for c in citations]
    output = "\n\n".join(stripped) + "\n"
    bib_out.parent.mkdir(parents=True, exist_ok=True)
    bib_out.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
