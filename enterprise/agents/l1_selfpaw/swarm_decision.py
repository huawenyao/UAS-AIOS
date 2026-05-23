"""
个人蜂群决策引擎（SelfPaw 企业版能力5）
五视角辩证决策 → 可审计决策备忘录
继承 selfpaw-cognitive-swarm 的否定之否定方法论
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List
import uuid


@dataclass
class PerspectiveAnalysis:
    """单一视角分析"""
    perspective: str    # analyst / critic / strategist / risk_officer / synthesizer
    stance: str         # support / challenge / neutral
    key_points: List[str]
    confidence: float
    recommendation: str


@dataclass
class DecisionMemo:
    """可审计决策备忘录"""
    memo_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    decision_question: str = ""
    context: Dict = field(default_factory=dict)
    perspectives: List[PerspectiveAnalysis] = field(default_factory=list)
    synthesis: str = ""
    recommended_action: str = ""
    risk_level: str = "medium"  # low / medium / high
    confidence: float = 0.0
    alternatives: List[str] = field(default_factory=list)
    created_by: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_markdown(self) -> str:
        lines = [
            f"# 决策备忘录 {self.memo_id[:8]}",
            f"**问题**: {self.decision_question}",
            f"**风险级别**: {self.risk_level} | **置信度**: {self.confidence:.0%}",
            "",
            "## 五视角分析",
        ]
        for p in self.perspectives:
            lines.extend([
                f"### {p.perspective}（{p.stance}）",
                *[f"- {pt}" for pt in p.key_points],
                f"**建议**: {p.recommendation}",
                "",
            ])
        lines.extend([
            "## 综合判断",
            self.synthesis,
            "",
            "## 推荐行动",
            f"**{self.recommended_action}**",
        ])
        if self.alternatives:
            lines.extend(["", "## 备选方案", *[f"- {a}" for a in self.alternatives]])
        return "\n".join(lines)


class SwarmDecisionEngine:
    """
    五智能体蜂群决策引擎
    角色：
    - Analyst    — 数据与事实分析
    - Critic     — 质疑与否定（否定之否定）
    - Strategist — 战略价值判断
    - RiskOfficer— 风险与合规评估
    - Synthesizer— 综合与决策
    """

    def __init__(self, user_id: str, domain_context: Dict = None):
        self.user_id = user_id
        self.domain_context = domain_context or {}

    def decide(self, question: str, context: Dict = None) -> DecisionMemo:
        """执行五视角辩证决策"""
        ctx = {**self.domain_context, **(context or {})}
        perspectives = [
            self._analyst_perspective(question, ctx),
            self._critic_perspective(question, ctx),
            self._strategist_perspective(question, ctx),
            self._risk_officer_perspective(question, ctx),
        ]
        synthesis_perspective = self._synthesizer_perspective(question, ctx, perspectives)
        perspectives.append(synthesis_perspective)

        memo = DecisionMemo(
            decision_question=question,
            context=ctx,
            perspectives=perspectives,
            synthesis=synthesis_perspective.key_points[0] if synthesis_perspective.key_points else "",
            recommended_action=synthesis_perspective.recommendation,
            risk_level=self._assess_risk_level(perspectives),
            confidence=self._compute_confidence(perspectives),
            alternatives=self._generate_alternatives(question, ctx, perspectives),
            created_by=self.user_id,
        )
        return memo

    # ------------------------------------------------------------------
    # 五个视角智能体（规则驱动，可接 LLM）
    # ------------------------------------------------------------------
    def _analyst_perspective(self, question: str, ctx: Dict) -> PerspectiveAnalysis:
        points = []
        if ctx.get("amount"):
            points.append(f"金额维度：{ctx['amount']} 元")
        if ctx.get("customer_id"):
            points.append(f"客户维度：{ctx['customer_id']}")
        if ctx.get("timeline"):
            points.append(f"时间维度：{ctx['timeline']}")
        if not points:
            points = ["基于现有信息进行数据分析", "关键指标待补充"]

        return PerspectiveAnalysis(
            perspective="数据分析师",
            stance="neutral",
            key_points=points,
            confidence=0.7,
            recommendation="收集更多数据后决策",
        )

    def _critic_perspective(self, question: str, ctx: Dict) -> PerspectiveAnalysis:
        challenges = []
        amount = ctx.get("amount", 0)
        if isinstance(amount, (int, float)) and amount > 100000:
            challenges.append("金额较大，需谨慎评估风险")
        if not ctx.get("decision_maker"):
            challenges.append("决策人未确认，推进风险较高")
        challenges.append("质疑假设：当前方案是否是最优路径？")

        return PerspectiveAnalysis(
            perspective="批判审视者",
            stance="challenge",
            key_points=challenges or ["当前信息不足以做出确定性判断"],
            confidence=0.65,
            recommendation="补充关键验证后再行动",
        )

    def _strategist_perspective(self, question: str, ctx: Dict) -> PerspectiveAnalysis:
        strategic_points = []
        domain = ctx.get("domain", "general")
        if domain == "sales":
            strategic_points = ["战略价值：新客户拓展", "长期关系建立优先于短期利润"]
        elif domain == "finance":
            strategic_points = ["现金流优先", "账期管理影响 Q 末回款"]
        else:
            strategic_points = ["与组织战略方向一致性评估", "资源配置最优化"]

        return PerspectiveAnalysis(
            perspective="战略规划师",
            stance="support",
            key_points=strategic_points,
            confidence=0.75,
            recommendation="推进，并制定清晰里程碑",
        )

    def _risk_officer_perspective(self, question: str, ctx: Dict) -> PerspectiveAnalysis:
        risks = []
        if ctx.get("compliance_required"):
            risks.append("⚠️ 需要合规审查")
        if ctx.get("cross_department"):
            risks.append("⚠️ 跨部门协调风险")
        risks.append("识别关键风险点并制定缓释措施")

        return PerspectiveAnalysis(
            perspective="风险合规官",
            stance="neutral",
            key_points=risks,
            confidence=0.8,
            recommendation="完成风险评估后推进",
        )

    def _synthesizer_perspective(
        self,
        question: str,
        ctx: Dict,
        prior_perspectives: List[PerspectiveAnalysis],
    ) -> PerspectiveAnalysis:
        supports = sum(1 for p in prior_perspectives if p.stance == "support")
        challenges = sum(1 for p in prior_perspectives if p.stance == "challenge")
        avg_confidence = sum(p.confidence for p in prior_perspectives) / max(len(prior_perspectives), 1)

        if supports > challenges and avg_confidence > 0.7:
            synthesis = "综合多视角判断：建议推进，把控关键风险"
            recommendation = "启动行动计划，设置检查点"
        elif challenges > supports:
            synthesis = "多视角质疑较强：建议补充信息后再决策"
            recommendation = "暂缓，收集更多证据"
        else:
            synthesis = "各视角基本平衡：需要关键决策者介入"
            recommendation = "升级至上级或召开决策会议"

        return PerspectiveAnalysis(
            perspective="综合决策者",
            stance="neutral",
            key_points=[synthesis, f"支持:{supports} 质疑:{challenges}"],
            confidence=avg_confidence,
            recommendation=recommendation,
        )

    def _assess_risk_level(self, perspectives: List[PerspectiveAnalysis]) -> str:
        challenge_count = sum(1 for p in perspectives if p.stance == "challenge")
        if challenge_count >= 2:
            return "high"
        if challenge_count == 1:
            return "medium"
        return "low"

    def _compute_confidence(self, perspectives: List[PerspectiveAnalysis]) -> float:
        if not perspectives:
            return 0.5
        return round(sum(p.confidence for p in perspectives) / len(perspectives), 2)

    def _generate_alternatives(
        self,
        question: str,
        ctx: Dict,
        perspectives: List[PerspectiveAnalysis],
    ) -> List[str]:
        return [
            "方案A：分阶段推进，降低单次风险",
            "方案B：寻求外部专家意见",
            "方案C：延期至条件成熟再执行",
        ]
