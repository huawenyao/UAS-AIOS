# T1 · WorkStudio 详细设计

> 用户前台。Explore / Builder / Runtime = **AI 任务执行态**。  
> 用户首页是场景态，见 `T1-场景态与执行态.md`。  
> 服从：`T0产品定义.md` · `docs/AI_PRODUCT_CHARTER.md` · ADR-EDH-001/002  
> 配套后台：`T1-CapabilityHub详细设计.md`  
> 可交互 Demo：`demo/index.html`（浏览器直接打开）  
> 版本：T1.1 · 2026-08-22

---

## 1. 定位

WorkStudio 是企业用户面对的**唯一工作台壳**。它不拥有循环、权限、世界模型，只拥有：

- 当前工作对象
- 场景模式（Explore / Builder / Runtime）
- 证据、环位、晋升动作的呈现

循环、Skill 协议、cs.*、租户权限、审计在 Capability Hub。界面告诉 Agent 用户正在看什么——对齐 Codex Relay，而不是空白对话框首页。

**禁止**：按「日常办公 / PPT / 代码 / 设计」切 Tab（那是巨头面积战）。  
**必须**：按认知实践阶段切场景，并用 **Promote** 串成一条流。

```
┌─────────────────────────────────────────────────────────────┐
│ WorkStudio Shell                                            │
│  [Explore] [Builder] [Runtime]     对象: Theme|App|Instance │
│  五维条  谁/对谁/客体/时间/反馈      环位 草稿|要批|禁止     │
├───────────────┬─────────────────────────────────────────────┤
│ 对象树 / 阶段 │ 主画布（本场景的低维结构，不是聊天墙）        │
│               │ 证据盒 · 不确定点 · 建议 · 门禁              │
└───────────────┴─────────────────────────────────────────────┘
```

对话是手段，挂在对象上，不作为信息架构的根。

---

## 2. 三场景总表

| | Explore 探索研究 | Builder 应用化构建 | Runtime 运行治理 |
|--|------------------|--------------------|------------------|
| **用户要完成的工作** | 把问题做成可编译的主题方案 | 按 spec harness 把方案做成可运行应用 | 在权限内跑应用、管数据/产物/人 |
| **一级对象** | `ThemePack` | `AppBlueprint` → `AppRelease` | `AppInstance` |
| **闭环位置** | 输入 → 模拟 → 生成 | 交互 → 进化（知识固化） | 输出 → 收益 |
| **方法论** | loop-thinking-enhanced / 五铰链 / domain 分析 | subapp 生产协议 + reqharness 七阶段 | 认知循环 7 步读写 live WM |
| **Skill 策略** | **不限已安装**；可检索、试用、引用未入库方法 | 将选用知识**打包进应用**；未过契约不得入库 | **仅**启用且授权的 Skill / cs.* |
| **cs.* 写** | 禁止 | 禁止（可 mock / dry-run） | 允许，走 Hub 门禁 |
| **默认环位** | On loop · G0–G1 | In the loop · 质量门禁 | In the loop · G0–G6 |
| **成功** | 五维可指认 + 证据 + 不确定点显式 | invariant 全过 + 输出契约完备 | 岗位主体接受产物 + 审计完整 |
| **失败** | 把检索结果当事实；直接去调生产 | 一句话生成跳过世界模型分析 | 聊天历史当业务状态；静默越权 |

---

## 3. 场景 A · Explore（探索研究）

### 3.1 产品假设

用户面对的问题 **还没有** 现成 Skill/应用能诚实覆盖。若逼他先装专家，就会得到 WorkBuddy 式短链初稿，并丢失判断过程。

Explore 的竞争力：按**解决问题方法论**搜索、研究、构建主题方案。已有 Skill 只是可选工具，不是边界。

### 3.2 入口

- 自然语言问题 / 业务议题（先澄清意图，禁止原话当任务名）
- 或从 Runtime 异常 / 驳回一键「升级为研究」
- 或导入材料（纪要、数据、竞品页）作为 is 侧事实

不提供「专家市场首页」作为本场景默认。

### 3.3 主路径（与 loop-thinking-enhanced 同构）

```
Phase 0  任务规格     目标/场景/成功标准/约束/利益相关者
Phase 1  信息搜集     检索 · 引用 · 未装 Skill 发现 · 信源分级
Phase 2  五维分析     道法势术器 + 主客体 + 张力 + 动态加深
Phase 3  主题方案     ThemePack：多方案对冲 + 推荐下一步
```

动态智能投放（场景内路由，不站队 7 分钟 vs 41 分钟）：

| 信号 | 路径 |
|------|------|
| 目标清晰、低风险、已有高质量 Theme | 快走：规格 + 短检索 + 一页方案 |
| 目标模糊或高不确定性 | 加深：苏格拉底澄清 → 下钻 → 红队 |
| 高影响（对人/钱/合规） | 强制：不确定点、单一信源、未授权数据一律显式 |

### 3.4 工具面（Hub：profile=explore）

