"""
SelfPaw 企业版 — L1 个人数字分身
六大能力模块：
1. 组织身份绑定（SSO + 租户 + 岗位 + 数据 scope）
2. Intent Hub（意图识别 + 经营类升级 ΠPaw）
3. 岗位 Domain 包（Ontology + 可用 cs.*）
4. 授权内执行 + L2 分身代理（填表/发起流程/代拟邮件）
5. 个人蜂群决策（五视角 → 可审计备忘录）
6. 向上汇总（周报摘要 / SLA 异常 → ΠPaw Task）
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid

from .intent_hub import IntentHub, IntentUnit
from .swarm_decision import SwarmDecisionEngine, DecisionMemo
from ...platform.capability_services.cs_gateway import CapabilityServiceGateway, CSRequest
from ...platform.data_plane.tenant_manager import TenantManager, OrgIdentity
from ...platform.data_plane.event_stream import EventStream, DomainEvent


@dataclass
class WeeklySummary:
    """周报摘要（向上汇总能力）"""
    summary_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    week: str = ""
    completed_tasks: List[str] = field(default_factory=list)
    key_decisions: List[str] = field(default_factory=list)
    sla_exceptions: List[Dict] = field(default_factory=list)
    escalated_to_pipaw: List[str] = field(default_factory=list)
    next_week_focus: List[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_markdown(self) -> str:
        lines = [
            f"# 周报摘要 — {self.week}",
            f"**生成者**: {self.user_id}",
            "",
            "## 本周完成",
            *[f"- {t}" for t in self.completed_tasks],
            "",
            "## 关键决策",
            *[f"- {d}" for d in self.key_decisions],
        ]
        if self.sla_exceptions:
            lines += ["", "## SLA 异常（已升级 ΠPaw）"]
            for exc in self.sla_exceptions:
                lines.append(f"- {exc.get('type', '')}：{exc.get('description', '')}")
        lines += [
            "",
            "## 下周重点",
            *[f"- {f}" for f in self.next_week_focus],
        ]
        return "\n".join(lines)


class SelfPawEnterprise:
    """
    SelfPaw 企业版
    员工个人数字分身，第二大脑 + 任务代理 + 向上汇总
    """

    def __init__(
        self,
        user_id: str,
        tenant_id: str,
        tenant_manager: Optional[TenantManager] = None,
        cs_gateway: Optional[CapabilityServiceGateway] = None,
        event_stream: Optional[EventStream] = None,
    ):
        self.agent_id = f"selfpaw_{user_id}"
        self.user_id = user_id
        self.tenant_id = tenant_id

        # 依赖注入
        self._tenant_mgr = tenant_manager or TenantManager()
        self._gateway = cs_gateway or CapabilityServiceGateway()
        self._event_stream = event_stream or EventStream()

        # 六大能力模块
        self._identity: Optional[OrgIdentity] = None
        self._intent_hub: Optional[IntentHub] = None
        self._swarm_decision: Optional[SwarmDecisionEngine] = None
        self._domain_packages: List[str] = []

        # 活动记录
        self._task_log: List[Dict] = []
        self._decision_memos: List[DecisionMemo] = []
        self._intent_units: List[IntentUnit] = []

        # 初始化
        self._initialize()

    def _initialize(self):
        """能力1：绑定组织身份"""
        self._identity = self._tenant_mgr.get_identity(self.user_id)
        if self._identity:
            self._domain_packages = self._tenant_mgr.get_domain_packages(self.user_id)
            # 注册 cs_gateway 权限
            if self._identity.roles:
                perm = getattr(self._gateway, "_permission", None)
                if perm:
                    perm.assign_roles(self.agent_id, self._identity.roles + ["l1_user"])

        # 能力2：意图中枢
        self._intent_hub = IntentHub(self.user_id, self.tenant_id)

        # 能力5：个人蜂群决策
        self._swarm_decision = SwarmDecisionEngine(
            user_id=self.user_id,
            domain_context={"tenant_id": self.tenant_id, "domain_packages": self._domain_packages},
        )

    # ------------------------------------------------------------------
    # 能力2：意图识别与路由
    # ------------------------------------------------------------------
    def process_intent(self, user_input: str, context: Dict = None) -> Dict:
        """
        处理用户意图
        个人任务 → 本地执行
        业务事项 → 升级 ΠPaw
        """
        classification = self._intent_hub.classify(user_input, context)
        self._log_task("intent_classified", {"input": user_input, "domain": classification.domain})

        if classification.requires_pipaw:
            intent_unit = self._intent_hub.create_intent_unit(classification, context)
            self._intent_units.append(intent_unit)

            # 发布升级事件
            self._event_stream.publish(DomainEvent(
                event_type="intent.escalated_to_pipaw",
                aggregate_id=intent_unit.unit_id,
                aggregate_type="IntentUnit",
                tenant_id=self.tenant_id,
                actor_id=self.agent_id,
                payload={
                    "target_agent": intent_unit.target_agent,
                    "domain": classification.domain,
                    "category": classification.intent_category,
                },
            ))
            return {
                "mode": "escalated",
                "intent_unit_id": intent_unit.unit_id,
                "target_agent": intent_unit.target_agent,
                "classification": vars(classification),
                "message": f"已升级到 {intent_unit.target_agent}，创建意图单 {intent_unit.unit_id[:8]}",
            }
        else:
            return {
                "mode": "local_execution",
                "classification": vars(classification),
                "suggested_action": classification.suggested_action,
                "available_services": self._get_available_services(),
            }

    # ------------------------------------------------------------------
    # 能力3：岗位 Domain 包
    # ------------------------------------------------------------------
    def get_domain_ontology(self) -> Dict:
        """获取当前岗位的 Domain 本体（Ontology）"""
        domain_map = {
            "sales_ontology": {
                "entities": ["Lead", "Opportunity", "Quote", "Contract", "Customer"],
                "actions": ["qualify", "nurture", "propose", "negotiate", "close"],
                "metrics": ["pipeline_value", "win_rate", "sales_cycle", "arr"],
                "available_cs": ["cs.customer.qualify_lead", "cs.finance.create_quote", "cs.approval.create"],
            },
            "customer_success_ontology": {
                "entities": ["Customer", "HealthScore", "Ticket", "Renewal", "Expansion"],
                "actions": ["onboard", "monitor", "intervene", "expand", "renew"],
                "metrics": ["nrr", "churn_rate", "health_score", "nps"],
                "available_cs": ["cs.customer.health_score", "cs.invoice.ar_summary"],
            },
            "hr_ontology": {
                "entities": ["Requisition", "Candidate", "Employee", "Position", "Department"],
                "actions": ["recruit", "evaluate", "onboard", "develop", "offboard"],
                "metrics": ["time_to_hire", "retention_rate", "headcount"],
                "available_cs": ["cs.bpm.start", "cs.approval.create"],
            },
            "finance_ontology": {
                "entities": ["Invoice", "Payment", "Budget", "Revenue", "Expense"],
                "actions": ["invoice", "collect", "report", "forecast", "reconcile"],
                "metrics": ["arr", "nrr", "cashflow", "dso"],
                "available_cs": ["cs.invoice.*", "cs.finance.*"],
            },
        }
        return {
            pkg: domain_map.get(pkg, {"entities": [], "actions": [], "metrics": [], "available_cs": []})
            for pkg in self._domain_packages
        }

    # ------------------------------------------------------------------
    # 能力4：授权内执行（cs.* 代理调用）
    # ------------------------------------------------------------------
    def call_service(self, service: str, action: str, payload: Dict) -> Dict:
        """在授权范围内调用 cs.* 服务"""
        req = CSRequest(
            service=service,
            action=action,
            payload=payload,
            caller_id=self.agent_id,
            tenant_id=self.tenant_id,
        )
        resp = self._gateway.invoke(req)
        self._log_task("cs_called", {
            "service": service, "action": action,
            "status": resp.status, "latency_ms": resp.latency_ms,
        })
        return {"status": resp.status, "result": resp.result, "error": resp.error}

    def draft_email(self, to: str, subject: str, context: Dict) -> str:
        """代拟邮件（授权内执行能力）"""
        position = self._identity.position if self._identity else "员工"
        template = (
            f"主题：{subject}\n\n"
            f"尊敬的 {to}，\n\n"
            f"[由 {self._identity.name if self._identity else self.user_id} 的数字分身代拟]\n\n"
            f"根据我们的业务需求，{context.get('purpose', '就以下事项进行沟通')}：\n\n"
            f"{context.get('body', '[正文内容待填写]')}\n\n"
            f"如有问题，请随时联系。\n\n"
            f"此致\n{self._identity.name if self._identity else self.user_id}\n{position}"
        )
        self._log_task("email_drafted", {"to": to, "subject": subject})
        return template

    # ------------------------------------------------------------------
    # 能力5：个人蜂群决策
    # ------------------------------------------------------------------
    def make_decision(self, question: str, context: Dict = None) -> DecisionMemo:
        """五视角辩证决策"""
        memo = self._swarm_decision.decide(question, context)
        self._decision_memos.append(memo)
        self._log_task("decision_made", {
            "question": question[:50],
            "risk_level": memo.risk_level,
            "confidence": memo.confidence,
        })
        return memo

    # ------------------------------------------------------------------
    # 能力6：向上汇总
    # ------------------------------------------------------------------
    def generate_weekly_summary(
        self,
        week: str = None,
        sla_exceptions: List[Dict] = None,
    ) -> WeeklySummary:
        """生成周报摘要 + SLA 异常自动创建 ΠPaw Task"""
        current_week = week or datetime.now(timezone.utc).strftime("%Y-W%V")
        recent_tasks = self._task_log[-20:]

        completed = [
            t["detail"].get("question", t.get("type", ""))
            for t in recent_tasks
            if t.get("type") in ("cs_called", "decision_made", "email_drafted")
        ]

        key_decisions = [
            m.decision_question for m in self._decision_memos[-5:]
        ]

        exceptions = sla_exceptions or []
        escalated = [u.unit_id for u in self._intent_units[-10:]]

        summary = WeeklySummary(
            user_id=self.user_id,
            week=current_week,
            completed_tasks=completed[:10],
            key_decisions=key_decisions,
            sla_exceptions=exceptions,
            escalated_to_pipaw=escalated,
            next_week_focus=["跟进升级意图单", "完成待审批项目"],
        )

        # SLA 异常自动推送到 ΠPaw
        for exc in exceptions:
            self._event_stream.publish(DomainEvent(
                event_type="sla.exception_reported",
                aggregate_id=summary.summary_id,
                aggregate_type="WeeklySummary",
                tenant_id=self.tenant_id,
                actor_id=self.agent_id,
                payload=exc,
            ))

        self._log_task("weekly_summary_generated", {"week": current_week})
        return summary

    def get_status(self) -> Dict:
        """获取 SelfPaw 状态概览"""
        return {
            "agent_id": self.agent_id,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "identity": vars(self._identity) if self._identity else None,
            "domain_packages": self._domain_packages,
            "task_count": len(self._task_log),
            "decision_count": len(self._decision_memos),
            "intent_unit_count": len(self._intent_units),
        }

    def _log_task(self, task_type: str, detail: Dict):
        self._task_log.append({
            "type": task_type,
            "detail": detail,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def _get_available_services(self) -> List[str]:
        ontology = self.get_domain_ontology()
        services = []
        for pkg_data in ontology.values():
            services.extend(pkg_data.get("available_cs", []))
        return list(set(services))
