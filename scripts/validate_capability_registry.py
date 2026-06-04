#!/usr/bin/env python3
"""校验 configs/capability_registry.json 并列出 cs.* 能力服务。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "configs" / "capability_registry.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "capability_service.schema.json"

SERVICE_ID_RE = re.compile(r"^cs\.[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)?$")
OP_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_minimal(registry: dict) -> list[str]:
    errors: list[str] = []
    if registry.get("version") != "1.0.0":
        errors.append("version must be 1.0.0 for Phase-0 baseline")
    services = registry.get("services", [])
    if len(services) < 5:
        errors.append(f"need >= 5 services, got {len(services)}")
    seen_ids: set[str] = set()
    for svc in services:
        sid = svc.get("id", "")
        if not SERVICE_ID_RE.match(sid):
            errors.append(f"invalid service id: {sid}")
        if sid in seen_ids:
            errors.append(f"duplicate service id: {sid}")
        seen_ids.add(sid)
        ops = svc.get("operations", [])
        if not ops:
            errors.append(f"{sid}: no operations")
        op_names: set[str] = set()
        for op in ops:
            name = op.get("name", "")
            if not OP_NAME_RE.match(name):
                errors.append(f"{sid}.{name}: invalid operation name")
            if name in op_names:
                errors.append(f"{sid}: duplicate operation {name}")
            op_names.add(name)
            if not op.get("gates"):
                errors.append(f"{sid}.{name}: gates required")
            if op.get("approval_level") not in ("L1", "L2", "L3"):
                errors.append(f"{sid}.{name}: invalid approval_level")
    return errors


def validate_jsonschema(registry: dict) -> list[str]:
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema not installed; skipped schema validation"]
    schema = load_json(SCHEMA_PATH)
    validator = jsonschema.Draft7Validator(schema)
    errs = sorted(validator.iter_errors(registry), key=lambda e: e.path)
    return [f"schema: {e.message} @ {list(e.path)}" for e in errs]


def cmd_list(registry: dict) -> int:
    for svc in registry.get("services", []):
        ops = svc.get("operations", [])
        visible = [o["name"] for o in ops if o.get("agent_visible", True)]
        print(f"{svc['id']} ({svc['source_system']}) — {len(ops)} ops, agent_visible={visible}")
    print(f"\nTotal: {len(registry.get('services', []))} services")
    return 0


def cmd_validate(registry: dict, use_schema: bool) -> int:
    errors = validate_minimal(registry)
    if use_schema:
        errors.extend(validate_jsonschema(registry))
    schema_only = [e for e in errors if e.startswith("jsonschema not installed")]
    blocking = [e for e in errors if not e.startswith("jsonschema not installed")]
    if schema_only:
        print(schema_only[0])
    if blocking:
        for e in blocking:
            print(f"ERROR: {e}")
        return 1
    print("OK: capability_registry.json valid")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="UAS capability service registry")
    parser.add_argument("command", choices=["list", "validate"])
    parser.add_argument("--no-schema", action="store_true", help="skip jsonschema if available")
    args = parser.parse_args()
    if not REGISTRY_PATH.is_file():
        print(f"ERROR: missing {REGISTRY_PATH}")
        return 1
    registry = load_json(REGISTRY_PATH)
    if args.command == "list":
        return cmd_list(registry)
    return cmd_validate(registry, use_schema=not args.no_schema)


if __name__ == "__main__":
    raise SystemExit(main())
