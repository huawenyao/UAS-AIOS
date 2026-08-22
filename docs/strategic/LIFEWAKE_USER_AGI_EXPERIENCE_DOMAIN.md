# LifeWake：SelfPaw User AGI 生命体验域

> **状态**：Architecture Baseline · 2026-07-22  
> **定位**：SelfPaw 的消费体验域（Experience Domain），不是与 User AGI / Business AGI 并列的第三轨  
> **关联**：`UAS-AIOS_Delivery_Form_And_Product_Design.md`、`Enterprise_Digital_Human_Ecosystem_Product_Definition.md`

## 1. 产品边界

UAS-AIOS 保持双轨产品结构：

- **SelfPaw / User AGI**：服务个人目标、认知、关系与生活体验。
- **ΠPaw / Business AGI**：服务组织经营、岗位协作与企业流程。

LifeWake 属于 SelfPaw 下的 **生命体验域**。它把个人世界模型、记忆、关系和授权能力组织成可持续的消费体验，但不复制 SelfPaw Core，也不引入第三种 AGI 轨道或未经体系支持的层级。

```
UAS Kernel（I,K,R,A,S,G,E,Π）
  └─ SelfPaw Core（身份 · 记忆 · 个人世界模型 · Agent · 执行）
       └─ LifeWake Experience Domain Pack
            ├─ 领域本体与体验法则
            ├─ lw.* 领域能力与连接器
            ├─ 体验编排、表达策略与领域门禁
            └─ 具体体验（单人体验 · 关系共创 · 纪念与反馈）
```

关系中的三个层次职责明确：

| 层次 | 稳定职责 | 不承担 |
|------|----------|--------|
| SelfPaw Core | 个人身份、记忆、世界模型、运行时、通用治理与演化接入 | 不写死某种生命体验 |
| LifeWake Domain Pack | 生命体验本体、`lw.*` 能力、体验策略、领域素材与连接器 | 不定义新的产品轨道 |
| 具体体验 | 在明确目的、参与者、同意和仪式上下文中生成一次可感知结果 | 不绕过 Core 或平台协议 |

## 2. Domain Pack 组成

LifeWake Domain Pack 遵循“知识即配置、构建即运行”：

1. **Ontology**：人、关系、记忆、情绪信号、体验产物和反馈。
2. **Constraints**：目的限定、最小必要数据、可撤回同意、多人对等和高敏感场景升级。
3. **Capabilities**：隔离在 `lw.*` 命名空间的体验生成、领域检查、表达和连接器能力。
4. **Experience Recipes**：将意图、上下文、Agent 协作、能力调用与仪式步骤编排为具体体验。
5. **Evolution Policy**：根据参与者反馈生成可审计 ChangeSet，经人工或策略门禁后更新领域包。

`lw.*` 表达 LifeWake 的领域语义，不进入企业 `cs.*` 能力服务 schema。若未来其他体验域采用同类机制，应复用平台契约，而不是复用 LifeWake 的具体能力名。

## 3. 对 UAS G/E/Π 的反向扩展

LifeWake 暴露了个人体验场景中可跨领域复用的四类机制。这些机制上收为 UAS 协议扩展，领域实现仍留在 Domain Pack。

### 3.1 G：灵魂数据主权

“灵魂数据”指与个人身份、记忆、情绪、关系和身体信号相关、可影响主体自我表达的数据集合；它是治理语义，不是新增数据层。

- 每次处理绑定主体、控制者、明确目的和细粒度 scope。
- 默认最小必要、可过期、可撤回；撤回后禁止继续生成或共享。
- 多主体数据不能以单方授权替代其他参与者授权。
- 统一契约：`schemas/consent_record.schema.json`。

### 3.2 G + Π：关系共创

关系体验不是“用户 A 使用用户 B 的数据”，而是多个主体带着各自授权和贡献共同形成产物。

- 参与者、贡献、共同意图、互惠状态和产物归属可追溯。
- 缺少任一必要同意或互惠失衡时，平台可以阻断或降级。
- 统一契约：`schemas/bond_cocreation.schema.json`。

### 3.3 Π：仪式协议

仪式是体验交付的通用信封：把参与者、目的、步骤、产物、同意引用和完成状态组织为可互操作记录，而不是特指某种呈现形式。

- 协议只规定可验证的边界和生命周期。
- 文案、媒介、节奏与体验配方由领域包定义。
- 统一契约：`schemas/ritual_envelope.schema.json`。

### 3.4 E：情感价值闭环

UAS 七步价值闭环在消费体验域中需要记录“是否对主体产生预期且可接受的情感影响”，而不能只统计任务完成或调用次数。

- 影响记录绑定主体、目标产物、测量方法、维度、证据和时间。
- 低影响或负面影响只生成演化候选，不默认自动修改领域策略。
- 统一契约：`schemas/emotion_impact.schema.json`。

```
输入/授权 → 模拟 → 生成 → 仪式交互 → 情感影响反馈
    ▲                                      │
    └──── 经治理审核的 ChangeSet ← 反身评估 ┘
```

## 4. 兼容策略

1. 四个 schema 是 **可选协议扩展**；现有 SelfPaw 企业桥接和 ΠPaw 流程无需提供这些记录。
2. 新契约不改变 `cs.*` 命名、注册 schema、L1/L2/L3 企业执行分级或现有审计记录。
3. 产品轨道继续使用 `selfpaw` / `pipaw`；LifeWake 以 `selfpaw` 轨道下的 `experience_domain` 分类注册。
4. 平台只消费通用字段；`lw.*` 能力、体验类型和领域策略保持命名空间隔离。
5. 采用版本化 envelope 和宽松扩展字段；新增领域字段不得改变既有必填语义。

## 5. 原型成熟度与演进

当前 LifeWake 是 **User AGI Experience Domain 原型**：领域内 MVP 已有可运行验收，通用 G/E/Π schema 形成仓库级基线；跨 SelfPaw Core 的真实身份、记忆、持久化同意撤回和长期影响评估仍待闭环。

成熟度单独按体验域记录，不计入企业数字人 L1-L3 完成率：

| 维度 | 当前状态 | 下一闭环 |
|------|----------|----------|
| 产品定义 | baseline | 用户研究与体验组合验证 |
| 领域契约 | prototype | `lw.*` 与通用 schema 的 adapter |
| 可运行闭环 | prototype | SelfPaw Core 集成验收 |
| 生产治理 | planned | 持久化撤回、删除、导出与多人争议处理 |

