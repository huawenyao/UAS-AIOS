"""
Intent Hub — 意图中枢（SelfPaw 企业版能力2）
职责：
  - 识别用户意图（个人执行 vs 升级 ΠPaw）
  - 经营类意图一键升级 ΠPaw 职能/经营 Agent
  - 返回意图单 + Evidence
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid


@dataclass
class IntentClassification:
    intent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    raw_input: str = ""
    intent_type: str = ""     # personal_task / business_event / escalation_needed
    intent_category: str = "" # write / query / process / report / decision
    domain: str = ""          # sales / hr / finance / ops / personal
    confidence: float = 0.0
    requires_pipaw: bool = False
    suggested_action: str = ""
    evidence: List[Dict] = field(default_factory=list)
    escalation_target: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class IntentUnit:
    """意图单 — 向 ΠPaw 提交的标准化工作单元"""
    unit_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    originator_id: str = ""
    intent_classification: Optional[IntentClassification] = None
    context: Dict = field(default_factory=dict)
    evidence: List[Dict] = field(default_factory=list)  # 支撑证据
    priority: str = "normal"  # urgent / normal / low
    target_agent: str = ""    # l2_hr / l2_finance / l3_sales / ...
    status: str = "created"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IntentHub:
    """
    意图中枢
    个人任务 → 本地执行
    业务事项 → 升级 ΠPaw（创建意图单+证据）
    """

    # 经营类关键词映射
    BUSINESS_KEYWORDS = {
        "sales": ["客户", "报价", "合同", "签单", "线索", "跟进", "续费", "折扣"],
        "finance": ["发票", "报销", "付款", "预算", "账期", "回款"],
        "hr": ["招聘", "入职", "绩效", "离职", "调薪", "组织架构"],
        "ops": ["故障", "SLA", "交付", "部署", "上线"],
    }

    ESCALATION_TRIGGERS = [
        "需要审批", "需要决策", "跨部门", "客户投诉", "红线", "合规", "超出权限"
    ]

    def __init__(self, user_id: str, tenant_id: str):
        self.user_id = user_id
        self.tenant_id = tenant_id
        self._intent_history: List[IntentClassification] = []

    def classify(self, raw_input: str, context: Dict = None) -> IntentClassification:
        """意图识别分类"""
        ctx = context or {}
        domain = self._detect_domain(raw_input)
        requires_escalation = self._check_escalation_triggers(raw_input)
        intent_type, category = self._classify_type(raw_input, domain, requires_escalation)

        escalation_map = {
            "sales": "l3_sales_agent",
            "finance": "l2_finance_agent",
            "hr": "l2_hr_agent",
            "ops": "l2_ops_agent",
        }

        classification = IntentClassification(
            raw_input=raw_input,
            intent_type=intent_type,
            intent_category=category,
            domain=domain,
            confidence=self._compute_confidence(raw_input, domain, ctx),
            requires_pipaw=requires_escalation or intent_type == "business_event",
            suggested_action=self._suggest_action(intent_type, domain, raw_input),
            evidence=self._collect_evidence(raw_input, ctx),
            escalation_target=escalation_map.get(domain) if requires_escalation else None,
        )

        self._intent_history.append(classification)
        return classification

    def create_intent_unit(
        self,
        classification: IntentClassification,
        context: Dict = None,
        priority: str = "normal",
    ) -> IntentUnit:
        """创建意图单（用于向 ΠPaw 提交）"""
        target = classification.escalation_target or self._route_to_agent(classification)
        return IntentUnit(
            originator_id=self.user_id,
            intent_classification=classification,
            context=context or {},
            evidence=classification.evidence,
            priority=priority,
            target_agent=target,
        )

    def get_history(self) -> List[IntentClassification]:
        return list(self._intent_history)

    # ------------------------------------------------------------------
    # 内部分类逻辑（规则引擎，可替换 LLM）
    # ------------------------------------------------------------------
    def _detect_domain(self, text: str) -> str:
        for domain, keywords in self.BUSINESS_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return domain
        return "personal"

    def _check_escalation_triggers(self, text: str) -> bool:
        return any(trigger in text for trigger in self.ESCALATION_TRIGGERS)

    def _classify_type(self, text: str, domain: str, escalation: bool) -> tuple:
        if escalation:
            return "escalation_needed", "decision"
        if domain != "personal":
            return "business_event", self._detect_category(text)
        return "personal_task", self._detect_category(text)

    def _detect_category(self, text: str) -> str:
        if any(kw in text for kw in ["写", "起草", "生成", "模板"]):
            return "write"
        if any(kw in text for kw in ["查", "看", "统计", "分析"]):
            return "query"
        if any(kw in text for kw in ["发起", "提交", "申请", "开始"]):
            return "process"
        if any(kw in text for kw in ["汇报", "总结", "报告", "摘要"]):
            return "report"
        return "general"

    def _suggest_action(self, intent_type: str, domain: str, text: str) -> str:
        if intent_type == "personal_task":
            return f"本地执行：{domain} 任务"
        if intent_type == "business_event":
            return f"创建意图单并推送到 {domain} 职能 Agent"
        return f"升级审批：需要 {domain} 部门介入"

    def _collect_evidence(self, text: str, ctx: Dict) -> List[Dict]:
        evidence = []
        if ctx.get("current_opportunity"):
            evidence.append({"type": "opportunity", "ref": ctx["current_opportunity"]})
        if ctx.get("customer_id"):
            evidence.append({"type": "customer", "ref": ctx["customer_id"]})
        if ctx.get("amount"):
            evidence.append({"type": "amount", "value": ctx["amount"]})
        evidence.append({"type": "user_input", "text": text[:100]})
        return evidence

    def _compute_confidence(self, text: str, domain: str, ctx: Dict) -> float:
        base = 0.6
        if domain != "personal":
            base += 0.2
        if ctx:
            base += 0.1
        return min(base, 0.95)

    def _route_to_agent(self, cls: IntentClassification) -> str:
        route_map = {
            ("sales", "write"): "l1_self",
            ("sales", "query"): "l1_self",
            ("sales", "process"): "l3_sales_agent",
            ("finance", "process"): "l2_finance_agent",
            ("hr", "process"): "l2_hr_agent",
        }
        return route_map.get((cls.domain, cls.intent_category), "l1_self")
