"""
cs.approval — 审批语义能力服务
覆盖：报价审批 / 合同审批 / 折扣授权 / 信用审批 / 多级路由
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class ApprovalTask:
    task_id: str
    type: str             # quote / contract / discount / credit
    subject: str
    requester_id: str
    approver_ids: List[str]
    current_level: int
    total_levels: int
    status: str           # pending / approved / rejected / escalated
    payload: Dict
    comments: List[Dict] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    sla_hours: int = 24


@dataclass
class ApprovalRule:
    """审批矩阵规则（热更新支持）"""
    type: str
    condition: str          # python 表达式
    required_level: int
    approver_role: str
    auto_approve_threshold: Optional[float] = None


class ApprovalService:
    """
    cs.approval — 多级审批语义服务
    审批矩阵热更新，规则变更无需重启
    """

    def __init__(self):
        self._tasks: Dict[str, ApprovalTask] = {}
        self._rules: List[ApprovalRule] = self._default_rules()

    def _default_rules(self) -> List[ApprovalRule]:
        return [
            ApprovalRule("quote", "amount < 50000", 1, "sales_manager", auto_approve_threshold=10000),
            ApprovalRule("quote", "amount >= 50000 and amount < 200000", 2, "regional_director"),
            ApprovalRule("quote", "amount >= 200000", 3, "vp_sales"),
            ApprovalRule("discount", "discount_pct <= 10", 1, "sales_manager", auto_approve_threshold=5),
            ApprovalRule("discount", "discount_pct > 10 and discount_pct <= 20", 2, "regional_director"),
            ApprovalRule("contract", "contract_value < 100000", 2, "legal_counsel"),
            ApprovalRule("contract", "contract_value >= 100000", 3, "cco"),
        ]

    # ------------------------------------------------------------------
    # 创建与路由
    # ------------------------------------------------------------------
    def create_approval_task(
        self,
        type_: str,
        subject: str,
        requester_id: str,
        payload: Dict,
    ) -> ApprovalTask:
        """根据审批矩阵路由审批级别"""
        rule = self._match_rule(type_, payload)
        task = ApprovalTask(
            task_id=str(uuid.uuid4()),
            type=type_,
            subject=subject,
            requester_id=requester_id,
            approver_ids=self._resolve_approvers(rule),
            current_level=1,
            total_levels=rule.required_level if rule else 1,
            status="pending",
            payload=payload,
            sla_hours=self._get_sla(type_),
        )

        # 自动审批逻辑
        if rule and rule.auto_approve_threshold:
            val = payload.get("amount") or payload.get("discount_pct", 0)
            if val and float(val) <= rule.auto_approve_threshold:
                task.status = "approved"
                task.comments.append({"author": "system", "text": "自动审批通过（低于阈值）"})

        self._tasks[task.task_id] = task
        return task

    def approve(self, task_id: str, approver_id: str, comment: str = "") -> ApprovalTask:
        """审批通过（支持多级流转）"""
        task = self._get_task(task_id)
        task.comments.append({"author": approver_id, "text": comment or "审批通过", "action": "approve"})

        if task.current_level >= task.total_levels:
            task.status = "approved"
        else:
            task.current_level += 1
            task.status = "pending"

        task.updated_at = datetime.now(timezone.utc).isoformat()
        return task

    def reject(self, task_id: str, approver_id: str, reason: str) -> ApprovalTask:
        """驳回审批"""
        task = self._get_task(task_id)
        task.status = "rejected"
        task.comments.append({"author": approver_id, "text": reason, "action": "reject"})
        task.updated_at = datetime.now(timezone.utc).isoformat()
        return task

    def escalate(self, task_id: str, reason: str) -> ApprovalTask:
        """升级审批（SLA 超时或特殊情况）"""
        task = self._get_task(task_id)
        task.status = "escalated"
        task.comments.append({"author": "system", "text": f"升级: {reason}", "action": "escalate"})
        task.updated_at = datetime.now(timezone.utc).isoformat()
        return task

    def get_pending_tasks(self, approver_id: str) -> List[ApprovalTask]:
        return [t for t in self._tasks.values() if t.status == "pending" and approver_id in t.approver_ids]

    def reload_rules(self, rules: List[Dict]):
        """热更新审批矩阵"""
        self._rules = [
            ApprovalRule(
                r["type"], r["condition"], r["required_level"],
                r["approver_role"], r.get("auto_approve_threshold"),
            )
            for r in rules
        ]

    # ------------------------------------------------------------------
    # 适配器调用入口
    # ------------------------------------------------------------------
    def __call__(self, action: str, payload: Dict, context=None) -> Any:
        handlers = {
            "create": lambda p: vars(self.create_approval_task(
                p["type"], p["subject"], p["requester_id"], p
            )),
            "approve": lambda p: vars(self.approve(p["task_id"], p["approver_id"], p.get("comment", ""))),
            "reject": lambda p: vars(self.reject(p["task_id"], p["approver_id"], p["reason"])),
            "escalate": lambda p: vars(self.escalate(p["task_id"], p["reason"])),
            "pending": lambda p: [vars(t) for t in self.get_pending_tasks(p["approver_id"])],
        }
        handler = handlers.get(action)
        if not handler:
            raise ValueError(f"cs.approval: 未知 action={action}")
        return handler(payload)

    def _match_rule(self, type_: str, payload: Dict) -> Optional[ApprovalRule]:
        for rule in self._rules:
            if rule.type != type_:
                continue
            try:
                if eval(rule.condition, {}, payload):
                    return rule
            except Exception:
                continue
        return None

    def _resolve_approvers(self, rule: Optional[ApprovalRule]) -> List[str]:
        if not rule:
            return ["default_approver"]
        role_map = {
            "sales_manager": ["sm_001"],
            "regional_director": ["rd_001", "rd_002"],
            "vp_sales": ["vp_001"],
            "legal_counsel": ["legal_001"],
            "cco": ["cco_001"],
        }
        return role_map.get(rule.approver_role, ["default_approver"])

    def _get_task(self, task_id: str) -> ApprovalTask:
        if task_id not in self._tasks:
            raise ValueError(f"审批任务不存在: {task_id}")
        return self._tasks[task_id]

    def _get_sla(self, type_: str) -> int:
        return {"quote": 4, "discount": 2, "contract": 24, "credit": 8}.get(type_, 24)
