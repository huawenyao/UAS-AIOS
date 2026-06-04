#!/usr/bin/env bash
# EDH harness invariants (reqharness 变更验证)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
python harness/invariants/run-all.py
