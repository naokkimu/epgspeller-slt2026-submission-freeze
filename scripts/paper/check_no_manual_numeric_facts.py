#!/usr/bin/env python3
"""Fail if numeric literals appear in declared numeric-fact zones.

Policy (strict):
- Numeric facts (metrics, dataset sizes, hyperparameters, etc.) must not be handwritten in TeX.
- They must come from generated TeX (e.g., paper/generated/facts.tex or generated tables).

To avoid heuristics, this checker only scans zones explicitly declared in paper/facts_spec.yaml.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple

import yaml


class CheckError(RuntimeError):
    pass


def _strip_latex_comment(line: str) -> str:
    # Remove unescaped % comments.
    out = []
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "%":
            if i > 0 and line[i - 1] == "\\":
                out.append(ch)
                i += 1
                continue
            break
        out.append(ch)
        i += 1
    return "".join(out)


def _load_zones(spec_path: Path) -> List[Dict[str, str]]:
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise CheckError("facts_spec must be a YAML mapping")
    zones = spec.get("numeric_zones")
    if not isinstance(zones, list) or not zones:
        raise CheckError("facts_spec.numeric_zones must be a non-empty list")
    for z in zones:
        if not isinstance(z, dict):
            raise CheckError("Each numeric zone must be a mapping")
        if not isinstance(z.get("start_marker"), str) or not isinstance(z.get("end_marker"), str):
            raise CheckError("Each numeric zone must have start_marker and end_marker strings")
    return zones


def _find_zone_line_ranges(lines: List[str], start_marker: str, end_marker: str) -> List[Tuple[int, int]]:
    starts = [i for i, l in enumerate(lines) if start_marker in l]
    ends = [i for i, l in enumerate(lines) if end_marker in l]

    if not starts or not ends:
        raise CheckError(f"Missing zone markers: {start_marker!r} / {end_marker!r}")

    ranges: List[Tuple[int, int]] = []
    ei = 0
    for si in starts:
        while ei < len(ends) and ends[ei] <= si:
            ei += 1
        if ei >= len(ends):
            raise CheckError(f"Unmatched start marker at line {si+1}: {start_marker}")
        ranges.append((si + 1, ends[ei] - 1))  # exclusive of marker lines
        ei += 1

    # Ensure no extra end markers before first start (already handled) and no trailing ends.
    return [(a, b) for a, b in ranges if a <= b]


def _remove_allowed_constructs(s: str) -> str:
    # Remove common command arguments that may legitimately contain digits.
    patterns = [
        r"\\cite[a-zA-Z*]*\{[^}]*\}",
        r"\\ref\{[^}]*\}",
        r"\\eqref\{[^}]*\}",
        r"\\label\{[^}]*\}",
        r"\\bibliography\{[^}]*\}",
        r"\\bibliographystyle\{[^}]*\}",
        r"\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}",
        r"\\input\{[^}]*\}",
        r"\\url\{[^}]*\}",
        r"\\path\{[^}]*\}",
        r"\\href\{[^}]*\}\{[^}]*\}",
    ]
    for p in patterns:
        s = re.sub(p, "", s)
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", required=True)
    ap.add_argument("--facts_spec", required=True)
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    tex_path = (root / args.tex).resolve()
    spec_path = (root / args.facts_spec).resolve()

    if not tex_path.exists():
        raise SystemExit(f"TeX file not found: {tex_path}")
    if not spec_path.exists():
        raise SystemExit(f"facts_spec not found: {spec_path}")

    zones = _load_zones(spec_path)
    lines = tex_path.read_text(encoding="utf-8").splitlines()

    zone_ranges: List[Tuple[int, int]] = []
    for z in zones:
        zone_ranges.extend(_find_zone_line_ranges(lines, z["start_marker"], z["end_marker"]))

    # Scan each zone.
    digit_re = re.compile(r"[0-9]")

    for start_ln, end_ln in zone_ranges:
        for ln in range(start_ln, end_ln + 1):
            raw = lines[ln - 1]
            no_comment = _strip_latex_comment(raw)
            cleaned = _remove_allowed_constructs(no_comment)
            if digit_re.search(cleaned):
                raise CheckError(
                    "Numeric literal found in numeric-fact zone at "
                    f"{tex_path}:{ln}: {raw.strip()}"
                )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckError as e:
        print(f"ERROR: {e}")
        raise SystemExit(1)
