#!/usr/bin/env python3
"""校验 cs.form 契约与表单模板（REQ-EDH-PL-005）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_OPS = {"cs.form.render", "cs.form.submit", "cs.form.validate"}


def validate_case_form_001(workspace: Path) -> list[str]:
    template_path = workspace / "configs" / "form_templates" / "expense_reimbursement.sample.json"
    if not template_path.is_file():
        return ["missing expense_reimbursement template"]
    tpl = json.loads(template_path.read_text(encoding="utf-8"))
    fields = {f["id"]: f for f in tpl.get("fields", [])}
    sample = {"amount": 3200, "category": "travel", "receipt_ids": ["r1"]}
    for fid, spec in fields.items():
        if spec.get("required") and fid not in sample:
            return [f"CASE-FORM-001 missing field {fid}"]
    if sample["amount"] <= 5000 and not tpl.get("linked_process_template"):
        return ["CASE-FORM-001: missing linked_process_template"]
    return []


def validate(workspace: Path) -> list[str]:
    errors: list[str] = []
    if not (workspace / "schemas" / "cs_form_operation.schema.json").is_file():
        errors.append("missing cs_form_operation.schema.json")
    if not (workspace / "harness" / "knowledge" / "technical" / "cs-form-semantic-api.md").is_file():
        errors.append("missing cs-form-semantic-api.md")
    errors.extend(validate_case_form_001(workspace))
    return errors


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] != "validate":
        print("Usage: validate_cs_form.py validate", file=sys.stderr)
        return 2
    workspace = Path(__file__).resolve().parents[1]
    errors = validate(workspace)
    if errors:
        print(json.dumps({"status": "fail", "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "ok", "case": "CASE-FORM-001"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
