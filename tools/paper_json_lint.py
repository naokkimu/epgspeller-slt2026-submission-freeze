from __future__ import annotations

"""Strict, deterministic CI gate for paper/paper.json (paper-json v1.0.0).

Design goals:
- Fail-closed: CI mode rejects any format.version != expected (default: 1.0.0).
- Deterministic: stable ordering, stable exit code, no timestamps.
- Stdlib-only: safe to run in CI without pip installs.
- Manuscript-first: `paper/paper.json` is the paper itself (machine-readable manuscript).
"""

import argparse
import csv
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple, Union


SHA256_RE = re.compile(r"^[0-9a-f]{64}$", flags=re.IGNORECASE)
DEFAULT_BANNED_TOKEN_RE = r"\b(TBD|TODO|placeholder|mock)\b"
SLOT_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
DIGIT_RE = re.compile(r"[0-9]")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json_obj(path: Path) -> Dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise SystemExit(f"paper.json must be an object: {path}")
    return obj


def _rel(path: Path, *, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def _safe_str(x: Any) -> str:
    return "" if x is None else str(x)


def _ensure_list(doc: Dict[str, Any], key: str) -> List[Any]:
    v = doc.get(key)
    if v is None:
        return []
    if not isinstance(v, list):
        raise SystemExit(f"paper.json: {key} must be a list")
    return v


def _compile_banned_re(pattern: str) -> re.Pattern[str]:
    try:
        return re.compile(pattern, flags=re.IGNORECASE)
    except re.error as e:
        raise SystemExit(f"invalid banned token regex: {e}")


def _check_banned_token(value: Any, *, banned_re: re.Pattern[str], where: str, errors: List[str]) -> None:
    if not isinstance(value, str) or not value:
        return
    m = banned_re.search(value)
    if m:
        errors.append(f"banned token {m.group(0)!r} in {where}")


def _validate_rel_path(path_str: str, *, root: Path, where: str, errors: List[str]) -> Optional[Tuple[str, Path]]:
    raw = (path_str or "").strip()
    if not raw:
        errors.append(f"{where}: missing path")
        return None
    p = Path(raw)
    if p.is_absolute():
        errors.append(f"{where}: path must be relative (got absolute): {raw}")
        return None
    if ".." in p.parts:
        errors.append(f"{where}: path must not contain '..': {raw}")
        return None

    root_resolved = root.resolve()
    abs_path = (root_resolved / p).resolve()
    try:
        abs_path.relative_to(root_resolved)
    except Exception:
        errors.append(f"{where}: path escapes root: {raw}")
        return None
    return p.as_posix(), abs_path


def _validate_sha256(value: Any, *, where: str, errors: List[str]) -> Optional[str]:
    s = _safe_str(value).strip().lower()
    if not s or not SHA256_RE.match(s):
        errors.append(f"{where}: missing/invalid sha256 (expected 64-hex)")
        return None
    return s


def _json_pointer_get(obj: Any, pointer: str) -> Any:
    # RFC 6901-ish; minimal implementation.
    if pointer == "":
        return obj
    if not pointer.startswith("/"):
        raise ValueError("json pointer must start with '/'")
    cur: Any = obj
    for part in pointer.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, dict):
            if part not in cur:
                raise KeyError(part)
            cur = cur[part]
            continue
        if isinstance(cur, list):
            try:
                idx = int(part)
            except Exception as e:
                raise KeyError(part) from e
            if idx < 0 or idx >= len(cur):
                raise IndexError(idx)
            cur = cur[idx]
            continue
        raise KeyError(part)
    return cur


def _extract_table_cell(path: Path, *, delimiter: str, row: int, col: Union[int, str]) -> str:
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        header = next(reader, None)
        if header is None:
            raise ValueError("table is empty")
        header_str = [str(x) for x in header]
        if isinstance(col, int):
            col_idx = col
        else:
            if col not in header_str:
                raise KeyError(f"missing column: {col}")
            col_idx = header_str.index(col)

        for i, r in enumerate(reader):
            if i != row:
                continue
            if col_idx < 0 or col_idx >= len(r):
                raise IndexError(f"col index out of range: {col_idx}")
            return str(r[col_idx])
    raise IndexError(f"row index out of range: {row}")


