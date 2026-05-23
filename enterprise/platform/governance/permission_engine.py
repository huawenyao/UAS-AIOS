"""
权限引擎（RBAC + ABAC 混合）
职责：统一校验 Agent 调用权限，屏蔽底层资源授权
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class PermissionResult:
    allowed: bool
    reason: str
    matched_rule: Optional[str] = None


@dataclass
class PermissionRule:
    role: str
    service: str
    actions: List[str]   # ["*"] 表示所有
    conditions: Optional[Dict] = None


class PermissionEngine:
    """
    RBAC + ABAC 权限引擎
    Agent 只需提供 caller_id / tenant_id / service / action
    不需要了解底层权限模型
    """

    def __init__(self):
        self._role_assignments: Dict[str, List[str]] = {}   # caller_id -> [roles]
        self._rules: List[PermissionRule] = self._default_rules()
        self._tenant_configs: Dict[str, Dict] = {}

    def _default_rules(self) -> List[PermissionRule]:
        return [
            # L1 SelfPaw 权限
            PermissionRule("l1_user", "cs.customer", ["qualify_lead", "get_profile"]),
            PermissionRule("l1_user", "cs.approval", ["create", "pending"]),
            PermissionRule("l1_user", "cs.finance", ["create_quote"]),

            # L2 职能权限
            PermissionRule("l2_user", "cs.customer", ["*"]),
            PermissionRule("l2_user", "cs.approval", ["*"]),
            PermissionRule("l2_user", "cs.invoice", ["create", "submit", "ar_summary"]),
            PermissionRule("l2_user", "cs.finance", ["*"]),

            # 销售 AE 权限
            PermissionRule("sales_ae", "cs.customer", ["qualify_lead", "get_profile", "update_stage"]),
            PermissionRule("sales_ae", "cs.finance", ["create_quote"]),
            PermissionRule("sales_ae", "cs.approval", ["create", "pending"]),

            # CSM 权限
            PermissionRule("csm", "cs.customer", ["get_profile", "health_score", "update_stage"]),
            PermissionRule("csm", "cs.invoice", ["ar_summary", "check_overdue"]),

            # 审批人权限
            PermissionRule("approver", "cs.approval", ["approve", "reject", "escalate", "pending"]),
            PermissionRule("sales_manager", "cs.approval", ["*"]),
            PermissionRule("sales_manager", "cs.customer", ["*"]),

            # HR 权限
            PermissionRule("hr", "cs.bpm", ["start", "complete", "status"]),

            # 财务权限
            PermissionRule("finance", "cs.invoice", ["*"]),
            PermissionRule("finance", "cs.finance", ["*"]),

            # L3 经营 Agent 权限
            PermissionRule("l3_agent", "cs.customer", ["*"]),
            PermissionRule("l3_agent", "cs.approval", ["create", "pending"]),
            PermissionRule("l3_agent", "cs.finance", ["create_quote"]),
            PermissionRule("l3_agent", "cs.bpm", ["start", "status"]),

            # 系统 Agent 权限
            PermissionRule("system_agent", "cs.customer", ["*"]),
            PermissionRule("system_agent", "cs.approval", ["*"]),
            PermissionRule("system_agent", "cs.invoice", ["*"]),
            PermissionRule("system_agent", "cs.finance", ["*"]),
            PermissionRule("system_agent", "cs.bpm", ["*"]),
        ]

    def assign_roles(self, caller_id: str, roles: List[str]) -> None:
        self._role_assignments[caller_id] = roles

    def get_roles(self, caller_id: str) -> List[str]:
        return self._role_assignments.get(caller_id, [])

    def check(
        self,
        caller_id: str,
        tenant_id: str,
        service: str,
        action: str,
        context: Dict = None,
    ) -> PermissionResult:
        """权限检查主入口"""
        roles = self.get_roles(caller_id)

        if not roles:
            return PermissionResult(
                allowed=False,
                reason=f"调用者 {caller_id} 未分配角色",
            )

        for rule in self._rules:
            if rule.role not in roles:
                continue
            if rule.service != service:
                continue
            if "*" in rule.actions or action in rule.actions:
                # ABAC 条件检查
                if rule.conditions and not self._check_conditions(rule.conditions, context or {}):
                    continue
                return PermissionResult(
                    allowed=True,
                    reason="",
                    matched_rule=f"{rule.role}:{service}:{action}",
                )

        return PermissionResult(
            allowed=False,
            reason=f"角色 {roles} 无权调用 {service}.{action}",
        )

    def add_rule(self, rule: PermissionRule) -> None:
        self._rules.append(rule)

    def _check_conditions(self, conditions: Dict, context: Dict) -> bool:
        """简单 ABAC 条件检查"""
        for key, expected in conditions.items():
            actual = context.get(key)
            if isinstance(expected, list):
                if actual not in expected:
                    return False
            elif actual != expected:
                return False
        return True
