#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path


_UNICODE_TO_LATEX = {
    "Á": "{\\'A}",
    "á": "{\\'a}",
    "ã": "{\\~a}",
    "é": "{\\'e}",
    "ñ": "{\\~n}",
    "ó": "{\\'o}",
    "ü": "{\\\"u}",
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a UTF-8 BibTeX file into an ASCII-only BibTeX file by replacing a"
            " small, explicit set of Unicode characters with LaTeX accent commands."
            " Fail-fast if any non-ASCII characters remain."
        )
    )
    parser.add_argument("--in_bib", required=True, type=Path)
    parser.add_argument("--out_bib", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    input_path: Path = args.in_bib
    output_path: Path = args.out_bib

    text = input_path.read_text(encoding="utf-8")

    counts = Counter()
    out_chars: list[str] = []
    for ch in text:
        if ch in _UNICODE_TO_LATEX:
            out_chars.append(_UNICODE_TO_LATEX[ch])
            counts[ch] += 1
        else:
            out_chars.append(ch)

    out_text = "".join(out_chars)
    remaining_non_ascii = sorted({ch for ch in out_text if ord(ch) > 127})
    if remaining_non_ascii:
        pretty = ", ".join(f"{repr(ch)}(U+{ord(ch):04X})" for ch in remaining_non_ascii)
        raise SystemExit(
            f"[FAIL] Non-ASCII characters remain after sanitization: {pretty}\n"
            f"Please extend _UNICODE_TO_LATEX explicitly in {Path(__file__).as_posix()}."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(out_text, encoding="ascii")

    print("[OK] wrote:", output_path)
    if counts:
        print("[OK] replacements:")
        for ch, n in counts.most_common():
            print(f"  {repr(ch)} -> {_UNICODE_TO_LATEX[ch]}  (n={n})")


if __name__ == "__main__":
    main()