def _parse_bibtex_keys(text: str) -> Set[str]:
    # Minimal: extract keys from lines like "@article{key," with optional whitespace.
    keys: Set[str] = set()
    for m in re.finditer(r"@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,", text):
        keys.add(m.group(1))
    return keys


@dataclass(frozen=True)
class EvidenceState:
    evidence_id: str
    rel_path: str
    abs_path: Path
    sha256_declared: str
    exists: bool
    sha256_actual: Optional[str]
    sha256_ok: bool


def _slot_names_in_template(template: str) -> List[str]:
    out: List[str] = []
    seen: Set[str] = set()
    for m in SLOT_RE.finditer(template or ""):
        name = m.group(1)
        if name not in seen:
            out.append(name)
            seen.add(name)
    return out


def _extract_slot_value(
    slot_spec: Dict[str, Any],
    *,
    evidence_by_id: Dict[str, EvidenceState],
    root: Path,
) -> str:
    stype = _safe_str(slot_spec.get("type")).strip()
    if stype == "literal":
        return _safe_str(slot_spec.get("value"))
    if stype != "extract":
        raise ValueError(f"unknown slot type: {stype!r}")

    extract = slot_spec.get("extract")
    if not isinstance(extract, dict):
        raise ValueError("extract slot requires extract{}")
    kind = _safe_str(extract.get("kind")).strip()
    evidence_id = _safe_str(extract.get("evidence_id")).strip()
    if not evidence_id:
        raise ValueError("extract slot requires extract.evidence_id")
    ev = evidence_by_id.get(evidence_id)
    if ev is None:
        raise KeyError(f"unknown evidence_id: {evidence_id}")
    if not ev.exists or not ev.sha256_ok:
        raise ValueError(f"evidence not usable (missing or sha mismatch): {evidence_id} ({ev.rel_path})")

    path = ev.abs_path
    if kind == "tsv_cell":
        row = int(extract.get("row"))
        col = extract.get("col")
        if isinstance(col, int):
            col_spec: Union[int, str] = col
        else:
            col_spec = _safe_str(col).strip()
            if col_spec == "":
                raise ValueError("tsv_cell requires extract.col")
        return _extract_table_cell(path, delimiter="\t", row=row, col=col_spec)
    if kind == "csv_cell":
        row = int(extract.get("row"))
        col = extract.get("col")
        if isinstance(col, int):
            col_spec = col
        else:
            col_spec = _safe_str(col).strip()
            if col_spec == "":
                raise ValueError("csv_cell requires extract.col")
        return _extract_table_cell(path, delimiter=",", row=row, col=col_spec)
    if kind == "json_pointer":
        pointer = _safe_str(extract.get("pointer")).strip()
        if not pointer:
            raise ValueError("json_pointer requires extract.pointer")
        obj = json.loads(path.read_text(encoding="utf-8"))
        val = _json_pointer_get(obj, pointer)
        if isinstance(val, (dict, list)):
            return json.dumps(val, ensure_ascii=False, sort_keys=True)
        return _safe_str(val)
    if kind == "regex":
        pattern = _safe_str(extract.get("pattern"))
        if not pattern:
            raise ValueError("regex requires extract.pattern")
        group = int(extract.get("group", 1))
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.search(pattern, text)
        if not m:
            raise ValueError("regex did not match")
        return _safe_str(m.group(group))

    raise ValueError(f"unknown extract.kind: {kind!r}")


