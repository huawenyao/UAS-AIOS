# UAS-AIOS 治理平台管理后台设计（Platform Console / B 套件）

| 项 | 值 |
|----|-----|
| 地位 | **管理后台产品化权威**。回答：治理平台卖给谁、页面树长什么样、每页管什么、背后调什么、壳怎么落。 |
| 产品定义 | [`UAS_AIOS_PLATFORM_PRODUCT.md`](./UAS_AIOS_PLATFORM_PRODUCT.md)（三套件/B1-B5/旅程，本文深化其 §8） |
| 集成关系 | [`UAS_AIOS_CLUSTER_PRODUCTIZATION.md`](./UAS_AIOS_CLUSTER_PRODUCTIZATION.md)（管理产品化矩阵，本文落地为页面） |
| 交互序列 | [`UAS_AIOS_INTEGRATION_DESIGN.md`](./UAS_AIOS_INTEGRATION_DESIGN.md)（S-10~S-26 管理流/治理流） |
| 壳实施 | [`2026-09-11-nocobase-console-shell.md`](../superpowers/plans/2026-09-11-nocobase-console-shell.md)（NocoBase 壳 W0-W6，本文为它的产品前置） |
| 版本 | v1.0 · 2026-09-11 |
| 服从 | 宪章道-4 · ADR-EDH-001/002 · 一线菜单不得出现连接器/工作流 ID/Cube 查询语言 |

---

## 0. 一句话

治理平台不是「运维后台」，是 **Platform Console（套件 B）**：让平台管理员、知识管理员、合规官、实施顾问、值班运营**在界面上**完成「谁能调什么、知识怎么改、变更谁批、事后怎么追」，且**每一次写都止于 ChangeSet，每一次查都可审计**。

---

## 1. 角色与纪律

| 角色 | 主区 | 能做什么 | 永远不能 |
|------|------|----------|----------|
| 平台管理员 | B1 控制 / B3 能力 | 租户、剖面矩阵、试运行、目录启用、连接器槽 | 关审计、auto_apply、签经营任务 |
| 知识管理员 | B2 本体 / B5 口径 | 责任图、WM 寿命、Law Pack、口径状态 | 生产写路径、SoR 密钥、直接 UPDATE |
| 合规官 | B4 治理 | 审计检索导出、遗忘回执、双轨抽查、转派记录 | 业务派活、改 compiled |
| 实施顾问 | B2/制品 | Blueprint/Release、模板发布 | 跳过 invariant |
| 值班运营 | B5 运行 | 任务检索、滞留 SLA、精确续跑、摄入监视 | 改 ought、解释 Law |

**纪律**：① 一线账号默认无 `/console`；② 所有写 → ChangeSet draft（R-6）；③ SRE 零件逃生开关默认关、全程审计；④ 每个 403 有人话。

---

## 2. 信息架构（页面树）

```
/console                       Platform Console（NocoBase 壳 + 自定义 Block）
├── /overview                  总览：平面 SLO 健康（门禁延迟/stale/审批滞留/未接地率/403 人话覆盖）
├── /control                   B1 控制中心（平台管理员）
│   ├── /control/tenants       租户与套件开通
│   ├── /control/profiles      剖面矩阵（四剖面 × 读写 × 工具集）
│   ├── /control/simulator     门禁试运行（「若现在点写会怎样」）
│   └── /control/gates         403 分类分布 · 门禁延迟
├── /ontology                  B2 本体工作室（知识管理员）
│   ├── /ontology/graph        责任图投影画布【Block 1 · Cytoscape】
│   ├── /ontology/wm           世界模型三寿命对照【Block 2】
│   └── /ontology/law          Law Pack 版本对比与编译状态
├── /mesh                      B3 能力网格（平台管理员）
│   ├── /mesh/registry         能力目录（启用/审批级/副作用/绿灯）
│   ├── /mesh/mcp              MCP 工具预览（按剖面）
│   ├── /mesh/connectors       连接器槽（沙箱/生产/轮换/健康）
│   └── /mesh/schema           契约漂移检测
├── /governance                B4 治理中心（合规官）
│   ├── /governance/bindings   岗位绑定（人 ↔ position ↔ org.*）
│   ├── /governance/tracks     双轨抽查（升级工单与证据）
│   ├── /governance/skills     Skill 货架漏斗（discover→executed）
│   ├── /governance/artifacts  制品晋升条（Insight→…→Instance）
│   ├── /governance/audit      审计检索 / 合规包导出
│   ├── /governance/forget     遗忘回执检索
│   └── /governance/transfers  转派记录
├── /runtime                   B5 运行与知识运营（值班运营）
│   ├── /runtime/tasks         长任务检索（按 task_id/source_node_id）
│   ├── /runtime/approvals     审批滞留 SLA
│   ├── /runtime/caliber       口径状态（fresh/stale）
│   ├── /runtime/kg            时态摄入监视【Block 3 只读】
│   └── /runtime/models        模型路由（剖面→提供商）
└── /releases                  发布待办：ChangeSet 评审（所有写的汇合点）
```