允许：网络检索与抓取（租户可关）、文档解析、方法论 Pack、Skill **发现与只读试用**、世界模型草稿读写、子研究（隔离上下文）。  
禁止：cs.* 写、发邮件、改权限、发布 App、把试用 Skill 的副作用落到生产数据。

未安装 Skill 的处理：可 `preview`（读 SKILL.md 正文）、可 `cite`（写入 ThemePack 引用），不可 `execute` 带副作用部分。要执行副作用，必须 Promote 到 Builder 入库或 Runtime 授权后。

### 3.5 一级对象：ThemePack

```yaml
theme_id: thm-...
status: draft | reviewed | promoted | discarded
problem:
  goal: ...
  constraints: [...]
  success_criteria: [...]
  stakeholders: [...]
world_model_draft:          # 五维，缺一不可晋升
  space: ...
  time: ...
  subjects: [...]
  objects: [...]
  feedback: [...]
ought_vs_is:
  ought: ...
  is: ...
  gap: ...
methodology:
  pack: loop-thinking-enhanced | five-hinges | domain-builder
  depth: fast | deep | verify
evidence: [{source, captured_at, reliability, excerpt}]
uncertainties: [{claim, why_unverified, ask}]
options: [{id, summary, risks, cost}]
recommendation:
  next: stay_explore | promote_builder | discard
  why: ...
knowledge_used: [{type: skill|web|law|conversation, id, installed: bool}]
gates: []                    # Explore 不产出生产门禁，只产出研究门禁
```

UI 首屏：问题一句话、五维条、ought/is 对冲、推荐下一步。展开：证据、检索轨迹、未采用方案。再展开：原始材料。禁止把 Agent 日志作首屏。

### 3.6 与 T0 输出结构对齐

每轮结束必须能渲染：意图理解 · 所用知识（含「未安装仍引用」）· 证据 · 不确定点 · 建议 · 门禁（此处为研究门禁：信源不足则禁止 Promote）· 回滚（丢弃 Theme / 回退 Phase）。

---

## 4. 场景 B · Builder（AI 能力应用化）

### 4.1 产品假设

组织要的不是又一次精彩研究，而是 **下次换人也能跑、改法则即改行为** 的应用。Builder 把 ThemePack（或已有需求）编译为 UAS subapp。

「应用化」= 知识即配置 + spec harness 门禁，不是生成一堆页面。

### 4.2 入口

- Promote：合格 ThemePack（五维齐全、成功标准可测、至少一条反馈通道）
- 已有 `harness/requirements/*.req.md` 或用户粘贴需求（仍须补 world_model_analysis，禁止跳过）
- 从 Runtime 的演化建议「固化为应用版本」

### 4.3 主路径（两条协议必须同时满足）

**Subapp 生产协议（构建语义）**

1. intent_normalization  
2. world_model_analysis  
3. template_selection  
4. blueprint_design（须符合 subapp_output_contract）  
5. asset_generation  
6. validate（runtime validate + invariants）  
7. register（写入 Hub 应用目录，**未授权不启动实例**）

**reqharness 七阶段（质量语义）**

头脑风暴 → 规格 → 详细计划 → TDD/验收用例 → 实现 → 审查 → 交付  

阶段门禁未过则阻断，禁止「先生成再补契约」。

映射：生产协议 1–4 ≈ 规格+计划；5–6 ≈ 实现+验证；7 ≈ 交付。头脑风暴若已在 Explore 完成，Builder 显示为已满足的上游门禁，可回溯不可删除历史。

### 4.4 工具面（Hub：profile=builder）

允许：读写应用工作区、生成 configs/skills/tests、调用 mock cs.*、跑 `harness/invariants`、选择模板（uas-subapp / selfpaw-swarm / triadic）。  
禁止：对生产租户 cs.* 写；把未过 validate 的目录标记为可运行；跳过 governance_controls / evolution_loop 字段。

ADR-002 在本场景的体验：Agent 只能把 cs.* **绑定进蓝图**，执行发生在 Runtime。

### 4.5 一级对象：AppBlueprint / AppRelease

Blueprint 必填（输出契约）：

- `topic` `intent_model` `knowledge_assets` `agent_fabric` `governance_controls` `evolution_loop`
- 另必填：`world_model_analysis`、`source_theme_id`（可空但须声明来源）、`cs_bindings[]`、`template_id`

AppRelease = Blueprint + `invariant_report` + `content_hash` + `version`。  
没有 invariant 报告的 Release 不能 Promote 到 Runtime。

### 4.6 Builder 画布（降维）

首屏只问四件事：

1. 这个应用让哪个岗位、对哪个客体、发生什么状态变化？  
2. 用哪套法则 Pack / Skill（已打包清单）？  
3. 哪些动作是 cs.*，审批级别 L1/L2/L3？  
4. 现在过了哪些门禁，下一步卡在哪？

代码树、生成日志默认折叠。这是道-3。

### 4.7 DoR / DoD

