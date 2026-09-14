# UAS-AIOS 模块间集成交互设计

| 项 | 值 |
|----|-----|
| 地位 | **集成交互权威**。回答：模块与模块在每条业务/管理/治理流上「按什么顺序、过什么协议、带什么字段、失败怎么办」。 |
| 与既有文档分工 | [`UAS_AIOS_ARCHITECTURE_SPEC.md`](./UAS_AIOS_ARCHITECTURE_SPEC.md) 定义**接口字段**；[`UAS_AIOS_CLUSTER_PRODUCTIZATION.md`](./UAS_AIOS_CLUSTER_PRODUCTIZATION.md) 定义**协议原则**；本文定义**场景级交互序列与一致性契约**。冲突时：字段以 SPEC 为准，原则以 CLUSTER 为准，序列以本文为准。 |
| 管理后台 | [`UAS_AIOS_ADMIN_CONSOLE_DESIGN.md`](./UAS_AIOS_ADMIN_CONSOLE_DESIGN.md)（治理平台页面与 `hub.ops.*` 详规） |
| 版本 | v1.0 · 2026-09-11 |
| 服从 | 宪章道-4 · ADR-SEL-001/002/003 · ADR-EDH-001/002 |

---

## 0. 读法

每个交互场景（S-xx）给出五件事：**参与模块 → 时序 → 消息明细 → 失败分支 → 一致性与审计锚点**。场景是集成测试与 I-xx 验收的编写依据：一条场景至少对应一条自动化用例。

三组场景：**业务流**（S-01~S-07，使用平面的看见并办成）、**管理流**（S-10~S-14，配置与运维平面的知识变更）、**治理流**（S-20~S-26，控制平面的能力/身份/合规）。

---

## 1. 交互总则

| # | 规则 | 落点 |
|---|------|------|
| R-1 | 三条流分名：控制流（信封/判定）／数据流（切片/证据/任务）／管理流（ChangeSet/启用） | 任何消息必须可归入一条流；跨流即设计错误 |
| R-2 | 公共信封强制：`tenant_id, actor_id, profile, track, correlation_id, idempotency_key, source_node_id?`；`profile` 由入口强制 | CLUSTER §3.0；伪造 profile 作废 |
| R-3 | ID 链不断：`node_id → insight_id → task_id → workflow_id`；`correlation_id` 贯穿一次用户动作的所有模块与审计行 | §5.1 |
| R-4 | 写操作必须幂等键；连接器补偿信号回 Temporal，不在连接器内解释 Law | SPEC §5.4 |
| R-5 | 零件故障 = 降级说明（`stale`、人话、挂起），不是协议变更 | CLUSTER §2.2 |
| R-6 | 一切写配置类操作止于 ChangeSet draft；`decide=confirm` 之前无任何生产副作用 | S-10~S-14 公共尾段 |
| R-7 | 事件是投影不是状态：指挥舱/Console 消费事件，权威仍在各 Store + 审计链 | CLUSTER §2.3 |

---

## 2. 业务流场景（使用平面）

### S-01 看见：作战台打开与水合

**参与**：WorkStudio(M1) → Hub(M6) → 责任图(M2) → Cube(M15) → IAM(M8)

```
1  M1  POST hub.scene.pack.open {position_id, period}
2  M6  判定序 0-3（信封强制 profile=scene、租户、IAM 岗位绑定）
3  M6  读 M2 切片：position_id × period → nodes[]
4  M6  对 nodes[].kpi 批量 cs.metric.query（内部，不经模型）
5  M15 Cube /v1/load → {value, caliber_id, as_of}；失败 → is=缓存, stale=true
6  M6  计算 kpi.status（ought/is 偏差规则），返回 pack
7  M1  渲染今日必办（status=gate 上浮）；事件 pack.opened / kpi.hydrated|stale
```

**失败分支**：Cube 宕机 → pack 正常返回、节点标 `stale`（I-03）；无岗位绑定 → 403 + explain（I-10）；节点缺五维 → 节点标 `WM_INCOMPLETE`，不阻断其他节点。
**一致性**：`kpi.is` 只是投影缓存，权威在 Cube；库内快照带 `as_of`。
**验收**：A1、I-02、I-03、I-10。