入口与权限：`/console` 仅运营角色可见；NocoBase role ↔ `X-Ops-Role` 一一映射（§6.3）。

---

## 3. 逐页设计规格

> 格式：角色 · 目标 · 主组件 · 数据列/字段 · 操作 · 空态与错误 · API（hub.ops.*）· 审计。

### 3.0 /overview 总览

- **角色**：全部运营角色（按角色裁剪卡片）
- **主组件**：五张健康卡（使用/控制/运行/口径/合规）+ 发布待办数 + 事件流（最近 20 条 ops.* 与告警）
- **数据**：门禁 p95、stale 节点数、awaiting_approval 滞留 >SLA 数、未接地率（7 日）、遗忘回执可检索率
- **操作**：卡片点击下钻到对应区；无写操作
- **错误态**：某平面数据缺失 → 卡片灰显「数据延迟」，不阻塞其他卡
- **API**：`hub.ops.health.summary`、`hub.ops.changeset.list?status=draft`
- **审计**：只读，无

### 3.1 B1 控制中心

**/control/tenants 租户**
- 列：tenant_id、名称、开通套件（A/B/C）、连接器槽数、责任图版本、最近发布
- 操作：查看详情抽屉（剖面默认值、套件开关变更历史）；**开关套件 = changeset.submit(kind=tenant)**
- API：`hub.ops.tenant.get`、`hub.ops.changeset.submit`

**/control/profiles 剖面矩阵**
- 组件：4 剖面 × 能力族（cs 读/写、Skill、网络检索、记忆）矩阵格
- 每格：当前政策徽标（允许/拒绝/需审）+ 来源（默认/租户覆盖）
- 操作：格内点击 → 差异抽屉 → 修改仅生成 changeset；「恢复默认」同理
- API：`hub.ops.profile.matrix`

**/control/simulator 门禁试运行**（B1 核心卖点）
- 表单：actor（岗位/track）+ 拟调用（cs 名或 hub 接口）+ 剖面 + 输入摘要
- 结果：判定序逐步骤回放（tenant→registry→RBAC→approval→gates→scope），首个拒绝步骤红显 + `explain` 人话与下一步
- 红线：试运行**零副作用**（不调连接器、不落审计以外的任何写）
- API：`hub.ops.policy.explain`（mode=simulate）
- 验收：explain 可用率 100%（有码就有人话）

**/control/gates 403 分类与门禁健康**
- 列：错误码分布（近 24h/7d）、TOP 被拒操作、门禁链路 p50/p95
- 操作：点错误码 → 审计检索跳转（带过滤）
- API：`hub.ops.health.gate`、`hub.ops.audit.search`

### 3.2 B2 本体工作室（对齐 NocoBase 三块计划）

**/ontology/graph 责任图【自定义 Block 1】**
- 组件：Cytoscape 画布 + 四类边投影切换（org_cascade/kpi_split/stage_split/object_drill）+ 五件套校验灯
- 列/卡：node_id、goal 摘要、kpi（ought/is/stale 徽标）、process.cs_write 白名单、缺维红标
- 操作：拖拽/编辑**只改本地 state**；「校验」→ validate；「发布」→ publish（=submit，draft）；compiled 生产图只读
- 空态：无图 → 引导「从模板 ChangeSet 导入」
- API：`hub.ops.graph.get / validate / publish`
- 验收：无 `ops/kg/ingest` 路由、submit 后 `applied=false`

**/ontology/wm 世界模型寿命【Block 2】**
- 组件：draft/compiled/live 三列对照（同 world_model_id）
- 操作：draft 可编辑（经 validate）；compiled 列**只读**（PATCH 恒 422 的按钮级防护：无编辑入口）；live 只读 + 最近 patch 时间
- API：`hub.ops.wm.get`

