#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


def _resolve_skill_renderer() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    candidates = [
        codex_home
        / "skills"
        / "paperjson-manuscript-tex"
        / "scripts"
        / "render_paper_json_manuscript_tex.py",
        codex_home
        / "skills"
        / "_archive"
        / "20260304_entry_only"
        / "paperjson-manuscript-tex"
        / "scripts"
        / "render_paper_json_manuscript_tex.py",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise SystemExit(f"[ERROR] paperjson-manuscript-tex renderer not found: {candidates[0]}")


def _copy_interspeech_cls(root: Path, out_dir: Path) -> None:
    candidates = [
        root / "paper" / "submission" / "Interspeech.cls",
        root / "paper" / "submission" / "paper_kit" / "Interspeech.cls",
    ]
    for c in candidates:
        if c.exists():
            out_dir.mkdir(parents=True, exist_ok=True)
            dst = out_dir / "Interspeech.cls"
            try:
                if c.resolve() == dst.resolve():
                    return
            except FileNotFoundError:
                pass
            shutil.copyfile(c, dst)
            return
    raise SystemExit("[ERROR] Interspeech.cls not found under paper/submission or paper/submission/paper_kit")


def _rewrite_preamble(out_tex: Path) -> None:
    lines = out_tex.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise SystemExit("[ERROR] generated_main.tex is empty")
    try:
        docclass_idx = next(i for i, l in enumerate(lines) if l.lstrip().startswith(r"\documentclass"))
        title_idx = next(i for i, l in enumerate(lines) if l.lstrip().startswith(r"\title{"))
    except StopIteration:
        raise SystemExit("[ERROR] generated_main.tex missing \\documentclass or \\title")

    new_prefix: List[str] = []
    if lines:
        new_prefix.append(lines[0])
    new_prefix.append("% Target: INTERSPEECH 2026 Paper Kit (Interspeech.cls).")

    preamble = [
        r"\documentclass{Interspeech}",
        r"\usepackage{amsmath}",
        r"\usepackage{booktabs}",
        r"\usepackage{graphicx}",
        r"\usepackage{microtype}",
        r"\usepackage{url}",
        r"\def\UrlBreaks{\do\/\do-\do\_\do\&\do\?\do\#\do\%\do\=\do\+\do\~\do\:\do\.}",
        r"\Urlmuskip=0mu plus 1mu",
        r"\usepackage{hyperref}",
        r"\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}",
        "",
    ]

    new_lines = new_prefix + preamble + lines[title_idx:]
    out_tex.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def _expand_tabular_to_columnwidth(out_tex: Path) -> None:
    lines = out_tex.read_text(encoding="utf-8").splitlines()
    out_lines: List[str] = []
    for line in lines:
        if r"\begin{tabular*}{" in line:
            out_lines.append(line)
            continue
        if r"\begin{tabular}{" in line:
            prefix, rest = line.split(r"\begin{tabular}{", 1)
            out_lines.append(prefix + r"\begin{tabular*}{\columnwidth}{@{\extracolsep{\fill}}" + rest)
            continue
        if r"\end{tabular}" in line:
            out_lines.append(line.replace(r"\end{tabular}", r"\end{tabular*}"))
            continue
        out_lines.append(line)
    out_tex.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def _tighten_table_spacing(out_tex: Path) -> None:
    lines = out_tex.read_text(encoding="utf-8").splitlines()
    out_lines: List[str] = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(r"\begin{table}"):
            in_table = True
            out_lines.append(line)
            continue
        if stripped.startswith(r"\end{table}"):
            in_table = False
            out_lines.append(line)
            continue
        out_lines.append(line)
        if in_table and stripped.startswith(r"\centering"):
            out_lines.append(r"\small")
            out_lines.append(r"\setlength{\tabcolsep}{4pt}")
    out_tex.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def _restore_inline_refs(out_tex: Path) -> None:
    text = out_tex.read_text(encoding="utf-8")

    ref_re = re.compile(r"\\textbackslash\{\}(ref|pageref|eqref)\\\{((?:\\.|[^{}])+?)\\\}")

    def _repl(m: re.Match[str]) -> str:
        cmd = m.group(1)
        label = m.group(2)
        label = label.replace(r"\_", "_")
        return f"\\{cmd}{{{label}}}"

    text = ref_re.sub(_repl, text)
    text = re.sub(r"\\~\{\}(?=\\(?:ref|pageref|eqref)\{)", "~", text)
    out_tex.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Render paper-json manuscript to LaTeX using Interspeech class.")
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--paper-json", type=Path, default=Path("paper/paper.json"))
    ap.add_argument("--expected-version", type=str, default="1.0.0")
    ap.add_argument("--out-tex", type=Path, default=Path("paper/manuscript/generated_main.tex"))
    ap.add_argument("--out-trace-json", type=Path, default=Path("paper/snippets/manuscript_trace.json"))
    args = ap.parse_args()

    root = args.root.expanduser().resolve()
    out_tex = (root / args.out_tex).resolve() if not args.out_tex.is_absolute() else args.out_tex.resolve()
    out_trace = (root / args.out_trace_json).resolve() if not args.out_trace_json.is_absolute() else args.out_trace_json.resolve()
    paper_json = (root / args.paper_json).resolve() if not args.paper_json.is_absolute() else args.paper_json.resolve()

    renderer = _resolve_skill_renderer()
    cmd = [
        sys.executable,
        str(renderer),
        "--root",
        str(root),
        "--paper-json",
        str(paper_json),
        "--expected-version",
        str(args.expected_version),
        "--out-tex",
        str(out_tex),
        "--out-trace-json",
        str(out_trace),
    ]
    subprocess.run(cmd, check=True)

    _copy_interspeech_cls(root, out_tex.parent)
    _rewrite_preamble(out_tex)
    _expand_tabular_to_columnwidth(out_tex)
    _tighten_table_spacing(out_tex)
    _restore_inline_refs(out_tex)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
