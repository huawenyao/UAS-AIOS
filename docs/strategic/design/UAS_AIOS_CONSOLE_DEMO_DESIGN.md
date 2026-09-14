# UAS-AIOS Console Demo 设计（治理平面 + 运维平面）

| 项 | 值 |
|----|-----|
| 地位 | **Suite B 管理壳（治理/运维平面）离线 Demo 的设计权威**。使用平面复用已有 WorkStudio demo（`projects/aios-workstudio/demo/`），本文不重复设计。 |
| 实现落点 | `projects/aios-workstudio/Console/demo/`（纯 fixture + sessionStorage，模拟 `hub.ops.*`，无后端依赖） |
| 一致性约束 | **Console 的每一项管理能力必须能指回底层架构模块（M2-M24）；每个可运营模块必须有管理入口**。双向一致，以 §2 矩阵为判据。 |
| 上游权威 | 页面与角色纪律服从 [`UAS_AIOS_ADMIN_CONSOLE_DESIGN.md`](./UAS_AIOS_ADMIN_CONSOLE_DESIGN.md)；交互序列服从 [`UAS_AIOS_INTEGRATION_DESIGN.md`](./UAS_AIOS_INTEGRATION_DESIGN.md)；字段以 [`UAS_AIOS_ARCHITECTURE_SPEC.md`](./UAS_AIOS_ARCHITECTURE_SPEC.md) 为准 |
| 版本 | v1.0 · 2026-09-11 |

---

## 1. 设计总则

### 1.1 三平面 Demo 分工

| 平面 | Demo | 状态 |
|------|------|------|
| 使用平面（套件 A） | `projects/aios-workstudio/demo/`（WorkStudio LTC 作战台） | 已有，**复用不改** |
| 治理平面（B4） | `Console/demo/` 新增 4 页：audit / dualtrack / memory / evolution | 本文设计 |
| 运维平面（B1/B2/B3/B5） | `Console/demo/` 现有 8 页 + 新增 4 页：automation / caliber / workflows / wm | 本文设计 |

### 1.2 Demo 三条铁律

1. **ChangeSet 是唯一写通道**：所有 CRUD 不直接生效，一律 `submitChangeSet` → `#/publish` 人工确认 → `applied=true`。auto_apply 永久 OFF。
2. **自动化 = 辅助而非静默**：自动化运营作业只产出**发现（findings）、建议、处置草稿**；生效必须人工确认。Demo 中任何"一键"按钮的落点都是 ChangeSet / 处置单 / 审批单，不是直接改状态。
3. **红线可演示**：scene 禁写、双轨不混权（ΠPaw 读 Lethe 恒 403）、live/compiled 不可改、密钥不出明文、遗忘回执可检索——红线行为在 Demo 中以 403/disabled/toast 形式可复现。

### 1.3 两类管理场景的定义

| 类型 | 定义 | 在 Demo 中的形态 |
|------|------|------------------|
| **后台自动化运营（AU）** | 系统按策略周期巡检/检测/聚合，产出发现与建议；人只做确认 | `#/automation` 作业中心 + 各页内的作业结果卡 |
| **辅助 CRUD（CR）** | 人对业务对象（本体/法则/口径/绑定/目录等）的增改查，全程草稿 + ChangeSet | 各页表单/表格/编辑抽屉 |

---

## 2. 平面-模块-页面双向一致性矩阵（核心判据）

> 方向一：每个可运营模块 → 管理入口。方向二：每个 Console 能力 → 底层模块。✔=现有页，✚=本次新增页。