### S-02 洞察：接地分析

**参与**：M1 → M6/M5 → M2 → M16(Graphiti) → M15 → M19(LangGraph, explore) → M10

```
1  M1  POST hub.scene.insight.drill {source_node_id}
2  M5  校验节点五维完整；缺 → 422 WM_INCOMPLETE（停）
3  M6  新开 Thread profile=explore（THREAD_PROFILE_IMMUTABLE）
4  M19 inner.turn：kg.search(object_ref) + metric.query(kpi_id)（只读工具集）
5  M19 产出假设 + suggested_cs + evidence_refs[]
6  M5  接地检查：evidence_refs 至少一条 kg|metric 可解析；否 → 422 UNGROUNDED_INSIGHT
7  M10 落 Insight（grounded=true）；事件 insight.grounded
```

**失败分支**：未接地率累计 → Evolution 信号（S-06）；explore 剖面下任何写工具已被 M13 剥离。
**一致性**：Insight 只读引用，不写 SoR；`source_node_id` 进入 ID 链第 2 环。
**验收**：A4、I-04。

### S-03 办成：签发与执行闭环（主路径）

**参与**：M1 → M5/M6 → M10 → M18(Temporal) → M19(runtime) → M13 → M14 → SoR(M23) → M15 → M2 → M11

```
1  M1  POST hub.scene.task.issue {source_node_id, insight_id, assignee, due, cs_write[], evidence_refs[]}
2  M5  校验：cs_write ⊆ 节点 process.cs_write；否 → 422；落 Task(status=issued)；不启工作流
3  M1  POST hub.exec.open {task_id}
4  M6  Temporal.Start(RuntimeCycleWorkflow, args{task_id, source_node_id, profile=runtime, track})
     task.workflow_id 回写；事件 exec.opened
5  WF Activity LoadTaskAndCompiledWm（M3 compiled + M10 Task）
6  WF Activity RunInnerLoop：M19 turn(tool_allowlist ⊆ cs_write)
7  模型提议 cs.visit.schedule → M13 tools/call → M6 判定序全序重走 → M14 Connector 写 SoR
     （写操作带 Idempotency-Key；Connector 返结构化 result_code）
8  WF（approval_level ≥ L2 时插入 S-04）
9  WF Activity PatchLiveWm → M3 live 寿命 PATCH（禁碰 compiled）
10 WF Activity RefreshKpi：cs.metric.query → 更新节点 is（合流）
11 WF Activity WriteAudit → M11 追加（cs.invoked + 全链 correlation_id）
12 M1 SSE 收到完成事件；同一 node_id 再打开已合流（I-11）
```

**失败分支**：见 S-05；审批见 S-04。
**一致性**：步骤 7 之前 Task 为 `running`；步骤 10 成功才 `succeeded`；SoR 写成功而 RefreshKpi 失败 → `succeeded(degraded)` + stale 可见，不回滚合法写。
**验收**：A5、A6、I-05、I-06、I-07、I-11。

### S-04 人在回路：L2/L3 审批

**参与**：M18 → M1(待确认) → M6 → M11

```
1  WF 到达 approval_level≥L2 步骤 → WaitForSignal("approved"|"rejected")，Task=awaiting_approval
2  Hub SSE 推 approval.wait → M1 展示「待你确认」（不见 workflow_id）
3  用户 POST hub.instance.cycle_step {decision} → M6 映射 Temporal Signal
4  approved → WF 继续 S-03 步骤 7+；rejected → Task=returned + Evolution 信号
5  超时（SLA 配置）→ DraftChangeSet(timeout)，不自动通过
```

**一致性**：杀 Worker 后审批等待不丢（Temporal 耐久）；审批行入审计（actor、decision、耗时）。
**验收**：A6、I-06。

### S-05 失败与补偿

