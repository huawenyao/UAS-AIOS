# 数字人生态 Harness（reqharness 世界模型）

> 项目：`edh-ecosystem` · Phase-0 · UAS-AIOS 仓库根目录

## 快速开始

```bash
# 加载状态
# Read: harness/state.json, harness/entity-map.json, harness/knowledge/index.yaml

# 验证基线（reqharness 变更后必跑）
python harness/invariants/run-all.py

# 能力服务注册表
python scripts/validate_capability_registry.py list
python scripts/validate_capability_registry.py validate
python scripts/validate_enterprise_policy.py validate
python scripts/validate_connectors.py validate
python scripts/invoke_capability.py invoke cs.lead.qualify_lead --payload-json "{\"lead_id\":\"L-1001\"}"
```

迭代配置：`harness/reqharness.yaml`

## 目录

| 路径 | 用途 |
|------|------|
| `state.json` | 模块状态、sprint、指标 |
| `entity-map.json` | 实体图谱与依赖规则 |
| `knowledge/` | 产品/技术/领域/约束知识 |
| `requirements/*.req.md` | 需求与验收标准 |
| `invariants/run-all.py` | 基线验证 |

## 战略文档

- `docs/strategic/Enterprise_Digital_Human_Ecosystem_Product_Definition.md`
- `docs/strategic/UAS_AIPOS_SelfPaw_Integrated_Product_Tech_Architecture.md`

## 需求编号

| 前缀 | 含义 |
|------|------|
| REQ-EDH-BASE | 基线 |
| REQ-EDH-PL | 平台层 |
| REQ-EDH-SP | SelfPaw |
| REQ-EDH-PP | ΠPaw |
| REQ-EDH-K | UAS Kernel |

## reqharness 工作流

1. 任务前：读 state + entity-map + knowledge/index  
2. 执行：按角色走 Standard/Enterprise Flow  
3. 产出：回写 requirements / knowledge / entity-map  
4. 变更后：`python harness/invariants/run-all.py`
