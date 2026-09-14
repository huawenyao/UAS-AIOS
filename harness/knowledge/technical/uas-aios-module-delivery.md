# 技术方案：UAS-AIOS 模块交付（研究→规划）

| 项 | 值 |
|----|-----|
| 业务需求追溯 | REQ-UAS-AIOS-001 · REQ-UAS-M01–M24 |
| 技术目标 | 按冻结栈落地 Hub 家族与零件；阶段 A 可运行只读+签发 |
| 非目标 | 不重开选型；阶段 A 领域内核在 `services/hub-api`，Demo 走 pack.open 夹具 |
| 详细栈 | `docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md` |
| 契约 | `docs/strategic/design/UAS_AIOS_ARCHITECTURE_SPEC.md` §3–5 |

---

## 1. 整体架构

```
workstudio-web ──hub.*──► hub-api (M2–M12,M20,M21,M24)
                              ├ mcp-gateway (M13)
                              ├ temporal-worker (M18) ─ Temporal
                              │     └ InnerLoop (M19 LangGraph)
                              ├ cube-api (M15)
                              ├ graphiti-worker (M16) ─ Neo4j
                              ├ lethe-api (M17) ─ Postgres uas_lethe
                              └ connector-* (M14) ─ SoR (M23)
```

判定序、信封、场景禁写见规格 §2.3。端口：CubePort / KgPort / MemoryPort / InnerLoopPort。

---

## 2. 分模块详细设计（开发视角）

每模块需求卡含 TDD 用例名。下表是实现顺序、接口、数据、测试与发布。

### 阶段 A（0–6 周）承诺范围

| 模块 | 接口 | 数据 | 先写测试 | 人天(估) |
|------|------|------|----------|----------|
| M20 | schema 生成 CI | `schemas/insight.schema.json` `operating_task.schema.json` | drift CI | 2 |
| M2 | 内部 GraphStore + 被 pack.open 使用 | `ag_graph/node/edge` | five_tuple / tenant | 5 |
| M7 | Registry 加载 + 写操作标记 | 扩展 `capability_registry.json` | scene 隐藏写工具 | 3 |
| M6 | FastAPI `hub/v1` + PolicyChain | 无 SoR 密钥 | profile 注入、序、explain | 8 |
| M5 | `insight.drill` `task.issue` | insight / operating_task 表 | 无源节点/未接地/不启 Temporal | 5 |
| M1 | Demo 接 pack.open + 签发 | 无 | 零零件 SDK 契约测试 | 5 |
| M3 | `hub.wm.get/patch` 最小 | wm_doc | 禁 PATCH compiled | 3 |

合计约 31 人天（单小队 6 周含 20% buffer）。

### 阶段 B（Q1）

| 模块 | 接口 | 数据 | 先写测试 | 人天 |
|------|------|------|----------|------|
| M18 | exec.open → Workflow | Temporal store | 杀 Worker 续跑、L2 signal | 8 |
| M19 | InnerLoop SPI | checkpoint PG | 无出站 CRM | 8 |
| M24 | Broker 路由 | 无状态 | 换提供商契约不变 | 3 |
| M13 | MCP HTTP | 无 | list 过滤 + call 双检 | 5 |
| M16 | hub.kg.search/ingest | Neo4j | 未接地拦截 | 6 |
| M8 | OIDC + binding | iam_binding | 无岗位/双轨 | 5 |
| M10 | artifact API | MinIO + meta | file≠状态 | 3 |
| M11 | 追加审计 | 分区表 | hash chain | 3 |
| M14 | Connector SPI + mock 拜访 | KMS 引用 | 幂等、密钥不在 worker | 5 |

### 阶段 C（Q2）

| 模块 | 先写测试 | 人天 |
|------|----------|------|
| M15 Cube+OSI | stale、不签发 | 6 |
| M4 Law Pack | 未审批不进 compiled | 4 |
| M12 Evolution | auto_apply=false | 4 |
| M17 Lethe | pipaw 403、无 FK | 4 |
| M9 Skill 状态机 | explore 不可 execute | 4 |
| M23 真 SoR 槽 | object_ref 不复制主档 | 4 |
| M14 真 CRM 适配 | 沙箱槽 | 5 |

### 阶段 D（Q3–4）

| 模块 | 说明 | 人天 |
|------|------|------|
| M21 | P0 transfer 可提前到 C；A2A 网络 D | 4 |
| M22 | 默认不部署；仅评估 | 2 |
| 管理壳 | Hub Console / 审计台 / 口径运营 | 10 |