**/ontology/law Law Pack**
- 组件：条文列表 + 版本 diff 视图 + 冲突显式标记（应当 vs 事实冲突不静默）
- 操作：编辑条文 → `law.diff` 预览 → submit(kind=law_pack)；生效状态（待编译/已编译进 compiled vX）
- API：`hub.ops.law.diff`、`hub.ops.changeset.submit`
- 验收：未审批 changeset 不能 law.compile（I-09）

### 3.3 B3 能力网格

**/mesh/registry 能力目录**
- 列：cs 名、域、approval_level、gates、side_effects、idempotent、agent_visible、租户启用、契约绿灯
- 操作：启用/停用、审批级调整 → 全部 submit(kind=registry)；契约红灯条目禁用发布按钮
- API：`hub.ops.registry.list / patch`、`hub.ops.schema.drift`
- 验收：I-12（与 MCP tools/list 一致）

**/mesh/mcp 工具预览**
- 组件：剖面选择器 × track 选择器 → 该组合下 `tools/list` 实时预览（scene 下写工具应消失）
- 只读；用途是验证过滤正确性
- API：`hub.ops.mcp.preview`

**/mesh/connectors 连接器槽**
- 列：connector_id、SoR 类型、槽（sandbox/prod）、健康、最近轮换、死信数
- 操作：开槽（凭证直入 KMS，表单不回显）、沙箱健康检查、切槽（changeset）、轮换（双活窗口）
- 错误态：健康检查失败 → 红色 + result_code 人话（不暴露厂商错误页）
- API：`hub.ops.connector.list / rotate / slot`
- 红线：密钥永不明文回显；页面截图不含凭证

**/mesh/schema 契约漂移**
- 组件：Registry ↔ MCP ↔ Pydantic 三处对测结果、漂移字段列表
- 操作：跳转 CI 报告；漂移存在时全站发布按钮降级（仅提示，强制在 CI）
- API：`hub.ops.schema.drift`

### 3.4 B4 治理中心（合规官主场）

**/governance/bindings 岗位绑定**
- 列：user（IdP）、position_id、org.* 节点、track 默认、scope、绑定来源、生效时间
- 操作：新增/调整绑定 → permissionChangeSet；「模拟此人视角」→ 试运行跳转（带参数）
- API：`hub.ops.iam.bindings`
- 验收：I-10（无绑定打不开切片）

**/governance/tracks 双轨抽查**
- 列：升级工单（SelfPaw→ΠPaw）列表：申请人、目标操作、证据链、审批人、结论、耗时
- 操作：抽查详情抽屉（证据可解析性检查）；批量导出抽查样本
- 指标：无证据升级 = 0（护栏）
- API：`hub.ops.iam.bindings`、`hub.ops.audit.search(type=escalation)`
- 红线：合规官不能代批业务动作

**/governance/skills Skill 货架**
- 组件：漏斗图（discovered→previewed→cited→installed→enabled→executed）+ 合规报表（explore 剖面 execute 次数应恒 0）
- 列：skill_id、状态、引用制品、安装租户、启用剖面
- 操作：状态流转仅 install/enable 可手动（且走 changeset）；explore→execute 无按钮（状态机硬约束）
- API：`hub.ops.skill.*`

**/governance/artifacts 制品晋升**
- 组件：晋升条（Insight/Task→ThemePack→Blueprint→Release→Instance）+ 每级数量与滞留
- 红线：`kind=file`（报告/PDF）条目禁用「当状态源」操作（UI 无此按钮）
- API：`hub.ops.artifact.*`

**/governance/audit 审计检索/导出**
- 筛选：correlation_id / source_node_id / task_id / cs 名 / actor / track / 时间段 / 结果码
- 视图：调用链时间线（判定序各步骤 + gates_passed + scope）
- 操作：导出合规包（审计行+证据指针+回执引用）；导出动作自身入审计
- API：`hub.ops.audit.search / export`
- 红线：界面无「编辑/删除审计」任何入口（追加写）

**/governance/forget 遗忘回执**
- 列：receipt_id、申请人（脱敏）、forget 范围、签名、归档时间、可验证状态
- 操作：验签重放（只读校验）；离职清库作业进度查看
- API：`hub.ops.memory.receipt.get`
- 验收：回执可检索率 100%（护栏）

**/governance/transfers 转派记录**
- 列：task_id、源岗位→目标岗位、source_node_id、操作人、时间、审计链接
- API：`hub.ops.audit.search(type=task.transfer)`

