#!/usr/bin/env python3
"""Validate the committed presence and status records."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRESENCE_DIR = ROOT / "docs" / "presence"
STATUS_PATH = ROOT / "docs" / "status.json"
REQUIRED_PRESENCE_FIELDS = {
    "machine",
    "hwid",
    "state",
    "beat_iso",
    "head",
    "free_bytes_gib",
    "ram_bytes",
    "running_pids",
}
VALID_STATES = {"working", "quiet", "silent"}


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read {path.relative_to(ROOT)}: {error}") from error


def validate() -> list[str]:
    errors: list[str] = []
    presence_paths = sorted(PRESENCE_DIR.glob("*.json"))
    if not presence_paths:
        errors.append("docs/presence contains no machine records")

    machines: set[str] = set()
    for path in presence_paths:
        record = load_json(path)
        if not isinstance(record, dict):
            errors.append(f"{path.relative_to(ROOT)} is not a JSON object")
            continue
        missing = REQUIRED_PRESENCE_FIELDS - record.keys()
        if missing:
            errors.append(
                f"{path.relative_to(ROOT)} missing fields: {', '.join(sorted(missing))}"
            )
        machine = record.get("machine")
        if not isinstance(machine, str) or not machine:
            errors.append(f"{path.relative_to(ROOT)} has no machine id")
        elif machine in machines:
            errors.append(f"duplicate machine id: {machine}")
        else:
            machines.add(machine)
        if record.get("state") not in VALID_STATES:
            errors.append(f"{path.relative_to(ROOT)} has invalid state")
        if not isinstance(record.get("running_pids"), list):
            errors.append(f"{path.relative_to(ROOT)} running_pids must be a list")

    status = load_json(STATUS_PATH)
    if not isinstance(status, dict):
        errors.append("docs/status.json is not a JSON object")
    else:
        status_machines = {
            row.get("machine")
            for row in status.get("machines", [])
            if isinstance(row, dict)
        }
        if status_machines != machines:
            errors.append("docs/status.json machine list does not match presence records")

    return errors


def main() -> int:
    try:
        errors = validate()
    except ValueError as error:
        print(f"AUDIT FAILED: {error}")
        return 1
    if errors:
        print("AUDIT FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"AUDIT PASSED: {len(list(PRESENCE_DIR.glob('*.json')))} machine records verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())