| 失败点 | 行为 | 补偿 |
|--------|------|------|
| InnerLoop 超时/异常 | Activity 有限重试（上限内） | 超限 → Task=failed，ChangeSet 信号 |
| InvokeCs Connector 5xx | 幂等重试（仅 idempotent=true） | 重放不双写；最终失败 → result_code 入审计 + failed |
| SoR 已写、RefreshKpi 失败 | 不回滚 SoR（合法写） | 重试 RefreshKpi；标 `succeeded(degraded)`，作战台 stale |
| SoR 已写、业务需撤销 | operation 声明补偿 cs 才允许 | 补偿调用同样走判定序与审计 |
| 模型提议越权工具 | 判定序步骤 3/5 拒绝 | 403 + explain；信号入 Evolution |

**验收**：A5、A6、I-06；连接器幂等重放用例（MODULE M14）。

### S-06 驳回与演化信号

**参与**：M1 → M5 → M12(Evolution) → M4/M7（潜在回写目标）

`task.return` / 审批超时 / 未接地率阈值 / 收益信号 → M12 归因 → `ChangeSet(draft, auto_apply=false, rollback_ref, regression_cases)` → 事件 `changeset.drafted` → 治理台待办（S-26 评审）。**禁止**「模型下次换个说法再写」式会话内自愈。

### S-07 指挥舱合流

**参与**：M1(/command) → M6 → M2（org_cascade 聚合）→ M15（同口径切片）→ 事件投影

指挥舱 = 责任图子树投影 + 同一 Cube 口径，不是另一套报表模型；消费 `cs.invoked / wm.live.patched / kpi.hydrated` 事件做刷新，审计仍是真相源（M11 不可替代）。
**验收**：I-11。

---

## 3. 管理流场景（配置与运维平面）

管理流公共尾段（R-6）：**任何 Console 写操作 → `hub.ops.changeset.submit` → `draft`（applied=false）→ 评审 decide=confirm → 编译/热载 → 生效 → 审计管理事件**。以下场景只写差异段。

### S-10 责任图变更发布

**参与**：Console(B2 块1) → M6(hub.ops) → M2 → M12

```
编辑画布（本地 state，不落库）→ POST ops/graph/validate（五维校验，返回 incomplete[]）
→ POST ops/graph/publish（= changeset.submit 别名，kind=graph）
→ draft → 评审 confirm → 写 ag_* 表 → 下次 pack.open 生效
```

**一致性**：发布前旧图继续服务；incomplete 非空可 submit 但 decide 页必须红显。
**验收**：I-02、I-09。

### S-11 Law Pack 变更

**参与**：Console(法则页) → M6 → M4 → M12 → M3(compiled)

```
ops/law.diff（版本对比）→ changeset.submit(kind=law_pack) → confirm
→ law.compile → 新 compiled WM（draft→compiled 晋升）→ Runtime 下次启动加载
```

**红线**：Runtime 永不 PATCH compiled；会话内改生产知识 = 违规。
**验收**：I-09、MODULE M4。

### S-12 口径发布与状态

**参与**：知识管理员 → git(OSI YAML) → CI（M20 漂移）→ Cube(M15) → Console(口径页)

```
configs/metrics/osi/*.yml 变更 → CI 校验 + validate_capability_registry
→ 编译进 Cube（P0 手工同步）→ ops/caliber.status 可见 fresh/stale
```

**一致性**：`kpi.caliber_id` 引用必须已注册，否则节点水合标 `CALIBER_MISSING`；仓 Semantic View 不作唯一真相。
**验收**：I-03、I-12。

### S-13 时态知识摄入

**参与**：ETL/CRM webhook（服务账号） → M6 hub.kg.ingest_episode → M16 → Console(时态页只读)

```
episode（实体白名单 + object_ref 必填）→ ingest → Graphiti add_episode
→ ops/kg.ingest_status 监视延迟/失败；Console 无 ingest UI、无写 CRM 按钮
```

**红线**：ingest ≠ cs 写；episode id 永不复用 `an-*` 命名空间。
**验收**：I-04。

### S-14 遗忘处置（合规）

**参与**：当事人/SelfPaw → M6 hub.memory.self.forget → M17(Lethe) → M11

```
forget（仅 track=selfpaw 且 scope=self）→ Lethe lexical 清除
→ Ed25519 签名回执 → 审计指针写入经营库（内容不进经营库）
→ Console 遗忘页 ops/memory.receipt.get 可检索
离职作业：批量 forget + 回执归档；责任图/Graphiti/Cube 不动
```

