# Requirement: REQ-EDH-SP-003 - Intent Hub 与升级 ΠPaw



## Status: completed



## 需求层级: 产品



## 优先级: P0



## Acceptance Criteria



- [x] IntentObject 扩展：`escalation_target`, `evidence_refs[]`

- [x] 意图分类：personal | collaboration | business_outward

- [x] `POST /intent/escalate` 跨产品契约（创建 ΠPaw Working Task）

- [x] E2E 用例：员工提交客诉→ΠPaw 客服 Task 可见



## 映射能力



SP-03 · SP-07 · entity-map SelfPawEnterprise_to_PiPaw



## 交付物



| 类型 | 路径 |

|------|------|

| Schema | `schemas/intent_object.schema.json`, `schemas/working_task.schema.json` |

| 策略/样例 | `configs/intent_escalation_policy.sample.json`, `configs/intent_samples/complaint_escalation.sample.json` |

| 运行时 | `asui-cli/src/asui/intent_hub.py` |

| API 草案 | `harness/knowledge/technical/intent-escalation-api.md` |

| 校验/CLI | `scripts/validate_intent_escalation.py`, `scripts/escalate_intent.py` |

| 测试 | `asui-cli/tests/test_intent_escalation.py` |



## 验证



```bash

python scripts/validate_intent_escalation.py validate

python scripts/escalate_intent.py escalate

python harness/invariants/run-all.py

```