**进入 Builder（DoR）**：ThemePack 五维齐全，或需求含 goal/constraints/audience/success_metrics。  
**离开 Builder（DoD）**：输出契约字段全；至少一条 invariant 套件跑过；治理含审计与人检查点；演化含反馈通道；双轨 scope 声明。

---

## 5. 场景 C · Runtime（运行环境）

### 5.1 产品假设

应用只有在 **组织、权限、数据、产物、审计** 里跑，才算产品。Runtime 是经营闭环所在，不是「聊天里再跑一遍」。

### 5.2 入口

- 从 AppRelease 部署实例（选租户、岗位、数据 scope）
- 员工从岗位工作对象进入（候选人/单据/工单），不从「选一个 Agent」进入
- 指挥席从例外队列进入（超时、门禁拒绝、未接地率升高）

### 5.3 子域（必须同时有，禁止只做聊天运行）

| 子域 | 用户看见 | Hub 模块 |
|------|----------|----------|
| 运行 | 当前实例、7 步状态、live 五维、建议动作 | Harness profile=runtime · WM live |
| 数据 | 主数据视图、scope 过滤后的记录 | cs.* + scope_rules |
| 产物 | 报告/文件/Theme 引用/ChangeSet | Artifact Store |
| 组织 | 租户、部门、岗位、人 | Identity |
| 权限 | 角色、operation、L1/L2/L3、审批单 | RBAC/ABAC · Gates |
| 审计 | 谁在何时对何客体做了何动作 | Audit Chain |

### 5.4 工具面（Hub：profile=runtime）

允许：经 Hub 调用已授权 cs.*；读写本实例 live WM；写审计；提交升级（Intent Escalation，须带证据）。  
禁止：直连生产库；读取未授权个人记忆到经营轨；G2+ 无回滚声明的动作；用对话覆盖实例状态。

状态在 `database/` 与世界模型，不在聊天记录。对话只是对状态的注释。

### 5.5 一级对象：AppInstance

```yaml
instance_id: ins-...
release_id: rel-...
tenant_id: t-...
product_track: selfpaw | pipaw
scope: self | dept | dept_tree | tenant | project
cycle_state: input|simulate|generate|interact|evolve|output|revenue
world_model_ref: wm-live-...
gates_visible: [草稿|要批|禁止]
```

员工视图 ≠ 指挥席视图（ADR-001）。同一实例，指挥席默认 Above loop 只看例外。

### 5.6 与 T0 价值流

T0 同时只深做 **一条** 岗位流作为 Runtime 标杆 App（默认招聘短名单 / World Model Studio）。三场景壳先通用；标杆 App 用来证明「过关」可感知。禁止 T1 同时铺销售+客服+招聘三套 Runtime 皮肤。

---

## 6. 场景切换与 Promote

| 动作 | 前置 | 结果 | 失败时 |
|------|------|------|--------|
| Explore → Builder | ThemePack 五维+成功标准+反馈通道 | 创建 Blueprint，source_theme_id 绑定 | 列出缺失维/未接地项 |
| Builder → Runtime | AppRelease invariant 全过 | 创建 Instance，选租户与 scope | 展示失败 invariant |
| Runtime → Explore | 用户标记「法则不够/事实冲突」 | 新 ThemePack，引用 instance 证据 | 无 |
| Runtime → Builder | 演化建议被接受 | 新 Blueprint 版本 | 须走 ChangeSet，禁静默改生产知识 |

Promote 是主按钮。三个场景可以并列打开，但对象链必须可追溯，禁止复制粘贴聊天当交接。

---

## 7. 信息架构（Shell）

持久区（三场景共用）：租户切换、场景、当前对象、五维条、环位、证据盒入口、个人/经营轨徽章。  
可变区：该场景画布。  
折叠区：轨迹、原始材料、Hub 调试。

空状态：

- Explore：问「要过关的问题是什么？」  
- Builder：问「把哪个 Theme 编译成应用？」  
- Runtime：问「哪个岗位实例现在卡住？」  

不允许三个空状态都是大输入框占满首屏。

---

## 8. 体验不变式（场景级）

1. 任何场景首屏能回答五维，否则未建模。  
2. Explore 引用未安装 Skill 必须标 `installed: false`。  
3. Builder 无世界模型分析不得生成资产。  
4. Runtime 任何写操作可在审计链反查到 actor、track、gate。  
5. 不确定点在 Explore 是一等公民；到 Runtime 若仍未接地，不得进入建议（INV-05）。

---

## 9. T1 范围 / 非目标

**做**：Shell + 三场景对象模型 + Promote 契约 + 与 Hub 策略剖面的接口。招聘短名单作为 Runtime 示例实例。  
**不做**：专家团市场、多内容类型工作台、Explore 直接发生产邮件、Builder 一键无门禁上线。

## 10. 验收（T1 设计完成的定义）

- 产品/设计评审能用本文件走完「一个模糊问题 → Theme → App → Instance → 审计」而不补充口头架构。  
- 每场景有禁止清单，且能指出 Hub 哪个剖面执行该禁止。  
- 与 `T1-CapabilityHub详细设计.md` 的对象名、状态机一致。
