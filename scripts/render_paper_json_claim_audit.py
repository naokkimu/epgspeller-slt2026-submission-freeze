#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _get_id(obj: Any) -> Optional[str]:
    if isinstance(obj, dict):
        v = obj.get("id")
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


@dataclass(frozen=True)
class EvidenceCheck:
    evidence_id: str
    path: str
    exists: bool
    sha256_pinned: Optional[str]
    sha256_actual: Optional[str]
    sha256_ok: Optional[bool]


def _check_evidence(evidence: List[Any], root: Path) -> Tuple[List[EvidenceCheck], List[str]]:
    checks: List[EvidenceCheck] = []
    errors: List[str] = []

    for i, ev in enumerate(evidence):
        if not isinstance(ev, dict):
            errors.append(f"evidence[{i}] not an object")
            continue
        ev_id = _get_id(ev) or f"<no-id:{i}>"
        path_s = ev.get("path")

        if not isinstance(path_s, str) or not path_s.strip():
            checks.append(
                EvidenceCheck(
                    evidence_id=ev_id,
                    path="",
                    exists=False,
                    sha256_pinned=(ev.get("sha256") if isinstance(ev.get("sha256"), str) else None),
                    sha256_actual=None,
                    sha256_ok=None,
                )
            )
            continue

        rel = Path(path_s)
        abs_path = (root / rel).resolve() if not rel.is_absolute() else rel
        exists = abs_path.exists()

        sha_pin = ev.get("sha256") if isinstance(ev.get("sha256"), str) else None
        sha_act = None
        ok = None

        if exists and sha_pin and len(sha_pin.strip()) == 64:
            sha_act = _sha256_file(abs_path)
            ok = sha_act == sha_pin.strip().lower()

        checks.append(
            EvidenceCheck(
                evidence_id=ev_id,
                path=path_s,
                exists=exists,
                sha256_pinned=sha_pin,
                sha256_actual=sha_act,
                sha256_ok=ok,
            )
        )

    return checks, errors


def render(paper_json: Path, root: Path, out_md: Path, strict: bool) -> int:
    doc = _load_json(paper_json)
    if not isinstance(doc, dict):
        raise ValueError("paper.json must be an object")

    claims = doc.get("claims", [])
    evidence = doc.get("evidence", [])
    runs = doc.get("runs", [])
    experiments = doc.get("experiments", [])

    if (
        not isinstance(claims, list)
        or not isinstance(evidence, list)
        or not isinstance(runs, list)
        or not isinstance(experiments, list)
    ):
        raise ValueError("paper.json must contain list fields: claims/evidence/runs/experiments")

    evidence_by_id: Dict[str, Dict[str, Any]] = {}
    for ev in evidence:
        if not isinstance(ev, dict):
            continue
        ev_id = _get_id(ev)
        if ev_id:
            evidence_by_id[ev_id] = ev

    ev_checks, ev_errors = _check_evidence(evidence, root=root)

    md: List[str] = []
    md.append("# Claim audit (paper.json)")
    md.append("")

    md.append("## Summary")
    md.append(f"- Claims: {len(claims)}")
    md.append(f"- Evidence: {len(evidence)}")
    md.append(f"- Runs: {len(runs)}")
    md.append(f"- Experiments: {len(experiments)}")
    md.append("")

    if ev_errors:
        md.append("## Evidence parse errors")
        for e in ev_errors:
            md.append(f"- {e}")
        md.append("")

    md.append("## Evidence checks")
    if not ev_checks:
        md.append("(no evidence registered)")
        md.append("")
    else:
        md.append("| evidence_id | path | exists | sha256_ok |")
        md.append("|---|---|---:|---:|")
        for ch in ev_checks:
            sha_ok = "" if ch.sha256_ok is None else ("yes" if ch.sha256_ok else "no")
            md.append(f"| {ch.evidence_id} | {ch.path} | {str(ch.exists).lower()} | {sha_ok} |")
        md.append("")

    md.append("## Claims")
    if not claims:
        md.append("(no claims registered)")
        md.append("")
    else:
        for i, cl in enumerate(claims):
            if not isinstance(cl, dict):
                md.append(f"- claims[{i}] is not an object")
                continue
            cl_id = _get_id(cl) or f"<no-id:{i}>"
            stmt = cl.get("statement") or cl.get("claim") or cl.get("text") or ""
            md.append(f"### {cl_id}")
            if isinstance(stmt, str) and stmt.strip():
                md.append(stmt.strip())

            refs = None
            for key in ("evidence_ids", "evidence", "evidenceIds"):
                if key in cl:
                    refs = cl.get(key)
                    break

            if isinstance(refs, list):
                missing: List[str] = []
                for rid in refs:
                    if not isinstance(rid, str) or not rid.strip():
                        continue
                    if rid.strip() not in evidence_by_id:
                        missing.append(rid.strip())
                md.append(f"- evidence_refs: {len(refs)}")
                if missing:
                    md.append("- missing_evidence_ids: " + ", ".join(missing))
            md.append("")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(md).rstrip() + "\n")

    if strict:
        for ch in ev_checks:
            if ch.path and not ch.exists:
                return 1
            if ch.sha256_ok is False:
                return 1
        if ev_errors:
            return 1

    return 0


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--paper-json", default="paper/paper.json")
    p.add_argument("--root", default=".")
    p.add_argument("--out-md", required=True)
    p.add_argument("--strict", action="store_true")
    args = p.parse_args(argv)

    return render(
        paper_json=Path(args.paper_json),
        root=Path(args.root),
        out_md=Path(args.out_md),
        strict=bool(args.strict),
    )


if __name__ == "__main__":
    raise SystemExit(main())
