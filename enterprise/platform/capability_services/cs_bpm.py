"""
cs.bpm — BPM 流程能力服务（语义封装）
覆盖：流程发起 / 任务流转 / 状态查询 / SLA 监控
"""
from __future__ import annotations
from typing import Any, Dict
from .cs_crm import BPMConnector


class BPMService:
    """cs.bpm 语义流程服务"""

    def __init__(self, connector: BPMConnector = None):
        self._bpm = connector or BPMConnector()

    def start(self, process_key: str, variables: Dict) -> Dict:
        return self._bpm.start_process(process_key, variables)

    def complete_task(self, task_id: str, output: Dict = None) -> Dict:
        return self._bpm.complete_task(task_id, output)

    def get_status(self, instance_id: str) -> Dict:
        return self._bpm.get_process_status(instance_id)

    def __call__(self, action: str, payload: Dict, context=None) -> Any:
        handlers = {
            "start": lambda p: self.start(p["process_key"], p.get("variables", {})),
            "complete": lambda p: self.complete_task(p["task_id"], p.get("output")),
            "status": lambda p: self.get_status(p["instance_id"]),
        }
        handler = handlers.get(action)
        if not handler:
            raise ValueError(f"cs.bpm: 未知 action={action}")
        return handler(payload)
