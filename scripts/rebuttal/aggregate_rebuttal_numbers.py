#!/usr/bin/env python3
"""
Aggregate rebuttal eval JSONs into YAML/MD summaries.
"""

import argparse
import glob
import json
import pickle
import re
from pathlib import Path
from statistics import mean, pstdev
from typing import Dict, List, Any, Optional

import yaml


def load_model_args(model_path: Optional[str]) -> Dict[str, Any]:
    if not model_path:
        return {}
    args_path = Path(model_path) / "args"
    if not args_path.exists():
        return {}
    with open(args_path, "rb") as f:
        return pickle.load(f)


def best_by_cer(entries: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not entries:
        return None
    return sorted(entries, key=lambda x: x["cer"])[0]


def _parse_subject_seed(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Derive subject and seed from dataset/model paths when available."""

    def _find(pattern: str, text: Optional[str]) -> Optional[str]:
        if not text:
            return None
        m = re.search(pattern, text)
        return m.group(1) if m else None

    dataset_path = entry.get("dataset_path", "") or ""
    model_path = entry.get("model_path", "") or ""
    subject = _find(r"subj(\d+)_ds1", dataset_path) or _find(r"subj(\d+)_ds1", model_path)
    seed = entry.get("seed")
    if seed is None:
        seed = _find(r"protocolS_seed(\d+)", dataset_path) or _find(r"protocolS_seed(\d+)", model_path)
        if seed is not None:
            try:
                seed = int(seed)
            except ValueError:
                pass
    return {"subject": subject, "seed": seed}


def aggregate(inputs: List[str], out_yaml: Path, out_md: Path):
    records: List[Dict[str, Any]] = []
    for pattern in inputs:
        for path in glob.glob(pattern):
            with open(path, "r") as f:
                payload = json.load(f)
            payload["source_file"] = path
            # Enrich with model args if available
            margs = load_model_args(payload.get("model_path"))
            payload["specaug_on"] = bool(margs.get("aug_conf"))
            payload["param_count"] = payload.get("param_count", margs.get("param_count"))
            payload["seed"] = payload.get("seed", margs.get("seed"))
            payload["split_seed"] = payload.get("split_seed", margs.get("split_seed"))
            parsed = _parse_subject_seed(payload)
            payload["subject"] = payload.get("subject", parsed.get("subject"))
            payload["seed"] = payload.get("seed", parsed.get("seed"))
            records.append(payload)

    def is_protocol_s(rec: Dict[str, Any]) -> bool:
        return "protocolS_eval_" in rec.get("source_file", "")

    def is_rebuttal(rec: Dict[str, Any]) -> bool:
        return "rebuttal_eval_" in rec.get("source_file", "")

    # Buckets
    # IMPORTANT: keep legacy A/C/D/E/CV computed from rebuttal_eval_* only
    greedy = [r for r in records if is_rebuttal(r) and "lexicon_source" not in r]
    lexicon = [r for r in records if is_rebuttal(r) and "lexicon_source" in r]

    def bucket_by_partition(entries):
        d: Dict[str, List[Dict[str, Any]]] = {"test": [], "competition": []}
        for r in entries:
            part = r.get("partition")
            if part in d:
                d[part].append(r)
        return d

    greedy_by_part = bucket_by_partition(greedy)
    lexicon_by_part = bucket_by_partition(lexicon)

    # D/E selection anchored to seed0 and specaug flag
    def select(entries: List[Dict[str, Any]], *, specaug_on: bool):
        return [
            r
            for r in entries
            if r.get("specaug_on") == specaug_on
            and r.get("seed") == 0  # seed0 only for A/D/E
        ]

    de = {"D": {}, "E": {}}
    for part, arr in greedy_by_part.items():
        de["D"][part] = best_by_cer(select(arr, specaug_on=True))
        de["E"][part] = best_by_cer(select(arr, specaug_on=False))

    # CV: use specaug_off greedy only (A condition) across split seeds
    cv = {}
    for part in ["test", "competition"]:
        vals = [r["cer"] for r in greedy_by_part[part] if r.get("specaug_on") is False]
        cv[part] = {
            "mean": mean(vals) if vals else None,
            "std": pstdev(vals) if len(vals) > 1 else 0.0 if len(vals) == 1 else None,
            "n": len(vals),
        }

    # Lexicon variants
    def select_lex(entries: List[Dict[str, Any]], source: str):
        return [r for r in entries if r.get("lexicon_source") == source]

    result = {
        # A uses SpecAug OFF, seed0 greedy
        "A": {part: de["E"][part] for part in ["test", "competition"]},
        "C_train": {
            part: best_by_cer(select_lex(lexicon_by_part[part], "train"))
            for part in ["test", "competition"]
        },
        "C_all": {
            part: best_by_cer(select_lex(lexicon_by_part[part], "all"))
            for part in ["test", "competition"]
        },
        "D": de["D"],
        # E is defined equal to A (SpecAug OFF seed0) for naming consistency
        "E": {part: de["E"][part] for part in ["test", "competition"]},
        "CV": cv,
        "sources": inputs,
    }

    # Protocol-S aggregation (seen-word / instance holdout across subjects)
    proto_records = [r for r in records if is_protocol_s(r)]

    def summarize_proto(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not rows:
            return {"mean": None, "std": None, "n": 0, "items": []}
        cer_vals = [r["cer"] for r in rows]
        return {
            "mean": mean(cer_vals) if cer_vals else None,
            "std": pstdev(cer_vals) if len(cer_vals) > 1 else 0.0 if len(cer_vals) == 1 else None,
            "n": len(cer_vals),
            "items": [
                {
                    "subject": r.get("subject"),
                    "seed": r.get("seed"),
                    "cer": r.get("cer"),
                    "wer": r.get("wer"),
                    "model_path": r.get("model_path"),
                    "dataset_path": r.get("dataset_path"),
                    "source_file": r.get("source_file"),
                }
                for r in sorted(
                    rows, key=lambda x: (str(x.get("subject") or ""), x.get("seed"))
                )
            ],
        }

    proto_greedy_test = [
        r for r in proto_records if r.get("partition") == "test" and "lexicon_source" not in r
    ]
    proto_lex_train_test = [
        r
        for r in proto_records
        if r.get("partition") == "test" and r.get("lexicon_source") == "train"
    ]

    if proto_records:
        result["ProtocolS"] = {
            "greedy_test": summarize_proto(proto_greedy_test),
            "lex_train_test": summarize_proto(proto_lex_train_test),
        }

    out_yaml.parent.mkdir(parents=True, exist_ok=True)
    with open(out_yaml, "w") as f:
        yaml.safe_dump(result, f, sort_keys=False, default_flow_style=False)
    print(f"Wrote {out_yaml}")

    # Markdown summary (test partition primary)
    def fmt(entry):
        if not entry:
            return "NA"
        return f"{entry['cer']:.4f}"

    lines = [
        f"A (SpecAug OFF, greedy, seed0, test): {fmt(result['A']['test'])}",
        f"C_train (lexicon=train, test): {fmt(result['C_train']['test'])}",
        f"C_all (lexicon=all/oracle, test): {fmt(result['C_all']['test'])}",
        f"D (SpecAug ON, greedy, seed0, test): {fmt(result['D']['test'])}",
        f"E (alias of A, SpecAug OFF, test): {fmt(result['E']['test'])}",
        f"CV (SpecAug OFF, test) mean±std over n={cv['test']['n']}: "
        f"{cv['test']['mean'] if cv['test']['mean'] is not None else 'NA'} ± "
        f"{cv['test']['std'] if cv['test']['std'] is not None else 'NA'}",
    ]
    # Protocol-S summary (test partition) if available
    if "ProtocolS" in result:
        ps = result["ProtocolS"]
        ps_g = ps["greedy_test"]
        ps_l = ps["lex_train_test"]

        def fmt_mean_std(block):
            if not block or block["n"] == 0 or block["mean"] is None:
                return "NA"
            return f"{block['mean']:.4f} ± {block['std']:.4f} (n={block['n']})"

        lines.append(f"Protocol-S greedy test CER mean±std: {fmt_mean_std(ps_g)}")
        lines.append(f"Protocol-S train-lex test CER mean±std: {fmt_mean_std(ps_l)}")
        lines.append("Protocol-S per-run (subj, seed, greedy_CER, lex_train_CER):")
        greedy_lookup = {(r.get('subject'), r.get('seed')): r for r in ps_g.get('items', [])}
        lex_lookup = {(r.get('subject'), r.get('seed')): r for r in ps_l.get('items', [])}
        keys = sorted(set(list(greedy_lookup.keys()) + list(lex_lookup.keys())))
        for key in keys:
            g = greedy_lookup.get(key)
            l = lex_lookup.get(key)
            lines.append(
                f"  subj{key[0]} seed{key[1]}: "
                f"greedy_CER={g['cer'] if g else 'NA'}, "
                f"lex_train_CER={l['cer'] if l else 'NA'}"
            )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    with open(out_md, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {out_md}")


def main():
    parser = argparse.ArgumentParser(description="Aggregate rebuttal eval JSONs.")
    parser.add_argument("--inputs", nargs="+", required=True, help="JSON files or glob patterns.")
    parser.add_argument("--out_yaml", type=Path, required=True)
    parser.add_argument("--out_md", type=Path, required=True)
    args = parser.parse_args()

    aggregate(args.inputs, args.out_yaml, args.out_md)


if __name__ == "__main__":
    main()