### 3.5 B5 运行与知识运营

**/runtime/tasks 长任务检索**
- 筛选：task_id / source_node_id / 状态 / 时间段
- 列：状态（含 awaiting_approval 滞留时长）、当前步骤、最近事件
- 操作：失败任务「精确续跑」（`runtime.retry`，不回滚合法 SoR 写）；**不展示 workflow_id**，SRE 逃生另授权
- API：`hub.ops.runtime.task.get / retry`

**/runtime/approvals 审批滞留**
- 列：滞留 >SLA 的 awaiting_approval 任务、等待人、已等时长
- 操作：催办通知（发事件，不代批）；超时策略查看（DraftChangeSet(timeout) 关联）
- API：`hub.ops.runtime.task.get?status=awaiting_approval`

**/runtime/caliber 口径状态**
- 列：kpi_id、caliber_id、fresh/stale、as_of、Cube 健康
- 红线：页面不出现 CubeQL；口径定义变更只指回 git/OSI YAML 流程
- API：`hub.ops.caliber.status`

**/runtime/kg 时态摄入【Block 3 只读】**
- 组件：object_ref 时间线浏览（只读投影）+ 摄入延迟/失败监视
- 红线：无写 CRM 按钮、无 ingest UI（ingest 仅服务账号 ETL）
- API：`hub.ops.kg.search`、`hub.ops.kg.ingest_status`

**/runtime/models 模型路由**
- 列：剖面 → 提供商/模型、限流、token 用量（按 correlation 聚合）
- 操作：路由调整 → changeset；禁用某模型 → changeset
- API：`hub.ops.model.route`（PATCH→changeset）
- 红线：一线菜单永不出现「选模型」

### 3.6 /releases 发布待办（汇合点）

- 列：changeset_id、kind（graph/law_pack/release/permission/caliber/registry/tenant）、提交人、diff 摘要、影响范围、回归 CASE 状态、回滚指针
- 操作：打开评审抽屉（diff + impact_scope + regression_cases + 试运行跳转）→ `decide=confirm|reject`；confirm 后状态跟踪（applied→生效版本）；`rollback` 一键回滚（自身也是 changeset）
- 硬约束：无 auto_apply 开关；未过回归 CASE 的 confirm 按钮禁用
- API：`hub.ops.changeset.list / submit / decide`
- 验收：I-09

---

## 4. 治理工作流（界面级）

### W-1 ChangeSet 评审流

```
任意页写操作 → 本地草稿 → validate（五维/漂移/白名单）
→ submit（draft, applied=false, auto_apply=false）
→ /releases 待办 + 通知评审人
→ 评审抽屉：diff / 影响范围 / 回归 CASE / 试运行
→ decide：confirm → apply（写配置权威 → 编译/热载 → 版本+1 → 事件 ops.*.decided）
         reject → 归档 + 驳回原因（进演化信号）
→ 异常回滚：rollback_ref → 新 changeset（kind=rollback）
```

### W-2 双轨抽查流

每周样本 → /governance/tracks → 证据可解析性逐条核 → 无证据升级工单 → 标记违规 → permissionChangeSet 收紧 → 审计导出留档。

### W-3 遗忘处置流

当事人申请 → SelfPaw 侧 forget → Lethe 清除 + 回执 → /governance/forget 可检索 → 离职作业：批量 forget → 回执归档包 → 合规导出。**全程不触碰**责任图/Graphiti/Cube。

### W-4 能力上线流

新 operation 草案（git PR）→ CI 校验+漂移 → /mesh/registry 预演（mcp.preview 按剖面）→ changeset → confirm → 热载 → /control/simulator 回归「scene 下不可见写工具」。

---

## 5. `hub.ops.*` 接口详规（schema 级）

**公共约束**：前缀 `/hub/v1/ops/`；OIDC Bearer + `X-Tenant-Id` + `X-Ops-Role`；服务端强制 `profile=builder`（忽略伪造）；写接口必须 `Idempotency-Key`；错误体同 SPEC §4 统一格式；全部 ops 调用入审计（`type=ops.*`）。

