#!/usr/bin/env python3
"""
Aggregate rebuttal eval JSONs into YAML/MD summaries.
"""

import argparse
import glob
import json
import pickle
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
            records.append(payload)

    # Buckets
    greedy = [r for r in records if "lexicon_source" not in r]
    lexicon = [r for r in records if "lexicon_source" in r]

    def bucket_by_partition(entries):
        d: Dict[str, List[Dict[str, Any]]] = {"test": [], "competition": []}
        for r in entries:
            part = r.get("partition")
            if part in d:
                d[part].append(r)
        return d

    greedy_by_part = bucket_by_partition(greedy)
    lexicon_by_part = bucket_by_partition(lexicon)

    # D/E selection
    def select_specaug(entries: List[Dict[str, Any]], flag: bool):
        return [r for r in entries if r.get("specaug_on") == flag]

    de = {"D": {}, "E": {}}
    for part, arr in greedy_by_part.items():
        de["D"][part] = best_by_cer(select_specaug(arr, True))
        de["E"][part] = best_by_cer(select_specaug(arr, False))

    # CV: use specaug_off greedy only (A condition) across split seeds
    cv = {}
    for part in ["test", "competition"]:
        vals = [r["cer"] for r in greedy_by_part[part] if r.get("specaug_on") is False]
        cv[part] = {
            "mean": mean(vals) if vals else None,
            "std": pstdev(vals) if len(vals) > 1 else 0.0 if len(vals) == 1 else None,
            "n": len(vals),
        }

    result = {
        "A": {part: best_by_cer(greedy_by_part[part]) for part in ["test", "competition"]},
        "C": {part: best_by_cer(lexicon_by_part[part]) for part in ["test", "competition"]},
        "D": de["D"],
        "E": de["E"],
        "CV": cv,
        "sources": inputs,
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
        f"A (greedy, test): {fmt(result['A']['test'])}",
        f"C (lexicon, test): {fmt(result['C']['test'])}",
        f"D (SpecAug ON, test): {fmt(result['D']['test'])}",
        f"E (SpecAug OFF, test): {fmt(result['E']['test'])}",
        f"CV (SpecAug OFF, test) mean±std over n={cv['test']['n']}: "
        f"{cv['test']['mean'] if cv['test']['mean'] is not None else 'NA'} ± "
        f"{cv['test']['std'] if cv['test']['std'] is not None else 'NA'}",
    ]
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

