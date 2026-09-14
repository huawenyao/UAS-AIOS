"""UAS-AIOS Hub 阶段 A：信封、门禁、责任图切片、签发。无 SoR 密钥、不启 Temporal。"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


WM_DIMS = ("space", "time", "subject", "object", "feedback")

ERROR_HTTP = {
    "WM_INCOMPLETE": 422,
    "PROFILE_FORBIDS_SIDE_EFFECT": 403,
    "INVARIANT_FAILED": 422,
    "GATE_BLOCKED": 403,
    "TRACK_ESCALATION_REQUIRED": 403,
    "SKILL_NOT_EXECUTABLE_IN_PROFILE": 403,
    "SCOPE_DENIED": 403,
    "MEMORY_TRACK_FORBIDDEN": 403,
    "THREAD_PROFILE_IMMUTABLE": 409,
    "TASK_SOURCE_REQUIRED": 422,
    "CALIBER_MISSING": 422,
    "UNGROUNDED_INSIGHT": 422,
    "TENANT_MISMATCH": 403,
    "OPERATION_NOT_FOUND": 404,
    "TASK_NOT_ISSUED": 422,
}

EXPLAIN = {
    "PROFILE_FORBIDS_SIDE_EFFECT": {
        "message": "现在是作战台，不能改 CRM。请签发任务后进入运行。",
        "next": "hub.scene.task.issue",
    },
    "TASK_SOURCE_REQUIRED": {
        "message": "经营任务必须带责任图源节点。",
        "next": "从今日必办选择节点再签发",
    },
    "UNGROUNDED_INSIGHT": {
        "message": "建议还没有证据，不能派活。",
        "next": "补时间线或口径证据后再 drill",
    },
    "WM_INCOMPLETE": {
        "message": "这个位置还没建模完整（缺五维），不能签发。",
        "next": "请知识管理员补世界模型投影",
    },
    "TENANT_MISMATCH": {
        "message": "当前账号不属于这张经营图的租户。",
        "next": "联系平台管理员开通岗位",
    },
    "MEMORY_TRACK_FORBIDDEN": {
        "message": "经营轨道不能读个人记忆。",
        "next": "使用岗位上下文而不是个人备忘",
    },
    "TRACK_ESCALATION_REQUIRED": {
        "message": "个人轨道不能直接写经营系统，需要带证据升级。",
        "next": "提交升级工单",
    },
    "THREAD_PROFILE_IMMUTABLE": {
        "message": "同一会话不能改剖面，请新开执行。",
        "next": "新开 Thread",
    },
    "CALIBER_MISSING": {
        "message": "这个指标还没有口径，数字不能当经营事实。",
        "next": "配置 caliber 后再打开作战台",
    },
    "OPERATION_NOT_FOUND": {
        "message": "能力目录里没有这个动作，或本租户未启用。",
        "next": "在能力网格启用 operation",
    },
    "GATE_BLOCKED": {
        "message": "治理门禁拒绝了这次调用。",
        "next": "查看审计与门禁说明",
    },
    "SCOPE_DENIED": {
        "message": "当前范围看不到这些客户或数据。",
        "next": "申请更大 scope 或换岗位",
    },
    "INVARIANT_FAILED": {
        "message": "发布前检查没过，不能进入运行。",
        "next": "修复 invariant 后再 release",
    },
    "SKILL_NOT_EXECUTABLE_IN_PROFILE": {
        "message": "现在只能引用技能，不能执行。",
        "next": "安装并在运行态启用后再用",
    },
    "TASK_NOT_ISSUED": {
        "message": "还没有签发的经营任务，不能进入运行。",
        "next": "hub.scene.task.issue",
    },
}


class HubError(Exception):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.http = ERROR_HTTP.get(code, 400)
        self.detail = detail
        super().__init__(code)

    def as_body(self) -> dict[str, Any]:
        exp = EXPLAIN.get(self.code, {"message": self.code, "next": ""})
        return {
            "error": {
                "code": self.code,
                "message": exp["message"],
                "explain_ref": "hub.policy.explain",
                "next": exp["next"],
                "retryable": False,
                "detail": self.detail,
            }
        }


@dataclass
class Envelope:
    tenant_id: str
    actor_id: str
    profile: str
    track: str
    correlation_id: str = "corr-test"
    idempotency_key: str = ""
    source_node_id: str | None = None
    position_id: str | None = None
    thread_id: str | None = None


@dataclass
class PolicyTrace:
    steps: list[str] = field(default_factory=list)

    def add(self, name: str) -> None:
        self.steps.append(name)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