**验收**：I-08、A8。

---

## 4. 治理流场景（控制平面）

### S-20 能力发布（Registry → MCP）

**参与**：平台管理员 → Console(B3) → M7 → CI(M20) → M12 → M13

```
ops/registry.patch（启用/审批级覆盖）→ CI 漂移检测（schema 三处生成对测）
→ changeset.submit → confirm → Registry 热载 → MCP tools/list 变化
→ ops/mcp.preview 按剖面验证可见集
```

**一致性**：Registry 名 ↔ MCP tools/list ↔ Pydantic 三处同源（I-12）；scene 剖面下写工具不可见（I-05）。

### S-21 连接器接入与轮换

**参与**：客户 IT + 平台管理员 → Console(B3) → M14 → KMS

```
1 开槽：connector.slot=sandbox（凭证入 KMS，界面不明文回显）
2 映射：configs/connectors/{id}.map.yml → 沙箱跑幂等/健康检查
3 切槽：slot=prod 经 changeset；审计 ops.connector.rotated
4 轮换：ops/connector.rotate → 旧凭证吊销窗口期双活只读
```

**红线**：密钥不出连接器进程；tool description 无 URL/Token/SQL。

### S-22 岗位绑定（身份进经营）

**参与**：IdP（人） → M8 → Console(B4) → M2

```
OIDC 登录（IdP 只提供人）→ ops/iam.bindings 绑定 user ↔ position_id ↔ org.*
→ 绑定变更 = permissionChangeSet → 生效后 pack.open 可见对应切片
```

**验收**：I-10（无绑定 → 空切片或 403）。

### S-23 双轨升级（SelfPaw → ΠPaw）

**参与**：M1(个人区) → M6 → M8 → M11

```
SelfPaw 发起经营写 → 判定序步骤 3 拒绝：403 TRACK_ESCALATION_REQUIRED
→ 用户附证据发起升级工单（intent-escalation-api）→ ΠPaw 确认
→ 原请求以 track=pipaw 重放（新 correlation_id，引用原 ID）
```

**红线**：升级必须带证据、禁止静默；Lethe 对 ΠPaw 恒 403（A8）。

### S-24 审计检索与合规导出

**参与**：合规官 → Console(B4) → M11

```
ops/audit.search（correlation_id | source_node_id | task_id | cs 名 | 时间段）
→ ops/audit.export（合规包：审计行 + 证据指针 + 回执引用）
```

**红线**：审计追加写、hash 链；指挥舱 KPI 不是审计；导出动作本身入审计。

### S-25 跨岗位转派

**参与**：M1（指挥舱） → M6 hub.task.transfer → M8 → M10 →（P1+ A2A）

```
P0：transfer 改 assignee → 审计 + 通知；source_node_id 与 ID 链不变
P1+：岗位 Agent Card（position_id, cs_allowlist, track=pipaw）→ A2A task send
      → 对端仍进对方 Hub 判定序；A2A 载荷不是身份权威；跨租户默认拒绝
```

### S-26 ChangeSet 评审（治理流汇合点）

**参与**：各管理流产 draft → Console(发布待办) → 评审人 → M12 → 目标（law/release/permission/caliber/graph）

```
list → 打开 diff + impact_scope + regression_cases → 试运行 explain（B1）
→ decide=confirm|reject（无 auto）→ apply：写配置权威 + 触发编译/热载
→ 审计管理事件 ops.changeset.decided；rollback_ref 一键回滚
```

**验收**：I-09；`auto_apply=true` 在任何入口都无法生效。

---

## 5. 状态一致性契约

### 5.1 ID 链（一次「看见并办成」的全链可追溯）

```
an-stage-visit ──drill──► ins-* ──issue──► tsk-* ──exec.open──► workflow_id
     ▲                                                              │
     └──────────── RefreshKpi 合流（同一 node_id） ◄────────────────┘
correlation_id 贯穿全部审计行；task.return/reject 终结链但保留审计。
```

### 5.2 `kpi.is` 三态

