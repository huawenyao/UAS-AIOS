"""实验室 Worker 入口。无 Temporal 集群时不要当第三套循环。"""

from __future__ import annotations

import os


def main() -> int:
    address = os.environ.get("TEMPORAL_ADDRESS", "")
    if not address:
        print("TEMPORAL_ADDRESS unset; use InMemoryOuterLoop. Compose: deploy/compose/docker-compose.yml")
        return 0
    try:
        import temporalio  # noqa: F401
    except ImportError:
        print("install temporalio to run the worker against", address)
        return 1
    print("temporal worker would poll", address, "queue uas-runtime; activities call Hub")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