| 接口 | 方法 | X-Ops-Role | 请求核心字段 | 响应核心字段 |
|------|------|-----------|--------------|--------------|
| `ops.tenant.get` | GET | platform_admin | tenant_id? | tenants[]{套件,版本,槽数} |
| `ops.health.summary` | GET | *（按角色裁剪） | — | planes[]{slo,status} |
| `ops.health.gate` | GET | platform_admin | window | p50/p95, 403_by_code[] |
| `ops.policy.explain` | POST | * | {code?|simulate:{actor,call,profile,input}} | {message,next,trace[]（判定序回放）} |
| `ops.profile.matrix` | GET | platform_admin | tenant_id | matrix[4×能力族]{policy,source} |
| `ops.graph.get` | GET | knowledge_admin | graph_id? | {nodes[](含_incomplete),edges[],profile:"builder"} |
| `ops.graph.validate` | POST | knowledge_admin | {nodes[]} | {incomplete:[{node_id,missing[]}]} |
| `ops.graph.publish` | POST | knowledge_admin | {patch} + Idem | changeset{status:"draft",applied:false} |
| `ops.wm.get` | GET | knowledge_admin | world_model_id | {lifetimes:{draft,compiled,live}} |
| `ops.law.diff` | GET | knowledge_admin | pack_id, from, to | {diff,conflicts[]} |
| `ops.registry.list` | GET | platform_admin | domain? | operations[]{审批级,副作用,绿灯} |
| `ops.registry.patch` | POST | platform_admin | {op,enable?,approval_level?} + Idem | changeset draft |
| `ops.mcp.preview` | GET | platform_admin | {profile,track} | tools[]（该组合可见集） |
| `ops.connector.list` | GET | platform_admin | — | connectors[]{slot,health,dead_letters} |
| `ops.connector.rotate` | POST | platform_admin | {connector_id} + Idem | {rotation_id,window}（无明文） |
| `ops.connector.slot` | POST | platform_admin | {connector_id,slot} + Idem | changeset draft |
| `ops.schema.drift` | GET | platform_admin | — | {drifted:[{op,field}],ci_ref} |
| `ops.iam.bindings` | GET/POST | compliance/platform_admin | {user_id,position_id,org_node,scope} | bindings[] / changeset draft |
| `ops.audit.search` | GET | compliance | {correlation_id?,source_node_id?,task_id?,cs?,actor?,window} | rows[]{全字段} |
| `ops.audit.export` | POST | compliance | 同 search + {format} | {package_ref,audit_id}（导出自审） |
| `ops.changeset.list` | GET | * | {status?,kind?} | changesets[]{diff 摘要,regression,rollback_ref} |
| `ops.changeset.submit` | POST | *（按 kind 限角色） | {kind,patch,evidence_refs[]} + Idem | {changeset_id,status:"draft",applied:false,auto_apply:false} |
| `ops.changeset.decide` | POST | reviewer（≠提交人） | {changeset_id,decision,note} + Idem | {status,applied_version?} |
| `ops.memory.receipt.get` | GET | compliance | {receipt_id?|user_ref?} | receipts[]{signature,archived_at} |
| `ops.runtime.task.get` | GET | sre | {task_id?|source_node_id?|status?} | tasks[]{state,step,wait_age}（无 workflow_id 明文给业务角色） |
| `ops.runtime.retry` | POST | sre | {task_id,from_step} + Idem | {resumed:true,audit_id} |
| `ops.caliber.status` | GET | knowledge_admin/sre | kpi_id? | items[]{caliber_id,stale,as_of} |
| `ops.kg.search` | POST | knowledge_admin | {object_ref?|query,valid_at?} | {facts[],write_path:false} |
| `ops.kg.ingest_status` | GET | sre | — | {lag,failed[]}（**无** ops.kg.ingest 路由） |
| `ops.skill.*`（list/transition） | GET/POST | compliance/platform_admin | {skill_id,to_state} | transition 仅 install/enable 且 changeset |
| `ops.artifact.*`（list/promote） | GET/POST | implementer | {artifact_id,to_kind} | 晋升结果；kind=file 无 promote |
| `ops.model.route` | GET/PATCH | platform_admin | {profile,provider?} | routes[]；PATCH→changeset |

**新增错误码**（补 SPEC §4.5）：`OPS_ROLE_REQUIRED`（403，非运营角色）、`CHANGESET_REVIEWER_CONFLICT`（403，提交人不能自审）、`REGRESSION_NOT_PASSED`（422，回归未过禁止 confirm）、`COMPILED_IMMUTABLE`（422，PATCH compiled）。

---

## 6. NocoBase 壳映射与落地纪律

### 6.1 页面实现方式分布

