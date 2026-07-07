#!/usr/bin/env python3
"""Project wrapper — delegates to llm-audit-supplement-zip skill script."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = Path(__file__).resolve().parent / "supplement_config.yaml"
SKILL_SCRIPT = Path.home() / ".codex" / "skills" / "llm-audit-supplement-zip" / "scripts" / "build_supplement.py"


def main() -> int:
    if not SKILL_SCRIPT.exists():
        print(f"Skill script not found: {SKILL_SCRIPT}", file=sys.stderr)
        print("Install skill: ~/.codex/skills/llm-audit-supplement-zip/", file=sys.stderr)
        return 1
    cmd = [
        "uv",
        "run",
        "--with",
        "pyyaml",
        "python",
        str(SKILL_SCRIPT),
        "--root",
        str(ROOT),
        "--config",
        str(CONFIG),
    ]
    env = os.environ.copy()
    return subprocess.call(cmd, cwd=ROOT, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
