"""M22 Utopia Spike 夹具。只读导出，禁止写路径。"""

from __future__ import annotations

from typing import Any


class FixtureReview:
    def export_candidates(self, query: str, write: bool = False, **kwargs: Any) -> dict[str, Any]:
        _ = query, write, kwargs
        return {"candidates": [], "write_path": False}