| 页面 | 实现 | 说明 |
|------|------|------|
| B2 三块（graph/wm/kg） | **自定义 BlockModel**（Cytoscape 等） | 按 nocobase-console-shell 计划 W4-W5 |
| 列表/表单类（registry/connectors/bindings/skills/artifacts/audit/changesets/transfers/tasks/caliber/models） | NocoBase 原生页面编排 + `hubOps.ts` 数据源 | 禁 CollectionBlockModel 存经营对象 |
| 试运行/剖面矩阵/WM 对照/漏斗 | 自定义 Block（轻量） | 表单不足以表达判定序回放 |
| 总览 | NocoBase 页 + 健康卡 Block | 只读 |

### 6.2 壳纪律（与计划文件一致，产品化复述）

- 插件唯一：`@uas/plugin-console`；黑名单：`plugin-workflow*`、`plugin-ai*`、`plugin-mcp-server`（configs/console/deny-plugins.json）
- 禁止 Collection：`ag_node` `ag_graph` `episodes` `kpi_is`（经营对象真相在 Hub，不进 NocoBase 主库）
- 禁止客户端路径：`invoke_cs`、`kg/ingest`
- 发布按钮唯一语义：`changeset.submit`；界面上不存在「直接生效」
- 一线账号无 `/console` 菜单（角色裁剪）

### 6.3 角色映射

| NocoBase role | X-Ops-Role | 可见菜单 |
|---------------|-----------|----------|
| console_platform_admin | platform_admin | control / mesh / releases |
| console_knowledge_admin | knowledge_admin | ontology / runtime-caliber / releases |
| console_compliance | compliance | governance / releases(只读非本人提交) |
| console_implementer | implementer | artifacts / releases |
| console_sre | sre | runtime / overview |

`ops.changeset.decide` 额外校验：评审人 ≠ 提交人（CHANGESET_REVIEWER_CONFLICT）。

### 6.4 与既有计划的对齐

nocobase-console-shell 计划覆盖 **B2 三块 + 壳**（W0-W6）。本文新增页（B1/B3/B4/B5 + overview + releases）按同一壳纪律扩展，建议追加切片：

```
W7  releases 汇合页 + changeset.decide（评审抽屉）
W8  B1 控制三页（tenants/profiles/simulator）
W9  B3 能力三页（registry/mcp/connectors）+ schema 漂移
W10 B4 治理六页（bindings/tracks/skills/artifacts/audit/forget/transfers）
W11 B5 运行四页 + overview 健康卡
W12 全量门禁验收（角色裁剪/黑名单/无明文/无 auto_apply）
```

每片验收同纪律：curl 可测 ops → 壳页面 → 架构测试（无 Collection/无 ingest/无 invoke_cs/无 auto_apply）。

---

## 7. 验收清单（产品化完成定义）

| # | 验收 | 对应 |
|---|------|------|
| C-1 | 一线账号无 /console；运营角色菜单按 §6.3 裁剪 | 纪律 |
| C-2 | 全站无「直接生效」按钮；任意写路径最终落地为 changeset draft | R-6 |
| C-3 | simulator 对 12 个错误码全部返回人话 + 下一步 | SPEC §4.5 |
| C-4 | 密钥/URL/SQL 在任何页面与 tool description 不出现 | ADR-EDH-002 |
| C-5 | 审计导出包含 ID 链全段（node→insight→task→workflow） | S-24 |
| C-6 | 遗忘回执可检索率 100%；导出动作自审 | S-14 |
| C-7 | compiled PATCH 恒 422 且界面无入口 | §3.2 |
| C-8 | decide 提交人≠评审人；回归未过 confirm 禁用 | §3.6 |
| C-9 | scene 剖面 mcp.preview 无写工具 | I-05 |
| C-10 | 无 NocoBase Collection 存经营对象；无 plugin-workflow/ai/mcp | §6.2 |

---

## 8. 与已有文档的关系

| 文档 | 回答 |
|------|------|
| **本文** | 治理平台页面树、逐页规格、工作流、ops 详规、壳映射 |
| PLATFORM_PRODUCT | 三套件定位与 B1-B5 一句话（本文深化其 §8） |
| CLUSTER_PRODUCTIZATION | 管理产品化矩阵（本文落地为页面） |
| INTEGRATION_DESIGN | 管理流/治理流的交互序列（本文是它们的界面落点） |
| nocobase-console-shell 计划 | B2 三块 + 壳的工程实施（本文是其产品前置并扩展 W7-W12） |

争议时：德压过术；运营方便不得把写路径、密钥、零件术语暴露给一线。
