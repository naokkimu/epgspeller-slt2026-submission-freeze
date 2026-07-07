#!/usr/bin/env python3
"""Freeze IEEE SLT 2026 submission snapshot: bundle, manifest, SHA256SUMS, optional export dir."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head(root: Path) -> tuple[str, bool]:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    dirty = bool(
        subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True).strip()
    )
    return commit, dirty


def git_branch(root: Path) -> str:
    return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root, text=True).strip()


def copy_if_exists(src: Path, dst: Path) -> bool:
    if not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def copy_tree_filtered(src: Path, dst: Path, *, exclude_dirs: Iterable[str]) -> None:
    if not src.is_dir():
        return
    exclude = set(exclude_dirs)
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        if any(part in exclude for part in rel.parts):
            continue
        if path.is_dir():
            continue
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def load_artifact_sources(config_path: Path) -> list[str]:
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    return [item["src"] for item in cfg.get("artifacts", []) or []]


def write_sha256sums(root: Path, rel_paths: list[str]) -> None:
    lines: list[str] = []
    for rel in sorted(rel_paths):
        path = root / rel
        if path.is_file():
            lines.append(f"{sha256_file(path)}  {rel}")
    (root / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Freeze SLT 2026 submission snapshot.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root")
    parser.add_argument(
        "--export-dir",
        type=Path,
        default=None,
        help="Optional standalone export directory for GitHub archive repo",
    )
    parser.add_argument(
        "--submission-pack",
        type=Path,
        default=Path("/Volumes/lysd26/SLT_submission/epgspeller-lexicon-free-slt2026"),
        help="Uploaded submission pack directory",
    )
    parser.add_argument(
        "--freeze-tag",
        default="freeze-slt2026-submission-20260707",
        help="Freeze tag identifier",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    pack = args.submission_pack.expanduser().resolve()
    freeze_dir = root / "reports" / "slt2026" / "submission"
    config_path = root / "paper" / "supplement" / "supplement_config.yaml"

    freeze_dir.mkdir(parents=True, exist_ok=True)

    # Submission uploads (canonical OpenReview pack)
    pack_files = {
        "EPGSpeller: Lexicon-Free Silent Spelling.pdf": "main_submission.pdf",
        "put_this_zip_to_your_agent_or_llm_chat.zip": "put_this_zip_to_your_agent_or_llm_chat.zip",
        "openreview_packet.md": "openreview_packet.md",
        "manifest.json": "submission_pack_manifest.json",
        "README.md": "submission_pack_README.md",
    }
    copied_rels: list[str] = []
    submission_names: list[str] = []
    for src_name, dst_name in pack_files.items():
        src = pack / src_name
        dst = freeze_dir / dst_name
        if copy_if_exists(src, dst):
            rel = f"reports/slt2026/submission/{dst_name}"
            copied_rels.append(rel)
            submission_names.append(dst_name)

    # In-repo manuscript + supplement sources
    repo_copies = [
        (root / "paper" / "final" / "slt2026.pdf", freeze_dir / "slt2026.pdf", "slt2026.pdf"),
        (
            root / "paper" / "submission" / "openreview_packet_epgspeller_slt2026.md",
            freeze_dir / "openreview_packet_project.md",
            "openreview_packet_project.md",
        ),
        (
            root / "paper" / "submission" / "put_this_zip_to_your_agent_or_llm_chat.zip",
            freeze_dir / "put_this_zip_project_copy.zip",
            "put_this_zip_project_copy.zip",
        ),
    ]
    for src, dst, name in repo_copies:
        if copy_if_exists(src, dst):
            copied_rels.append(f"reports/slt2026/submission/{name}")
            submission_names.append(name)

    # Freeze manifest
    commit, dirty = git_head(root)
    branch = git_branch(root)
    title = "EPGSpeller: Lexicon-Free Silent Spelling Recognition with Electropalatography"
    manifest = {
        "freeze_tag": args.freeze_tag,
        "venue": "IEEE SLT 2026",
        "title": title,
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_root": str(root),
        "branch": branch,
        "commit": commit,
        "dirty": dirty,
        "submission_pack_dir": str(pack),
        "checks_note": "Post-submission freeze; integrity gate passed at build time.",
        "artifacts": [{"path": rel, "sha256": sha256_file(root / rel)} for rel in copied_rels],
    }
    manifest_path = root / "reports" / "slt2026" / f"freeze_manifest_{args.freeze_tag}.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    write_sha256sums(freeze_dir, submission_names)

    # Tarball of submission bundle
    tar_path = root / "reports" / "slt2026" / f"{args.freeze_tag}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(freeze_dir, arcname=f"{args.freeze_tag}/submission")

    # Optional export directory for standalone GitHub archive
    if args.export_dir:
        export = args.export_dir.expanduser().resolve()
        if export.exists():
            shutil.rmtree(export)
        export.mkdir(parents=True)

        readme = f"""# EPGSpeller — IEEE SLT 2026 Submission Freeze

**Title:** {title}

**Freeze tag:** `{args.freeze_tag}`

**Source commit:** `{commit}` on branch `{branch}`

This repository is a **read-only post-submission snapshot**. Do not treat it as an active development tree.

## Upload bundle (`submission/`)

| File | Role |
|---|---|
| `main_submission.pdf` | OpenReview main PDF |
| `put_this_zip_to_your_agent_or_llm_chat.zip` | LLM audit supplementary zip |
| `openreview_packet.md` | OpenReview field packet |
| `submission_pack_manifest.json` | Pack file hashes |

Verify: `shasum -a 256 -c SHA256SUMS.txt`

## In-repo sources (`paper/`, `supplement/`, `results/`)

LaTeX sources, supplement config, and result CSVs referenced by the audit zip.

Generated: {manifest["timestamp_utc"]}
"""
        (export / "README.md").write_text(readme, encoding="utf-8")
        shutil.copy2(manifest_path, export / "FREEZE_MANIFEST.json")
        shutil.copytree(freeze_dir, export / "submission")

        # Paper sources (no LaTeX aux noise)
        copy_tree_filtered(
            root / "paper" / "final",
            export / "paper" / "final",
            exclude_dirs={
                "slt_audit_artifacts",
                "slt_audit_artifacts_closeout",
                "build",
            },
        )
        copy_tree_filtered(
            root / "paper" / "supplement",
            export / "paper" / "supplement",
            exclude_dirs={"staging"},
        )
        for rel in load_artifact_sources(config_path):
            src = root / rel
            dst = export / rel
            if src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

        export_sums: list[str] = []
        for path in sorted(export.rglob("*")):
            if path.is_file() and path.name != "SHA256SUMS.txt":
                rel = path.relative_to(export).as_posix()
                export_sums.append(f"{sha256_file(path)}  {rel}")
        (export / "SHA256SUMS.txt").write_text("\n".join(export_sums) + "\n", encoding="utf-8")

    print(f"freeze_tag: {args.freeze_tag}")
    print(f"manifest: {manifest_path}")
    print(f"submission_dir: {freeze_dir}")
    print(f"tarball: {tar_path}")
    print(f"commit: {commit} dirty={dirty}")
    if args.export_dir:
        print(f"export_dir: {args.export_dir}")
    if dirty:
        print("WARNING: working tree was dirty at freeze time; commit before tagging for a clean freeze.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