| 模块 | 平面 | 管理入口（页面） | 自动化运营（AU） | 辅助 CRUD（CR） |
|------|------|------------------|------------------|------------------|
| M2 责任图 | 运维 · 本体 | ✔ `#/ontology` | AU-06 五件套校验巡检 | CR-01 节点五件套编辑 → ChangeSet |
| M3 世界模型 | 运维 · 本体 | ✚ `#/wm` | AU-07 WM 漂移扫描 | CR-02 draft 条目编辑 → 编译申请 |
| M4 Law Pack | 治理 | ✔ `#/govern` + ✚ `#/evolution` | AU-08 版本冲突自动检测 | CR-03 条文修订草案 → ChangeSet |
| M6 Hub 控制面 | 控制 | ✔ `#/control` / `#/integrate` | （健康指标在 overview） | CR 套件启停 → ChangeSet（现有） |
| M7 Registry | 控制 | ✔ `#/mesh` | AU-09 Schema 漂移巡检（现有夹具联动） | CR approval_level / 启用 → ChangeSet（现有） |
| M8 IAM 双轨 | 治理 | ✚ `#/dualtrack` | AU-02 双轨未升级引用扫描 | CR-04 岗位绑定（人↔角色↔节点）→ ChangeSet |
| M11 Audit | 治理 | ✚ `#/audit` | AU-01 审计异常模式巡检 | CR-05 检索/导出（只读；导出自审） |
| M12 Evolution | 治理 | ✚ `#/evolution` | AU-08 信号聚合 + 回归自动执行 | CR-03 草案评审通过/驳回 |
| M13 MCP Gateway | 控制 | ✔ `#/mesh`（工具过滤） | — | —（只读演示 list≠call） |
| M14 Connector | 运维 | ✔ `#/mesh`（槽位） | AU-04 健康巡检 → 降级建议 | CR 槽位切换 / 轮换 → ChangeSet（现有） |
| M15 Cube+OSI 口径 | 运维 | ✚ `#/caliber` | AU-03 stale 巡检 + 重跑建议 | CR-06 口径草稿编辑 → ChangeSet |
| M16 Graphiti | 运维 | ✔ `#/run`（KG 只读） | AU-05 ingest lag 检测 | CR-07 实体白名单编辑 → ChangeSet |
| M17 Lethe 记忆 | 治理 | ✚ `#/memory` | AU-10 离职批量遗忘作业 | CR-08 遗忘申请处置 → 回执 |
| M18 Temporal | 运维 | ✚ `#/workflows` | AU-11 卡点 workflow 巡检 | CR-09 信号重发 / 催办（L3 停留） |
| M19 LangGraph 内环 | 运维 | ✚ `#/workflows`（内环面板） | cycle_step 失败率统计 | —（只读观测） |
| M24 Broker | 运维 | ✔ `#/run`（模型路由） | AU-12 配额监控 → 降档建议 | CR 路由模型/rpm → ChangeSet（现有） |
| M22 Utopia | 运维 | 默认不部署（开关位，只读） | — | — |
| M1/M5/套件 A | 使用平面 | WorkStudio demo（不在本壳） | — | — |

**一致性校验规则**：新增任何 Console 页面/按钮时，必须能填入本表一行（模块 + AU/CR 至少一项）；填不进 = 该能力越过了底层模块，拒绝实现。

---

## 3. 自动化运营场景（AU）

> 统一形态：`作业定义（schedule/策略）→ 运行 → findings → 人工处置（ChangeSet/处置单/审批）→ 审计`。**Demo 中"运行"为夹具驱动**， findings 预置但按状态过滤展示。

| # | 作业 | 模块 | 业务对象 | 自动化逻辑 | 人工介入点 | Demo 演示点 |
|---|------|------|----------|-----------|-----------|-------------|
| AU-01 | 审计异常巡检 | M11 | 审计事件链 | 周期扫描：连续 403、跨租户尝试、scene 写尝试、ops 高频失败 | 确认生成处置单 | `#/audit` 异常面板 + 模式高亮 |
| AU-02 | 双轨未升级扫描 | M8/M17 | 岗位绑定 + 记忆引用 | 扫描 ΠPaw 证据引用了未确认升级的 SelfPaw 记忆 | 逐条通过/驳回升级请求 | `#/dualtrack` 扫描结果卡 |
| AU-03 | 口径 stale 巡检 | M15 | caliber + kpi.is | ought 超刷新窗未回填 → stale 清单 + 重跑建议 | 确认重跑（ChangeSet） | `#/caliber` stale 卡 + 状态徽标 |
| AU-04 | 连接器健康巡检 | M14 | connector 调用指标 | 失败率/延迟超阈 → 建议切 sandbox（不自动切） | 一键转 ChangeSet | `#/automation` + `#/mesh` 联动 |
| AU-05 | KG ingest lag 检测 | M16 | episode 摄入 | lag 超阈 + 失败原因聚类（WM_INCOMPLETE/schema drift） | 转本体修复任务 | `#/run` 现有卡 + automation 汇总 |
| AU-06 | 责任图五件套巡检 | M2 | ag_node | 周期全量校验（WM 五维 + caliber） | 修复草稿 → ChangeSet | `#/ontology` 现有校验 + 巡检历史 |
| AU-07 | WM 漂移扫描 | M3 | wm_doc live | live WM 与责任图边冲突检测 | 修订 draft → 编译申请 | `#/wm` 漂移卡 |
| AU-08 | 演化信号聚合 + 回归 | M12/M4 | 信号 / 草案 / CASE | 信号聚合成草案；草案关联回归 CASE 自动执行 | 评审通过/驳回；未过回归禁发布 | `#/evolution`（REGRESSION_NOT_PASSED 演示） |
| AU-09 | Schema 漂移巡检 | M20/M7 | registry↔MCP↔Pydantic | 三处生成一致性比对 | 修复后解锁发布 | `#/overview` 现有夹具（联动阻断发布） |
| AU-10 | 离职批量遗忘作业 | M17 | 记忆域 + 回执 | 按人员批量检索 → 影响预览 → 擦除 → 回执生成 | 合规官确认执行（L3 语义） | `#/memory` 作业卡 + 回执登记簿 |
| AU-11 | 卡点 workflow 巡检 | M18 | workflow instance | L3 审批停留 >60min 清单 | 重发信号/催办 | `#/workflows` 卡点高亮 |
| AU-12 | 模型配额监控 | M24 | 路由用量 | rpm 用量 >80% → 建议降级 cheap 档 | 一键转 ChangeSet（模型路由） | `#/automation` + `#/run` 联动 |

