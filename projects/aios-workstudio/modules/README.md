# aios-workstudio 模块目录

来源：`docs/strategic/design/uas-aios-cluster.html`  
规则：禁止平行建设：本仓库只实现使用平面壳 + CapabilityHub 门面 + Console 壳契约；零件实现落在 services/  
Hub：`http://127.0.0.1:18088`

| ID | 模块 | 平面 | 本仓库角色 | 代码落点 |
|----|------|------|------------|----------|
| `m1` | [M1 WorkStudio · 使用平面](./use/M01-workstudio/SPEC.md) | 使用平面 · 套件 A | 本产品实现 | `projects/aios-workstudio/packages/workstudio-web` |
| `m5` | [M5 Insight→Task 编译器](./use/M05-insight-task/SPEC.md) | 使用平面（嵌在作战台） | 本产品组合（UI 在此，内核在 Hub） | `services/hub-api/uas_hub/insight_task.py` |
| `sse` | [进度 SSE](./use/sse-progress/SPEC.md) | 使用平面 | 本产品组合（UI 在此，内核在 Hub） | `services/hub-api/uas_hub/http_app.py` |
| `m6` | [M6 Capability Hub 控制面](./control/M06-capability-hub/SPEC.md) | 控制平面 | 本产品实现 | `projects/aios-workstudio/CapabilityHub` |
| `nb` | [NocoBase · Platform Console 壳](./console/nocobase-shell/SPEC.md) | 套件 B 可视化壳 | Console 可视化壳（不当内核） | `projects/aios-workstudio/Console` |
| `hubc` | [Hub Console · B1 控制中心](./console/B1-hub-console/SPEC.md) | Platform Console（NocoBase 壳内） | Console 可视化壳（不当内核） | `projects/aios-workstudio/Console` |
| `pack` | [Pack Studio](./console/B2-pack-studio/SPEC.md) | Platform Console（NocoBase 壳内） | Console 可视化壳（不当内核） | `projects/aios-workstudio/Console` |
| `gov` | [Governance Console · B4](./console/B4-governance/SPEC.md) | Platform Console（NocoBase 壳内） | Console 可视化壳（不当内核） | `projects/aios-workstudio/Console` |
| `m7` | [M7 Capability Registry cs.*](./control/M07-registry/SPEC.md) | 控制 / 系统面 | 本产品只经 hub.* 消费 | `configs/capability_registry.json` |
| `m13` | [M13 MCP Gateway](./control/M13-mcp-gateway/SPEC.md) | 协议面 | 本产品只经 hub.* 消费 | `services/hub-api/uas_hub/adapters/mcp.py` |
| `m8` | [M8 Identity & Policy](./control/M08-iam/SPEC.md) | 治理面 | 本产品只经 hub.* 消费 | `services/hub-api/uas_hub/adapters/iam.py` |
| `m11` | [M11 Audit](./control/M11-audit/SPEC.md) | 治理面 | 本产品只经 hub.* 消费 | `services/hub-api/uas_hub/hub.py` |
| `m12` | [M12 Evolution Engine](./control/M12-evolution/SPEC.md) | 演化面 | 本产品只经 hub.* 消费 | `services/hub-api/uas_hub/adapters/evolution.py` |
| `m10` | [M10 Artifact Store](./control/M10-artifact/SPEC.md) | 运行面 | 本产品只经 hub.* 消费 | `services/hub-api/uas_hub/adapters/artifact.py` |
| `m9` | [M9 Skill 协议状态机](./control/M09-skill/SPEC.md) | 编织面 | 本产品只经 hub.* 消费 | `projects/aios-workstudio/CapabilityHub/capability_hub/skills.py` |
| `m20` | [M20 工具类型 · JSON Schema](./control/M20-schema/SPEC.md) | 协议面 | 本产品只经 hub.* 消费 | `schemas/` |
| `m21` | [M21 跨岗位委托 · A2A](./control/M21-a2a/SPEC.md) | 编织 / 协议 | 本产品只经 hub.* 消费 | `services/hub-api/uas_hub/hub.py` |
| `m2` | [M2 责任图 Accountability Graph](./ops/M02-accountability-graph/SPEC.md) | K-L0 经营本体 · Console 块 1 | 本产品只经 hub.* 消费 | `services/hub-api/uas_hub/graph_store.py` |
| `m3` | [M3 世界模型 Store](./ops/M03-wm-store/SPEC.md) | K-L0 · Console 块 2 | 本产品只经 hub.* 消费 | `services/hub-api/uas_hub/wm_store.py` |
| `m4` | [M4 Law Pack](./ops/M04-law-pack/SPEC.md) | K-L0 / 德 · Pack Studio | 本产品只经 hub.* 消费 | `services/hub-api/uas_hub/adapters/law.py` |
| `m14` | [M14 System Connector](./ops/M14-connector/SPEC.md) | 系统面 | 平台零件 · 不在本产品实现 | `services/hub-api/uas_hub/adapters/connector.py` |
| `m23` | [M23 主数据 SoR](./ops/M23-sor/SPEC.md) | 系统面 | 外部系统 · 只连接 | `客户 CRM/ERP/仓` |
| `m18` | [M18 外环 · Temporal](./ops/M18-temporal/SPEC.md) | 运行面 | 平台零件 · 不在本产品实现 | `services/temporal-worker` |
| `m19` | [M19 内环 · LangGraph 1.0](./ops/M19-innerloop/SPEC.md) | 编织 / 运行 | 平台零件 · 不在本产品实现 | `services/hub-api/uas_hub/adapters/inner_loop.py` |
| `m24` | [M24 模型推理 Broker](./ops/M24-broker/SPEC.md) | 编织面 | 平台零件 · 不在本产品实现 | `services/hub-api/uas_hub/adapters/broker.py` |
| `m15` | [M15 口径服务 · Cube + OSI](./ops/M15-cube-osi/SPEC.md) | K-L1 · Console 口径页 | 平台零件 · 不在本产品实现 | `services/hub-api/uas_hub/adapters/cube.py` |
| `m16` | [M16 时态知识 · Graphiti](./ops/M16-graphiti/SPEC.md) | K-L2 · Console 块 3 | 平台零件 · 不在本产品实现 | `services/hub-api/uas_hub/adapters/kg.py` |
| `m17` | [M17 个人记忆 · Lethe](./ops/M17-lethe/SPEC.md) | K-L3 | 平台零件 · 不在本产品实现 | `services/hub-api/uas_hub/adapters/memory.py` |
| `m22` | [M22 Utopia（可选 Spike）](./ops/M22-utopia/SPEC.md) | 知识工程 | 默认不部署 | `默认不部署` |
| `idp` | [企业 IdP](./ops/idp/SPEC.md) | 身份源 | 外部系统 · 只连接 | `企业 IdP` |

重新生成：`python projects/aios-workstudio/modules/gen_specs.py`