---

## 3. 数据设计（增量）

| 库 | 对象 | 说明 |
|----|------|------|
| `uas_hub` | ag_* wm_doc insight operating_task skill_record artifact_meta iam_binding changeset audit_event checkpoint | 经营+控制 |
| `uas_lethe` | lethe 记忆 | **无 FK 到 uas_hub** |
| Neo4j | Graphiti 实体 | ID ≠ `an-*` |
| Temporal | workflow | 不存责任图 |
| MinIO | 制品字节 | sha256 |
| 仓 | Cube 上游 | 只读 |

迁移：Alembic 只管 `uas_hub`。Lethe 独立迁移链。

缺口 schema（阶段 A 第一周补）：`insight.schema.json` `operating_task.schema.json` `configs/gate_map.json`。

---

## 4. 接口设计

权威：规格 §4 `hub.*`。新增进程不对外暴露第二套「WorkStudio API」。  
错误码目录规格 §4.5，explain 必须覆盖。  
MCP 工具名 = `cs.{domain}.{action}`。

跨团队契约：WorkStudio 团队只消费 `hub/v1` + SSE；零件团队只实现 Port，不改信封。

---

## 5. 非功能

| 项 | 目标 |
|----|------|
| pack.open p95 | <2s（含 Cube 水合或 stale 路径） |
| 门禁 | 无 I/O 的步骤 0–5 p99 <20ms |
| 安全 | OIDC、租户、密钥 KMS、剖面服务端强制 |
| 可观测 | OTel trace=`correlation_id`；审计≠KPI |

---

## 6. 测试策略

| 层 | 范围 |
|----|------|
| 单元 | PolicyChain 序、状态机、schema |
| 契约 | `harness/invariants` 扩展：场景写拒绝、Task 源节点、Lethe 隔离、Registry↔MCP 名 |
| 集成 | Compose：Hub+Temporal+Mock 连接器（阶段 B） |
| E2E | 规格 A1–A12 衡川样例 |
| 性能 | 阶段 C 再测 Cube 水合批量 |

TDD 纪律：先红后绿；每模块需求卡「TDD 先写」列为 DoD 入口。

---

## 7. 发布与回滚

- P0：Docker Compose 实验室；无 K8s 前置  
- 灰度：租户开关 Registry 启用  
- 回滚：Law/口径/权限经 ChangeSet 回滚指针；Workflow 不回滚已合法 SoR 写（除非 operation 声明补偿 cs）

---

## 8. 风险

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| 内环再引入第三套框架 | 中 | 高 | ADR-SEL-002；CI 搜 httpx CRM |
| Graphiti 运维 | 中 | 中 | P0 可延迟接地用夹具，接口名冻结 |
| Cube 未就绪 | 中 | 中 | YAML/SQL 替身，`cs.metric.query` 名冻结 |
| 范围膨胀到管理壳 | 高 | 中 | 阶段 A 不做 Console，只做门禁 |

---

## 9. 质量门禁（进入开发）

DoR（程序）：
- [x] 产品 PRD 与 24 模块需求卡
- [x] ADR-SEL 回写 harness
- [x] 模块设计与规格交叉引用
- [ ] 三 Amigos 对本文件阶段 A 表签字（人工）

DoD（每个模块）：见各 `REQ-UAS-M*.req.md`。

---

## 10. 阶段 A 落地（sprint-002）

| 产物 | 路径 |
|------|------|
| Hub 领域内核 | `services/hub-api/uas_hub/` |
| 单测 | `python scripts/validate_uas_aios_phase_a.py` |
| 场景夹具 | `python scripts/export_hub_pack_open.py` → `projects/aios-workstudio/demo/hub-pack-open.fixture.js` |
| Demo | `projects/aios-workstudio/demo/index.html` 渲染 gate 节点；scene 写走 explain |

下一切片：本机 `docker compose -f deploy/compose/docker-compose.yml up` 后接 Temporal SDK Worker（I-06 live）；Postgres 存图；schema codegen 漂移 CI。

---

## 11. 全局协议（Π）

权威：`configs/protocol/KERNEL.yaml` · `configs/protocol/registry.json` · `services/hub-api/uas_hub/ports.py`。

Hub 经 Port 访问零件；夹具在 `uas_hub/adapters/`。一线禁词与判定序写在注册表根上。切片任务只带本模块 verbs + 红灯测试。




