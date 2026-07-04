#!/usr/bin/env python3
"""校验 cs.process 契约与流程模板（REQ-EDH-PL-004）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_OPS = {"cs.process.start", "cs.process.advance", "cs.process.escalate"}
TEMPLATE_IDS = {"sales_quote_approval", "cs_customer_service"}


def validate(workspace: Path) -> list[str]:
    errors: list[str] = []
    schema = workspace / "schemas" / "cs_process_operation.schema.json"
    if not schema.is_file():
        errors.append("missing cs_process_operation.schema.json")

    doc = workspace / "harness" / "knowledge" / "technical" / "cs-process-semantic-api.md"
    if not doc.is_file():
        errors.append("missing cs-process-semantic-api.md")

    for tid in TEMPLATE_IDS:
        path = workspace / "configs" / "process_templates" / f"{tid}.json"
        if not path.is_file():
            errors.append(f"missing template {tid}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        esc = data.get("escalation", {})
        if esc.get("operation") != "cs.process.escalate":
            errors.append(f"{tid}: escalation.operation must be cs.process.escalate")

    registry = workspace / "projects" / "enterprise-sales-os" / "configs" / "system_registry.json"
    if registry.is_file():
        caps = set(json.loads(registry.read_text(encoding="utf-8")).get("capabilities", []))
        if not REQUIRED_OPS.issubset(caps):
            errors.append(f"enterprise-sales-os missing process caps: {REQUIRED_OPS - caps}")

    return errors


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] != "validate":
        print("Usage: validate_cs_process.py validate", file=sys.stderr)
        return 2
    workspace = Path(__file__).resolve().parents[1]
    errors = validate(workspace)
    if errors:
        print(json.dumps({"status": "fail", "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "ok", "operations": sorted(REQUIRED_OPS)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
