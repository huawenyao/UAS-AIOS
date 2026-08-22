# T1 · Capability Hub 详细设计

> 能力后台。WorkStudio **场景态 + 执行态** 共用的编译器与运行时中枢。  
> 服从：ADR-EDH-001/002 · cs.* 目录 · RBAC/ABAC · Skill 协议 · T0 · `T1-场景态与执行态.md`  
> 配套前台：`T1-WorkStudio详细设计.md` · `T1-场景态与执行态.md`  
> 版本：T1.1 · 2026-08-22

---

## 1. 定位

Capability Hub 不是「多一个 Agent 后台」，而是：

> 把知识、能力、循环、权限、产物编译成 **按场景生效的策略剖面**，并持久化世界模型的三种寿命。

WorkStudio 拥有界面与当前对象。Hub 拥有：世界模型、Skill 协议、cs.*、Harness、身份治理、制品、审计、演化。

对标分层：学 Codex 的「应用拥有界面、harness 拥有循环」；学企业规格的 cs.* 与双轨；**不学** 专家人设中台、把知识图谱当世界模型。

```
                    WorkStudio
                      场景态（驾驶舱 / 价值流 / Todo）
                      执行态（Explore / Builder / Runtime）
                                      │  Insight→Task 或 Theme/App/Instance
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│ Capability Hub                                                  │
│  World Model Store     Skill Protocol      Capability Registry  │
│  Harness Broker        Identity & Policy   Artifact Store       │
│  Audit & ChangeSet     Evolution Engine                         │
│  剖面：scene | explore | builder | runtime                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 模块职责

| 模块 | 职责 | 非职责 |
|------|------|--------|
| **World Model Store** | 五维 + ought/is + 法则 Pack；draft/compiled/live 三寿命 | 不存聊天全文当状态 |
| **Skill Protocol** | agentskills.io 兼容；渐进披露；发现 ≠ 执行 | 不做人设商城 |
| **Capability Registry** | `cs.{domain}.{action}` 契约、租户启用、审批级别 | 不把 REST 暴露给模型 |
| **Harness Broker** | 为场景态 DIKW 与三执行循环选剖面 | 不自研第三套循环内核（采购 Codex/Pi 级） |
| **Identity & Policy** | 租户、组织、用户、RBAC/ABAC、双轨、scope | 不在场景里各写一套权限 |
| **Artifact Store** | ThemePack、Blueprint、Release、报告、文件 | 不替代主数据系统 |
| **Audit & ChangeSet** | 调用链、晋升、权限变更、法则回写 | 不做运营看板代替审计 |
| **Evolution Engine** | 驳回/超时/收益 → 建议回写法则 | 禁止静默改生产知识 |

---

## 3. 世界模型三寿命（统一语言的后端）

| 寿命 | 谁写 | 谁读 | 对应场景 | 晋升条件 |
|------|------|------|----------|----------|
| `draft` | Explore 循环 | Builder 分析步 | Explore | 五维齐全 + 反馈通道 |
| `compiled` | Builder 固化进 App 配置 | Runtime 启动时加载 | Builder | invariant 通过 |
| `live` | Runtime 每步读写 | 指挥席 / 演化 | Runtime | 实例运行中 |

同一 `world_model_id` 可有多个寿命版本。Runtime **不得**直接改 compiled；要改法则走 ChangeSet → 新 Release。Explore 改 draft 不影响 live。

字段最小集（与 Studio 原型对齐）：`space` `time` `subjects` `objects` `feedback` `laws[]` `ought` `is` `gates[]`。

缺维 = 未建模 = Promote 失败原因码 `WM_INCOMPLETE`。

---

## 4. 策略剖面（同一 Hub，四套政策）

这是 Hub 的核心机制。禁止为场景/执行态复制多套注册中心。`profile=scene` 只出洞察与 Task，**不写生产**。

| 政策项 | `profile=scene` | `profile=explore` | `profile=builder` | `profile=runtime` |
|--------|-----------------|-------------------|-------------------|-------------------|
| Skill 可见性 | 已装法则 Pack 只读 | 已装 + 市场/外链 **发现** | 蓝图声明的集合 | 实例启用 ∩ 角色授权 |
| Skill 执行 | 禁止 | 无副作用子集 / 沙箱只读 | 生成文件、跑测试、mock | 生产工具 + 沙箱策略 |
| 网络检索 | 关（用已落盘数据） | 允许（租户开关） | 默认关，规格需要时可开 | 默认关，除非 cs 封装 |
| cs.* 读 | 聚合只读 / 脱敏 KPI | 仅 mock 或脱敏样例 | mock + 契约校验 | 真读 + scope_rules |
| cs.* 写 | **拒绝** | **拒绝** | **拒绝**（dry-run 例外） | 按 L1/L2/L3 + G 层 |
| 循环目标 | DIKW 上行、下钻、签发 | 上下文长、可加深、可红队 | 可重复、可验证、缓存稳定 | 低漂移、可中断、可审批暂停 |
| 压缩策略 | 保留 Insight + 五维草稿 | 保留不确定点与信源 | 保留契约字段与失败测试 | 保留 live WM 与审计指针 |
| 默认 track | scene（Above loop） | selfpaw | shared（构建者） | 实例声明 selfpaw\|pipaw |
| 产出落盘 | Insight · Task | ThemePack | Blueprint + Release | Instance 事件 + Artifact |

Harness Broker 在 `thread/start`（或等价）时注入 profile。中途改 profile 必须新开 Thread，避免污染 prompt cache 前缀（Codex 教训）。

---

## 5. Skill 协议：发现与执行分离

用户硬约束：Explore **不限项目已有 Skill**。Hub 必须把「看见」和「动手」拆开。

```
discover  →  preview（读 SKILL.md） →  cite（写入 ThemePack）
                 ↓
            install（入库，Builder 或管理员）
                 ↓
            enable（租户/实例）
                 ↓
            execute（仅 builder 无副作用 或 runtime 授权）
