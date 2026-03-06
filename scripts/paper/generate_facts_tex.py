#!/usr/bin/env python3
"""Generate LaTeX facts/tables from pinned evidence in paper/paper.json.

Constraints:
- No handwritten numeric facts in the manuscript.
- Every generated number must be traceable to a pinned evidence file.

This script is deterministic: same inputs => identical outputs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import yaml


@dataclass(frozen=True)
class EvidenceRef:
    evidence_id: str
    path: Path
    sha256: str
    kind: str


class SpecError(RuntimeError):
    pass


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_paper_json(paper_json_path: Path) -> Dict[str, Any]:
    with paper_json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_evidence(paper_json: Mapping[str, Any], root: Path, evidence_id: str) -> EvidenceRef:
    matches = [e for e in paper_json.get("evidence", []) if e.get("id") == evidence_id]
    if not matches:
        raise SpecError(f"evidence_id not found in paper.json: {evidence_id}")
    if len(matches) != 1:
        raise SpecError(f"evidence_id is not unique in paper.json: {evidence_id}")

    e = matches[0]
    rel_path = e.get("path")
    sha256_expected = e.get("sha256")
    kind = e.get("kind", "")

    if not isinstance(rel_path, str) or not rel_path:
        raise SpecError(f"Invalid evidence.path for {evidence_id}: {rel_path!r}")
    if not isinstance(sha256_expected, str) or not sha256_expected:
        raise SpecError(f"Missing evidence.sha256 for {evidence_id}")

    abs_path = (root / rel_path).resolve()
    if not abs_path.exists():
        raise SpecError(f"Evidence file missing for {evidence_id}: {abs_path}")

    sha256_actual = _sha256_file(abs_path)
    if sha256_actual != sha256_expected:
        raise SpecError(
            "sha256 mismatch for evidence_id="
            f"{evidence_id}: expected={sha256_expected} actual={sha256_actual} path={abs_path}"
        )

    return EvidenceRef(evidence_id=evidence_id, path=abs_path, sha256=sha256_expected, kind=kind)


def _read_csv_dicts(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise SpecError(f"CSV has no header: {path}")
        return list(reader)


def _filter_rows(rows: Sequence[Mapping[str, str]], filters: Optional[Mapping[str, Any]] = None) -> List[Mapping[str, str]]:
    if not filters:
        return list(rows)

    out: List[Mapping[str, str]] = []
    for row in rows:
        ok = True
        for k, v in filters.items():
            if k not in row:
                raise SpecError(f"Filter column missing: {k}")
            if str(row[k]) != str(v):
                ok = False
                break
        if ok:
            out.append(row)
    return out


def _unique_values(rows: Sequence[Mapping[str, str]], column: str) -> List[str]:
    if not rows:
        raise SpecError("No rows to compute unique values")

    vals: List[str] = []
    for r in rows:
        if column not in r:
            raise SpecError(f"CSV column missing: {column}")
        vals.append(r[column])
    return sorted(set(vals))


def _parse_float(value: str, context: str) -> float:
    try:
        return float(value)
    except Exception as e:
        raise SpecError(f"Failed to parse float for {context}: {value!r}") from e


def _mean_std(values: Sequence[float]) -> Tuple[float, float]:
    if not values:
        raise SpecError("Cannot compute mean/std of empty list")
    mean = sum(values) / len(values)
    var = sum((x - mean) ** 2 for x in values) / len(values)
    return mean, math.sqrt(var)


def _load_smartpalate_grid(path: Path) -> List[List[int]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        grid: List[List[int]] = []
        for row in reader:
            if not row:
                continue
            parsed: List[int] = []
            for cell in row:
                cell = cell.strip()
                if cell == "":
                    continue
                try:
                    parsed.append(int(cell))
                except Exception as e:
                    raise SpecError(f"Non-integer cell in smartpalate CSV: {cell!r}") from e
            if parsed:
                grid.append(parsed)

    if not grid:
        raise SpecError(f"Empty smartpalate grid: {path}")
    return grid


def _smartpalate_stats(grid: List[List[int]]) -> Dict[str, int]:
    n_rows = len(grid)
    n_cols = max(len(r) for r in grid)

    counts: Dict[int, int] = {}
    for r in grid:
        for v in r:
            if v in (-1, 124):
                continue
            counts[v] = counts.get(v, 0) + 1

    if not counts:
        raise SpecError("No valid channels found in smartpalate grid")

    max_ch = max(counts)
    total_channels = max_ch + 1
    mapped_channels = len(counts)
    unmapped_channels = total_channels - mapped_channels
    duplicated_channels = sum(1 for c in counts.values() if c > 1)

    return {
        "grid_rows": n_rows,
        "grid_cols": n_cols,
        "total_channels": total_channels,
        "mapped_channels": mapped_channels,
        "unmapped_channels": unmapped_channels,
        "duplicated_channels": duplicated_channels,
    }


def _format_value(value: Any, fmt: Optional[str] = None) -> str:
    if fmt is None:
        return str(value)
    try:
        return fmt.format(value)
    except Exception as e:
        raise SpecError(f"Failed to format value={value!r} with fmt={fmt!r}") from e


def _latex_newcommand(cmd: str, value: str) -> str:
    if not re.fullmatch(r"[A-Za-z]+", cmd):
        raise SpecError(f"latex_cmd must be letters only (no digits): {cmd}")

    if any(ch in value for ch in ("\n", "\r")):
        raise SpecError(f"latex_cmd value contains newline for {cmd}: {value!r}")
    if "}" in value:
        raise SpecError(f"latex_cmd value contains }} for {cmd}: {value!r}")

    # Use detokenize to safely render underscores and other special characters in text mode.
    return "\\newcommand{\\%s}{\\detokenize{%s}}" % (cmd, value)


def _render_table_hxx(
    *,
    table_name: str,
    rows: Sequence[Mapping[str, str]],
    protocol: str,
    row_order: Sequence[Mapping[str, Any]],
    frontends: Sequence[Mapping[str, str]],
    metrics: Sequence[Mapping[str, Any]],
) -> Tuple[str, Dict[str, Any]]:
    if not rows:
        raise SpecError(f"{table_name}: no CSV rows")

    required_cols = {"protocol", "subset_method", "subset_K", "frontend", "split_id"}
    for m in metrics:
        required_cols.add(m["key"])
    for col in required_cols:
        if col not in rows[0]:
            raise SpecError(f"{table_name}: missing required column: {col}")

    rows_p = [r for r in rows if r.get("protocol") == protocol]
    if not rows_p:
        raise SpecError(f"{table_name}: no rows after protocol filter: {protocol}")

    # Columns: K + (frontend,metric) pairs.
    header_cols: List[str] = ["K"]
    for m in metrics:
        for fe in frontends:
            header_cols.append(f"{fe['label']} {m['label']}")

    n_cols = len(header_cols)

    lines: List[str] = []
    col_spec = "l" + "".join("c" for _ in range(n_cols - 1))
    lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
    lines.append("\\toprule")
    lines.append(" & ".join(header_cols) + " \\\\")
    lines.append("\\midrule")

    provenance_rows: List[Dict[str, Any]] = []

    def format_pm(mean: float, std: float, fmt: str) -> str:
        m = fmt.format(mean)
        s = fmt.format(std)
        return f"${m}\\pm{s}$"

    for ro in row_order:
        if "section" in ro:
            section = str(ro["section"]).strip()
            lines.append("\\midrule")
            lines.append(f"\\multicolumn{{{n_cols}}}{{l}}{{\\textbf{{{section}}}}} \\\\")
            continue

        subset_method = ro.get("subset_method")
        subset_K = ro.get("subset_K")
        if subset_method is None or subset_K is None:
            raise SpecError(f"{table_name}: row_order entries must have section or (subset_method, subset_K): {ro}")

        subset_method = str(subset_method)
        subset_K_int = int(subset_K)
        subset_K_str = str(subset_K_int)

        row_cells: List[str] = [subset_K_str]

        for m in metrics:
            key = m["key"]
            fmt = m.get("fmt")
            plusminus = bool(m.get("plusminus", False))
            if not isinstance(fmt, str) or not fmt:
                raise SpecError(f"{table_name}: missing fmt for metric {key}")

            for fe in frontends:
                fe_name = fe["frontend"]

                matched = [
                    r
                    for r in rows_p
                    if r.get("subset_method") == subset_method
                    and str(r.get("subset_K")) == subset_K_str
                    and r.get("frontend") == fe_name
                ]

                if not matched:
                    raise SpecError(
                        f"{table_name}: no matched rows for subset_method={subset_method} subset_K={subset_K_str} frontend={fe_name}"
                    )

                vals = [_parse_float(r[key], context=f"{table_name}.{key}") for r in matched]
                mean, std = _mean_std(vals)

                cell = format_pm(mean, std, fmt) if plusminus else fmt.format(mean)
                row_cells.append(cell)

                provenance_rows.append(
                    {
                        "subset_method": subset_method,
                        "subset_K": subset_K_int,
                        "frontend": fe_name,
                        "metric": key,
                        "n": len(vals),
                        "mean": mean,
                        "std": std,
                    }
                )

        lines.append(" & ".join(row_cells) + " \\\\")

    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")

    prov = {
        "table": table_name,
        "protocol": protocol,
        "columns": header_cols,
        "rows": provenance_rows,
    }

    return "\n".join(lines) + "\n", prov


def _render_table_h12(
    *,
    table_name: str,
    rows: Sequence[Mapping[str, str]],
    protocol: str,
    model_family: str,
    subset_method: str,
    subset_K: int,
    drop_rates: Sequence[float],
    column_enable_aug: str,
    metric_mean: str,
    metric_std: str,
    fmt: str,
) -> Tuple[str, Dict[str, Any]]:
    if not rows:
        raise SpecError(f"{table_name}: no CSV rows")

    required = {
        "protocol",
        "model_family",
        "subset_method",
        "subset_K",
        "drop_rate",
        column_enable_aug,
        metric_mean,
        metric_std,
    }
    for col in required:
        if col not in rows[0]:
            raise SpecError(f"{table_name}: missing required column: {col}")

    rows_p = [
        r
        for r in rows
        if r.get("protocol") == protocol
        and r.get("model_family") == model_family
        and r.get("subset_method") == subset_method
        and str(r.get("subset_K")) == str(subset_K)
    ]
    if not rows_p:
        raise SpecError(f"{table_name}: no rows after filters")

    header_cols = ["Drop rate", "No spatial aug", "Spatial aug"]

    lines: List[str] = []
    lines.append("\\begin{tabular}{lcc}")
    lines.append("\\toprule")
    lines.append(" & ".join(header_cols) + " \\\\")
    lines.append("\\midrule")

    prov_rows: List[Dict[str, Any]] = []

    def format_pm(mean: float, std: float) -> str:
        m = fmt.format(mean)
        s = fmt.format(std)
        return f"${m}\\pm{s}$"

    for q in drop_rates:
        # Match by float rather than strict string.
        matched_q = []
        for r in rows_p:
            try:
                if abs(float(r.get("drop_rate", "nan")) - float(q)) < 1e-9:
                    matched_q.append(r)
            except Exception:
                continue
        if not matched_q:
            raise SpecError(f"{table_name}: missing drop_rate={q}")

        cells = [str(q)]
        for aug in (0, 1):
            matched = [r for r in matched_q if int(float(r.get(column_enable_aug, "nan"))) == aug]
            if len(matched) != 1:
                raise SpecError(
                    f"{table_name}: expected exactly 1 row for drop_rate={q} enable_aug={aug}, got {len(matched)}"
                )
            r0 = matched[0]
            mean = _parse_float(r0[metric_mean], context=f"{table_name}.{metric_mean}")
            std = _parse_float(r0[metric_std], context=f"{table_name}.{metric_std}")
            cells.append(format_pm(mean, std))
            prov_rows.append(
                {
                    "drop_rate": float(q),
                    "enable_spatial_aug": aug,
                    "mean": mean,
                    "std": std,
                }
            )

        lines.append(" & ".join(cells) + " \\\\")

    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")

    prov = {
        "table": table_name,
        "protocol": protocol,
        "model_family": model_family,
        "subset_method": subset_method,
        "subset_K": subset_K,
        "rows": prov_rows,
    }

    return "\n".join(lines) + "\n", prov


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--facts_spec", required=True)
    ap.add_argument("--paper_json", default="paper/paper.json")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    facts_spec_path = (root / args.facts_spec).resolve()
    paper_json_path = (root / args.paper_json).resolve()

    if not facts_spec_path.exists():
        raise SystemExit(f"facts_spec not found: {facts_spec_path}")
    if not paper_json_path.exists():
        raise SystemExit(f"paper.json not found: {paper_json_path}")

    spec = yaml.safe_load(facts_spec_path.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise SystemExit("facts_spec must be a YAML mapping")

    outputs = spec.get("outputs")
    if not isinstance(outputs, dict):
        raise SystemExit("facts_spec.outputs must be a mapping")

    out_facts_tex = (root / outputs.get("facts_tex", "paper/generated/facts.tex")).resolve()
    out_manifest = (root / outputs.get("manifest_json", "results/facts_manifest.json")).resolve()
    out_provenance_tex = (root / outputs.get("provenance_tex", "paper/generated/provenance.tex")).resolve()

    paper_json = _load_paper_json(paper_json_path)

    manifest: Dict[str, Any] = {
        "facts_spec": os.path.relpath(facts_spec_path, root),
        "paper_json": os.path.relpath(paper_json_path, root),
        "facts": [],
        "tables": [],
        "provenance_macros": [],
    }

    out_facts_tex.parent.mkdir(parents=True, exist_ok=True)
    out_manifest.parent.mkdir(parents=True, exist_ok=True)
    out_provenance_tex.parent.mkdir(parents=True, exist_ok=True)

    facts = spec.get("facts", [])
    if not isinstance(facts, list):
        raise SystemExit("facts_spec.facts must be a list")

    macro_lines: List[str] = []
    macro_lines.append("% Auto-generated by scripts/paper/generate_facts_tex.py")
    macro_lines.append(f"% facts_spec: {os.path.relpath(facts_spec_path, root)}")
    macro_lines.append(f"% paper_json: {os.path.relpath(paper_json_path, root)}")
    macro_lines.append("")

    smartpalate_cache: Dict[str, Dict[str, int]] = {}

    for fact in facts:
        if not isinstance(fact, dict):
            raise SpecError("Each fact must be a mapping")
        fact_id = fact.get("id")
        latex_cmd = fact.get("latex_cmd")
        extract = fact.get("extract")

        if not isinstance(fact_id, str) or not fact_id:
            raise SpecError(f"Invalid fact.id: {fact_id!r}")
        if not isinstance(latex_cmd, str) or not latex_cmd:
            raise SpecError(f"Invalid fact.latex_cmd for {fact_id}")
        if not isinstance(extract, dict):
            raise SpecError(f"Invalid fact.extract for {fact_id}")

        ex_type = extract.get("type")
        evidence_id = extract.get("evidence_id")
        fmt = extract.get("format")

        if not isinstance(ex_type, str) or not ex_type:
            raise SpecError(f"Invalid extract.type for fact {fact_id}")
        if not isinstance(evidence_id, str) or not evidence_id:
            raise SpecError(f"Invalid extract.evidence_id for fact {fact_id}")

        ev = _resolve_evidence(paper_json, root, evidence_id)

        value: Any
        provenance: Dict[str, Any] = {
            "fact_id": fact_id,
            "latex_cmd": latex_cmd,
            "extract": dict(extract),
            "evidence_id": ev.evidence_id,
            "evidence_path": os.path.relpath(ev.path, root),
            "evidence_sha256": ev.sha256,
        }

        if ex_type.startswith("smartpalate_"):
            if evidence_id not in smartpalate_cache:
                grid = _load_smartpalate_grid(ev.path)
                smartpalate_cache[evidence_id] = _smartpalate_stats(grid)
            stats = smartpalate_cache[evidence_id]

            mapping = {
                "smartpalate_grid_rows": "grid_rows",
                "smartpalate_grid_cols": "grid_cols",
                "smartpalate_total_channels": "total_channels",
                "smartpalate_mapped_channels": "mapped_channels",
                "smartpalate_unmapped_channels": "unmapped_channels",
                "smartpalate_duplicated_channels": "duplicated_channels",
            }
            if ex_type not in mapping:
                raise SpecError(f"Unknown smartpalate extract type: {ex_type}")
            value = stats[mapping[ex_type]]

        elif ex_type == "csv_unique_count":
            column = extract.get("column")
            regex = extract.get("regex")
            filters = extract.get("filters")

            if not isinstance(column, str) or not column:
                raise SpecError(f"csv_unique_count requires column for fact {fact_id}")
            if regex is not None and not isinstance(regex, str):
                raise SpecError(f"csv_unique_count regex must be string for fact {fact_id}")
            if filters is not None and not isinstance(filters, dict):
                raise SpecError(f"csv_unique_count filters must be mapping for fact {fact_id}")

            rows = _read_csv_dicts(ev.path)
            rows = _filter_rows(rows, filters)
            vals = _unique_values(rows, column)
            if regex:
                rx = re.compile(regex)
                vals = [v for v in vals if rx.search(v)]
            value = len(vals)
            provenance["unique_values"] = vals

        elif ex_type == "csv_unique_sorted_join":
            column = extract.get("column")
            regex = extract.get("regex")
            joiner = extract.get("join")
            filters = extract.get("filters")

            if not isinstance(column, str) or not column:
                raise SpecError(f"csv_unique_sorted_join requires column for fact {fact_id}")
            if regex is not None and not isinstance(regex, str):
                raise SpecError(f"csv_unique_sorted_join regex must be string for fact {fact_id}")
            if not isinstance(joiner, str):
                raise SpecError(f"csv_unique_sorted_join requires join string for fact {fact_id}")
            if filters is not None and not isinstance(filters, dict):
                raise SpecError(f"csv_unique_sorted_join filters must be mapping for fact {fact_id}")

            rows = _read_csv_dicts(ev.path)
            rows = _filter_rows(rows, filters)
            vals = _unique_values(rows, column)
            if regex:
                rx = re.compile(regex)
                vals = [v for v in vals if rx.search(v)]
            value = joiner.join(vals)
            provenance["unique_values"] = vals

        elif ex_type == "csv_unique_value":
            column = extract.get("column")
            filters = extract.get("filters")

            if not isinstance(column, str) or not column:
                raise SpecError(f"csv_unique_value requires column for fact {fact_id}")
            if filters is not None and not isinstance(filters, dict):
                raise SpecError(f"csv_unique_value filters must be mapping for fact {fact_id}")

            rows = _read_csv_dicts(ev.path)
            rows = _filter_rows(rows, filters)
            uniq = _unique_values(rows, column)
            if len(uniq) != 1:
                raise SpecError(f"csv_unique_value expected 1 unique value for {fact_id}, got {uniq}")

            raw_val = uniq[0]
            # Preserve integers without .0 when possible.
            try:
                fval = float(raw_val)
                ival = int(fval)
                value = ival if abs(fval - ival) < 1e-12 else fval
            except Exception:
                value = raw_val

        else:
            raise SpecError(f"Unknown extract.type for fact {fact_id}: {ex_type}")

        value_str = _format_value(value, fmt)
        macro_lines.append(_latex_newcommand(latex_cmd, value_str))
        manifest["facts"].append({**provenance, "value": value_str})

    out_facts_tex.write_text("\n".join(macro_lines) + "\n", encoding="utf-8")

    # Tables
    tables = spec.get("tables", [])
    if not isinstance(tables, list):
        raise SystemExit("facts_spec.tables must be a list")

    for t in tables:
        if not isinstance(t, dict):
            raise SpecError("Each table must be a mapping")
        name = t.get("name")
        out_tex = t.get("out_tex")
        source = t.get("source")

        if not isinstance(name, str) or not name:
            raise SpecError(f"Invalid table.name: {name!r}")
        if not isinstance(out_tex, str) or not out_tex:
            raise SpecError(f"Invalid table.out_tex for {name}")
        if not isinstance(source, dict) or not isinstance(source.get("evidence_id"), str):
            raise SpecError(f"Invalid table.source.evidence_id for {name}")

        protocol = str(t.get("protocol", ""))
        if not protocol:
            raise SpecError(f"Table {name} missing protocol")

        ev = _resolve_evidence(paper_json, root, source["evidence_id"])
        rows = _read_csv_dicts(ev.path)

        out_tex_path = (root / out_tex).resolve()
        out_tex_path.parent.mkdir(parents=True, exist_ok=True)

        table_manifest: Dict[str, Any] = {
            "table": name,
            "out_tex": os.path.relpath(out_tex_path, root),
            "source_evidence_id": ev.evidence_id,
            "source_path": os.path.relpath(ev.path, root),
            "source_sha256": ev.sha256,
        }

        if name.startswith("h12_"):
            rendered, prov = _render_table_h12(
                table_name=name,
                rows=rows,
                protocol=protocol,
                model_family=str(t.get("model_family")),
                subset_method=str(t.get("subset_method")),
                subset_K=int(t.get("subset_K")),
                drop_rates=[float(x) for x in t.get("drop_rates", [])],
                column_enable_aug=str(t.get("column_enable_aug")),
                metric_mean=str(t.get("metric_mean")),
                metric_std=str(t.get("metric_std")),
                fmt=str(t.get("fmt")),
            )
        else:
            rendered, prov = _render_table_hxx(
                table_name=name,
                rows=rows,
                protocol=protocol,
                row_order=t.get("row_order", []),
                frontends=t.get("frontends", []),
                metrics=t.get("metrics", []),
            )

        out_tex_path.write_text(rendered, encoding="utf-8")
        table_manifest["provenance"] = prov
        manifest["tables"].append(table_manifest)

    # Provenance macros (evidence IDs + sha256 prefixes)
    provenance_macros = spec.get("provenance_macros", [])
    if provenance_macros is None:
        provenance_macros = []
    if not isinstance(provenance_macros, list):
        raise SpecError("facts_spec.provenance_macros must be a list")

    prov_lines: List[str] = []
    prov_lines.append("% Auto-generated by scripts/paper/generate_facts_tex.py")
    prov_lines.append(f"% facts_spec: {os.path.relpath(facts_spec_path, root)}")
    prov_lines.append(f"% paper_json: {os.path.relpath(paper_json_path, root)}")
    prov_lines.append("")

    for ent in provenance_macros:
        if not isinstance(ent, dict):
            raise SpecError("Each provenance_macros entry must be a mapping")
        latex_cmd = ent.get("latex_cmd")
        sha_cmd = ent.get("sha_cmd")
        sha_prefix_len = ent.get("sha_prefix_len", 12)
        evidence_id = ent.get("evidence_id")

        if not isinstance(latex_cmd, str) or not latex_cmd:
            raise SpecError("provenance_macros.latex_cmd must be a non-empty string")
        if not isinstance(evidence_id, str) or not evidence_id:
            raise SpecError(f"provenance_macros entry missing evidence_id for {latex_cmd!r}")
        if sha_cmd is not None and (not isinstance(sha_cmd, str) or not sha_cmd):
            raise SpecError(f"provenance_macros.sha_cmd must be a non-empty string for {latex_cmd!r}")
        if not isinstance(sha_prefix_len, int) or sha_prefix_len <= 0:
            raise SpecError(f"provenance_macros.sha_prefix_len must be positive int for {latex_cmd!r}")

        ev = _resolve_evidence(paper_json, root, evidence_id)
        prov_lines.append(_latex_newcommand(latex_cmd, ev.evidence_id))
        manifest["provenance_macros"].append(
            {
                "latex_cmd": latex_cmd,
                "evidence_id": ev.evidence_id,
                "evidence_path": os.path.relpath(ev.path, root),
                "evidence_sha256": ev.sha256,
            }
        )
        if sha_cmd is not None:
            prov_lines.append(_latex_newcommand(sha_cmd, ev.sha256[:sha_prefix_len]))
            manifest["provenance_macros"].append(
                {
                    "latex_cmd": sha_cmd,
                    "evidence_id": ev.evidence_id,
                    "evidence_path": os.path.relpath(ev.path, root),
                    "evidence_sha256": ev.sha256,
                    "sha_prefix_len": sha_prefix_len,
                }
            )

    out_provenance_tex.write_text("\n".join(prov_lines) + "\n", encoding="utf-8")

    out_manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
