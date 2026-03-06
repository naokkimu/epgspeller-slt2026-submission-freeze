#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _dump_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=False) + "\n")


def _require_id(item: Any) -> str:
    if not isinstance(item, dict):
        raise ValueError("item must be a JSON object")
    v = item.get("id")
    if not isinstance(v, str) or not v.strip():
        raise ValueError("item.id must be a non-empty string")
    return v.strip()


def _upsert_list(lst: List[Any], item: Dict[str, Any]) -> None:
    item_id = _require_id(item)
    for i, it in enumerate(lst):
        if isinstance(it, dict) and it.get("id") == item_id:
            lst[i] = item
            return
    lst.append(item)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--paper-json", default="paper/paper.json")
    p.add_argument(
        "--kind",
        required=True,
        choices=["claims", "evidence", "runs", "experiments"],
        help="which list to upsert into",
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--item-json", help="single JSON object as a string")
    src.add_argument("--item-file", help="path to a JSON object file")
    src.add_argument("--items-file", help="path to a JSON array file")
    p.add_argument("--sort", action="store_true", help="sort the target list by id after upsert")
    args = p.parse_args(argv)

    pj_path = Path(args.paper_json)
    doc = _load_json(pj_path)
    if not isinstance(doc, dict):
        raise ValueError("paper.json must be a JSON object")

    target = doc.get(args.kind)
    if not isinstance(target, list):
        raise ValueError(f"paper.json.{args.kind} must be a list")

    items: List[Dict[str, Any]] = []
    if args.item_json is not None:
        obj = json.loads(args.item_json)
        if not isinstance(obj, dict):
            raise ValueError("--item-json must be an object")
        items = [obj]
    elif args.item_file is not None:
        obj = _load_json(Path(args.item_file))
        if not isinstance(obj, dict):
            raise ValueError("--item-file must contain an object")
        items = [obj]
    elif args.items_file is not None:
        arr = _load_json(Path(args.items_file))
        if not isinstance(arr, list):
            raise ValueError("--items-file must contain an array")
        for it in arr:
            if not isinstance(it, dict):
                raise ValueError("--items-file array elements must be objects")
        items = arr

    for it in items:
        _upsert_list(target, it)

    if args.sort:
        target.sort(key=lambda x: (x.get("id") if isinstance(x, dict) else ""))

    doc[args.kind] = target
    _dump_json(pj_path, doc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
