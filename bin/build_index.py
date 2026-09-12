#!/usr/bin/env python3
"""Build a content-addressed index of workspace files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_EXCLUDES = {".git", ".DS_Store", "__pycache__", "node_modules", "_index"}
TEXT_SUFFIXES = {".md", ".json", ".py", ".qmd", ".csv", ".txt", ".yml", ".yaml", ".html", ".css"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def kind(path: Path) -> str:
    if path.name == "AGENTS.md":
        return "law"
    if path.name == "SKILL.md":
        return "skill"
    return path.suffix.lstrip(".") or "file"


def title(path: Path) -> str | None:
    if path.suffix not in TEXT_SUFFIXES:
        return None
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^#\s+(.+?)\s*$", line)
            if match:
                return match.group(1)
    except UnicodeDecodeError:
        return None
    return None


def build(root: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in DEFAULT_EXCLUDES for part in path.parts):
            continue
        relative = path.relative_to(root).as_posix()
        record: dict[str, object] = {
            "_id": f"file:{relative}",
            "type": "file-index",
            "path": relative,
            "kind": kind(path),
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        }
        record_title = title(path)
        if record_title:
            record["title"] = record_title
        records.append(record)
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output or root / "_index" / "files.json"
    records = build(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "count": len(records),
        "records": records,
    }
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"INDEX BUILT: {len(records)} records -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())