```

状态机：`discovered | previewed | cited | installed | enabled | executed`。  
Explore 最高到 `cited`。Builder `install` 进应用 `knowledge_assets`。Runtime `enable+execute`。

兼容：`SKILL.md` YAML 头进工具描述（渐进披露）；正文按需。同时识别 `AGENTS.md` / `CLAUDE.md` / 法则 Pack 为项目法则，不是 Skill。

未装 Skill 引用必须在 ThemePack `knowledge_used[].installed=false`。缺失该字段视为契约失败。

---

## 6. 能力注册中心（cs.*）

沿用已有目录与命名 `cs.{domain}.{action}`，不另起「WorkStudio API」。

调用链（Runtime）：

```
WorkStudio 动作
  → Hub Policy（profile + track + role）
  → Registry（operation 存在且租户启用）
  → RBAC（role × operation）
  → approval_level L1/L2/L3
  → gates G*
  → scope_rules 注入连接器
  → SystemConnector（密钥不出模型上下文）
  → 审计记录 + 可选 ChangeSet
```

Explore/Builder 若误发写操作：返回 `403 PROFILE_FORBIDS_SIDE_EFFECT`，并在 UI 提示「请 Promote 到 Runtime」。这是可感知的治理，不是静默失败。

Agent 只见语义名与 JSON schema，不见 REST URL、Token、SQL（ADR-002）。

---

## 7. Harness Broker

采购件：Codex core / Pi 级循环（工具、压缩、沙箱、审批暂停、事件流）。  
自有件：profile 注入、WM 读写钩子、cs.* 网关、Skill 状态机、双轨升级。

建议对外仍用 Thread / Turn / Item 语义，便于未来接 app-server；不把 WorkStudio 绑死某一发行版品牌。

三循环差异用 **instructions + tools 集合 + 审批策略** 表达，不要 fork 三份 Agent 代码。工具集合变更 = 新 Thread。

Hooks（确定性，模型不可跳过）：

- Explore：`PrePromote` 检查五维与信源  
- Builder：`PreGenerateAssets` 检查 world_model_analysis；`PreRelease` 跑 invariants  
- Runtime：`PreToolUse` 走 cs 网关；`PostToolUse` 写审计；升级必须 Evidence

Hooks 100% 执行；CLAUDE.md/Skill 只是咨询式。与 Claude Code 的教训对齐。

---

## 8. Identity · 组织 · 权限

复用 `enterprise-tenant-org-api` + `enterprise-rbac-abac-spec`，Runtime 场景是它们的 UX。

| 概念 | 定义 |
|------|------|
| Tenant | 企业隔离边界 |
| Org unit | 部门树，用于 dept / dept_tree scope |
| User | 人；可同时有员工轨与岗位绑定 |
| Role | 授权 operation 集合 |
| Job / Position | 岗位，绑定 compiled WM 与默认实例 |
| Track | `selfpaw` \| `pipaw`，实例级声明 |

判定顺序不变：tenant → role × operation → approval_level → gates → scope_rules → 审计。

Explore 默认 scope=self，允许读本租户脱敏样例。  
Builder 在「应用工作区」scope=project，与生产数据隔离。  
Runtime 用实例 scope；经营写操作无证据不得从 selfpaw 静默升 pipaw（Intent Escalation API）。

权限变更必须 `permissionChangeSet`，禁止后台改 JSON 当发布。

---

## 9. 制品、数据、产物

| 制品 | 所有者场景 | 存储 | 下游 |
|------|------------|------|------|
| Insight / Task | Scene | Artifact Store | 执行态注入 |
| ThemePack | Explore | Artifact Store | Builder 输入 |
| AppBlueprint | Builder | 应用工作区 + Artifact | Release |
| AppRelease | Builder | 不可变制品库 | Runtime 部署 |
| AppInstance | Runtime | 运行时库 | live WM + 事件 |
| Report / File | Runtime/Explore | Artifact | 用户下载；不可当状态源 |
| AuditRecord | 全场景 | 审计链 | 合规 |
| ChangeSet | Builder/Runtime/治理 | 演化库 | 新 Release / 新法则 |

数据平面：主数据仍在业务系统，经 cs.* 访问。Hub 不复制一套 CRM。产物是工作结果，主数据是客体记录，世界模型是对二者的低维编译。三者不可互相冒充。

---

## 10. 演化

来源：Runtime 驳回、改写、审批超时、未接地率、收益指标；Explore 红队发现的法则缺口；Builder 测试失败模式。

流程：信号 → 归因 → ChangeSet（建议）→ 人确认 → 回写法则 Pack 或新 Release → 下次 compiled/live 生效。

禁止：Hermes 式会话内自主改生产 Skill 且无 ChangeSet。复利可以有，必须可审计。

收益步：Evolution Engine 读取实例的 `revenue_feedback`（价值闭环协议待建设项，T1 须留接口，T0 标杆可用短名单接受率代替）。

---

## 11. 对 WorkStudio 的接口（契约级）

前台只调这组语义，不直接调模型或连接器。

```
hub.scene.pack.list | open
hub.scene.insight.list | drill
hub.scene.task.issue | return
hub.exec.open(task_id)
hub.theme.create | update | get | promote
hub.app.normalize | analyze_wm | select_template | design | generate | validate | release
hub.instance.deploy | cycle_step | invoke_cs | list_artifacts | escalate
hub.skill.discover | preview | cite | install | enable
hub.wm.get | patch          # 按寿命；live patch 仅经 cycle_step
hub.policy.explain          # 返回当前 profile 下为何 403
hub.audit.query
hub.org.* / hub.iam.*       # 复用已有企业 API
```

错误码（UI 必须展示人话）：`WM_INCOMPLETE` `PROFILE_FORBIDS_SIDE_EFFECT` `INVARIANT_FAILED` `GATE_BLOCKED` `TRACK_ESCALATION_REQUIRED` `SKILL_NOT_EXECUTABLE_IN_PROFILE` `SCOPE_DENIED`。

`hub.policy.explain` 是治理可感知的关键——用户看见「现在是研究模式，不能发信」，而不是「出错了」。

---

## 12. 与现有仓库的映射（禁止平行建设）

| Hub 模块 | 已有落点 | T1 增量 |
|----------|----------|---------|
| WM Store | `examples/world-model-studio/configs/world_model.json` · `run_cognitive_cycle.py` | 三寿命与 Theme/Instance 绑定 |
| Skill | `.claude/skills/` · agentskills 实践 | discover/cite 状态机 |
| cs.* | `configs/capability_registry.json` · validate 脚本 | profile 拒绝写 |
| IAM | tenant/rbac schemas · `validate_enterprise_policy.py` | Runtime UX |
| Audit | `enterprise-audit-chain-spec.md` | Promote/Release 事件类型 |
| Subapp | `create_sub_uas_app.py` · producer protocol | Builder 场景编排 |
| Invariants | `harness/invariants/run-all.py` | PreRelease Hook |
| Escalation | `intent-escalation-api.md` | Runtime 升级按钮 |

---

## 13. T1 不做

- 不自研新的 Agent 框架替代 Codex/Pi 循环  
- 不把知识图谱查询冒充五维世界模型  
- 不建专家团 SKU 市场作为 Hub 首页  
- 不为 Explore 单独开生产连接器「方便一下」  
- 不在 Hub 内保存明文密钥（SystemConnector 分区）

---

## 14. 验收

- 三剖面矩阵（本文 §4）可被实现为配置，而不是三套服务。  
- Explore 引用未装 Skill 能 cite 不能 execute。  
- Builder validate 失败不能 release。  
- Runtime 跨租户、跨 track 调用被已有 invariant 拒绝。  
- WorkStudio 仅依赖 §11 接口即可走通「问题 → 应用 → 实例」。
