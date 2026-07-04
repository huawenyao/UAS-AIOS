# 企业世界模型规格（REQ-EDH-PP-003）

> **status**: frozen-draft · Phase-0

## 五维最小字段集

| 维度 | 配置路径 | 必填 |
|------|----------|------|
| 空间 space | `dimensions.space` | tenant_id, systems[] |
| 时间 time | `dimensions.time` | SLA / 有效期 |
| 主体 subject | `dimensions.subject[]` | id, type |
| 客体 object | `dimensions.object[]` | id, lifecycle[] |
| 反馈 feedback | `dimensions.feedback[]` | id, type |

Schema：`schemas/enterprise_world_model.schema.json`  
样例：`configs/enterprise_world_model.sample.json`  
SubApp：`projects/enterprise-sales-os/configs/world_model.json`

## 法则包（SLA / 审批矩阵 / 合规红线）

见 `configs/cs_law_pack.sample.json` 或 subapp `law_pack_ref`。

## 与 governance_policy 对齐

| governance 字段 | WM 映射 |
|-----------------|---------|
| `risk_levels` | lens 风险视角 |
| `discount_approval_threshold` | 审批矩阵法则 |
| `audit_required` | mirror 审计链 |

## 三身份

| 身份 | 配置键 | 含义 |
|------|--------|------|
| 镜像 mirror | `identities.mirror` | 状态与审计反映世界 |
| 透镜 lens | `identities.lens` | 策略与风险看本质 |
| 熔炉 furnace | `identities.furnace` | ChangeSet 重塑配置 |

验证：`python scripts/validate_enterprise_wm.py validate`