def lint(
    paper_json_path: Path,
    *,
    root: Path,
    mode: str = "dev",
    expected_version: str = "1.0.0",
    banned_token_re: Optional[str] = None,
) -> int:
    doc = _load_json_obj(paper_json_path)
    errors: List[str] = []
    warnings: List[str] = []

    if mode not in {"dev", "ci"}:
        raise SystemExit(f"unknown mode: {mode!r}")

    fmt = doc.get("format")
    if not isinstance(fmt, dict) or fmt.get("name") != "paper-json":
        errors.append("missing/invalid: format.name == 'paper-json'")
        version = None
    else:
        version = _safe_str(fmt.get("version")).strip()

    # Fail-closed on format.version mismatch.
    if version != expected_version:
        msg = f"format.version must be {expected_version!r} (got {version!r})"
        if mode == "ci":
            errors.append(msg)
        else:
            errors.append(msg)

    policy = doc.get("policy")
    policy_obj = policy if isinstance(policy, dict) else {}
    banned_pat = banned_token_re if banned_token_re is not None else _safe_str(policy_obj.get("banned_token_re")).strip()
    if not banned_pat:
        banned_pat = DEFAULT_BANNED_TOKEN_RE
    banned_re = _compile_banned_re(banned_pat)

    forbid_digits = bool(policy_obj.get("forbid_digits_in_templates", True))
    allowlist = policy_obj.get("allowlist_block_kinds")
    if isinstance(allowlist, list):
        allow_kinds = sorted(set([_safe_str(x).strip() for x in allowlist if _safe_str(x).strip()]))
    else:
        allow_kinds = ["bullets", "equation", "figure", "paragraph", "table"]

    # Evidence registry (sha256 required even in dev).
    evidence_state: Dict[str, EvidenceState] = {}
    evidence_ids_seen: Set[str] = set()
    evidence_list = _ensure_list(doc, "evidence")
    for ev in evidence_list:
        if not isinstance(ev, dict):
            errors.append("evidence entry must be an object")
            continue
        ev_id = _safe_str(ev.get("id")).strip()
        if not ev_id:
            errors.append("evidence entry missing id")
            continue
        if ev_id in evidence_ids_seen:
            errors.append(f"duplicate evidence id: {ev_id}")
            continue
        evidence_ids_seen.add(ev_id)

        _check_banned_token(ev.get("notes"), banned_re=banned_re, where=f"evidence {ev_id}.notes", errors=errors)

        rel = _safe_str(ev.get("path")).strip()
        vr = _validate_rel_path(rel, root=root, where=f"evidence {ev_id}", errors=errors)
        sha = _validate_sha256(ev.get("sha256"), where=f"evidence {ev_id}.sha256", errors=errors)
        if vr is None or sha is None:
            continue
        rel_path, abs_path = vr

        exists = abs_path.exists() and abs_path.is_file()
        if not exists:
            if mode == "ci":
                errors.append(f"evidence {ev_id}: missing file: {rel_path}")
            else:
                warnings.append(f"evidence {ev_id}: missing file: {rel_path}")
            evidence_state[ev_id] = EvidenceState(
                evidence_id=ev_id,
                rel_path=rel_path,
                abs_path=abs_path,
                sha256_declared=sha,
                exists=False,
                sha256_actual=None,
                sha256_ok=False,
            )
            continue

        actual = _sha256_file(abs_path)
        sha_ok = actual.lower() == sha.lower()
        if not sha_ok:
            errors.append(f"evidence {ev_id}: sha256 mismatch: declared={sha} actual={actual} path={rel_path}")
        evidence_state[ev_id] = EvidenceState(
            evidence_id=ev_id,
            rel_path=rel_path,
            abs_path=abs_path,
            sha256_declared=sha,
            exists=True,
            sha256_actual=actual.lower(),
            sha256_ok=sha_ok,
        )

    # Runs/experiments: banned token scan (CI only).
    if mode == "ci":
        for run in _ensure_list(doc, "runs"):
            if not isinstance(run, dict):
                continue
            rid = _safe_str(run.get("id")).strip() or "<missing id>"
            cmd = run.get("command")
            if not isinstance(cmd, dict):
                continue
            _check_banned_token(cmd.get("cwd"), banned_re=banned_re, where=f"run {rid}.command.cwd", errors=errors)
            argv = cmd.get("argv")
            if isinstance(argv, list):
                for i, a in enumerate(argv):
                    _check_banned_token(a, banned_re=banned_re, where=f"run {rid}.command.argv[{i}]", errors=errors)

        for exp in _ensure_list(doc, "experiments"):
            if not isinstance(exp, dict):
                continue
            eid = _safe_str(exp.get("id")).strip() or "<missing id>"
            _check_banned_token(exp.get("name"), banned_re=banned_re, where=f"experiment {eid}.name", errors=errors)
            _check_banned_token(exp.get("protocol"), banned_re=banned_re, where=f"experiment {eid}.protocol", errors=errors)

    # Manuscript + blocks.
    manuscript = doc.get("manuscript")
    if not isinstance(manuscript, dict):
        errors.append("missing/invalid: manuscript{}")
        manuscript = {}
    title = _safe_str(manuscript.get("title")).strip()
    if not title:
        warnings.append("manuscript.title is empty")

    bib_keys: Optional[Set[str]] = None
    bib = manuscript.get("bibliography")
    if bib is not None:
        if not isinstance(bib, dict):
            errors.append("manuscript.bibliography must be an object")
        else:
            bib_ev_id = _safe_str(bib.get("bibtex_evidence_id")).strip()
            if not bib_ev_id:
                errors.append("manuscript.bibliography.bibtex_evidence_id must be non-empty")
            else:
                ev = evidence_state.get(bib_ev_id)
                if ev is None:
                    errors.append(f"bibliography references unknown evidence_id: {bib_ev_id}")
                else:
                    if mode == "ci" and (not ev.exists or not ev.sha256_ok):
                        errors.append(f"bibliography evidence is missing/invalid: {bib_ev_id} ({ev.rel_path})")
                    if ev.exists and ev.sha256_ok:
                        try:
                            bib_text = ev.abs_path.read_text(encoding="utf-8", errors="replace")
                        except Exception as e:
                            errors.append(f"failed to read bibtex evidence: {bib_ev_id} ({ev.rel_path}) error={e!r}")
                        else:
                            bib_keys = _parse_bibtex_keys(bib_text)

    blocks = _ensure_list(doc, "blocks")
    blocks_by_id: Dict[str, Dict[str, Any]] = {}
    for b in blocks:
        if not isinstance(b, dict):
            errors.append("blocks[] entries must be objects")
            continue
        bid = _safe_str(b.get("id")).strip()
        if not bid:
            errors.append("block missing id")
            continue
        if bid in blocks_by_id:
            errors.append(f"duplicate block id: {bid}")
            continue
        blocks_by_id[bid] = b

    sections = manuscript.get("sections")
    if sections is None:
        sections = []
    if not isinstance(sections, list):
        errors.append("manuscript.sections must be a list")
        sections = []

    referenced_block_ids: List[str] = []
    section_ids_seen: Set[str] = set()
    for sec in sections:
        if not isinstance(sec, dict):
            errors.append("manuscript.sections[] entries must be objects")
            continue
        sid = _safe_str(sec.get("id")).strip()
        if not sid:
            errors.append("section missing id")
            continue
        if sid in section_ids_seen:
            errors.append(f"duplicate section id: {sid}")
            continue
        section_ids_seen.add(sid)
        blk_ids = sec.get("blocks")
        if blk_ids is None:
            blk_ids = []
        if not isinstance(blk_ids, list):
            errors.append(f"section {sid}: blocks must be a list")
            continue
        for x in blk_ids:
            bid = _safe_str(x).strip()
            if not bid:
                errors.append(f"section {sid}: block id must be non-empty string")
                continue
            referenced_block_ids.append(bid)

    def _validate_template_text(text: str, *, where: str) -> None:
        _check_banned_token(text, banned_re=banned_re, where=where, errors=errors)
        if forbid_digits and DIGIT_RE.search(text or ""):
            errors.append(f"digits are forbidden in templates: {where}")

    def _validate_slot_spec(name: str, spec: Any, *, where: str) -> None:
        if not isinstance(spec, dict):
            errors.append(f"{where}: slot {name} must be an object")
            return
        stype = _safe_str(spec.get("type")).strip()
        if stype == "literal":
            val = _safe_str(spec.get("value"))
            _check_banned_token(val, banned_re=banned_re, where=f"{where}.slots.{name}.value", errors=errors)
            if forbid_digits and DIGIT_RE.search(val or ""):
                errors.append(f"digits are forbidden in literal slot values: {where}.slots.{name}.value")
            return
        if stype == "extract":
            try:
                _extract_slot_value(spec, evidence_by_id=evidence_state, root=root)
            except Exception as e:
                errors.append(f"{where}.slots.{name}: extraction failed: {e!r}")
            return
        errors.append(f"{where}.slots.{name}: unknown slot type: {stype!r}")

    def _validate_citations(citations: Any, *, where: str) -> None:
        if citations is None:
            return
        if not isinstance(citations, list):
            errors.append(f"{where}.citations must be a list")
            return
        if bib_keys is None:
            # Without a bibtex snapshot, we cannot verify keys.
            warnings.append(f"{where}.citations present but no manuscript.bibliography.bibtex_evidence_id to verify keys")
            return
        for c in citations:
            raw = _safe_str(c).strip()
            if not raw:
                errors.append(f"{where}.citations contains empty key")
                continue
            key = raw[1:] if raw.startswith("@") else raw
            if key not in bib_keys:
                errors.append(f"{where}.citations references missing bib key: {key}")

    ASSERT_OPS = {"==", "!=", "<", "<=", ">", ">="}
    NUM_OPS = {"<", "<=", ">", ">="}

    def _assert_operand_value(value: Any, *, where: str) -> Any:
        if isinstance(value, (int, float, str)):
            return value
        if isinstance(value, dict):
            # Treat as an extract spec (same shape as slots[].extract).
            return _extract_slot_value({"type": "extract", "extract": value}, evidence_by_id=evidence_state, root=root)
        raise ValueError(f"{where}: operand must be a number/string or an extract object")

    def _cast_value(value: Any, cast: str) -> Any:
        s = str(value).strip()
        if cast == "string":
            return s
        if cast == "int":
            return int(s)
        if cast == "float":
            return float(s)
        raise ValueError(f"unknown cast: {cast!r}")

    def _compare(left: Any, op: str, right: Any) -> bool:
        if op == "==":
            return left == right
        if op == "!=":
            return left != right
        if op == "<":
            return left < right
        if op == "<=":
            return left <= right
        if op == ">":
            return left > right
        if op == ">=":
            return left >= right
        raise ValueError(f"unknown op: {op!r}")

    def _validate_assertions(assertions: Any, *, where: str) -> None:
        if assertions is None:
            return
        if not isinstance(assertions, list):
            errors.append(f"{where}.assertions must be a list")
            return
        seen_ids: Set[str] = set()
        for i, a in enumerate(assertions):
            if not isinstance(a, dict):
                errors.append(f"{where}.assertions[{i}] must be an object")
                continue
            aid = _safe_str(a.get("id")).strip()
            if not aid:
                errors.append(f"{where}.assertions[{i}].id must be non-empty")
                continue
            if aid in seen_ids:
                errors.append(f"{where}.assertions[{i}].id is duplicated: {aid!r}")
                continue
            seen_ids.add(aid)

            op = _safe_str(a.get("op")).strip()
            if op not in ASSERT_OPS:
                errors.append(f"{where}.assertions[{i}] ({aid}): invalid op: {op!r}")
                continue
            cast = _safe_str(a.get("cast")).strip() or None
            if cast is not None and cast not in {"float", "int", "string"}:
                errors.append(f"{where}.assertions[{i}] ({aid}): invalid cast: {cast!r}")
                continue
            if op in NUM_OPS and cast == "string":
                errors.append(f"{where}.assertions[{i}] ({aid}): numeric op requires numeric cast")
                continue

            try:
                left_raw = _assert_operand_value(a.get("left"), where=f"{where}.assertions[{i}].left")
                right_raw = _assert_operand_value(a.get("right"), where=f"{where}.assertions[{i}].right")
            except Exception as e:
                errors.append(f"{where}.assertions[{i}] ({aid}): operand extraction failed: {e!r}")
                continue

            try:
                if cast is not None:
                    left = _cast_value(left_raw, cast)
                    right = _cast_value(right_raw, cast)
                    ok = _compare(left, op, right)
                else:
                    if op in NUM_OPS:
                        left = _cast_value(left_raw, "float")
                        right = _cast_value(right_raw, "float")
                        ok = _compare(left, op, right)
                    else:
                        # For equality ops, try numeric comparison first; fall back to string.
                        try:
                            left = _cast_value(left_raw, "float")
                            right = _cast_value(right_raw, "float")
                            ok = _compare(left, op, right)
                        except Exception:
                            ok = _compare(str(left_raw), op, str(right_raw))
            except Exception as e:
                errors.append(f"{where}.assertions[{i}] ({aid}): evaluation failed: {e!r}")
                continue

            if not ok:
                errors.append(
                    f"{where}.assertions[{i}] ({aid}) failed: left={left_raw!r} op={op} right={right_raw!r}"
                )

    def _validate_block(block: Dict[str, Any], *, where: str) -> None:
        kind = _safe_str(block.get("kind")).strip()
        status = _safe_str(block.get("status")).strip()
        if kind not in allow_kinds:
            errors.append(f"{where}: kind {kind!r} is not in allowlist")
        if status != "supported":
            errors.append(f"{where}: referenced block must have status='supported' (got {status!r})")

        ev_ids = block.get("evidence_ids")
        if not isinstance(ev_ids, list) or not ev_ids:
            errors.append(f"{where}: referenced block must have non-empty evidence_ids")
            ev_list: List[str] = []
        else:
            ev_list = []
            for x in ev_ids:
                s = _safe_str(x).strip()
                if not s:
                    errors.append(f"{where}: evidence_id must be non-empty string")
                    continue
                ev_list.append(s)
                if s not in evidence_state:
                    errors.append(f"{where}: unknown evidence_id: {s}")
                else:
                    ev = evidence_state[s]
                    if mode == "ci" and (not ev.exists or not ev.sha256_ok):
                        errors.append(f"{where}: evidence missing/invalid: {s} ({ev.rel_path})")

        _validate_assertions(block.get("assertions"), where=where)

        # Validate kind-specific fields (templates/slots/citations).
        if kind == "paragraph":
            tpl = _safe_str(block.get("template"))
            if not tpl.strip():
                errors.append(f"{where}: paragraph.template must be non-empty")
                tpl = ""
            _validate_template_text(tpl, where=f"{where}.template")
            slots = block.get("slots") or {}
            if not isinstance(slots, dict):
                errors.append(f"{where}.slots must be an object")
                slots = {}
            for sn in _slot_names_in_template(tpl):
                if sn not in slots:
                    errors.append(f"{where}: missing slot definition for {{{sn}}}")
                else:
                    _validate_slot_spec(sn, slots.get(sn), where=where)
            _validate_citations(block.get("citations"), where=where)
            return

        if kind == "bullets":
            items = block.get("items")
            if not isinstance(items, list) or not items:
                errors.append(f"{where}: bullets.items must be a non-empty list")
                return
            for i, it in enumerate(items):
                if not isinstance(it, dict):
                    errors.append(f"{where}.items[{i}] must be an object")
                    continue
                tpl = _safe_str(it.get("template"))
                if not tpl.strip():
                    errors.append(f"{where}.items[{i}].template must be non-empty")
                    tpl = ""
                _validate_template_text(tpl, where=f"{where}.items[{i}].template")
                slots = it.get("slots") or {}
                if not isinstance(slots, dict):
                    errors.append(f"{where}.items[{i}].slots must be an object")
                    slots = {}
                for sn in _slot_names_in_template(tpl):
                    if sn not in slots:
                        errors.append(f"{where}.items[{i}]: missing slot definition for {{{sn}}}")
                    else:
                        _validate_slot_spec(sn, slots.get(sn), where=f"{where}.items[{i}]")
                _validate_citations(it.get("citations"), where=f"{where}.items[{i}]")
            return

        if kind == "table":
            src = block.get("source")
            if not isinstance(src, dict):
                errors.append(f"{where}: table.source must be an object")
            else:
                sid = _safe_str(src.get("evidence_id")).strip()
                if not sid:
                    errors.append(f"{where}: table.source.evidence_id must be non-empty")
                elif sid not in evidence_state:
                    errors.append(f"{where}: table.source references unknown evidence_id: {sid}")
            cap = _safe_str(block.get("caption_template"))
            if not cap.strip():
                errors.append(f"{where}: table.caption_template must be non-empty")
                cap = ""
            _validate_template_text(cap, where=f"{where}.caption_template")
            slots = block.get("slots") or {}
            if not isinstance(slots, dict):
                errors.append(f"{where}.slots must be an object")
                slots = {}
            for sn in _slot_names_in_template(cap):
                if sn not in slots:
                    errors.append(f"{where}: missing slot definition for {{{sn}}}")
                else:
                    _validate_slot_spec(sn, slots.get(sn), where=where)
            _validate_citations(block.get("citations"), where=where)
            return

        if kind == "figure":
            src = block.get("source")
            if not isinstance(src, dict):
                errors.append(f"{where}: figure.source must be an object")
            else:
                sid = _safe_str(src.get("evidence_id")).strip()
                if not sid:
                    errors.append(f"{where}: figure.source.evidence_id must be non-empty")
                elif sid not in evidence_state:
                    errors.append(f"{where}: figure.source references unknown evidence_id: {sid}")
            cap = _safe_str(block.get("caption_template"))
            if not cap.strip():
                errors.append(f"{where}: figure.caption_template must be non-empty")
                cap = ""
            _validate_template_text(cap, where=f"{where}.caption_template")
            slots = block.get("slots") or {}
            if not isinstance(slots, dict):
                errors.append(f"{where}.slots must be an object")
                slots = {}
            for sn in _slot_names_in_template(cap):
                if sn not in slots:
                    errors.append(f"{where}: missing slot definition for {{{sn}}}")
                else:
                    _validate_slot_spec(sn, slots.get(sn), where=where)
            _validate_citations(block.get("citations"), where=where)
            return

        if kind == "equation":
            latex = _safe_str(block.get("latex"))
            if not latex.strip():
                errors.append(f"{where}: equation.latex must be non-empty")
            _check_banned_token(latex, banned_re=banned_re, where=f"{where}.latex", errors=errors)
            return

    # Validate referenced blocks only (paper = manuscript).
    for bid in referenced_block_ids:
        b = blocks_by_id.get(bid)
        if b is None:
            errors.append(f"manuscript references unknown block id: {bid}")
            continue
        _validate_block(b, where=f"block {bid}")

    for w in sorted(set(warnings)):
        print(f"[paper_json_lint][WARN] {w}")
    for e in sorted(set(errors)):
        print(f"[paper_json_lint][ERROR] {e}")
    if errors:
        return 1
    print("[paper_json_lint] OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint paper/paper.json (paper-json v1 manuscript gate)")
    ap.add_argument("--paper-json", type=Path, default=Path("paper/paper.json"))
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--mode", choices=["dev", "ci"], default="dev", help="Lint mode (default: dev)")
    ap.add_argument("--ci", action="store_true", help="Alias for --mode ci")
    ap.add_argument(
        "--expected-version",
        type=str,
        default="1.0.0",
        help="Fail-closed expected format.version (default: 1.0.0)",
    )
    ap.add_argument(
        "--banned-token-re",
        type=str,
        default=None,
        help="Override policy.banned_token_re (default: read from paper.json policy, then fallback).",
    )
    args = ap.parse_args()
    mode = "ci" if args.ci else args.mode
    return lint(
        args.paper_json,
        root=args.root.resolve(),
        mode=mode,
        expected_version=str(args.expected_version),
        banned_token_re=(str(args.banned_token_re) if args.banned_token_re is not None else None),
    )


if __name__ == "__main__":
    raise SystemExit(main())
