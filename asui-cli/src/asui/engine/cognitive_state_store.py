"""认知状态空间存储。"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "cognitive-state"


class CognitiveStateStore:
    """显式维护一次运行的认知状态空间。"""

    def __init__(self, app_root: Path, topic: str) -> None:
        self.app_root = app_root
        self.topic = topic
        self.slug = slugify(topic)
        self.state_path = app_root / "database" / "cognitive_state" / f"{self.slug}.json"
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state = {
            "topic": topic,
            "intent": {},
            "knowledge": {},
            "routes": [],
            "step_outputs": {},
            "tensions": [],
            "evaluation": {},
            "evolution": {},
            "timeline": [],
        }

    def update_intent(self, data: dict) -> None:
        self.state["intent"] = data
        self._append_timeline("intent_updated", data)

    def update_knowledge(self, data: dict) -> None:
        self.state["knowledge"] = data
        self._append_timeline("knowledge_updated", data)

    def record_route(self, route: dict) -> None:
        self.state["routes"].append(route)
        self._append_timeline("route_recorded", route)

    def record_step_output(self, step_id: str, output: dict) -> None:
        self.state["step_outputs"][step_id] = output
        self._append_timeline("step_output_recorded", {"step_id": step_id, "output_keys": sorted(output.keys())})

    def update_evaluation(self, data: dict) -> None:
        self.state["evaluation"] = data
        self._append_timeline("evaluation_updated", {"status": data.get("status")})

    def update_evolution(self, data: dict) -> None:
        self.state["evolution"] = data
        self._append_timeline("evolution_updated", data)

    def add_tension(self, tension: str) -> None:
        self.state["tensions"].append(tension)
        self._append_timeline("tension_added", {"tension": tension})

    def snapshot(self) -> dict:
        self.state_path.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")
        return self.state

    def _append_timeline(self, event: str, payload: dict) -> None:
        self.state["timeline"].append(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "event": event,
                "payload": payload,
            }
        )
