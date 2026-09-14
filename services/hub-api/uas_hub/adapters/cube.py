"""M15 Cube 夹具。失败标 stale，不签发，返回不见 CubeQL。优先读 OSI YAML。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from uas_hub.errors import utc_now

_DEFAULTS: dict[str, dict[str, Any]] = {
    "kpi-visit-dwell": {"value": 28, "caliber_id": "now - stage_entered_at"},
    "kpi-spend": {"value": 4290000, "caliber_id": "Σspend(bus_mtc,近30天)"},
}


def _load_osi(osi_dir: Path | None) -> dict[str, str]:
    formulas: dict[str, str] = {}
    if osi_dir is None or not osi_dir.is_dir():
        return formulas
    for path in osi_dir.glob("*.yml"):
        kpi_id = ""
        formula = ""
        for line in path.read_text(encoding="utf-8").splitlines():
            raw = line.strip()
            if raw.startswith("id:"):
                kpi_id = raw.split(":", 1)[1].strip()
            elif raw.startswith("formula:"):
                formula = raw.split(":", 1)[1].strip()
        if kpi_id and formula:
            formulas[kpi_id] = formula
    return formulas


class FixtureCube:
    """实验室口径。available=False 仍给缓存值并 stale=True。runtime 写后拜访停留下降。"""

    def __init__(self, osi_dir: Path | None = None) -> None:
        self._writes = 0
        self._osi = _load_osi(osi_dir)

    def note_runtime_write(self) -> None:
        self._writes += 1

    def query(
        self,
        kpi_id: str,
        *,
        grain: str = "",
        start: str = "",
        end: str = "",
        dimensions: dict[str, Any] | None = None,
        available: bool = True,
    ) -> dict[str, Any]:
        _ = (grain, start, end, dimensions)
        sample = _DEFAULTS.get(kpi_id)
        caliber = self._osi.get(kpi_id) or (sample or {}).get("caliber_id") or ""
        if sample is None:
            return {"value": None, "caliber_id": caliber, "as_of": utc_now(), "stale": True}
        value = sample["value"]
        if kpi_id == "kpi-visit-dwell" and self._writes:
            value = 10
        return {
            "value": value,
            "caliber_id": caliber or sample["caliber_id"],
            "as_of": utc_now(),
            "stale": not available,
        }