| 态 | 权威 | 展示规则 |
|----|------|----------|
| ought | 责任图（ChangeSet 才可改） | 不作缓存 |
| is(fresh) | Cube 查询结果 | 带 `as_of` |
| is(stale) | Hub 缓存 | 必须标 stale，禁止假装实时 |

### 5.3 WM 三寿命流转

`draft`（explore/builder 写）→ 五维齐全+反馈通道 → `compiled`（builder 经 ChangeSet 发布；Runtime 只读加载）→ `live`（仅 cycle_step 钩子 PATCH）。**运行时对 compiled 的 PATCH 恒 422**；live 不回写 compiled。

### 5.4 Task 状态机 × Temporal 映射

| Task | Temporal | 进入条件 |
|------|----------|----------|
| issued | （无工作流） | task.issue 成功 |
| opened/running | Running | exec.open |
| awaiting_approval | WaitForSignal | approval_level ≥ L2 |
| succeeded | Completed | RefreshKpi 成功 |
| succeeded(degraded) | Completed + stale 标记 | SoR 已写、刷新失败 |
| failed | Failed / 重试耗尽 | 见 S-05 |
| returned | Terminated(信号) | 驳回/超时 |

---

## 6. 事件目录（补 CLUSTER §2.3 管理流部分）

业务事件照录 CLUSTER §2.3；管理流事件新增：

| 事件 | 发出 | 消费 | 说明 |
|------|------|------|------|
| `ops.changeset.submitted` | M12 | 发布待办 | 含 kind/diff 摘要 |
| `ops.changeset.decided` | M12 | 审计+通知 | confirm/reject + 评审人 |
| `ops.graph.published` | M2 | 总览 | 责任图版本 +1 |
| `ops.law.compiled` | M4 | 总览 | 新 compiled 可用 |
| `ops.registry.enabled` | M7 | B3 | operation 启用变化 |
| `ops.connector.rotated` | M14 | B3+合规 | 不含密钥材料 |
| `ops.iam.binding_changed` | M8 | B4 | 岗位绑定变更 |
| `ops.runtime.retried` | M18 封装 | B5 | 精确续跑记录 |
| `memory.forgotten` | M17 | B4 合规 | 回执 id |

所有 `ops.*` 事件与业务 `cs.invoked` 同链不同类型，检索可分流。

---

## 7. 集成验收映射（场景 ↔ I-xx ↔ A-xx）

| 场景 | 集成验收（CLUSTER §6） | 产品验收（SPEC §10） |
|------|------------------------|----------------------|
| S-01 | I-01, I-02, I-03, I-10 | A1 |
| S-02 | I-04 | A4 |
| S-03 | I-05, I-06, I-07, I-11, I-12 | A5 |
| S-04 | I-06 | A6 |
| S-05 | I-06 | A5/A6 |
| S-06 | I-09 | — |
| S-07 | I-11 | — |
| S-10/S-11 | I-02, I-09 | A10 |
| S-12 | I-03, I-12 | — |
| S-13 | I-04 | — |
| S-14 | I-08 | A8 |
| S-20 | I-05, I-12 | A2/A9 |
| S-21 | （连接器幂等用例） | — |
| S-22 | I-10 | A11 |
| S-23 | I-08 | A7 |
| S-25 | — | （P1 A2A 补充） |
| S-26 | I-09 | — |

每条 S 场景 ⇒ `services/hub-api/tests/` 或 `harness/invariants/` 至少一条自动化用例；无自动化 = 集成未完成。

---

## 8. 与已有文档的关系

| 文档 | 回答 | 冲突时 |
|------|------|--------|
| **本文** | 场景级交互序列、失败分支、一致性契约 | — |
| SPEC | 接口字段、错误码、WBS | 字段以 SPEC 为准 |
| CLUSTER | 三平面、八协议原则 | 原则以 CLUSTER 为准 |
| MODULE_DESIGN | 模块内部方案 | 内部以 MODULE 为准 |
| ADMIN_CONSOLE_DESIGN | 管理后台页面与 ops 详规 | 页面以 ADMIN 为准 |

争议时：德压过术；任何「为了交互方便」而绕过判定序、暴露密钥、合并三条流的设计一律否决。
