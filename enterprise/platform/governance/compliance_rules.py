"""
合规规则引擎
职责：红线拦截 / 监管约束 / 数据保护合规
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class ComplianceViolation:
    rule_id: str
    severity: str         # block / warn
    description: str
    remedy: str


class ComplianceEngine:
    """
    合规规则引擎（热更新支持）
    核心职责：拦截违规，不是惩罚，是保护
    """

    def __init__(self):
        self._rules = self._default_rules()

    def _default_rules(self) -> List[Dict]:
        return [
            {
                "rule_id": "DISCOUNT_MAX",
                "description": "折扣率不得超过30%（未经CFO批准）",
                "severity": "block",
                "check": lambda payload: payload.get("discount_pct", 0) <= 30,
                "remedy": "请申请CFO特批折扣",
            },
            {
                "rule_id": "CONTRACT_LEGAL_REVIEW",
                "description": "超过100万合同必须经法务审核",
                "severity": "block",
                "check": lambda payload: not (
                    payload.get("contract_value", 0) >= 1000000 and
                    not payload.get("legal_reviewed", False)
                ),
                "remedy": "请先提交法务审核",
            },
            {
                "rule_id": "PERSONAL_DATA_CONSENT",
                "description": "处理个人数据需获得明确同意",
                "severity": "block",
                "check": lambda payload: payload.get("personal_data_consent", True),
                "remedy": "请获取数据主体同意后操作",
            },
            {
                "rule_id": "CREDIT_LIMIT",
                "description": "信用期限不超过90天（标准账期）",
                "severity": "warn",
                "check": lambda payload: payload.get("credit_days", 30) <= 90,
                "remedy": "超长账期需财务总监审批",
            },
        ]

    def check(self, action: str, payload: Dict) -> Tuple[bool, List[ComplianceViolation]]:
        """
        执行合规检查
        返回：(passed, violations)
        """
        violations = []
        for rule in self._rules:
            try:
                if not rule["check"](payload):
                    violations.append(ComplianceViolation(
                        rule_id=rule["rule_id"],
                        severity=rule["severity"],
                        description=rule["description"],
                        remedy=rule["remedy"],
                    ))
            except Exception:
                pass

        # 有 block 级违规则拦截
        blocked = any(v.severity == "block" for v in violations)
        return not blocked, violations

    def reload_rules_from_config(self, rules_config: List[Dict]) -> None:
        """从配置热更新规则（法则包热更新）"""
        # 保留内置规则，追加自定义规则
        self._rules = self._default_rules()
        for rc in rules_config:
            # 简单表达式规则（无需代码部署）
            expr = rc.get("expression", "True")
            rule = {
                "rule_id": rc["rule_id"],
                "description": rc["description"],
                "severity": rc.get("severity", "warn"),
                "check": lambda payload, e=expr: bool(eval(e, {}, payload)),
                "remedy": rc.get("remedy", "请联系管理员"),
            }
            self._rules.append(rule)