**`#/automation` 自动化运营中心**：全部 AU 作业的汇总驾驶舱——作业表（schedule/last_run/状态灯/findings 数）+ "立即运行"（夹具驱动）+ findings 抽屉 + 一键转 ChangeSet/处置单。页顶常驻原则条：**自动化只产出建议，生效必须人工确认 · auto_apply=OFF**。

---

## 4. 辅助 CRUD 场景（CR）

| # | 对象 | 模块 | 读 | 增/改 | 删 | 通道 | Demo 演示点 |
|---|------|------|----|-------|----|------|-------------|
| CR-01 | 责任节点五件套 | M2 | `#/ontology` 节点卡 | 编辑 owner/caliber/WM 维 → 校验预检 | 停用（软删） | ChangeSet `graph.node.update` | 缺维提交被预检拦截（WM_INCOMPLETE） |
| CR-02 | WM 条目 | M3 | `#/wm` 三寿命列表 | draft 编辑 → 编译申请 | draft 可弃 | ChangeSet `wm.compile` | live 条目点编辑 → COMPILED_IMMUTABLE toast |
| CR-03 | Law Pack 条文 | M4/M12 | `#/evolution` 现行 vs 候选 diff | 草案修订 → 回归 → ChangeSet | 废止走新版本 | ChangeSet `lawpack.promote` | 冲突声明表 + 评审人≠提交人 |
| CR-04 | 岗位绑定 | M8 | `#/dualtrack` 绑定表 | 新增/改派（人↔角色↔节点） | 解绑 | ChangeSet `iam.binding` | 升级请求无证据 → 通过按钮 disabled |
| CR-05 | 审计记录 | M11 | `#/audit` 多条件检索 | —（不可改） | —（不可删） | 只读 + 导出 | 导出动作自审 toast + hash 链片段展示 |
| CR-06 | 口径定义 | M15 | `#/caliber` 列表 + YAML 预览 | 草稿编辑 OSI YAML → 校验 → ChangeSet | 废弃（状态位） | ChangeSet `caliber.publish` | live 口径直接改 → COMPILED_IMMUTABLE |
| CR-07 | KG 实体白名单 | M16 | `#/run` 摄入状态 | 白名单增删 → ChangeSet | 同左 | ChangeSet `kg.policy` | 摄入失败原因与白名单联动 |
| CR-08 | 遗忘申请 | M17 | `#/memory` 申请队列 | 处置执行 → 回执 | 申请可撤 | 合规处置（非 ChangeSet，L3 审批语义） | 回执登记簿可检索（护栏指标） |

**CRUD 红线**：审计记录无增改删（CR-05）；live/compiled 对象不可原地改（CR-02/06）；双轨升级无证据不可通过（CR-04）；所有改动物理落点均为 pending ChangeSet。

---

## 5. 页面树与路由扩展

```
Console/demo（现有 8 页保留不动）
├── #/overview   总览（现有）
├── #/integrate  集成 · 剖面 dry-run（现有）
├── #/control    管控 · 套件与禁令（现有）
├── #/ontology   本体 · 责任图校验（现有）
├── #/mesh       网格 · 能力/连接器/MCP（现有）
├── #/govern     治理 · Law Pack 冲突（现有）
├── #/run        运行 · 模型/KG（现有）
├── #/publish    发布 · ChangeSet 队列（现有）
├── 治理平面（新增 4 页）
│   ├── #/audit      审计检索与异常巡检      M11
│   ├── #/dualtrack  双轨权限与升级评审      M8 · M17
│   ├── #/memory     记忆与遗忘处置          M17
│   └── #/evolution  演化信号 · 草案 · 回归   M12 · M4
└── 运维平面（新增 4 页）
    ├── #/automation 自动化运营中心（跨模块作业驾驶舱）
    ├── #/caliber    口径管理               M15
    ├── #/workflows  运行监控（外环+内环）    M18 · M19
    └── #/wm         世界模型管理            M3
```

