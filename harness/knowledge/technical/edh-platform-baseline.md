# 平台 + 模型技术基线（Phase-0）

## 分层

```
Model Layer     → providers / 领域模型 / 嵌入
Platform Layer  → UAS Kernel + 数字基础 + S-Grid 连接器
Data Plane      → 租户 · 主数据 · 事件 · 审计
```

## UAS 八元组映射

| 元组 | Phase-0 交付 |
|------|--------------|
| I | IntentObject / Intent Hub 契约 |
| K | Domain 认知包 + ASUI configs |
| R | UASRuntimeService + SelfPaw AEE |
| A | 岗位 Agent 编制（ΠPaw）+ ReAct（SelfPaw） |
| S | cs.* + SystemConnector |
| G | G1-G7 + L1/L2/L3 |
| E | ChangeSet + evolveApply |
| Π | MCP + Outward Webhook（规划） |

## 工程仓库

| 组件 | 路径 |
|------|------|
| UAS Kernel | `asui-cli/src/asui/engine/` |
| Runtime CLI | `scripts/run_uas_runtime_service.py` |
| SelfPaw 参考 | `../aipos/copaw-src`（只读对照） |
| 战略原型 UI | `docs/strategic/demo/` |

## ASUI 原则

- 知识即配置：业务规则进 `configs/`、`.claude/skills/`  
- 构建即运行：subapp validate/run 无需编译  
- 增量演化：`evolve_apply` + ChangeSet  

## Phase-0 技术出口

- [x] `schemas/capability_service.schema.json`（契约）  
- [x] `configs/capability_registry.json`（6 服务注册表）  
- [x] 租户/RBAC 规格（`enterprise_tenant` + `enterprise_permission` schema）  
- [x] 审计链 schema + 规格（REQ-EDH-PL-006）  
- [ ] Intent 升级 ΠPaw 跨产品 API 草案  