导航分组：rail 按「治理平面 / 运维平面 / 平台（现有页）」分组展示，角色 `frontline` 维持全锁定。

---

## 6. 夹具数据模型（data.js 新增）

| Fixture | 服务页面 | 关键字段 |
|---------|----------|----------|
| `AUTOMATION_JOBS`（8-12 个作业） | automation + 各页联动卡 | id/name/module/schedule/last_run/status/findings[{severity,summary,action_type,action_ref}] |
| `AUDIT_EVENTS`（15-20 条） | audit | id/ts/actor/type(hub.*\|ops.*)/object/result/error_code/correlation_id/hash_prev |
| `AUDIT_PATTERNS` | audit | 异常模式（连续 403/跨租户/scene 写尝试）→ 关联事件 id |
| `IAM_BINDINGS` | dualtrack | person/role/node_id/track/status |
| `UPGRADE_REQUESTS` | dualtrack | id/from_track/memory_ref/evidence_ref?/status（无证据项演示 disabled） |
| `MEMORY_DOMAINS` + `FORGET_REQUESTS` + `FORGET_RECEIPTS` | memory | 域计数/decay；申请（离职/合规）；回执（可检索） |
| `EVO_SIGNALS` + `EVO_DRAFTS` + `REGRESSION_CASES` | evolution | 信号聚合；草案 diff；CASE 结果（含 fail 演示发布阻断） |
| `CALIBERS` | caliber | key/owner/expr_yaml/status(ought/fresh/stale)/window/last_refresh |
| `WORKFLOW_INSTANCES` + `INNER_LOOP_STATS` | workflows | instance/task/step/wait_minutes/status（含 succeeded(degraded)）；checkpoint/token |
| `WM_ITEMS` | wm | id/type/lifecycle(draft/compiling/live)/node_ref/conflict? |

---

## 7. 演示剧本（5 分钟路径）

1. **#/automation** 开讲：自动化只产出建议 → 运行 `connector_health` → finding「ITSM 失败率 12%」→ 一键转 ChangeSet（不自动切槽）
2. **#/publish** 确认该 ChangeSet → 生效 → 回到 `#/mesh` 看槽位变化
3. **#/dualtrack**：升级请求 A（带证据）通过；请求 B（无证据）按钮 disabled → 双轨扫描卡展示拦截统计
4. **#/memory**：处置一条离职遗忘申请 → 回执生成 → 回执登记簿检索到（护栏=100%）
5. **#/evolution**：草案 `lp-2026.09.0` 回归 CASE 1 条 fail → 发布按钮 disabled（REGRESSION_NOT_PASSED）→ 切夹具 CASE 全绿 → 生成 ChangeSet
6. **#/caliber**：对 live 口径点编辑 → COMPILED_IMMUTABLE；改草稿 → 提交 ChangeSet
7. **#/workflows**：卡点 workflow（L3 停留 95min）→ 重发信号 → toast + 审计记录
8. **#/audit**：检索刚才全部操作（type=ops.* 过滤）→ 导出 → 导出自审 toast 收尾

## 8. 验收（D-xx，对齐 ADMIN_CONSOLE C-xx）

| # | 验收 | 判据 |
|---|------|------|
| D-01 | 模块一致性 | §2 矩阵双向成立；任一新按钮可指回模块行 |
| D-02 | ChangeSet 唯一写通道 | 全部 CRUD 落 pending；`#/publish` 确认后状态才变 |
| D-03 | 自动化不静默生效 | AU 全部 findings 需人工确认；auto_apply=OFF 常驻 |
| D-04 | 红线可复现 | 无证据升级 disabled；live 编辑被拒；frontline 全锁定 |
| D-05 | 遗忘护栏 | 处置→回执→可检索闭环可演示 |
| D-06 | 回归门禁 | CASE fail 时演化发布禁用 |
| D-07 | 审计自审 | 导出/处置动作产生审计 toast 与事件夹具关联 |
| D-08 | 离线可跑 | `python -m http.server` 即可演示；`?reset=1` 复位 |

## 9. 实施边界（Demo 不做什么）

- 不接真实 hub-api / NocoBase / 任何后端；不实现 invoke_cs、kg ingest 写、工作流真实控制
- 不引入新视觉语言：沿用现有 console.css 组件（card/data 表/status-pill/toast/changeset-item）
- 不改动现有 8 页的行为逻辑（仅 PAGES 数组追加与导航分组）
- 零件 UI 只读占位（SRE 逃生维持现有实现）

---

*本设计落地为 `Console/demo/` 代码增量；争议时：Console 是壳，真相在 Hub——Demo 演示的管理能力以底层模块实际能力为上界。*
